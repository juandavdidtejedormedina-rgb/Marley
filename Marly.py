from datetime import date
from pathlib import Path
import html
import unicodedata

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
LOCAL_EXCEL_PATHS = [
    BASE_DIR / "Datos final marley.xlsx",
    BASE_DIR / "Datos" / "Datos final marley.xlsx",
]
REMOTE_EXCEL_URL = (
    "https://raw.githubusercontent.com/"
    "juandavdidtejedormedina-rgb/Marley/"
    "4b965708640420750075a41a3d079816c91a3d36/"
    "Datos%20marley%20monta%C3%B1a.xlsx"
    #Datos%20final%20marley.xlsx
)
SENSOR_NAMES = ("WIGA", "ECOWITT")
TIME_BUCKET = "30min"
SERIES_END_OFFSET = pd.Timedelta(hours=23, minutes=30)
AXIS_END_OFFSET = pd.Timedelta(hours=23, minutes=59)
DateRange = tuple[date, date]

BRAND_COLORS = {
    "hero": "#4C4678",
    "sky": "#D6E5EC",
    "rose": "#E7D2DA",
    "beige": "#D9CDBA",
    "graphite": "#2D3040",
    "ink": "#1F2430",
    "paper": "#F7F4EE",
    "white": "#FFFFFF",
}

SHEETS = {
    "WIGA MARLEY": "WIGA",
    "ECOWIT MARLEY": "ECOWITT",
}

VARIABLES = {
    "Humedad Relativa (%)": {
        "title": "Comparativa de humedades",
        "unit": "%",
        "short": "Humedad",
        "colors": {"WIGA": "#5B6275", "ECOWITT": "#6E97F2"},
        "accent": "#8077AE",
        "soft": "rgba(128, 119, 174, 0.18)",
    },
    "Temperatura (°C)": {
        "title": "Comparativa de temperaturas",
        "unit": "°C",
        "short": "Temperatura",
        "colors": {"WIGA": "#D39A58", "ECOWITT": "#C06C84"},
        "accent": "#D39A58",
        "soft": "rgba(211, 154, 88, 0.18)",
    },
    "Radiación PAR (µmol m-2 s-1)": {
        "title": "Comparativa de radiación PAR",
        "unit": "µmol m-2 s-1",
        "short": "PAR",
        "colors": {"WIGA": "#8CBD63", "ECOWITT": "#524B82"},
        "accent": "#8CBD63",
        "soft": "rgba(140, 189, 99, 0.18)",
    },
}

CANONICAL_COLUMNS = {
    "fecha": "Fecha",
    "hora": "Hora",
    "humedad relativa (%)": "Humedad Relativa (%)",
    "humedad relativa %": "Humedad Relativa (%)",
    "temperatura (c)": "Temperatura (°C)",
    "temperatura °c": "Temperatura (°C)",
    "temperatura c": "Temperatura (°C)",
    "radiacion par (mol m-2 s-1)": "Radiación PAR (µmol m-2 s-1)",
    "radiacion par (umol m-2 s-1)": "Radiación PAR (µmol m-2 s-1)",
    "radiacion par umol m-2 s-1": "Radiación PAR (µmol m-2 s-1)",
}


def configure_page() -> None:
    st.set_page_config(
        page_title="Dashboard Marly",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def inject_styles() -> None:
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {{
    --elite-hero: {BRAND_COLORS["hero"]};
    --elite-sky: {BRAND_COLORS["sky"]};
    --elite-rose: {BRAND_COLORS["rose"]};
    --elite-beige: {BRAND_COLORS["beige"]};
    --elite-graphite: {BRAND_COLORS["graphite"]};
    --elite-ink: {BRAND_COLORS["ink"]};
    --elite-paper: {BRAND_COLORS["paper"]};
    --elite-white: {BRAND_COLORS["white"]};
    --font-display: 'Manrope', sans-serif;
    --font-body: 'Manrope', sans-serif;
    --font-brand: 'Cormorant Garamond', serif;
}}

.stApp {{
    background:
        radial-gradient(circle at 12% 18%, rgba(217, 205, 186, 0.22), transparent 22%),
        radial-gradient(circle at 88% 10%, rgba(214, 229, 236, 0.34), transparent 28%),
        linear-gradient(180deg, #fcfaf6 0%, var(--elite-paper) 58%, #f2eee6 100%);
    color: var(--elite-ink);
    font-family: var(--font-body);
}}

[data-testid="stAppViewContainer"] > .main {{
    padding-top: 1.2rem;
}}

[data-testid="stAppViewContainer"] > .main .block-container {{
    max-width: 1180px;
    padding-left: 1rem;
    padding-right: 1rem;
}}

[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
}}

[data-testid="collapsedControl"] {{
    display: none !important;
}}

[data-testid="stAppViewContainer"] > .main .block-container {{
    max-width: 1360px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 1.2rem;
    padding-right: 1.2rem;
}}


.hero-card {{
    position: relative;
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 1rem;
    padding: 1.55rem 1.6rem;
    margin: 0 0 1.3rem 0;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 30px;
    background:
        radial-gradient(circle at 18% 18%, rgba(255,255,255,0.16), transparent 18%),
        linear-gradient(135deg, #5f598f 0%, #4c4678 38%, #2d3040 100%);
    box-shadow: 0 28px 68px rgba(35, 30, 58, 0.22);
    overflow: hidden;
}}

.hero-card::before {{
    content: "";
    position: absolute;
    inset: 1px;
    border-radius: 29px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    pointer-events: none;
}}

.hero-kicker {{
    margin: 0 0 0.45rem 0;
    color: rgba(255, 244, 238, 0.84);
    font-family: var(--font-brand);
    font-size: 1rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-weight: 700;
}}

.hero-card h1 {{
    margin: 0;
    color: var(--elite-white);
    font-family: var(--font-display);
    font-weight: 800;
    font-size: 2.35rem;
    line-height: 1.03;
    letter-spacing: -0.04em;
}}

.hero-subtitle {{
    margin: 0.85rem 0 0 0;
    max-width: 46rem;
    color: rgba(255, 255, 255, 0.82);
    font-size: 1.02rem;
    line-height: 1.7;
}}

.summary-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.85rem;
    margin: 0.35rem 0 1.15rem 0;
}}

.summary-card {{
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 164px;
    padding: 1.05rem 1.05rem 1rem 1.05rem;
    border-radius: 24px;
    border: 1px solid rgba(76, 70, 120, 0.10);
    background: linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(247,244,238,0.96) 100%);
    box-shadow: 0 18px 40px rgba(45, 48, 64, 0.09);
    overflow: hidden;
}}

.summary-card::before {{
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 5px;
    background: linear-gradient(90deg, var(--summary-accent), var(--summary-accent-soft));
}}

.summary-card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.9rem;
}}

.summary-card-label {{
    color: #646874;
    font-family: var(--font-display);
    font-size: 0.88rem;
    font-weight: 700;
}}

.summary-card-chip {{
    display: inline-flex;
    align-items: center;
    padding: 0.22rem 0.58rem;
    border-radius: 999px;
    background: rgba(76, 70, 120, 0.08);
    color: var(--elite-hero);
    font-size: 0.75rem;
    font-weight: 700;
}}

.summary-card-value {{
    display: flex;
    align-items: flex-end;
    gap: 0.34rem;
    min-height: 3.1rem;
}}

.summary-card-number {{
    color: var(--elite-graphite);
    font-family: var(--font-display);
    font-size: 2.16rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.04em;
}}

.summary-card-unit {{
    margin-bottom: 0.3rem;
    color: #5f6472;
    font-size: 0.88rem;
    font-weight: 600;
}}

.summary-card-footer {{
    margin-top: auto;
    padding-top: 0.72rem;
    color: #757985;
    font-size: 0.86rem;
    line-height: 1.55;
}}

.section-title {{
    margin: 1.2rem 0 0.75rem 0;
    color: var(--elite-graphite);
    font-family: var(--font-display);
    font-size: 1.16rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}}

.chart-shell {{
    padding: 1rem 1rem 0.45rem 1rem;
    margin-bottom: 1rem;
    border-radius: 28px;
    border: 1px solid rgba(76, 70, 120, 0.09);
    background: linear-gradient(180deg, rgba(255,255,255,0.90), rgba(247,244,238,0.96));
    box-shadow: 0 20px 44px rgba(45, 48, 64, 0.08);
}}

.chart-title {{
    margin: 0 0 0.2rem 0;
    color: var(--elite-graphite);
    font-family: var(--font-display);
    font-size: 1.14rem;
    font-weight: 800;
}}

.chart-caption {{
    margin: 0 0 0.95rem 0;
    color: #6f7380;
    font-size: 0.92rem;
    line-height: 1.55;
}}

.data-shell {{
    margin-top: 1rem;
}}

.map-card {{
    margin: 0.35rem 0 1.25rem 0;
    padding: 1rem 1rem 0.6rem 1rem;
    border-radius: 28px;
    border: 1px solid rgba(76, 70, 120, 0.09);
    background: linear-gradient(180deg, rgba(255,255,255,0.90), rgba(247,244,238,0.96));
    box-shadow: 0 20px 44px rgba(45, 48, 64, 0.08);
}}

.map-title {{
    margin: 0 0 0.2rem 0;
    color: var(--elite-graphite);
    font-family: var(--font-display);
    font-size: 1.06rem;
    font-weight: 800;
}}

.map-caption {{
    margin: 0 0 0.9rem 0;
    color: #6f7380;
    font-size: 0.92rem;
    line-height: 1.55;
}}

.map-link {{
    display: inline-flex;
    align-items: center;
    margin: 0.2rem 0 0.65rem 0;
    color: var(--elite-hero);
    font-weight: 700;
    text-decoration: none;
}}

.map-link:hover {{
    text-decoration: underline;
}}


.selector-shell {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 0.2rem 0 1rem 0;
    color: var(--elite-graphite);
    font-family: var(--font-display);
    font-size: 0.98rem;
    font-weight: 700;
}}

[data-testid="stDataFrame"] {{
    border-radius: 22px;
    overflow: hidden;
    border: 1px solid rgba(76, 70, 120, 0.08);
    box-shadow: 0 18px 36px rgba(45, 48, 64, 0.06);
}}

@media (max-width: 980px) {{
    .summary-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}

    .hero-card h1 {{
        font-size: 1.9rem;
    }}
}}

@media (max-width: 640px) {{
    .summary-grid {{
        grid-template-columns: 1fr;
    }}

    .hero-card {{
        padding: 1.2rem;
        border-radius: 24px;
    }}
}}
</style>
        """,
        unsafe_allow_html=True,
    )


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(text))
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(normalized.lower().split())


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {}
    for column in df.columns:
        key = normalize_text(column)
        if key in CANONICAL_COLUMNS:
            renamed[column] = CANONICAL_COLUMNS[key]
    return df.rename(columns=renamed)


def ensure_expected_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in ["Fecha", "Hora", *VARIABLES.keys()]:
        if column not in df.columns:
            df[column] = pd.NA
    return df


def load_wiga_sheet(source: str | Path, sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(source, sheet_name=sheet_name)
    df = standardize_columns(df)
    df = ensure_expected_columns(df)
    return df


def load_ecowitt_sheet(source: str | Path, sheet_name: str) -> pd.DataFrame:
    # ECOWITT arrives without a stable header row, so we normalize it manually.
    raw = pd.read_excel(source, sheet_name=sheet_name, header=None)
    raw = raw.iloc[:, :4].copy()
    raw.columns = [
        "FechaHora",
        "Humedad Relativa (%)",
        "Radiación PAR (µmol m-2 s-1)",
        "Temperatura (°C)",
    ]

    # Some files store the first timestamp as a mistaken header in row 0.
    raw["FechaHora"] = pd.to_datetime(raw["FechaHora"], errors="coerce")
    raw["Humedad Relativa (%)"] = pd.to_numeric(raw["Humedad Relativa (%)"], errors="coerce")
    raw["Radiación PAR (µmol m-2 s-1)"] = pd.to_numeric(raw["Radiación PAR (µmol m-2 s-1)"], errors="coerce")
    raw["Temperatura (°C)"] = pd.to_numeric(raw["Temperatura (°C)"], errors="coerce")
    raw = raw.dropna(subset=["FechaHora"])
    raw["Fecha"] = raw["FechaHora"].dt.strftime("%Y-%m-%d")
    raw["Hora"] = raw["FechaHora"].dt.strftime("%H:%M:%S")
    return raw[["Fecha", "Hora", "Humedad Relativa (%)", "Radiación PAR (µmol m-2 s-1)", "Temperatura (°C)"]]


def resolve_excel_source() -> str | Path:
    for candidate in LOCAL_EXCEL_PATHS:
        if candidate.exists():
            return candidate
    return REMOTE_EXCEL_URL


@st.cache_data(show_spinner="Cargando archivo de datos...")
def load_data() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    excel_source = resolve_excel_source()

    source_frames: dict[str, pd.DataFrame] = {}

    for sheet_name, source_name in SHEETS.items():
        if source_name == "WIGA":
            df = load_wiga_sheet(excel_source, sheet_name)
        else:
            df = load_ecowitt_sheet(excel_source, sheet_name)
        df["FechaHora"] = pd.to_datetime(
            df["Fecha"].astype(str) + " " + df["Hora"].astype(str),
            errors="coerce",
        )
        df = df.dropna(subset=["FechaHora"]).sort_values("FechaHora")

        columns = ["FechaHora", *VARIABLES.keys()]
        df = df[columns].copy()
        for variable in VARIABLES:
            df.rename(columns={variable: f"{variable} - {source_name}"}, inplace=True)
        source_frames[source_name] = df

    merged = None
    for frame in source_frames.values():
        merged = frame if merged is None else merged.merge(frame, on="FechaHora", how="outer")

    if merged is None:
        raise ValueError("No fue posible construir la tabla consolidada de sensores.")
    merged = merged.sort_values("FechaHora").reset_index(drop=True)

    return merged, source_frames


def build_hero() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div>
                <p class="hero-kicker">Dashboard ambiental</p>
                <h1>Comparativa visual entre WIGA y ECOWITT en la finca Marly</h1>
                <p class="hero-subtitle">
                    Lectura comparativa de humedad relativa, temperatura y radiación PAR
                    para detectar diferencias entre ambos equipos a lo largo del tiempo
                    con un estilo ejecutivo y fácil de leer.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_number(value: float | int, decimals: int = 1) -> str:
    return f"{value:,.{decimals}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def build_full_time_index(selected_range: DateRange) -> pd.DatetimeIndex:
    start_date, end_date = selected_range
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)
    return pd.date_range(
        start=start_ts,
        end=end_ts + SERIES_END_OFFSET,
        freq=TIME_BUCKET,
    )


def date_filter(df: pd.DataFrame) -> tuple[pd.DataFrame, DateRange, date, date]:
    min_date = df["FechaHora"].min().date()
    max_date = df["FechaHora"].max().date()

    if "selected_day" not in st.session_state:
        st.session_state["selected_day"] = max_date

    start_date = st.session_state["selected_day"]
    end_date = st.session_state["selected_day"]

    mask = df["FechaHora"].dt.date.between(start_date, end_date)
    filtered = df.loc[mask].copy()
    return filtered, (start_date, end_date), min_date, max_date


def render_day_navigation(min_date: date, max_date: date) -> None:
    current_day = st.session_state["selected_day"]

    col1, col2, col3, col4 = st.columns([1, 1.4, 1, 1.3])
    with col1:
        if st.button("◀ Día anterior", width="stretch", disabled=current_day <= min_date):
            new_day = (pd.Timestamp(current_day) - pd.Timedelta(days=1)).date()
            st.session_state["selected_day"] = new_day
            st.rerun()

    with col2:
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:0.45rem; color:{BRAND_COLORS['graphite']};
                        font-family:Manrope,sans-serif; font-size:1rem; font-weight:700;">
                {current_day.strftime('%Y-%m-%d')}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        if st.button("Día siguiente ▶", width="stretch", disabled=current_day >= max_date):
            new_day = (pd.Timestamp(current_day) + pd.Timedelta(days=1)).date()
            st.session_state["selected_day"] = new_day
            st.rerun()

    with col4:
        selected_day = st.date_input(
            "Seleccionar fecha",
            value=current_day,
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed",
        )
        if selected_day != current_day:
            st.session_state["selected_day"] = selected_day
            st.rerun()


def get_time_axis_config(df: pd.DataFrame) -> dict:
    min_time = df["FechaHora"].min()
    max_time = df["FechaHora"].max()
    span = max_time - min_time
    total_days = max(span.total_seconds() / 86400, 0)

    if total_days <= 1.1:
        return {
            "tickformat": "%H:%M",
            "dtick": 1 * 60 * 60 * 1000,
            "title": "Hora del dia",
        }
    if total_days <= 3:
        return {
            "tickformat": "%d/%m\n%H:%M",
            "dtick": 6 * 60 * 60 * 1000,
            "title": "Fecha y hora",
        }
    if total_days <= 10:
        return {
            "tickformat": "%d/%m\n%H:%M",
            "dtick": 12 * 60 * 60 * 1000,
            "title": "Fecha y hora",
        }
    return {
        "tickformat": "%d/%m/%Y",
        "dtick": 24 * 60 * 60 * 1000,
        "title": "Fecha",
    }


def build_hourly_series(
    df: pd.DataFrame,
    column_name: str,
    selected_range: DateRange,
) -> pd.DataFrame:
    source_df = df[["FechaHora", column_name]].dropna(subset=[column_name]).copy()
    if source_df.empty:
        return source_df

    source_df["FechaHora"] = source_df["FechaHora"].dt.floor(TIME_BUCKET)
    source_df = source_df.groupby("FechaHora", as_index=False)[column_name].mean()
    full_index = build_full_time_index(selected_range)
    source_df = source_df.set_index("FechaHora").reindex(full_index).rename_axis("FechaHora").reset_index()
    return source_df

def build_hourly_comparison(df: pd.DataFrame, variable: str, selected_range: DateRange) -> pd.DataFrame:
    # This is the shared comparison table used by both charts and metrics.
    wiga_col = f"{variable} - WIGA"
    ecowitt_col = f"{variable} - ECOWITT"

    hourly_wiga = build_hourly_series(df, wiga_col, selected_range).rename(columns={wiga_col: "WIGA"})
    hourly_eco = build_hourly_series(df, ecowitt_col, selected_range).rename(columns={ecowitt_col: "ECOWITT"})
    comparison = hourly_wiga.merge(hourly_eco, on="FechaHora", how="outer")
    comparison["DiffPct"] = pd.NA
    comparison["DiffValue"] = pd.NA

    valid_mask = (
        comparison["WIGA"].notna()
        & comparison["ECOWITT"].notna()
    )
    comparison.loc[valid_mask, "DiffValue"] = (
        comparison.loc[valid_mask, "WIGA"] - comparison.loc[valid_mask, "ECOWITT"]
    ).abs()

    pct_mask = valid_mask & (comparison["ECOWITT"] != 0)
    comparison.loc[pct_mask, "DiffPct"] = (
        comparison.loc[pct_mask, "DiffValue"]
        / comparison.loc[pct_mask, "ECOWITT"]
        * 100
    )
    comparison["DiffValueLabel"] = comparison["DiffValue"].apply(
        lambda value: "No disponible"
        if pd.isna(value)
        else f"{value:.2f}"
    )
    comparison["DiffPctLabel"] = comparison["DiffPct"].apply(
        lambda value: "No disponible"
        if pd.isna(value)
        else f"{value:.2f}%"
    )
    return comparison


def get_available_sources(comparison: pd.DataFrame) -> list[str]:
    return [source_name for source_name in SENSOR_NAMES if comparison[source_name].notna().any()]


def get_y_axis_config(df: pd.DataFrame, variable: str) -> dict:
    series = []
    for source_name in SENSOR_NAMES:
        column_name = f"{variable} - {source_name}"
        if column_name in df.columns:
            clean = pd.to_numeric(df[column_name], errors="coerce").dropna()
            if not clean.empty:
                series.append(clean)

    if not series:
        return {"title": VARIABLES[variable]["unit"]}

    values = pd.concat(series, ignore_index=True)
    vmin = float(values.min())
    vmax = float(values.max())

    if variable == "Humedad Relativa (%)":
        axis_min = max(0, min(100, (int(vmin // 5) * 5) - 5))
        axis_max = min(100, (int(vmax // 5) * 5) + 5)
        if axis_max <= axis_min:
            axis_max = min(100, axis_min + 5)
        return {
            "title": "Humedad relativa (%)",
            "range": [axis_min, axis_max],
            "dtick": 5,
            "ticksuffix": "%",
        }

    if variable == "Temperatura (°C)":
        axis_min = round(vmin - 1.5, 1)
        axis_max = round(vmax + 1.5, 1)
        return {
            "title": "Temperatura (°C)",
            "range": [axis_min, axis_max],
            "dtick": 2,
        }

    axis_min = max(0, int(vmin * 0.95))
    axis_max = int(vmax * 1.05) if vmax > 0 else 10
    spread = max(axis_max - axis_min, 1)
    if spread <= 100:
        dtick = 10
    elif spread <= 300:
        dtick = 25
    elif spread <= 800:
        dtick = 50
    else:
        dtick = 100
    return {
        "title": "Radiacion PAR (µmol m-2 s-1)",
        "range": [-25, axis_max],
        "dtick": dtick,
    }


def make_chart(comparison: pd.DataFrame, variable: str, selected_range: DateRange) -> go.Figure:
    config = VARIABLES[variable]
    fig = go.Figure()
    time_axis = get_time_axis_config(comparison)
    y_axis = get_y_axis_config(comparison.rename(columns={name: f"{variable} - {name}" for name in SENSOR_NAMES}), variable)
    start_date, end_date = selected_range

    for source_name in SENSOR_NAMES:
        source_df = comparison[["FechaHora", source_name, "DiffValueLabel", "DiffPctLabel"]].copy()
        if source_df[source_name].dropna().empty:
            continue

        fig.add_trace(
            go.Scatter(
                x=source_df["FechaHora"],
                y=source_df[source_name],
                name=source_name,
                mode="lines+markers",
                line=dict(color=config["colors"][source_name], width=3),
                marker=dict(size=6),
                connectgaps=False,
                customdata=source_df[["DiffValueLabel", "DiffPctLabel"]],
                hovertemplate=(
                    "<b>%{x|%Y-%m-%d %H:%M}</b><br>"
                    + f"{source_name}: "
                    + "%{y:.2f} "
                    + config["unit"]
                    + (
                        "<br>Diferencia valor: %{customdata[0]} "
                        + config["unit"]
                        + "<br>Diferencia %: %{customdata[1]}"
                        if source_name == SENSOR_NAMES[0]
                        else ""
                    )
                    + "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title=dict(
            text=config["title"],
            x=0,
            xanchor="left",
            font=dict(size=21, color=BRAND_COLORS["graphite"], family="Manrope, sans-serif"),
        ),
        height=470,
        margin=dict(l=28, r=28, t=74, b=28),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(250,248,243,0.72)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(255,255,255,0.72)",
            bordercolor="rgba(76, 70, 120, 0.08)",
            borderwidth=1,
            font=dict(size=11, family="Manrope, sans-serif", color=BRAND_COLORS["graphite"]),
        ),
        xaxis=dict(
            title=time_axis["title"],
            showgrid=True,
            gridcolor="rgba(76, 70, 120, 0.07)",
            zeroline=False,
            tickformat=time_axis["tickformat"],
            dtick=time_axis["dtick"],
            tickangle=0,
            ticklabelmode="period",
            range=(
                [pd.Timestamp(start_date), pd.Timestamp(start_date) + AXIS_END_OFFSET]
                if start_date == end_date
                else [pd.Timestamp(start_date), pd.Timestamp(end_date) + AXIS_END_OFFSET]
            ),
            tickfont=dict(size=11, family="Manrope, sans-serif", color=BRAND_COLORS["graphite"]),
        ),
        yaxis=dict(
            title=y_axis["title"],
            showgrid=True,
            gridcolor="rgba(76, 70, 120, 0.07)",
            zeroline=False,
            range=y_axis.get("range"),
            dtick=y_axis.get("dtick"),
            ticksuffix=y_axis.get("ticksuffix", ""),
            separatethousands=True,
            tickfont=dict(size=11, family="Manrope, sans-serif", color=BRAND_COLORS["graphite"]),
        ),
        font=dict(family="Manrope, sans-serif", color=BRAND_COLORS["graphite"]),
        hoverlabel=dict(
            bgcolor="rgba(249, 246, 240, 0.98)",
            bordercolor="rgba(76, 70, 120, 0.16)",
            font=dict(family="Manrope, sans-serif", color=BRAND_COLORS["graphite"], size=12),
        ),
    )

    return fig


def make_scatter_comparison(comparison: pd.DataFrame, variable: str) -> go.Figure | None:
    hourly = comparison.dropna(subset=list(SENSOR_NAMES)).copy()
    if hourly.empty:
        return None

    config = VARIABLES[variable]
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=hourly["WIGA"],
            y=hourly["ECOWITT"],
            mode="markers",
            name="Comparación",
            marker=dict(
                size=9,
                color="#6E97F2",
                opacity=0.78,
                line=dict(color="rgba(255,255,255,0.75)", width=1),
            ),
            customdata=hourly[["FechaHora", "DiffValueLabel", "DiffPctLabel"]],
            hovertemplate=(
                "<b>%{customdata[0]|%Y-%m-%d %H:%M}</b><br>"
                + "WIGA: %{x:.2f} " + config["unit"]
                + "<br>ECOWITT: %{y:.2f} " + config["unit"]
                + "<br>Diferencia valor: %{customdata[1]} " + config["unit"]
                + "<br>Diferencia %: %{customdata[2]}"
                + "<extra></extra>"
            ),
        )
    )

    combined = pd.concat([hourly["WIGA"], hourly["ECOWITT"]], ignore_index=True)
    min_val = float(combined.min())
    max_val = float(combined.max())
    padding = (max_val - min_val) * 0.08 if max_val > min_val else 1.0
    axis_min = min_val - padding
    axis_max = max_val + padding

    fig.add_trace(
        go.Scatter(
            x=[axis_min, axis_max],
            y=[axis_min, axis_max],
            mode="lines",
            name="Referencia y = x",
            line=dict(color="#D39A58", width=2, dash="dash"),
            hoverinfo="skip",
        )
    )

    fig.update_layout(
        title=dict(
            text="Dispersión entre sensores",
            x=0,
            xanchor="left",
            font=dict(size=20, color=BRAND_COLORS["graphite"], family="Manrope, sans-serif"),
        ),
        height=430,
        margin=dict(l=28, r=28, t=72, b=28),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(250,248,243,0.72)",
        template="plotly_white",
        font=dict(family="Manrope, sans-serif", color=BRAND_COLORS["graphite"]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(255,255,255,0.72)",
            bordercolor="rgba(76, 70, 120, 0.08)",
            borderwidth=1,
            font=dict(size=11, family="Manrope, sans-serif", color=BRAND_COLORS["graphite"]),
        ),
        xaxis=dict(
            title=f"WIGA ({config['unit']})",
            range=[axis_min, axis_max],
            showgrid=True,
            gridcolor="rgba(76, 70, 120, 0.07)",
            zeroline=False,
            tickfont=dict(size=11, family="Manrope, sans-serif", color=BRAND_COLORS["graphite"]),
        ),
        yaxis=dict(
            title=f"ECOWITT ({config['unit']})",
            range=[axis_min, axis_max],
            scaleanchor="x",
            scaleratio=1,
            showgrid=True,
            gridcolor="rgba(76, 70, 120, 0.07)",
            zeroline=False,
            tickfont=dict(size=11, family="Manrope, sans-serif", color=BRAND_COLORS["graphite"]),
        ),
        hoverlabel=dict(
            bgcolor="rgba(249, 246, 240, 0.98)",
            bordercolor="rgba(76, 70, 120, 0.16)",
            font=dict(family="Manrope, sans-serif", color=BRAND_COLORS["graphite"], size=12),
        ),
    )

    return fig


def get_difference_stats(comparison: pd.DataFrame) -> dict:
    valid_diff = pd.to_numeric(comparison["DiffValue"], errors="coerce").dropna()

    if valid_diff.empty:
        return {"std_diff": None, "count": 0}

    std_diff = valid_diff.std()
    return {
        "std_diff": None if pd.isna(std_diff) else float(std_diff),
        "count": int(valid_diff.count()),
    }


def render_stats_block(comparison: pd.DataFrame, variable: str) -> None:
    config = VARIABLES[variable]
    stats = get_difference_stats(comparison)
    std_diff = stats["std_diff"]
    count_value = stats["count"]

    st.markdown(
        """
        <div class="chart-shell">
            <p class="chart-title">Desviación estándar de la diferencia</p>
            <p class="chart-caption">
                La desviación estándar de la diferencia indica qué tan variable es la separación entre ambos sensores a lo largo del tiempo. Un valor bajo sugiere una diferencia constante (buena consistencia), mientras que un valor alto indica que la diferencia fluctúa, evidenciando menor concordancia entre las mediciones.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.metric(
            "Desviación estándar de la diferencia",
            (
                f"{format_number(std_diff, 2)} {config['unit']}"
                if std_diff is not None
                else "Sin datos"
            ),
            help="Se calcula con la diferencia entre sensores en cada instante: WIGA - ECOWITT, y luego se obtiene su desviación estándar.",
        )
    with col2:
        st.caption(f"Registros comparados: {count_value}")


def render_chart_block(comparison: pd.DataFrame, variable: str, selected_range: DateRange) -> None:
    config = VARIABLES[variable]
    available_sources = get_available_sources(comparison)

    if not available_sources:
        st.markdown(
            f"""
            <div class="chart-shell">
                <p class="chart-title">{html.escape(config['title'])}</p>
                <p class="chart-caption">
                    No hay datos disponibles para esta variable en el rango seleccionado.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    overlap = comparison.dropna(subset=list(SENSOR_NAMES)).copy()
    diff_text = "Sin traslape suficiente para calcular diferencia promedio."
    if not overlap.empty:
        avg_diff = overlap["DiffValue"].mean()
        diff_text = f"Diferencia promedio entre sensores: {format_number(avg_diff, 2)} {config['unit']}"
    elif len(available_sources) == 1:
        diff_text = f"Solo hay datos disponibles para {available_sources[0]} en este rango."

    render_stats_block(comparison, variable)
    st.caption(diff_text)
    st.plotly_chart(make_chart(comparison, variable, selected_range), width="stretch")


def render_scatter_block(comparison: pd.DataFrame, variable: str) -> None:
    fig = make_scatter_comparison(comparison, variable)
    if fig is None:
        st.info("No hay suficientes datos simultáneos entre WIGA y ECOWITT para construir la dispersión.")
        return

    st.markdown(
        """
        <div class="chart-shell">
            <p class="chart-title">Comparación directa entre sensores</p>
            <p class="chart-caption">
                En esta gráfica de dispersión, cada punto representa una medición simultánea de ambos sensores: WIGA en el eje X y ECOWITT en el eje Y. La línea diagonal (y = x) representa una concordancia perfecta entre ambos sensores.
            </p>
            <p class="chart-caption">
                Los puntos cercanos a esta línea indican una alta concordancia en las mediciones. Cuando un punto se ubica por encima de la línea, el sensor ECOWITT registra valores mayores que WIGA; mientras que si se ubica por debajo, WIGA registra valores superiores a ECOWITT. La dispersión de los puntos respecto a la línea permite evaluar la consistencia y diferencias entre ambos dispositivos.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig, width="stretch")


def build_detail_table(df: pd.DataFrame) -> pd.DataFrame:
    table = df.copy()
    table["FechaHora"] = table["FechaHora"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return table


def build_summary_table(source_data: dict[str, pd.DataFrame], selected_range: DateRange) -> pd.DataFrame:
    summary_rows = []
    for source_name, source_df in source_data.items():
        current = source_df[source_df["FechaHora"].dt.date.between(*selected_range)].copy()
        summary_rows.append(
            {
                "Equipo": source_name,
                "Registros": len(current),
                "Inicio": current["FechaHora"].min().strftime("%Y-%m-%d %H:%M") if not current.empty else "-",
                "Fin": current["FechaHora"].max().strftime("%Y-%m-%d %H:%M") if not current.empty else "-",
            }
        )
    return pd.DataFrame(summary_rows)


def main() -> None:
    configure_page()
    inject_styles()
    build_hero()

    try:
        comparative_df, source_data = load_data()
    except Exception as error:
        st.error(f"No fue posible cargar el archivo de Excel. Detalle: {error}")
        st.stop()

    filtered_df, selected_range, min_date, max_date = date_filter(comparative_df)

    if filtered_df.empty:
        st.warning("No hay datos disponibles para el rango seleccionado.")
        st.stop()

    st.markdown('<div class="section-title">Series comparativas</div>', unsafe_allow_html=True)
    render_day_navigation(min_date, max_date)
    st.markdown(
        '<div class="selector-shell">Selecciona la variable que quieres analizar</div>',
        unsafe_allow_html=True,
    )
    selected_variable = st.segmented_control(
        "Variable",
        options=list(VARIABLES.keys()),
        format_func=lambda x: VARIABLES[x]["title"].replace("Comparativa de ", "").capitalize(),
        default=list(VARIABLES.keys())[0],
        label_visibility="collapsed",
    )
    comparison = build_hourly_comparison(filtered_df, selected_variable, selected_range)
    render_chart_block(comparison, selected_variable, selected_range)
    render_scatter_block(comparison, selected_variable)

    with st.expander("Ver registros y resumen", expanded=False):
        st.markdown('<div class="data-shell"></div>', unsafe_allow_html=True)
        tab_data, tab_resume = st.tabs(["Tabla completa", "Resumen por equipo"])

        with tab_data:
            st.dataframe(build_detail_table(filtered_df), width="stretch", hide_index=True)

        with tab_resume:
            st.dataframe(build_summary_table(source_data, selected_range), width="stretch", hide_index=True)


if __name__ == "__main__":
    main()
