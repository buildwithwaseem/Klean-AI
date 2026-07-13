"""
Generate a sample messy dataset for testing Klean AI.
Run: python generate_sample_data.py
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)

N = 500

data = {
    "CustomerID": np.arange(1, N + 1).astype(float),  # Intentionally float (should be int)
    "Name": [f"Customer_{i}" for i in range(1, N + 1)],
    "Age": np.random.randint(18, 75, N).astype(float),
    "Income": np.random.normal(55000, 15000, N).round(2),
    "SpendingScore": np.random.randint(1, 101, N),
    "Gender": np.random.choice(["Male", "Female", "Other"], N),
    "City": np.random.choice(["New York", "San Francisco", "Chicago", "Austin", "Seattle", "Miami"], N),
    "JoinDate": pd.date_range("2019-01-01", periods=N, freq="D").astype(str),  # String dates
    "PurchaseAmount": np.random.exponential(200, N).round(2),
    "Satisfaction": np.random.choice(["Low", "Medium", "High", "Very High"], N),
    "NumericString": [str(x) for x in np.random.randint(100, 999, N)],  # Numeric stored as string
}

df = pd.DataFrame(data)

# Inject missing values
for col in ["Age", "Income", "Gender", "City", "PurchaseAmount"]:
    mask = np.random.choice([True, False], N, p=[0.08, 0.92])
    df.loc[mask, col] = np.nan

# Inject outliers in Income and PurchaseAmount
outlier_idx = np.random.choice(N, 10, replace=False)
df.loc[outlier_idx, "Income"] = np.random.uniform(200000, 500000, len(outlier_idx))
outlier_idx2 = np.random.choice(N, 8, replace=False)
df.loc[outlier_idx2, "PurchaseAmount"] = np.random.uniform(3000, 8000, len(outlier_idx2))

# Inject duplicate rows
dup_rows = df.sample(15, random_state=42)
df = pd.concat([df, dup_rows], ignore_index=True)

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

output_path = os.path.join(os.path.dirname(__file__), "sample_messy_dataset.csv")
df.to_csv(output_path, index=False)
print(f"[OK] Generated sample dataset: {output_path}")
print(f"     Shape: {df.shape}")
print(f"     Missing cells: {df.isnull().sum().sum()}")
print(f"     Duplicate rows: {df.duplicated().sum()}")
