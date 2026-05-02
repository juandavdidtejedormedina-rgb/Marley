import streamlit as st

# ============================================================
# CONFIGURACIÓN BÁSICA
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
# ESTILOS BÁSICOS
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

    .card {
        background: white;
        border-radius: 36px;
        padding: 4rem 2rem;
        text-align: center;
        box-shadow: 0 18px 45px rgba(91, 141, 239, 0.14);
        border: 1px solid #e8f5e9;
    }

    .titulo {
        font-size: 3.5rem;
        font-weight: 900;
        color: #22c55e;
        margin-bottom: 0rem;
    }

    .titulo span {
        color: #38bdf8;
    }

    .subtitulo {
        color: #16a34a;
        font-size: 1.25rem;
        font-weight: 800;
        margin-top: 0.5rem;
    }

    .portada {
        width: 100%;
        max-height: 780px;
        object-fit: contain;
        filter: drop-shadow(0 18px 35px rgba(15, 23, 42, 0.12));
    }

    .frase {
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
        width: 270px;
        height: 62px;
        border-radius: 999px;
        border: none;
        background: white;
        color: #172554;
        font-size: 1.05rem;
        font-weight: 800;
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.10);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DISEÑO PRINCIPAL
# ============================================================

col_izquierda, col_derecha = st.columns([1, 1.15], vertical_alignment="center")

with col_izquierda:
    st.markdown(
        """
        <div class="card">
            <div style="font-size: 3rem;">🏁</div>
            <div class="titulo">Life<span>Quest</span></div>
            <div class="subtitulo">Tu juego de hábitos saludables 💗</div>
            <div style="color:#86efac; font-size:1.4rem; margin-top:2rem;">— 🌱 —</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.button("👤 INICIAR SESIÓN")

    st.markdown(
        """
        <div class="frase">
            ✨ ¡Pequeños pasos, grandes cambios! ✨
        </div>
        """,
        unsafe_allow_html=True
    )

with col_derecha:
    st.image(IMAGEN_PORTADA, use_container_width=True)
