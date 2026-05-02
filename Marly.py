import streamlit as st

# ============================================================
# 1. CONSTANTES DE LA APLICACIÓN
# ============================================================

TITULO_PAGINA = "LifeQuest"
ICONO_PAGINA = "🦉"
LAYOUT_PAGINA = "wide"

NOMBRE_APP = "LifeQuest"
SUBTITULO_APP = "Tu juego de hábitos saludables 💗"
FRASE_MOTIVACIONAL = "✨ ¡Pequeños pasos, grandes cambios! ✨"
TEXTO_BOTON_INICIO = "👤 INICIAR SESIÓN"

IMAGEN_PORTADA = (
    "https://raw.githubusercontent.com/"
    "juandavdidtejedormedina-rgb/app-streamlite/"
    "cbeea9b924f7db779843abdef9922e7fcf3c649d/"
    "Imagen%20portada.png"
)


# ============================================================
# 2. CONFIGURACIÓN DE LA PÁGINA
# ============================================================

def configurar_pagina():
    """
    Configura la pestaña del navegador y el diseño general.
    """

    st.set_page_config(
        page_title=TITULO_PAGINA,
        page_icon=ICONO_PAGINA,
        layout=LAYOUT_PAGINA
    )


# ============================================================
# 3. ESTILOS VISUALES
# ============================================================

def aplicar_estilos():
    """
    Aplica estilos básicos a la aplicación.
    Aquí no se construye contenido, solo se modifica la apariencia.
    """

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

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: white;
            border-radius: 36px;
            box-shadow: 0 18px 45px rgba(91, 141, 239, 0.14);
            border: 1px solid #e8f5e9;
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
# 4. COMPONENTES VISUALES
# ============================================================

def mostrar_tarjeta_inicio():
    """
    Muestra la tarjeta principal con el logo, título y subtítulo.
    Esta versión usa componentes normales de Streamlit para evitar errores con HTML.
    """

    with st.container(border=True):
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            "<h1 style='text-align:center; font-size:60px;'>🏁</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <h1 style='text-align:center; font-size:58px; font-weight:900;'>
                <span style='color:#22c55e;'>Life</span><span style='color:#38bdf8;'>Quest</span>
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <h3 style='text-align:center; color:#16a34a;'>
                {SUBTITULO_APP}
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<h2 style='text-align:center; color:#86efac;'>— 🌱 —</h2>",
            unsafe_allow_html=True
        )

        st.markdown("<br><br>", unsafe_allow_html=True)


def mostrar_boton_inicio():
    """
    Muestra el botón de iniciar sesión.
    Por ahora no tiene función, solo es visual.
    """

    st.write("")
    st.button(TEXTO_BOTON_INICIO)


def mostrar_frase_motivacional():
    """
    Muestra la frase motivacional inferior.
    """

    st.markdown(
        f"""
        <h4 style='text-align:center; color:#16a34a; font-weight:900;'>
            {FRASE_MOTIVACIONAL}
        </h4>
        """,
        unsafe_allow_html=True
    )


def mostrar_imagen_portada():
    """
    Muestra la imagen del búho en la columna derecha.
    """

    st.image(
        IMAGEN_PORTADA,
        use_container_width=True
    )


# ============================================================
# 5. PANTALLA PRINCIPAL
# ============================================================

def mostrar_pantalla_inicio():
    """
    Construye la pantalla inicial usando dos columnas:
    izquierda para el menú y derecha para la imagen.
    """

    col_izquierda, col_derecha = st.columns(
        [1, 1.15],
        vertical_alignment="center"
    )

    with col_izquierda:
        mostrar_tarjeta_inicio()
        mostrar_boton_inicio()
        mostrar_frase_motivacional()

    with col_derecha:
        mostrar_imagen_portada()


# ============================================================
# 6. FUNCIÓN PRINCIPAL
# ============================================================

def ejecutar_app():
    """
    Ejecuta la aplicación completa.
    """

    configurar_pagina()
    aplicar_estilos()
    mostrar_pantalla_inicio()


# ============================================================
# 7. EJECUCIÓN
# ============================================================

ejecutar_app()
