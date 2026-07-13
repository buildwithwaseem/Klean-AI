"""
Klean AI — Custom CSS Theme
Futuristic Dark Mode with Neon Accents
"""

CUSTOM_CSS = """
<style>
/* ============================
   GOOGLE FONTS
   ============================ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ============================
   CSS VARIABLES & ROOT
   ============================ */
:root {
    --bg-primary: #0B0F19;
    --bg-secondary: #111827;
    --bg-card: #1E293B;
    --bg-card-hover: #243047;
    --bg-input: #0F172A;
    --border-subtle: rgba(99, 102, 241, 0.15);
    --border-glow: rgba(99, 102, 241, 0.4);
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --accent-indigo: #6366F1;
    --accent-indigo-light: #818CF8;
    --accent-teal: #14B8A6;
    --accent-teal-light: #2DD4BF;
    --accent-rose: #F43F5E;
    --accent-amber: #F59E0B;
    --accent-emerald: #10B981;
    --gradient-primary: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A78BFA 100%);
    --gradient-teal: linear-gradient(135deg, #14B8A6 0%, #06B6D4 100%);
    --gradient-rose: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%);
    --gradient-card: linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.6) 100%);
    --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.3), 0 1px 4px rgba(0, 0, 0, 0.2);
    --shadow-glow-indigo: 0 0 20px rgba(99, 102, 241, 0.3), 0 0 60px rgba(99, 102, 241, 0.1);
    --shadow-glow-teal: 0 0 20px rgba(20, 184, 166, 0.3), 0 0 60px rgba(20, 184, 166, 0.1);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ============================
   GLOBAL RESETS & BASE STYLES
   ============================ */
.stApp {
    background: var(--bg-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary) !important;
}

.stApp > header {
    background: transparent !important;
}

/* Main content area */
.main .block-container {
    padding: 2rem 3rem 4rem 3rem !important;
    max-width: 1400px !important;
}

/* ============================
   SCROLLBAR STYLING
   ============================ */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg-primary);
}
::-webkit-scrollbar-thumb {
    background: var(--bg-card);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--accent-indigo);
}

/* ============================
   SIDEBAR STYLING
   ============================ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #0B0F19 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
    width: 300px !important;
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] .stMarkdown label {
    color: var(--text-secondary) !important;
}

section[data-testid="stSidebar"] .stRadio label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    transition: var(--transition-fast) !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--accent-indigo-light) !important;
}

/* ============================
   HEADINGS & TEXT
   ============================ */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 900;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary);
    font-weight: 400;
    letter-spacing: 0.02em;
    margin-top: 0;
}

.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid var(--border-subtle);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ============================
   CARDS
   ============================ */
.glass-card {
    background: var(--gradient-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-card);
    backdrop-filter: blur(12px);
    transition: var(--transition-base);
}

.glass-card:hover {
    border-color: var(--border-glow);
    box-shadow: var(--shadow-card), var(--shadow-glow-indigo);
    transform: translateY(-2px);
}

/* ============================
   METRIC CARDS
   ============================ */
.metric-card {
    background: var(--gradient-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.5rem;
    text-align: center;
    transition: var(--transition-base);
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradient-primary);
    opacity: 0;
    transition: var(--transition-base);
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-glow-indigo);
    border-color: var(--border-glow);
}

.metric-card:hover::before {
    opacity: 1;
}

.metric-icon {
    font-size: 1.8rem;
    margin-bottom: 0.3rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-primary);
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.metric-value.indigo { color: var(--accent-indigo-light); }
.metric-value.teal { color: var(--accent-teal-light); }
.metric-value.rose { color: var(--accent-rose); }
.metric-value.amber { color: var(--accent-amber); }
.metric-value.emerald { color: var(--accent-emerald); }

.metric-label {
    font-size: 0.78rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-top: 0.2rem;
}


/* ============================
   TABS STYLING 
   ============================ */
div[data-testid="stTabs"] [data-baseweb="tab-list"],
.stTabs [data-baseweb="tab-list"] {
    gap: 4px !important;
    background: var(--bg-secondary) !important;
    border-radius: var(--radius-md) !important;
    padding: 4px !important;
    border: 1px solid var(--border-subtle) !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"],
.stTabs [data-baseweb="tab"] {
    height: 42px !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    transition: var(--transition-fast) !important;
    background: transparent !important;
    border: none !important;
    padding: 0 1.25rem !important;
}

/* Hover State override */
div[data-testid="stTabs"] button[data-baseweb="tab"]:hover,
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: rgba(99, 102, 241, 0.08) !important;
}

/* Active Tab Selector (Jo Cloud par blue ho jata tha) */
div[data-testid="stTabs"] button[aria-selected="true"],
.stTabs [aria-selected="true"] {
    background: var(--accent-indigo) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4) !important;
}

/* Extra line decoration ko kill karne ke liye */
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
    background-color: transparent !important;
}
/* ============================
   BUTTONS
   ============================ */
.stButton > button {
    background: var(--gradient-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.01em;
    transition: var(--transition-base) !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.5) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.stDownloadButton > button {
    background: var(--gradient-teal) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 2px 8px rgba(20, 184, 166, 0.3) !important;
    transition: var(--transition-base) !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(20, 184, 166, 0.5) !important;
}

/* ============================
   INPUTS, SELECTS, SLIDERS
   ============================ */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    transition: var(--transition-fast) !important;
}

.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within {
    border-color: var(--accent-indigo) !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
}

.stTextInput > div > div > input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-indigo) !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
}

.stNumberInput > div > div > input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
}

div[data-baseweb="slider"] div[role="slider"] {
    background: var(--accent-indigo) !important;
    border-color: var(--accent-indigo) !important;
}

/* ============================
   CHECKBOX & TOGGLE STYLING
   ============================ */
.stCheckbox label span {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

/* ============================
   FILE UPLOADER
   ============================ */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border-subtle) !important;
    border-radius: var(--radius-lg) !important;
    padding: 2rem !important;
    transition: var(--transition-base) !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-indigo) !important;
    background: rgba(99, 102, 241, 0.05) !important;
}

[data-testid="stFileUploader"] section {
    padding: 0 !important;
}

/* ============================
   DATAFRAME / TABLE STYLING
   ============================ */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
}

.stDataFrame div[data-testid="glideDataEditor"] {
    border-radius: var(--radius-md) !important;
}

/* ============================
   EXPANDERS
   ============================ */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    transition: var(--transition-fast) !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--accent-indigo) !important;
    color: var(--accent-indigo-light) !important;
}

/* ============================
   ALERT / SUCCESS / WARNING BOXES
   ============================ */
.stAlert {
    border-radius: var(--radius-md) !important;
    border: none !important;
}

div[data-testid="stNotification"] {
    border-radius: var(--radius-md) !important;
}

/* ============================
   DIVIDERS
   ============================ */
hr {
    border-color: var(--border-subtle) !important;
    margin: 1.5rem 0 !important;
}

/* ============================
   STATUS / BADGE
   ============================ */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}

.badge-success {
    background: rgba(16, 185, 129, 0.12);
    color: var(--accent-emerald);
    border: 1px solid rgba(16, 185, 129, 0.25);
}

.badge-warning {
    background: rgba(245, 158, 11, 0.12);
    color: var(--accent-amber);
    border: 1px solid rgba(245, 158, 11, 0.25);
}

.badge-danger {
    background: rgba(244, 63, 94, 0.12);
    color: var(--accent-rose);
    border: 1px solid rgba(244, 63, 94, 0.25);
}

/* ============================
   ANIMATIONS
   ============================ */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 8px rgba(99, 102, 241, 0.2); }
    50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.5); }
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.animate-in {
    animation: fadeInUp 0.5s ease-out forwards;
}

.loading-skeleton {
    background: linear-gradient(90deg, var(--bg-card) 25%, var(--bg-card-hover) 50%, var(--bg-card) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: var(--radius-sm);
    height: 1.2rem;
    margin-bottom: 0.5rem;
}

/* ============================
   SIDEBAR BRAND LOGO
   ============================ */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 0 1.5rem 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1.5rem;
}

.sidebar-brand-icon {
    width: 42px;
    height: 42px;
    background: var(--gradient-primary);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    box-shadow: var(--shadow-glow-indigo);
}

.sidebar-brand-text {
    font-size: 1.25rem;
    font-weight: 800;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}

.sidebar-brand-version {
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

/* ============================
   NAV ITEM STYLING
   ============================ */
.nav-item {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.65rem 1rem;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: var(--transition-fast);
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
}

.nav-item:hover {
    background: rgba(99, 102, 241, 0.08);
    color: var(--text-primary);
}

.nav-item.active {
    background: rgba(99, 102, 241, 0.12);
    color: var(--accent-indigo-light);
    border-left: 3px solid var(--accent-indigo);
}

/* ============================
   WELCOME CARD / EMPTY STATE
   ============================ */
.welcome-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
}

.welcome-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    animation: pulse-glow 3s infinite;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.welcome-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.welcome-desc {
    font-size: 1rem;
    color: var(--text-secondary);
    max-width: 500px;
    line-height: 1.6;
}

/* ============================
   FOOTER
   ============================ */
.app-footer {
    text-align: center;
    padding: 2rem 0 1rem 0;
    color: var(--text-muted);
    font-size: 0.75rem;
    border-top: 1px solid var(--border-subtle);
    margin-top: 3rem;
}

/* ============================
   PROGRESS BAR OVERRIDE
   ============================ */
.stProgress > div > div {
    background: var(--gradient-primary) !important;
    border-radius: var(--radius-sm) !important;
}

/* ============================
   TOOLTIP STYLING
   ============================ */
[data-testid="stTooltipContent"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-sm) !important;
}

/* ============================
   PLOTLY CHART CONTAINER
   ============================ */
.stPlotlyChart {
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    overflow: hidden;
    background: var(--bg-card);
}

/* ============================
   RESPONSIVE ADJUSTMENTS
   ============================ */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 1rem 3rem 1rem !important;
    }
    .hero-title {
        font-size: 2rem;
    }
    .metric-value {
        font-size: 1.5rem;
    }
}
</style>
"""

# Plotly theme constants used across all charts
PLOTLY_THEME = dict(
    bg_color="#0B0F19",
    card_bg="#1E293B",
    grid_color="rgba(99, 102, 241, 0.08)",
    text_color="#F1F5F9",
    text_secondary="#94A3B8",
    accent_indigo="#6366F1",
    accent_teal="#14B8A6",
    accent_rose="#F43F5E",
    accent_amber="#F59E0B",
    accent_emerald="#10B981",
    accent_purple="#A78BFA",
    font_family="Inter, sans-serif",
    colorscale=[
        [0.0, "#0B0F19"],
        [0.15, "#1E1B4B"],
        [0.3, "#3730A3"],
        [0.45, "#4F46E5"],
        [0.6, "#6366F1"],
        [0.75, "#818CF8"],
        [0.9, "#A78BFA"],
        [1.0, "#C4B5FD"],
    ],
)


def get_plotly_layout(**overrides):
    """Return a consistent Plotly layout dict with our dark theme."""
    layout = dict(
        paper_bgcolor=PLOTLY_THEME["bg_color"],
        plot_bgcolor=PLOTLY_THEME["card_bg"],
        font=dict(
            family=PLOTLY_THEME["font_family"],
            color=PLOTLY_THEME["text_color"],
            size=13,
        ),
        xaxis=dict(
            gridcolor=PLOTLY_THEME["grid_color"],
            zerolinecolor=PLOTLY_THEME["grid_color"],
            title_font=dict(size=12, color=PLOTLY_THEME["text_secondary"]),
            tickfont=dict(size=11, color=PLOTLY_THEME["text_secondary"]),
        ),
        yaxis=dict(
            gridcolor=PLOTLY_THEME["grid_color"],
            zerolinecolor=PLOTLY_THEME["grid_color"],
            title_font=dict(size=12, color=PLOTLY_THEME["text_secondary"]),
            tickfont=dict(size=11, color=PLOTLY_THEME["text_secondary"]),
        ),
        margin=dict(l=50, r=30, t=50, b=50),
        hoverlabel=dict(
            bgcolor=PLOTLY_THEME["card_bg"],
            font_size=12,
            font_family=PLOTLY_THEME["font_family"],
            bordercolor=PLOTLY_THEME["accent_indigo"],
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=PLOTLY_THEME["text_secondary"], size=11),
        ),
    )
    layout.update(overrides)
    return layout
