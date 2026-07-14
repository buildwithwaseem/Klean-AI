# 🧬 [Klean AI](https://buildwithwaseem-klean-ai-app-soo0ef.streamlit.app/)

**Automated Dataset Cleaner & Explorer — A Production-Grade Mini-EDA Tool**

Klean AI automates the data preprocessing, cleaning, and exploratory data analysis (EDA) pipeline with a polished, approachable workflow. It removes repetitive boilerplate code while keeping the experience intuitive and easy to understand.

---

## ✨ Features

### 📂 Tab 1: Smart Data Upload & Ingestion
- Drag-and-drop CSV / Excel file upload
- Instant "Data at a Glance" metrics: rows, columns, memory, missing cells, dtypes
- Interactive preview: First 5 / Last 5 rows + full schema view

### 🧹 Tab 2: Automated Data Cleaning
- **Missing Value Imputation** — Smart (Median for numeric, Mode for categorical) or Custom Constant
- **Duplicate Removal** — One-click deduplication with success metrics
- **Outlier Detection** — IQR method with adjustable multiplier slider + Clip/Drop options
- **Smart Type Casting** — Auto-detect misclassified columns (float→int, string→numeric, string→datetime)
- **CSV Download** — Export your cleaned dataset instantly

### 📊 Tab 3: Automated EDA
- **Descriptive Statistics** — Rich `.describe()` table with missing counts, dtypes, percentages
- **Target Variable Analysis** — Histogram + KDE for numeric, Count Plot for categorical
- **Correlation Matrix** — Interactive Plotly heatmap with multicollinearity warnings (|r| > 0.85)
- **Feature Distribution Hub** — Select any column for detailed distribution, skewness, kurtosis

### ⚙️ Tab 4: Advanced Feature Preparation
- **Feature Encoding** — One-Hot or Label Encoding with mapping previews
- **Feature Scaling** — StandardScaler (Z-score) or MinMaxScaler (0-1)
- **ML-Ready Download** — Export the fully prepared dataset

---
## 🚀 Live Demo

you can see the working model of the project:  
🔗 **[Klean AI Live Application](https://buildwithwaseem-klean-ai-app-soo0ef.streamlit.app/)**

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
streamlit run app.py
```

### 3. (Optional) Generate a test dataset
```bash
python generate_sample_data.py
```
This creates `sample_messy_dataset.csv` with intentional issues (missing values, outliers, duplicates, wrong dtypes) for testing.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.9+** | Core language |
| **Streamlit** | Web framework & UI |
| **Pandas / NumPy** | Data processing (vectorized) |
| **Plotly** | Interactive visualizations |
| **scikit-learn** | Feature encoding & scaling |
| **SciPy** | Statistical analysis (KDE, etc.) |

---

## 📁 Project Structure

```
klean ai/
├── .streamlit/
│   └── config.toml          # Streamlit theme & server config
├── app.py                    # Main Streamlit application (1033 lines)
├── styles.py                 # Custom CSS theme & Plotly theme constants
├── utils.py                  # Data processing utility functions
├── requirements.txt          # Python dependencies
├── generate_sample_data.py   # Test dataset generator
└── README.md                 # This file
```

---

## 🎨 Design

- **Theme:** Futuristic Dark Mode with neon accents
- **Colors:** Obsidian (#0B0F19), Slate (#1E293B), Electric Indigo (#6366F1), Teal (#14B8A6)
- **Typography:** Inter + JetBrains Mono from Google Fonts
- **Components:** Glass-morphism cards, animated metrics, loading skeletons, interactive Plotly charts

---

## 📝 License

MIT License. Built for data scientists who value speed and quality.
