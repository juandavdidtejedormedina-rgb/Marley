import streamlit as st

# =========================
# CONSTANTES
# =========================

TITULO_PAGINA = "LifeQuest"
ICONO_PAGINA = "🦉"
LAYOUT_PAGINA = "wide"

SUBTITULO_APP = "Tu juego de hábitos saludables"
FRASE_MOTIVACIONAL = "¡Pequeños pasos, grandes cambios!"
TEXTO_BOTON = "INICIAR SESIÓN"

IMAGEN_PORTADA = (
    "https://raw.githubusercontent.com/"
    "juandavdidtejedormedina-rgb/app-streamlite/"
    "cbeea9b924f7db779843abdef9922e7fcf3c649d/"
    "Imagen%20portada.png"
)


# =========================
# CONFIGURACIÓN
# =========================

def configurar_pagina():
    st.set_page_config(
        page_title=TITULO_PAGINA,
        page_icon=ICONO_PAGINA,
        layout=LAYOUT_PAGINA
    )


# =========================
# ESTILOS
# =========================

def aplicar_estilos():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #fbfff7, #f1fbff, #fff8ef);
        }

        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
        }

        div[data-testid="stButton"] > button {
            width: 260px;
            height: 60px;
            border-radius: 30px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================
# COMPONENTES
# =========================

def mostrar_tarjeta_inicio():
    with st.container(border=True):
        st.markdown(
            """
            <h1 style='text-align:center; font-size:60px;'>🏁</h1>
            <h1 style='text-align:center; font-size:58px;'>
                <span style='color:#22c55e;'>Life</span><span style='color:#38bdf8;'>Quest</span>
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"<h3 style='text-align:center; color:#16a34a;'>{SUBTITULO_APP}</h3>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h2 style='text-align:center; color:#86efac;'>— 🌱 —</h2>",
            unsafe_allow_html=True
        )


def mostrar_boton():
    st.button(TEXTO_BOTON)


def mostrar_frase():
    st.markdown(
        f"<h4 style='text-align:center; color:#16a34a;'>{FRASE_MOTIVACIONAL}</h4>",
        unsafe_allow_html=True
    )


def mostrar_imagen():
    st.image(IMAGEN_PORTADA, use_container_width=True)


# =========================
# PANTALLA PRINCIPAL
# =========================

def mostrar_inicio():
    col_izquierda, col_derecha = st.columns([1, 1.15])

    with col_izquierda:
        mostrar_tarjeta_inicio()
        mostrar_boton()
        mostrar_frase()

    with col_derecha:
        mostrar_imagen()


# =========================
# EJECUCIÓN
# =========================

def ejecutar_app():
    configurar_pagina()
    aplicar_estilos()
    mostrar_inicio()


ejecutar_app()
