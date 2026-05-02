import streamlit as st

# ============================================================
# CONFIGURACIÓN BÁSICA DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="LifeQuest",
    page_icon="🦉",
    layout="wide"
)

# ============================================================
# IMAGEN DE PORTADA
# ============================================================

IMAGEN_PORTADA = (
    "https://raw.githubusercontent.com/"
    "juandavdidtejedormedina-rgb/app-streamlite/"
    "cbeea9b924f7db779843abdef9922e7fcf3c649d/"
    "Imagen%20portada.png"
)

# ============================================================
# ESTILOS VISUALES
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fbfff7 0%, #f1fbff 45%, #fff8ef 100%);
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1250px;
    }

    .login-card {
        background: white;
        border-radius: 36px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: 0 18px 45px rgba(91, 141, 239, 0.14);
        border: 1px solid #e8f5e9;
        min-height: 520px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .logo-circle {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: #d9f99d;
        margin: 0 auto 1rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
    }

    .life-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
    }

    .life-title .life {
        color: #22c55e;
    }

    .life-title .quest {
        color: #38bdf8;
    }

    .subtitle {
        color: #16a34a;
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 2rem;
    }

    .divider {
        color: #86efac;
        font-size: 1.4rem;
        margin-bottom: 2rem;
    }

    .portada-img {
        width: 100%;
        max-height: 780px;
        object-fit: contain;
        filter: drop-shadow(0 18px 35px rgba(15, 23, 42, 0.12));
    }

    .cute-note {
        text-align: center;
        color: #16a34a;
        font-weight: 900;
        font-size: 1.1rem;
        margin-top: 2rem;
    }

    div[data-testid="stButton"] {
        display: flex;
        justify-content: center;
    }

    div[data-testid="stButton"] > button {
        width: 260px;
        height: 60px;
        border-radius: 999px;
        border: none;
        background: white;
        color: #172554;
        font-size: 1.05rem;
        font-weight: 800;
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.10);
    }

    div[data-testid="stButton"] > button:hover {
        background: #f0fdf4;
        color: #16a34a;
        transform: translateY(-2px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DISEÑO DE LA PÁGINA PRINCIPAL
# ============================================================

col_izquierda, col_derecha = st.columns([1, 1.15], vertical_alignment="center")

# ============================================================
# COLUMNA IZQUIERDA: MENÚ DE INICIO
# ============================================================

with col_izquierda:
    st.markdown(
        """
        <div class="login-card">
            <div class="logo-circle">🏁</div>

            <div class="life-title">
                <span class="life">Life</span><span class="quest">Quest</span>
            </div>

            <div class="subtitle">
                Tu juego de hábitos saludables 💗
            </div>

            <div class="divider">
                — 🌱 —
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.button("👤 INICIAR SESIÓN")

    st.markdown(
        """
        <div class="cute-note">
            ✨ ¡Pequeños pasos, grandes cambios! ✨
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# COLUMNA DERECHA: IMAGEN DEL BÚHO
# ============================================================

with col_derecha:
    st.markdown(
        f"""
        <img class="portada-img" src="{IMAGEN_PORTADA}">
        """,
        unsafe_allow_html=True
    )
