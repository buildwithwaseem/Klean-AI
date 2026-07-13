"""
╔════════════════════════════════════════════════════════════════════════════════╗
║              Klean AI — Main Application                                       ║
║      Automated Dataset Cleaner & Explorer (Mini-EDA Tool)                      ║
║                                                                                ║
║  A production-grade Streamlit app that automates data preprocessing,           ║
║  cleaning, and exploratory data analysis. Features a futuristic dark-mode      ║
║  UI with neon accents and human-friendly workflows.                            ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Local modules
from styles import CUSTOM_CSS, PLOTLY_THEME, get_plotly_layout
from utils import (
    load_dataset,
    get_data_overview,
    impute_missing_values,
    remove_duplicates,
    detect_outliers_iqr,
    handle_outliers,
    smart_type_cast,
    compute_descriptive_stats,
    compute_correlation_matrix,
    get_highly_correlated_pairs,
    compute_column_stats,
    apply_one_hot_encoding,
    apply_label_encoding,
    apply_scaling,
    dataframe_to_csv_bytes,
)


# ======================================================================
#  PAGE CONFIG
# ======================================================================

st.set_page_config(
    page_title="Klean AI — Automated Dataset Cleaner & Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Klean AI v1.0 — Built for data scientists who value speed and quality.",
    },
)

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ======================================================================
#  SESSION STATE INITIALIZATION
# ======================================================================

def init_session_state():
    """Initialize all session state variables if they don't exist."""
    defaults = {
        "df_original": None,        # The raw uploaded dataframe
        "df_working": None,         # The current working copy (post-cleaning)
        "file_name": None,          # Name of the uploaded file
        "overview": None,           # Data overview dict
        "cleaning_log": [],         # Log of cleaning actions performed
        "upload_timestamp": None,   # When the file was uploaded
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session_state()


# ======================================================================
#  HELPER: RENDER METRIC CARDS
# ======================================================================

def render_metric_card(icon: str, value, label: str, color: str = "indigo"):
    """Render a single metric card with icon, value, and label."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value {color}">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(icon: str, title: str):
    """Render a styled section header."""
    st.markdown(f'<div class="section-header">{icon} {title}</div>', unsafe_allow_html=True)


def render_status_badge(text: str, badge_type: str = "success"):
    """Render a colored status badge."""
    return f'<span class="status-badge badge-{badge_type}">● {text}</span>'


# ======================================================================
#  SIDEBAR
# ======================================================================

def render_sidebar():
    """Render the sidebar with branding and navigation info."""
    with st.sidebar:
        # Brand header
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🧬</div>
            <div>
                <div class="sidebar-brand-text">Klean AI</div>
                <div class="sidebar-brand-version">v1.0 • Production</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Dataset status
        if st.session_state.df_working is not None:
            overview = st.session_state.overview
            st.markdown(f"""
            <div style="padding: 0.75rem; background: rgba(99,102,241,0.08); border-radius: 8px; border: 1px solid rgba(99,102,241,0.15); margin-bottom: 1rem;">
                <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #64748B; font-weight: 600; margin-bottom: 0.5rem;">📂 Active Dataset</div>
                <div style="font-size: 0.9rem; font-weight: 600; color: #F1F5F9; margin-bottom: 0.75rem;">{st.session_state.file_name}</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                    <div style="font-size: 0.75rem; color: #94A3B8;">
                        <span style="color: #6366F1; font-weight: 700;">{overview['total_rows']:,}</span> Rows
                    </div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">
                        <span style="color: #14B8A6; font-weight: 700;">{overview['total_columns']}</span> Columns
                    </div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">
                        <span style="color: #F59E0B; font-weight: 700;">{overview['numerical_cols']}</span> Numeric
                    </div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">
                        <span style="color: #A78BFA; font-weight: 700;">{overview['categorical_cols']}</span> Categoric
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Cleaning log
            if st.session_state.cleaning_log:
                st.markdown("""
                <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #64748B; font-weight: 600; margin-bottom: 0.5rem;">🔧 Cleaning History</div>
                """, unsafe_allow_html=True)
                for entry in st.session_state.cleaning_log[-8:]:
                    badge_html = render_status_badge(entry, "success")
                    st.markdown(badge_html, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="padding: 1rem; text-align: center; color: #64748B; font-size: 0.85rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📁</div>
                No dataset loaded.<br>
                <span style="font-size: 0.75rem;">Upload a CSV or Excel file to get started.</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        # Footer in sidebar
        st.markdown("""
        <div style="text-align: center; color: #475569; font-size: 0.7rem; padding-top: 0.5rem;">
            Built with ❤️ using Streamlit & Plotly by buildwithwaseem<br>
            <span style="color: #6366F1;">Klean AI</span> © 2026
        </div>
        """, unsafe_allow_html=True)


# ======================================================================
#  TAB 1: SMART DATA UPLOAD & INGESTION
# ======================================================================

def render_upload_tab():
    """Render the data upload and overview tab."""

    # Hero header
    st.markdown("""
    <div class="animate-in">
        <div class="hero-title">Smart Data Ingestion</div>
        <div class="hero-subtitle">Upload your dataset and get instant insights at a glance</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader(
        "📂 Drag and drop your dataset here",
        type=["csv", "xlsx", "xls"],
        help="Supported formats: CSV, XLSX, XLS (max 200 MB)",
        key="file_uploader",
    )

    if uploaded_file is not None:
        # Only reload if it's a new file
        if st.session_state.file_name != uploaded_file.name:
            with st.spinner(""):
                # Show loading animation
                progress_placeholder = st.empty()
                progress_placeholder.markdown("""
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
                    <div style="color: #94A3B8; font-size: 0.9rem;">Analyzing your dataset...</div>
                    <div class="loading-skeleton" style="width: 60%; margin: 1rem auto;"></div>
                    <div class="loading-skeleton" style="width: 40%; margin: 0.5rem auto;"></div>
                </div>
                """, unsafe_allow_html=True)

                try:
                    df = load_dataset(uploaded_file)
                    st.session_state.df_original = df.copy()
                    st.session_state.df_working = df.copy()
                    st.session_state.file_name = uploaded_file.name
                    st.session_state.overview = get_data_overview(df)
                    st.session_state.cleaning_log = []
                    st.session_state.upload_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    progress_placeholder.empty()
                except Exception as e:
                    progress_placeholder.empty()
                    st.error(f"❌ Error loading file: {str(e)}")
                    return

        # Display overview
        if st.session_state.df_working is not None:
            _render_data_overview()

    else:
        # Welcome / empty state
        st.markdown("""
        <div class="welcome-container animate-in">
            <div class="welcome-icon">🧬</div>
            <div class="welcome-title">Welcome to Klean AI</div>
            <div class="welcome-desc">
                Drop your CSV or Excel file above to begin. Klean AI will automatically
                analyze your data, clean it, and generate insightful visualizations — all in seconds.
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_data_overview():
    """Render the 'Data at a Glance' dashboard after upload."""
    overview = st.session_state.overview
    df = st.session_state.df_working

    render_section_header("📊", "Data at a Glance")

    # Metric cards row
    cols = st.columns(6)
    metrics = [
        ("📐", f"{overview['total_rows']:,}", "Total Rows", "indigo"),
        ("📏", f"{overview['total_columns']}", "Total Columns", "teal"),
        ("💾", overview['memory_usage'], "Memory Usage", "amber"),
        ("🔢", f"{overview['numerical_cols']}", "Numerical", "emerald"),
        ("🏷️", f"{overview['categorical_cols']}", "Categorical", "rose"),
        ("⚠️", f"{overview['missing_pct']}%", "Missing Cells", "amber" if overview['missing_pct'] > 0 else "emerald"),
    ]
    for col, (icon, value, label, color) in zip(cols, metrics):
        with col:
            render_metric_card(icon, value, label, color)

    st.markdown("<br>", unsafe_allow_html=True)

    # Column type breakdown in a card
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("##### 🔢 Numerical Columns")
        if overview["numerical_col_names"]:
            for c in overview["numerical_col_names"]:
                missing = int(df[c].isnull().sum())
                badge = render_status_badge(f"{c} ({missing} missing)", "success" if missing == 0 else "warning")
                st.markdown(badge, unsafe_allow_html=True)
        else:
            st.caption("No numerical columns detected.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("##### 🏷️ Categorical Columns")
        if overview["categorical_col_names"]:
            for c in overview["categorical_col_names"]:
                missing = int(df[c].isnull().sum())
                badge = render_status_badge(f"{c} ({missing} missing)", "success" if missing == 0 else "warning")
                st.markdown(badge, unsafe_allow_html=True)
        else:
            st.caption("No categorical columns detected.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Data preview
    render_section_header("👁️", "Data Preview")

    preview_tabs = st.tabs(["🔝 First 5 Rows", "🔚 Last 5 Rows", "📋 Full Schema"])
    with preview_tabs[0]:
        st.dataframe(df.head(), use_container_width=True, height=240)
    with preview_tabs[1]:
        st.dataframe(df.tail(), use_container_width=True, height=240)
    with preview_tabs[2]:
        schema_df = pd.DataFrame({
            "Column": df.columns,
            "Dtype": df.dtypes.astype(str).values,
            "Non-Null": df.notna().sum().values,
            "Null": df.isnull().sum().values,
            "Null %": (df.isnull().sum() / len(df) * 100).round(2).values,
            "Unique": df.nunique().values,
        })
        st.dataframe(schema_df, use_container_width=True, height=400)


# ======================================================================
#  TAB 2: AUTOMATED DATA CLEANING
# ======================================================================

def render_cleaning_tab():
    """Render the automated data cleaning tab."""
    if st.session_state.df_working is None:
        _render_no_data_message("Upload a dataset first to start cleaning.")
        return

    st.markdown("""
    <div class="animate-in">
        <div class="hero-title">Automated Data Cleaning</div>
        <div class="hero-subtitle">One-click operations to prepare your dataset for analysis</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df = st.session_state.df_working

    # ---- Missing Value Imputation ----
    render_section_header("🩹", "Missing Value Imputation")

    total_missing = int(df.isnull().sum().sum())

    if total_missing == 0:
        st.success("✅ No missing values detected. Your dataset is complete!")
    else:
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 1.1rem; font-weight: 600; color: #F1F5F9;">
                        ⚠️ {total_missing:,} missing cells detected
                    </span>
                    <span style="font-size: 0.85rem; color: #94A3B8; margin-left: 0.75rem;">
                        across {int(df.isnull().any().sum())} columns
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            impute_strategy = st.radio(
                "Imputation Strategy",
                options=["Smart (Median for Numbers, Mode for Categories)", "Custom Constant"],
                horizontal=True,
                key="impute_strategy",
            )
        with col2:
            constant_val = None
            if "Custom" in impute_strategy:
                constant_val = st.text_input("Fill value:", value="0", key="constant_fill")

        if st.button("🩹 Impute Missing Values", key="btn_impute", use_container_width=True):
            with st.spinner("Imputing missing values..."):
                strategy = "smart" if "Smart" in impute_strategy else "constant"
                df_clean, report = impute_missing_values(df, strategy=strategy, constant_value=constant_val)
                st.session_state.df_working = df_clean
                st.session_state.overview = get_data_overview(df_clean)
                st.session_state.cleaning_log.append(f"Imputed {report['total_filled']} cells")
            st.success(f"✅ Successfully imputed **{report['total_filled']:,}** missing values across **{len(report['columns_imputed'])}** columns.")
            st.rerun()

    st.markdown("---")

    # ---- Duplicate Removal ----
    render_section_header("🔁", "Duplicate Row Removal")

    dup_count = int(df.duplicated().sum())
    if dup_count == 0:
        st.success("✅ No duplicate rows found.")
    else:
        st.warning(f"⚠️ **{dup_count:,}** duplicate rows detected.")
        if st.button("🗑️ Remove All Duplicates", key="btn_dedup", use_container_width=True):
            with st.spinner("Removing duplicates..."):
                df_clean, removed = remove_duplicates(df)
                st.session_state.df_working = df_clean
                st.session_state.overview = get_data_overview(df_clean)
                st.session_state.cleaning_log.append(f"Removed {removed} duplicates")
            st.success(f"✅ Removed **{removed:,}** duplicate rows. Dataset now has **{len(df_clean):,}** rows.")
            st.rerun()

    st.markdown("---")

    # ---- Outlier Detection & Handling ----
    render_section_header("📏", "Outlier Detection & Handling")

    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not num_cols:
        st.info("ℹ️ No numerical columns available for outlier detection.")
    else:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            outlier_col = st.selectbox("Select column:", num_cols, key="outlier_col")
        with col2:
            iqr_multiplier = st.slider("IQR Multiplier:", min_value=1.0, max_value=3.0, value=1.5, step=0.1, key="iqr_mult")
        with col3:
            outlier_method = st.selectbox("Action:", ["Clip (Winsorize)", "Drop Rows"], key="outlier_method")

        if outlier_col:
            outlier_mask = detect_outliers_iqr(df, outlier_col, multiplier=iqr_multiplier)
            outlier_count = int(outlier_mask.sum())

            if outlier_count > 0:
                st.markdown(f"""
                <div class="glass-card">
                    <span style="color: #F59E0B; font-weight: 600;">⚡ {outlier_count:,} outliers</span>
                    <span style="color: #94A3B8;"> detected in </span>
                    <span style="color: #6366F1; font-weight: 600;">{outlier_col}</span>
                    <span style="color: #94A3B8;"> (IQR × {iqr_multiplier})</span>
                </div>
                """, unsafe_allow_html=True)

                # Quick box plot preview
                fig = go.Figure()
                fig.add_trace(go.Box(
                    y=df[outlier_col].dropna(),
                    name=outlier_col,
                    marker_color=PLOTLY_THEME["accent_indigo"],
                    boxmean="sd",
                    line=dict(color=PLOTLY_THEME["accent_indigo"]),
                ))
                fig.update_layout(**get_plotly_layout(
                    title=dict(text=f"Distribution of {outlier_col}", font=dict(size=14)),
                    height=300,
                    showlegend=False,
                ))
                st.plotly_chart(fig, use_container_width=True)

                if st.button("🔧 Handle Outliers", key="btn_outlier", use_container_width=True):
                    method = "clip" if "Clip" in outlier_method else "drop"
                    with st.spinner("Handling outliers..."):
                        df_clean, count = handle_outliers(df, outlier_col, method=method, multiplier=iqr_multiplier)
                        st.session_state.df_working = df_clean
                        st.session_state.overview = get_data_overview(df_clean)
                        action_word = "Clipped" if method == "clip" else "Dropped"
                        st.session_state.cleaning_log.append(f"{action_word} {count} outliers in {outlier_col}")
                    st.success(f"✅ {action_word} **{count:,}** outliers in **{outlier_col}**.")
                    st.rerun()
            else:
                st.success(f"✅ No outliers detected in **{outlier_col}** with IQR × {iqr_multiplier}.")

    st.markdown("---")

    # ---- Smart Type Casting ----
    render_section_header("🔄", "Smart Type Casting")

    if st.button("🔄 Auto-Detect & Fix Column Types", key="btn_typecast", use_container_width=True):
        with st.spinner("Analyzing column types..."):
            df_clean, changes = smart_type_cast(df)
            st.session_state.df_working = df_clean
            st.session_state.overview = get_data_overview(df_clean)

        if changes:
            st.session_state.cleaning_log.append(f"Recast {len(changes)} columns")
            st.success(f"✅ Auto-corrected **{len(changes)}** column type(s):")
            changes_df = pd.DataFrame(changes)
            st.dataframe(changes_df, use_container_width=True, height=200)
            st.rerun()
        else:
            st.info("ℹ️ All column types appear correct. No changes needed.")

    st.markdown("---")

    # ---- Download Cleaned Data ----
    render_section_header("⬇️", "Download Cleaned Dataset")

    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 0.85rem; color: #94A3B8;">Current shape: </span>
                <span style="font-size: 1rem; font-weight: 700; color: #14B8A6;">{df.shape[0]:,} rows × {df.shape[1]} columns</span>
            </div>
            <div>
                <span style="font-size: 0.85rem; color: #94A3B8;">Missing: </span>
                <span style="font-size: 1rem; font-weight: 700; color: {'#10B981' if int(df.isnull().sum().sum()) == 0 else '#F59E0B'};">
                    {int(df.isnull().sum().sum()):,} cells
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    csv_bytes = dataframe_to_csv_bytes(df)
    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=csv_bytes,
        file_name=f"cleaned_{st.session_state.file_name.rsplit('.', 1)[0]}.csv",
        mime="text/csv",
        key="download_cleaned",
        use_container_width=True,
    )


# ======================================================================
#  TAB 3: AUTOMATED EDA
# ======================================================================

def render_eda_tab():
    """Render the automated EDA tab."""
    if st.session_state.df_working is None:
        _render_no_data_message("Upload a dataset first to explore.")
        return

    st.markdown("""
    <div class="animate-in">
        <div class="hero-title">Exploratory Data Analysis</div>
        <div class="hero-subtitle">Deep insights and visualizations, generated automatically</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df = st.session_state.df_working

    # ---- Descriptive Statistics ----
    render_section_header("📈", "Descriptive Statistics")

    with st.expander("View Full Descriptive Statistics Table", expanded=True):
        try:
            desc = compute_descriptive_stats(df)
            st.dataframe(desc, use_container_width=True, height=400)
        except Exception as e:
            st.error(f"Could not generate descriptive statistics: {e}")

    st.markdown("---")

    # ---- Target Variable Analysis ----
    render_section_header("🎯", "Target Variable Analysis")

    all_cols = df.columns.tolist()
    target_col = st.selectbox("Select a target / focus column:", all_cols, key="target_col")

    if target_col:
        col_stats = compute_column_stats(df[target_col])

        # Stats cards
        stat_cols = st.columns(4)
        stat_items = [
            ("📊", str(col_stats.get("count", "—")), "Non-Null Count", "indigo"),
            ("❓", str(col_stats.get("missing", "—")), "Missing", "amber"),
            ("🔗", str(col_stats.get("unique", "—")), "Unique Values", "teal"),
            ("📐", str(col_stats.get("dtype", "—")), "Data Type", "rose"),
        ]
        for col, (icon, val, label, color) in zip(stat_cols, stat_items):
            with col:
                render_metric_card(icon, val, label, color)

        st.markdown("<br>", unsafe_allow_html=True)

        if pd.api.types.is_numeric_dtype(df[target_col]):
            # Numerical target: Histogram + KDE
            _render_numerical_target(df, target_col, col_stats)
        else:
            # Categorical target: Count plot
            _render_categorical_target(df, target_col)

    st.markdown("---")

    # ---- Correlation Matrix ----
    render_section_header("🔗", "Correlation Matrix")

    corr = compute_correlation_matrix(df)
    if corr.empty:
        st.info("ℹ️ Need at least 2 numerical columns to compute correlation.")
    else:
        # Heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale=PLOTLY_THEME["colorscale"],
            zmin=-1, zmax=1,
            text=corr.values.round(2),
            texttemplate="%{text}",
            textfont=dict(size=10, color="#E2E8F0"),
            hoverongaps=False,
            colorbar=dict(
                title=dict(
                    text="Correlation",
                    font=dict(size=11, color=PLOTLY_THEME["text_secondary"]),
                ),
                tickfont=dict(size=10, color=PLOTLY_THEME["text_secondary"]),
            ),
        ))
        fig.update_layout(**get_plotly_layout(
            title=dict(text="Pearson Correlation Heatmap", font=dict(size=15)),
            height=max(400, len(corr.columns) * 35 + 100),
            xaxis=dict(tickangle=-45),
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Highly correlated pairs
        high_corr = get_highly_correlated_pairs(corr, threshold=0.85)
        if high_corr:
            st.markdown("""
            <div class="glass-card">
                <div style="font-weight: 600; color: #F59E0B; margin-bottom: 0.5rem;">
                    ⚠️ Highly Correlated Feature Pairs (|r| > 0.85)
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8;">
                    These pairs may cause multicollinearity in predictive models. Consider dropping one from each pair.
                </div>
            </div>
            """, unsafe_allow_html=True)
            corr_df = pd.DataFrame(high_corr)
            st.dataframe(corr_df, use_container_width=True)
        else:
            st.success("✅ No highly correlated feature pairs detected (threshold: |r| > 0.85).")

    st.markdown("---")

    # ---- Feature Distribution Hub ----
    render_section_header("📊", "Feature Distribution Hub")

    dist_col = st.selectbox("Select a column to explore:", all_cols, key="dist_col")
    if dist_col:
        _render_feature_distribution(df, dist_col)


def _render_numerical_target(df: pd.DataFrame, col: str, stats: dict):
    """Render histogram + KDE + stats for a numerical target."""
    clean_data = df[col].dropna()

    # Additional numeric stats
    extra_cols = st.columns(4)
    extras = [
        ("📉", str(stats.get("mean", "—")), "Mean", "indigo"),
        ("📊", str(stats.get("median", "—")), "Median", "teal"),
        ("📐", str(stats.get("skewness", "—")), "Skewness", "amber"),
        ("📏", str(stats.get("kurtosis", "—")), "Kurtosis", "emerald"),
    ]
    for c, (icon, val, label, color) in zip(extra_cols, extras):
        with c:
            render_metric_card(icon, val, label, color)

    st.markdown("<br>", unsafe_allow_html=True)

    # Histogram + KDE plot
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Histogram(
            x=clean_data,
            nbinsx=50,
            marker_color=PLOTLY_THEME["accent_indigo"],
            opacity=0.7,
            name="Histogram",
        ),
        secondary_y=False,
    )

    # KDE curve
    try:
        from scipy.stats import gaussian_kde
        kde_x = np.linspace(clean_data.min(), clean_data.max(), 200)
        kde = gaussian_kde(clean_data)
        kde_y = kde(kde_x)
        fig.add_trace(
            go.Scatter(
                x=kde_x,
                y=kde_y,
                mode="lines",
                name="KDE",
                line=dict(color=PLOTLY_THEME["accent_teal"], width=2.5),
            ),
            secondary_y=True,
        )
    except Exception:
        pass

    fig.update_layout(**get_plotly_layout(
        title=dict(text=f"Distribution of {col}", font=dict(size=15)),
        height=420,
        barmode="overlay",
        xaxis_title=col,
        yaxis_title="Count",
    ))
    fig.update_yaxes(
        title_text="Density",
        secondary_y=True,
        gridcolor=PLOTLY_THEME["grid_color"],
        title_font=dict(size=12, color=PLOTLY_THEME["text_secondary"]),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_categorical_target(df: pd.DataFrame, col: str):
    """Render count plot for a categorical target."""
    value_counts = df[col].value_counts().head(30)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=value_counts.index.astype(str),
        y=value_counts.values,
        marker=dict(
            color=value_counts.values,
            colorscale=[[0, PLOTLY_THEME["accent_indigo"]], [1, PLOTLY_THEME["accent_teal"]]],
            line=dict(width=0),
        ),
        text=value_counts.values,
        textposition="outside",
        textfont=dict(size=11, color=PLOTLY_THEME["text_secondary"]),
    ))
    fig.update_layout(**get_plotly_layout(
        title=dict(text=f"Value Counts — {col}", font=dict(size=15)),
        height=420,
        xaxis_title=col,
        yaxis_title="Count",
        xaxis=dict(tickangle=-45),
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Balance check
    if len(value_counts) >= 2:
        imbalance_ratio = value_counts.iloc[0] / value_counts.iloc[-1]
        if imbalance_ratio > 3:
            st.warning(f"⚠️ **Class imbalance detected.** The most frequent class is {imbalance_ratio:.1f}× more common than the least frequent.")
        else:
            st.success("✅ Classes appear reasonably balanced.")


def _render_feature_distribution(df: pd.DataFrame, col: str):
    """Render detailed distribution view for any column."""
    stats = compute_column_stats(df[col])

    # Stats row
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    stat_strs = []
    for k, v in stats.items():
        stat_strs.append(f"**{k.replace('_', ' ').title()}:** `{v}`")
    st.markdown(" · ".join(stat_strs))
    st.markdown('</div>', unsafe_allow_html=True)

    if pd.api.types.is_numeric_dtype(df[col]):
        # Histogram with box
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75, 0.25], vertical_spacing=0.04)

        clean = df[col].dropna()
        fig.add_trace(
            go.Histogram(
                x=clean,
                nbinsx=40,
                marker_color=PLOTLY_THEME["accent_indigo"],
                opacity=0.8,
                name="Distribution",
            ),
            row=1, col=1,
        )
        fig.add_trace(
            go.Box(
                x=clean,
                marker_color=PLOTLY_THEME["accent_teal"],
                name="Box Plot",
                boxmean="sd",
            ),
            row=2, col=1,
        )
        fig.update_layout(**get_plotly_layout(
            title=dict(text=f"Distribution & Box Plot — {col}", font=dict(size=14)),
            height=450,
            showlegend=False,
        ))
        # Update subplot axes
        fig.update_xaxes(gridcolor=PLOTLY_THEME["grid_color"], row=1, col=1)
        fig.update_xaxes(gridcolor=PLOTLY_THEME["grid_color"], row=2, col=1)
        fig.update_yaxes(gridcolor=PLOTLY_THEME["grid_color"], row=1, col=1, title_text="Count")
        fig.update_yaxes(gridcolor=PLOTLY_THEME["grid_color"], row=2, col=1)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Bar chart of value counts
        vc = df[col].value_counts().head(25)
        fig = go.Figure(go.Bar(
            y=vc.index.astype(str),
            x=vc.values,
            orientation="h",
            marker=dict(
                color=vc.values,
                colorscale=[[0, PLOTLY_THEME["accent_indigo"]], [1, PLOTLY_THEME["accent_purple"]]],
            ),
            text=vc.values,
            textposition="outside",
            textfont=dict(size=11, color=PLOTLY_THEME["text_secondary"]),
        ))
        fig.update_layout(**get_plotly_layout(
            title=dict(text=f"Top Value Counts — {col}", font=dict(size=14)),
            height=max(350, len(vc) * 28 + 100),
            yaxis=dict(autorange="reversed"),
            xaxis_title="Count",
        ))
        st.plotly_chart(fig, use_container_width=True)


# ======================================================================
#  TAB 4: ADVANCED FEATURE PREPARATION
# ======================================================================

def render_feature_tab():
    """Render the feature engineering / preparation tab."""
    if st.session_state.df_working is None:
        _render_no_data_message("Upload a dataset first for feature preparation.")
        return

    st.markdown("""
    <div class="animate-in">
        <div class="hero-title">Feature Preparation</div>
        <div class="hero-subtitle">Encode categories and scale features for ML-ready data</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df = st.session_state.df_working

    # ---- Feature Encoding ----
    render_section_header("🔤", "Feature Encoding")

    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if not cat_cols:
        st.success("✅ No categorical text columns remaining. All columns are already numeric.")
    else:
        st.markdown(f"""
        <div class="glass-card">
            <span style="font-size: 0.9rem; color: #94A3B8;">
                Detected <span style="color: #6366F1; font-weight: 700;">{len(cat_cols)}</span>
                categorical column(s): {', '.join(f'<code>{c}</code>' for c in cat_cols)}
            </span>
        </div>
        """, unsafe_allow_html=True)

        encode_cols = st.multiselect(
            "Select columns to encode:",
            cat_cols,
            default=cat_cols,
            key="encode_cols",
        )

        col1, col2 = st.columns(2)

        with col1:
            encoding_method = st.selectbox(
                "Encoding Method:",
                ["One-Hot Encoding (Dummy Variables)", "Label Encoding (Integer Mapping)"],
                key="encoding_method",
            )

        with col2:
            # Show preview of unique values for selected columns
            if encode_cols:
                preview_col = st.selectbox("Preview unique values for:", encode_cols, key="encode_preview")
                if preview_col:
                    uniques = df[preview_col].dropna().unique()[:15]
                    st.caption(f"Sample values: {', '.join(str(u) for u in uniques)}")

        if encode_cols and st.button("🔤 Apply Encoding", key="btn_encode", use_container_width=True):
            with st.spinner("Encoding features..."):
                if "One-Hot" in encoding_method:
                    df_encoded = apply_one_hot_encoding(df, encode_cols)
                    new_cols = len(df_encoded.columns) - len(df.columns)
                    st.session_state.df_working = df_encoded
                    st.session_state.overview = get_data_overview(df_encoded)
                    st.session_state.cleaning_log.append(f"One-Hot encoded {len(encode_cols)} cols (+{new_cols} new)")
                    st.success(f"✅ One-Hot Encoding applied. Added **{new_cols}** new binary columns.")
                else:
                    df_encoded, mappings = apply_label_encoding(df, encode_cols)
                    st.session_state.df_working = df_encoded
                    st.session_state.overview = get_data_overview(df_encoded)
                    st.session_state.cleaning_log.append(f"Label encoded {len(encode_cols)} cols")
                    st.success(f"✅ Label Encoding applied to **{len(encode_cols)}** column(s).")
                    if mappings:
                        with st.expander("View Label Encoding Mappings"):
                            for col_name, mapping in mappings.items():
                                st.markdown(f"**{col_name}:**")
                                mapping_df = pd.DataFrame(list(mapping.items()), columns=["Original", "Encoded"])
                                st.dataframe(mapping_df, use_container_width=True, height=200)
                st.rerun()

    st.markdown("---")

    # ---- Feature Scaling ----
    render_section_header("⚖️", "Feature Scaling")

    num_cols = df.select_dtypes(include=np.number).columns.tolist()

    if not num_cols:
        st.info("ℹ️ No numerical columns available for scaling.")
    else:
        scale_cols = st.multiselect(
            "Select numerical columns to scale:",
            num_cols,
            default=num_cols,
            key="scale_cols",
        )

        scaling_method = st.selectbox(
            "Scaling Method:",
            [
                "StandardScaler (Z-score Normalization: mean=0, std=1)",
                "MinMaxScaler (0-1 Normalization)",
            ],
            key="scaling_method",
        )

        if scale_cols and st.button("⚖️ Apply Scaling", key="btn_scale", use_container_width=True):
            method = "standard" if "Standard" in scaling_method else "minmax"
            with st.spinner("Scaling features..."):
                df_scaled = apply_scaling(df, scale_cols, method=method)
                st.session_state.df_working = df_scaled
                st.session_state.overview = get_data_overview(df_scaled)
                method_name = "StandardScaler" if method == "standard" else "MinMaxScaler"
                st.session_state.cleaning_log.append(f"Scaled {len(scale_cols)} cols ({method_name})")
            st.success(f"✅ Applied **{method_name}** to **{len(scale_cols)}** column(s).")
            st.rerun()

    st.markdown("---")

    # ---- Download Prepared Data ----
    render_section_header("⬇️", "Download Prepared Dataset")

    # Show current state
    current_df = st.session_state.df_working
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                <span style="font-size: 0.85rem; color: #94A3B8;">Shape: </span>
                <span style="font-size: 1rem; font-weight: 700; color: #14B8A6;">{current_df.shape[0]:,} × {current_df.shape[1]}</span>
            </div>
            <div>
                <span style="font-size: 0.85rem; color: #94A3B8;">Numeric: </span>
                <span style="font-size: 1rem; font-weight: 700; color: #6366F1;">{current_df.select_dtypes(include=np.number).shape[1]}</span>
            </div>
            <div>
                <span style="font-size: 0.85rem; color: #94A3B8;">Categorical: </span>
                <span style="font-size: 1rem; font-weight: 700; color: #A78BFA;">{current_df.select_dtypes(exclude=np.number).shape[1]}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    csv_bytes = dataframe_to_csv_bytes(current_df)
    st.download_button(
        label="⬇️ Download ML-Ready Dataset",
        data=csv_bytes,
        file_name=f"prepared_{st.session_state.file_name.rsplit('.', 1)[0]}.csv",
        mime="text/csv",
        key="download_prepared",
        use_container_width=True,
    )

    # Preview of the final dataset
    with st.expander("Preview Final Dataset", expanded=False):
        st.dataframe(current_df.head(20), use_container_width=True, height=400)


# ======================================================================
#  COMMON COMPONENTS
# ======================================================================

def _render_no_data_message(message: str):
    """Render a message when no data is loaded."""
    st.markdown(f"""
    <div class="welcome-container animate-in">
        <div class="welcome-icon">📁</div>
        <div class="welcome-title">No Dataset Loaded</div>
        <div class="welcome-desc">{message}</div>
    </div>
    """, unsafe_allow_html=True)


# ======================================================================
#  MAIN APP
# ======================================================================

def main():
    """Main application entry point."""
    # Render sidebar
    render_sidebar()

    # Main content area tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📂  Upload & Ingest",
        "🧹  Data Cleaning",
        "📊  EDA & Insights",
        "⚙️  Feature Prep",
    ])

    with tab1:
        render_upload_tab()

    with tab2:
        render_cleaning_tab()

    with tab3:
        render_eda_tab()

    with tab4:
        render_feature_tab()

    # Footer
    st.markdown("""
    <div class="app-footer">
        <span style="color: #6366F1;">Klean AI</span> · Automated Dataset Cleaner & Explorer · v1.0<br>
        Built with Streamlit · Plotly · scikit-learn · Pandas
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
