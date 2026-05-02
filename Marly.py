import streamlit as st

# ============================================================
# 1. CONSTANTES DE LA APLICACIÓN
# ============================================================

# Nombre que aparecerá como título de la pestaña del navegador
TITULO_PAGINA = "LifeQuest"

# Ícono que aparecerá en la pestaña del navegador
ICONO_PAGINA = "🦉"

# Tipo de distribución de la página: wide permite usar más espacio horizontal
LAYOUT_PAGINA = "wide"

# Nombre visual de la aplicación
NOMBRE_APP = "LifeQuest"

# Subtítulo que se muestra debajo del nombre de la app
SUBTITULO_APP = "Tu juego de hábitos saludables 💗"

# Frase motivacional inferior
FRASE_MOTIVACIONAL = "✨ ¡Pequeños pasos, grandes cambios! ✨"

# Texto del botón inicial
TEXTO_BOTON_INICIO = "👤 INICIAR SESIÓN"

# Imagen de portada ubicada en GitHub en formato raw
# Esta imagen aparece en la parte derecha de la pantalla
IMAGEN_PORTADA = (
    "https://raw.githubusercontent.com/"
    "juandavdidtejedormedina-rgb/app-streamlite/"
    "cbeea9b924f7db779843abdef9922e7fcf3c649d/"
    "Imagen%20portada.png"
)


# ============================================================
# 2. CONFIGURACIÓN GENERAL DE STREAMLIT
# ============================================================

def configurar_pagina():
    """
    Configura la página principal de Streamlit.

    Aquí se define:
    - El título de la pestaña del navegador.
    - El ícono de la pestaña.
    - El diseño horizontal amplio.
    """

    st.set_page_config(
        page_title=TITULO_PAGINA,
        page_icon=ICONO_PAGINA,
        layout=LAYOUT_PAGINA
    )


# ============================================================
# 3. ESTILOS VISUALES DE LA APLICACIÓN
# ============================================================

def aplicar_estilos():
    """
    Aplica estilos CSS personalizados a la aplicación.

    Estos estilos permiten que la interfaz se vea más tierna,
    colorida y parecida a una app de hábitos tipo juego.
    """

    st.markdown(
        """
        <style>
        /* Fondo general de la aplicación */
        .stApp {
            background: linear-gradient(135deg, #fbfff7 0%, #f1fbff 45%, #fff8ef 100%);
        }

        /* Oculta la barra superior por defecto de Streamlit */
        header {
            visibility: hidden;
        }

        /* Controla el ancho y el espacio superior del contenido */
        .block-container {
            padding-top: 2rem;
            max-width: 1250px;
        }

        /* Tarjeta principal del menú de inicio */
        .card {
            background: white;
            border-radius: 36px;
            padding: 4rem 2rem;
            text-align: center;
            box-shadow: 0 18px 45px rgba(91, 141, 239, 0.14);
            border: 1px solid #e8f5e9;
        }

        /* Título principal LifeQuest */
        .titulo {
            font-size: 3.5rem;
            font-weight: 900;
            color: #22c55e;
            margin-bottom: 0rem;
        }

        /* Parte azul del título: Quest */
        .titulo span {
            color: #38bdf8;
        }

        /* Subtítulo debajo del nombre de la app */
        .subtitulo {
            color: #16a34a;
            font-size: 1.25rem;
            font-weight: 800;
            margin-top: 0.5rem;
        }

        /* Imagen de portada del búho */
        .portada {
            width: 100%;
            max-height: 780px;
            object-fit: contain;
            filter: drop-shadow(0 18px 35px rgba(15, 23, 42, 0.12));
        }

        /* Frase motivacional inferior */
        .frase {
            text-align: center;
            color: #16a34a;
            font-weight: 900;
            font-size: 1.1rem;
            margin-top: 2rem;
        }

        /* Centra los botones de Streamlit */
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
        }

        /* Estilo del botón principal */
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

        /* Efecto al pasar el mouse sobre el botón */
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
# 4. COMPONENTES VISUALES REUTILIZABLES
# ============================================================

def mostrar_tarjeta_inicio():
    """
    Muestra la tarjeta principal de la aplicación.

    Esta tarjeta contiene:
    - Un ícono superior.
    - El nombre LifeQuest.
    - El subtítulo de la app.
    - Un divisor decorativo.
    """

    st.markdown(
        f"""
        <div class="card">
            <div style="font-size: 3rem;">🏁</div>

            <div class="titulo">
                Life<span>Quest</span>
            </div>

            <div class="subtitulo">
                {SUBTITULO_APP}
            </div>

            <div style="color:#86efac; font-size:1.4rem; margin-top:2rem;">
                — 🌱 —
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_boton_inicio():
    """
    Muestra el botón inicial de iniciar sesión.

    En esta primera versión el botón todavía no navega
    a otra pantalla; solo se muestra visualmente.
    """

    st.write("")

    st.button(TEXTO_BOTON_INICIO)


def mostrar_frase_motivacional():
    """
    Muestra la frase motivacional debajo del botón.
    """

    st.markdown(
        f"""
        <div class="frase">
            {FRASE_MOTIVACIONAL}
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_imagen_portada():
    """
    Muestra la imagen del búho en la parte derecha.

    Se usa st.image porque es más sencillo y seguro
    para mostrar imágenes externas en Streamlit.
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
    Construye la pantalla inicial de la aplicación.

    La pantalla se divide en dos columnas:
    - Columna izquierda: tarjeta LifeQuest, botón y frase.
    - Columna derecha: imagen del búho.
    """

    col_izquierda, col_derecha = st.columns(
        [1, 1.15],
        vertical_alignment="center"
    )

    # Contenido de la columna izquierda
    with col_izquierda:
        mostrar_tarjeta_inicio()
        mostrar_boton_inicio()
        mostrar_frase_motivacional()

    # Contenido de la columna derecha
    with col_derecha:
        mostrar_imagen_portada()


# ============================================================
# 6. FUNCIÓN PRINCIPAL
# ============================================================

def ejecutar_app():
    """
    Función principal que ejecuta la aplicación.

    Aquí se llaman en orden:
    1. La configuración de la página.
    2. Los estilos visuales.
    3. La pantalla principal.
    """

    configurar_pagina()
    aplicar_estilos()
    mostrar_pantalla_inicio()


# ============================================================
# 7. EJECUCIÓN DE LA APLICACIÓN
# ============================================================

ejecutar_app()
