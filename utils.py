"""
Klean AI — Utility Functions
Optimized data processing, cleaning, and analysis helpers.
All operations use vectorized Pandas/NumPy for maximum performance.
"""

import io
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder


# ======================================================================
#  DATA INGESTION HELPERS
# ======================================================================

def load_dataset(uploaded_file) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a Pandas DataFrame.
    Handles edge cases: empty files, corrupt data, encoding issues.
    """
    try:
        file_name = uploaded_file.name.lower()
        if file_name.endswith(".csv"):
            # Try UTF-8 first, fall back to latin-1 for older datasets
            try:
                df = pd.read_csv(uploaded_file, low_memory=False)
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding="latin-1", low_memory=False)
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

        if df.empty:
            raise ValueError("The uploaded file is empty or contains no data.")

        return df

    except Exception as e:
        raise RuntimeError(f"Failed to load the dataset: {str(e)}")


def get_data_overview(df: pd.DataFrame) -> dict:
    """
    Compute a quick 'Data at a Glance' overview of the dataframe.
    Returns a dict with key metrics.
    """
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = int(df.isnull().sum().sum())
    memory_bytes = df.memory_usage(deep=True).sum()

    # Classify columns
    numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    return {
        "total_rows": df.shape[0],
        "total_columns": df.shape[1],
        "numerical_cols": len(numerical_cols),
        "categorical_cols": len(categorical_cols),
        "missing_cells": missing_cells,
        "missing_pct": round((missing_cells / total_cells) * 100, 2) if total_cells > 0 else 0.0,
        "memory_usage": format_bytes(memory_bytes),
        "memory_bytes": memory_bytes,
        "duplicate_rows": int(df.duplicated().sum()),
        "numerical_col_names": numerical_cols,
        "categorical_col_names": categorical_cols,
    }


def format_bytes(size_bytes: int) -> str:
    """Convert bytes to a human-readable string."""
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}"


# ======================================================================
#  DATA CLEANING FUNCTIONS
# ======================================================================

def impute_missing_values(df: pd.DataFrame, strategy: str = "smart", constant_value=None) -> tuple[pd.DataFrame, dict]:
    """
    Impute missing values using the chosen strategy.
    
    Strategies:
        'smart'    — Median for numerical, Mode for categorical
        'constant' — Fill all missing with a user-supplied constant
    
    Returns: (cleaned_df, report_dict)
    """
    df = df.copy()
    report = {"columns_imputed": [], "total_filled": 0}

    if strategy == "constant" and constant_value is not None:
        filled = int(df.isnull().sum().sum())
        df = df.fillna(constant_value)
        report["total_filled"] = filled
        report["columns_imputed"] = df.columns.tolist()
        return df, report

    # Smart imputation
    for col in df.columns:
        missing_count = int(df[col].isnull().sum())
        if missing_count == 0:
            continue

        # Skip columns that are 100% missing — nothing to learn from
        if missing_count == len(df):
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            fill_val = df[col].median()
            df[col] = df[col].fillna(fill_val)
        else:
            mode_vals = df[col].mode()
            if not mode_vals.empty:
                df[col] = df[col].fillna(mode_vals.iloc[0])

        report["columns_imputed"].append(col)
        report["total_filled"] += missing_count

    return df, report


def remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove exact duplicate rows. Returns (cleaned_df, count_removed)."""
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removed = before - len(df)
    return df, removed


def detect_outliers_iqr(df: pd.DataFrame, col: str, multiplier: float = 1.5) -> pd.Series:
    """
    Detect outliers in a numerical column using the IQR method.
    Returns a boolean Series (True = outlier).
    """
    if not pd.api.types.is_numeric_dtype(df[col]):
        return pd.Series([False] * len(df), index=df.index)

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR
    return (df[col] < lower) | (df[col] > upper)


def handle_outliers(df: pd.DataFrame, col: str, method: str = "clip", multiplier: float = 1.5) -> tuple[pd.DataFrame, int]:
    """
    Handle outliers in a numerical column.
    
    Methods:
        'clip'  — Winsorize: clip values to the IQR boundaries
        'drop'  — Remove rows containing outliers
    
    Returns: (cleaned_df, count_affected)
    """
    df = df.copy()
    if not pd.api.types.is_numeric_dtype(df[col]):
        return df, 0

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR

    outlier_mask = (df[col] < lower) | (df[col] > upper)
    count = int(outlier_mask.sum())

    if method == "clip":
        df[col] = df[col].clip(lower=lower, upper=upper)
    elif method == "drop":
        df = df[~outlier_mask].reset_index(drop=True)

    return df, count


def smart_type_cast(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """
    Attempt to auto-correct column dtypes:
      - Object columns that are really numeric → convert to numeric
      - Numeric columns that are really integer IDs → convert to int
      - Object columns that look like dates → convert to datetime
    
    Returns: (corrected_df, list_of_changes)
    """
    df = df.copy()
    changes = []

    for col in df.columns:
        original_dtype = str(df[col].dtype)

        # Skip columns with all missing values
        if df[col].isnull().all():
            continue

        # 1. Try numeric conversion for object columns
        if df[col].dtype == "object":
            # Try datetime first (common pattern)
            try:
                converted = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
                # Accept if >=70% parsed successfully
                if converted.notna().sum() / df[col].notna().sum() >= 0.7:
                    df[col] = converted
                    changes.append({
                        "column": col,
                        "from": original_dtype,
                        "to": str(df[col].dtype),
                    })
                    continue
            except Exception:
                pass

            # Try numeric conversion
            try:
                converted = pd.to_numeric(df[col], errors="coerce")
                if converted.notna().sum() / df[col].notna().sum() >= 0.7:
                    df[col] = converted
                    changes.append({
                        "column": col,
                        "from": original_dtype,
                        "to": str(df[col].dtype),
                    })
                    continue
            except Exception:
                pass

        # 2. Float columns that are really integers (e.g., 1.0, 2.0, 3.0)
        if pd.api.types.is_float_dtype(df[col]):
            non_null = df[col].dropna()
            if len(non_null) > 0 and (non_null == non_null.astype(int)).all():
                try:
                    df[col] = df[col].astype("Int64")  # Nullable integer
                    changes.append({
                        "column": col,
                        "from": original_dtype,
                        "to": "Int64",
                    })
                except (ValueError, TypeError):
                    pass

    return df, changes


# ======================================================================
#  EDA / ANALYSIS FUNCTIONS
# ======================================================================

def compute_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a rich descriptive statistics table."""
    try:
        desc = df.describe(include="all").T
        # Add additional stats
        desc["missing"] = df.isnull().sum()
        desc["missing_%"] = (df.isnull().sum() / len(df) * 100).round(2)
        desc["dtype"] = df.dtypes
        # Reorder columns to put important info first
        priority = ["dtype", "count", "missing", "missing_%", "unique", "top", "freq", "mean", "std", "min", "25%", "50%", "75%", "max"]
        cols_present = [c for c in priority if c in desc.columns]
        remaining = [c for c in desc.columns if c not in cols_present]
        desc = desc[cols_present + remaining]
        return desc
    except Exception:
        return df.describe(include="all").T


def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Pearson correlation matrix for numerical columns."""
    num_df = df.select_dtypes(include=np.number)
    if num_df.shape[1] < 2:
        return pd.DataFrame()
    return num_df.corr(method="pearson").round(4)


def get_highly_correlated_pairs(corr_matrix: pd.DataFrame, threshold: float = 0.85) -> list:
    """Find pairs of features with |correlation| > threshold."""
    pairs = []
    if corr_matrix.empty:
        return pairs
    cols = corr_matrix.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr_matrix.iloc[i, j]
            if abs(val) > threshold:
                pairs.append({
                    "feature_1": cols[i],
                    "feature_2": cols[j],
                    "correlation": round(val, 4),
                })
    return pairs


def compute_column_stats(series: pd.Series) -> dict:
    """Compute detailed stats for a single column."""
    result = {
        "dtype": str(series.dtype),
        "count": int(series.count()),
        "missing": int(series.isnull().sum()),
        "unique": int(series.nunique()),
    }

    if pd.api.types.is_numeric_dtype(series):
        clean = series.dropna()
        if len(clean) > 0:
            result.update({
                "mean": round(float(clean.mean()), 4),
                "median": round(float(clean.median()), 4),
                "std": round(float(clean.std()), 4),
                "min": round(float(clean.min()), 4),
                "max": round(float(clean.max()), 4),
                "skewness": round(float(clean.skew()), 4),
                "kurtosis": round(float(clean.kurtosis()), 4),
                "variance": round(float(clean.var()), 4),
                "range": round(float(clean.max() - clean.min()), 4),
                "iqr": round(float(clean.quantile(0.75) - clean.quantile(0.25)), 4),
            })
    else:
        mode_vals = series.mode()
        result["mode"] = str(mode_vals.iloc[0]) if not mode_vals.empty else "N/A"

    return result


# ======================================================================
#  FEATURE ENGINEERING FUNCTIONS
# ======================================================================

def apply_one_hot_encoding(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Apply One-Hot Encoding to specified categorical columns."""
    df = df.copy()
    try:
        df = pd.get_dummies(df, columns=columns, drop_first=False, dtype=int)
    except Exception:
        pass
    return df


def apply_label_encoding(df: pd.DataFrame, columns: list) -> tuple[pd.DataFrame, dict]:
    """
    Apply Label Encoding to specified categorical columns.
    Returns (encoded_df, mapping_dict).
    """
    df = df.copy()
    mappings = {}
    for col in columns:
        if col not in df.columns:
            continue
        try:
            le = LabelEncoder()
            non_null_mask = df[col].notna()
            df.loc[non_null_mask, col] = le.fit_transform(df.loc[non_null_mask, col].astype(str))
            df[col] = pd.to_numeric(df[col], errors="coerce")
            mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))
        except Exception:
            pass
    return df, mappings


def apply_scaling(df: pd.DataFrame, columns: list, method: str = "standard") -> pd.DataFrame:
    """
    Scale numerical columns.
    Methods: 'standard' (Z-score) or 'minmax' (0-1).
    """
    df = df.copy()
    if not columns:
        return df

    valid_cols = [c for c in columns if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
    if not valid_cols:
        return df

    try:
        scaler = StandardScaler() if method == "standard" else MinMaxScaler()
        # Only scale rows where all selected columns are non-null
        mask = df[valid_cols].notna().all(axis=1)
        if mask.sum() > 0:
            df.loc[mask, valid_cols] = scaler.fit_transform(df.loc[mask, valid_cols])
    except Exception:
        pass

    return df


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to CSV bytes for download."""
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8")
    return buffer.getvalue()
