import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Referencia de Precios Percha",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded",
)

C1 = "#002a5c"
C2 = "#004b8e"
C3 = "#005dab"
C4 = "#017dc3"

st.markdown(f"""
<style>
html, body, [class*="css"], .stApp, .block-container {{
    font-family: Arial, sans-serif !important;
    background-color: #f4f7fb;
}}

/* ── Sidebar background ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {C1} 0%, {C2} 60%, {C3} 100%);
}}

/* Sidebar text – labels, markdown, radio */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {{
    color: white !important;
    font-family: Arial, sans-serif !important;
}}

/* Selectbox trigger box */
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {{
    background-color: rgba(255,255,255,0.13) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 6px !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] svg {{
    fill: white !important;
}}

/* ── Dropdown portal: render outside sidebar with DARK text ── */
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul {{
    background-color: #ffffff !important;
}}
[data-baseweb="popover"] [role="option"],
[data-baseweb="popover"] li,
[data-baseweb="popover"] li span,
[data-baseweb="popover"] [data-baseweb="option"],
[data-baseweb="popover"] [data-baseweb="option"] span,
[data-baseweb="popover"] [data-baseweb="option"] div {{
    color: #1a1a2e !important;
    font-family: Arial, sans-serif !important;
    font-size: 13px !important;
    background-color: #ffffff !important;
}}
[data-baseweb="popover"] [role="option"]:hover {{
    background-color: #e8f0fb !important;
    color: {C2} !important;
}}
[data-baseweb="popover"] [aria-selected="true"],
[data-baseweb="popover"] [aria-selected="true"] span {{
    background-color: #dbeafe !important;
    color: {C1} !important;
    font-weight: 700 !important;
}}

/* Header */
.header-bar {{
    background: linear-gradient(90deg, {C1} 0%, {C3} 60%, {C4} 100%);
    border-radius: 12px;
    padding: 22px 32px;
    margin-bottom: 22px;
}}
.header-bar h1 {{
    color: white; font-size: 24px; font-weight: 700;
    margin: 0; font-family: Arial, sans-serif;
}}
.header-bar p {{
    color: #9ecbee; font-size: 13px; margin: 4px 0 0 0;
    font-family: Arial, sans-serif;
}}

/* KPI cards */
.kpi-card {{
    background: white; border-radius: 10px; padding: 16px 20px;
    border-left: 5px solid {C3};
    box-shadow: 0 1px 6px rgba(0,42,92,0.09);
    height: 100%;
}}
.kpi-card .kpi-val {{
    font-size: 26px; font-weight: 700; color: {C2};
    font-family: Arial, sans-serif;
}}
.kpi-card .kpi-lbl {{
    font-size: 11px; color: #7a8fa6; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.05em;
    font-family: Arial, sans-serif;
}}

hr {{ border-color: rgba(255,255,255,0.15); }}
[data-testid="stDataFrame"] {{ font-family: Arial, sans-serif !important; }}
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("https://github.com/JoseProanioM/productosAlpina/blob/2765f6f64529159629650cfd5c14d15ef751ee9a/precios.csv")
    df["Variedad"] = df["Variedad"].fillna("—")
    df["Tipo de Producto"] = df["Tipo de Producto"].fillna("—")
    df["Precio con escenario"] = df["Precio Percha SMX"] + df["Aumento de precio"]
    return df

df = load_data()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
  <h1>🏷️ Referencia de Precios Percha - Supermaxi (31 de enero de 2026)</h1>
  <p>Herramienta de consulta de precios</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar filters (cascading) ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-size:18px;font-weight:700;color:white;padding:4px 0 14px 0;font-family:Arial;'>🔍 Filtros</div>", unsafe_allow_html=True)

    # 1 – Categoría
    cats = ["Todas"] + sorted(df["Categoría"].dropna().unique().tolist())
    categoria = st.selectbox("Categoría", cats)
    df_f = df if categoria == "Todas" else df[df["Categoría"] == categoria]

    # 2 – Marca
    marcas = ["Todas"] + sorted(df_f["Marca / Línea"].dropna().unique().tolist())
    marca = st.selectbox("Marca / Línea", marcas)
    df_f = df_f if marca == "Todas" else df_f[df_f["Marca / Línea"] == marca]

    # 3 – Tipo de Producto
    tipos = ["Todos"] + sorted([t for t in df_f["Tipo de Producto"].dropna().unique() if t != "—"])
    tipo = st.selectbox("Tipo de Producto", tipos)
    df_f = df_f if tipo == "Todos" else df_f[df_f["Tipo de Producto"] == tipo]

    # 4 – Presentación
    presis = ["Todas"] + sorted(df_f["Presentación"].dropna().unique().tolist())
    presentacion = st.selectbox("Presentación", presis)
    df_f = df_f if presentacion == "Todas" else df_f[df_f["Presentación"] == presentacion]

    # 5 – Tamaño / Contenido  ← NEW
    tamanios = ["Todos"] + sorted(df_f["Tamaño / Contenido"].dropna().unique().tolist())
    tamanio = st.selectbox("Tamaño / Contenido", tamanios)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:11px;color:#7ab3d3;font-family:Arial;text-align:center;'>SMX · {pd.Timestamp.today().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

# ── Apply filters ──────────────────────────────────────────────────────────────
filtered = df.copy()
if categoria   != "Todas": filtered = filtered[filtered["Categoría"]          == categoria]
if marca       != "Todas": filtered = filtered[filtered["Marca / Línea"]       == marca]
if tipo        != "Todos": filtered = filtered[filtered["Tipo de Producto"]    == tipo]
if presentacion!= "Todas": filtered = filtered[filtered["Presentación"]        == presentacion]
if tamanio     != "Todos": filtered = filtered[filtered["Tamaño / Contenido"]  == tamanio]

# ── KPIs ───────────────────────────────────────────────────────────────────────
id_cols = ["Marca / Línea", "Tipo de Producto", "Presentación", "Variedad", "Tamaño / Contenido"]
base_only   = filtered.drop_duplicates(subset=id_cols)["Precio Percha SMX"]
n_prods     = len(base_only)
precio_min  = base_only.min()  if n_prods > 0 else 0.0
precio_max  = base_only.max()  if n_prods > 0 else 0.0
precio_prom = base_only.mean() if n_prods > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
for col, val, lbl in [
    (c1, str(n_prods),          "Productos encontrados"),
    (c2, f"${precio_prom:.2f}", "Precio promedio"),
    (c3, f"${precio_min:.2f}",  "Precio mínimo"),
    (c4, f"${precio_max:.2f}",  "Precio máximo"),
]:
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

# ── Price table: one row per product, price columns per scenario ───────────────
st.markdown(f"<div style='color:{C1};font-size:16px;font-weight:700;font-family:Arial;margin-bottom:10px;'>📋 Tabla de precios</div>", unsafe_allow_html=True)

if filtered.empty:
    st.info("No se encontraron productos con los filtros seleccionados.")
else:
    all_id = ["Categoría", "Marca / Línea", "Tipo de Producto", "Presentación", "Variedad", "Tamaño / Contenido"]

    # Pivot so each product is a single row with one price column per scenario
    piv = filtered.pivot_table(
        index=all_id,
        columns="Escenario",
        values="Precio con escenario",
        aggfunc="first",
    ).reset_index()
    piv.columns.name = None

    # Attach base price
    base_map = (
        filtered[all_id + ["Precio Percha SMX"]]
        .drop_duplicates(subset=all_id)
        .set_index(all_id)["Precio Percha SMX"]
    )
    piv = piv.set_index(all_id)
    piv.insert(0, "Precio Base", base_map)
    piv = piv.reset_index()

    # Guarantee all scenario columns exist
    for s in ["+ 2%", "+ 5%", "+ 10%"]:
        if s not in piv.columns:
            piv[s] = float("nan")

    piv = piv.rename(columns={"+ 2%": "▲ +2%", "+ 5%": "▲ +5%", "+ 10%": "▲ +10%"})

    price_cols = ["Precio Base", "▲ +2%", "▲ +5%", "▲ +10%"]
    piv = piv[all_id + price_cols]

    for c in price_cols:
        piv[c] = piv[c].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "—")

    def style_table(styler):
        styler.set_table_styles([
            {"selector": "th", "props": [
                ("background-color", C1), ("color", "white"),
                ("font-family", "Arial, sans-serif"), ("font-size", "12px"),
                ("font-weight", "700"), ("text-align", "center"),
            ]},
            {"selector": "td", "props": [
                ("font-family", "Arial, sans-serif"), ("font-size", "13px"),
            ]},
        ])
        styler.set_properties(subset=["Precio Base"], **{
            "background-color": "#eef4ff", "color": C2,
            "font-weight": "700", "text-align": "center",
        })
        styler.set_properties(subset=["▲ +2%"], **{
            "background-color": "#e8f5e9", "color": "#2e7d32",
            "font-weight": "600", "text-align": "center",
        })
        styler.set_properties(subset=["▲ +5%"], **{
            "background-color": "#fff8e1", "color": "#f57f17",
            "font-weight": "600", "text-align": "center",
        })
        styler.set_properties(subset=["▲ +10%"], **{
            "background-color": "#fce4ec", "color": "#c62828",
            "font-weight": "600", "text-align": "center",
        })
        return styler

    st.dataframe(piv.style.pipe(style_table), use_container_width=True, height=500)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:20px 0 8px 0;color:#b0bcc8;font-size:11px;font-family:Arial,sans-serif;'>
  Herramienta interna · SMX · Uso exclusivo para encuestadores
</div>
""", unsafe_allow_html=True)
