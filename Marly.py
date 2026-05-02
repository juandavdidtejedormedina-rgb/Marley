import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="LifeQuest",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# RUTAS RAW DE GITHUB
# ============================================================

IMAGEN_PORTADA = "https://raw.githubusercontent.com/juandavdidtejedormedina-rgb/app-streamlite/cbeea9b924f7db779843abdef9922e7fcf3c649d/Imagen%20portada.png"

VIDEO_PERSONAJE = "https://raw.githubusercontent.com/juandavdidtejedormedina-rgb/app-streamlite/cbeea9b924f7db779843abdef9922e7fcf3c649d/personaje%202.mp4"

ARCHIVO_USUARIOS = Path("usuarios_lifequest.csv")


# ============================================================
# ESTADO DE SESIÓN
# ============================================================

if "pantalla" not in st.session_state:
    st.session_state.pantalla = "menu"

if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = None


# ============================================================
# FUNCIONES PARA USUARIOS
# ============================================================

def cargar_usuarios():
    if ARCHIVO_USUARIOS.exists():
        return pd.read_csv(ARCHIVO_USUARIOS)

    return pd.DataFrame(
        columns=[
            "nombre",
            "personaje",
            "nivel",
            "xp_total",
            "racha"
        ]
    )


def guardar_usuarios(df):
    df.to_csv(ARCHIVO_USUARIOS, index=False)


def registrar_usuario(nombre, personaje):
    usuarios = cargar_usuarios()
    nombre_limpio = nombre.strip()

    if nombre_limpio == "":
        return False, "Debes escribir tu nombre."

    if not usuarios.empty:
        existe = usuarios["nombre"].str.lower().eq(nombre_limpio.lower()).any()
        if existe:
            return False, "Este usuario ya está registrado."

    nuevo_usuario = pd.DataFrame(
        [
            {
                "nombre": nombre_limpio,
                "personaje": personaje,
                "nivel": 1,
                "xp_total": 0,
                "racha": 0
            }
        ]
    )

    usuarios = pd.concat([usuarios, nuevo_usuario], ignore_index=True)
    guardar_usuarios(usuarios)

    return True, "Usuario registrado correctamente."


def obtener_usuario(nombre):
    usuarios = cargar_usuarios()

    if usuarios.empty:
        return None

    usuario = usuarios[
        usuarios["nombre"].str.lower() == nombre.lower()
    ]

    if usuario.empty:
        return None

    return usuario.iloc[0].to_dict()


# ============================================================
# CSS PARA ESTILO TIERNO TIPO JUEGO
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
        padding-bottom: 2rem;
        max-width: 1250px;
    }

    .main-wrapper {
        min-height: 88vh;
        display: flex;
        align-items: center;
    }

    .login-card {
        background: rgba(255,255,255,0.95);
        border-radius: 36px;
        padding: 3rem 2.5rem;
        box-shadow: 0 18px 45px rgba(91, 141, 239, 0.14);
        border: 1px solid #e8f5e9;
        text-align: center;
    }

    .logo-circle {
        width: 92px;
        height: 92px;
        border-radius: 50%;
        background: linear-gradient(135deg, #d9f99d, #bbf7d0);
        margin: auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.18);
        margin-bottom: 1rem;
    }

    .life-title {
        font-size: 3.6rem;
        font-weight: 900;
        line-height: 1;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }

    .life-title span.life {
        color: #22c55e;
    }

    .life-title span.quest {
        color: #38bdf8;
    }

    .subtitle {
        color: #22a65a;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 2.2rem;
    }

    .soft-divider {
        color: #86efac;
        font-size: 1.4rem;
        margin-bottom: 2rem;
    }

    .cute-note {
        margin-top: 2rem;
        color: #22a65a;
        font-weight: 800;
        font-size: 1.05rem;
    }

    .portada-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .portada-img {
        width: 100%;
        max-height: 760px;
        object-fit: contain;
        filter: drop-shadow(0 18px 35px rgba(15, 23, 42, 0.12));
    }

    div[data-testid="stButton"] > button {
        border-radius: 999px;
        border: none;
        min-height: 68px;
        font-size: 1.25rem;
        font-weight: 900;
        letter-spacing: 0.5px;
        width: 100%;
        box-shadow: 0 10px 20px rgba(15, 23, 42, 0.10);
        transition: all 0.2s ease;
    }

    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 26px rgba(15, 23, 42, 0.13);
    }

    .register-card {
        background: rgba(255,255,255,0.97);
        border-radius: 34px;
        padding: 2.3rem;
        box-shadow: 0 18px 45px rgba(91, 141, 239, 0.14);
        border: 1px solid #e0f2fe;
    }

    .register-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #22c55e;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .register-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 1.8rem;
    }

    .video-card {
        background: white;
        border-radius: 30px;
        padding: 1rem;
        border: 1px solid #dcfce7;
        box-shadow: 0 12px 30px rgba(34, 197, 94, 0.10);
    }

    .welcome-card {
        background: rgba(255,255,255,0.95);
        border-radius: 30px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 18px 45px rgba(91, 141, 239, 0.14);
        border: 1px solid #e8f5e9;
    }

    .welcome-title {
        font-size: 3rem;
        font-weight: 900;
        color: #22c55e;
    }

    .welcome-text {
        color: #64748b;
        font-size: 1.2rem;
    }

    video {
        border-radius: 24px !important;
        width: 100% !important;
        max-height: 560px !important;
        object-fit: cover !important;
    }

    @media (max-width: 900px) {
        .life-title {
            font-size: 2.6rem;
        }
        .subtitle {
            font-size: 1.05rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PANTALLA 1: MENÚ PRINCIPAL
# ============================================================

def pantalla_menu():
    col_izquierda, col_derecha = st.columns([1, 1.15], vertical_alignment="center")

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
                <div class="soft-divider">— 🌱 —</div>
            """,
            unsafe_allow_html=True
        )

        if st.button("👤 INICIAR SESIÓN"):
            st.session_state.pantalla = "login"
            st.rerun()

        st.write("")

        if st.button("😊 REGISTRARSE"):
            st.session_state.pantalla = "registro"
            st.rerun()

        st.markdown(
            """
                <div class="cute-note">
                    ✨ ¡Pequeños pasos, grandes cambios! ✨
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_derecha:
        st.markdown(
            f"""
            <div class="portada-box">
                <img class="portada-img" src="{IMAGEN_PORTADA}">
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PANTALLA 2: REGISTRO
# ============================================================

def pantalla_registro():
    col_formulario, col_video = st.columns([1, 1.1], vertical_alignment="center")

    with col_formulario:
        st.markdown(
            """
            <div class="register-card">
                <div class="register-title">Crea tu personaje 🦉</div>
                <div class="register-subtitle">
                    Escribe tu nombre y elige tu compañero de aventura.
                </div>
            """,
            unsafe_allow_html=True
        )

        nombre = st.text_input(
            "Tu nombre",
            placeholder="Ejemplo: Camila"
        )

        personaje = st.selectbox(
            "Selecciona tu personaje",
            ["Búho aventurero"]
        )

        st.write("")

        if st.button("✨ Crear mi cuenta"):
            exito, mensaje = registrar_usuario(nombre, personaje)

            if exito:
                st.success(mensaje)
                st.session_state.usuario_actual = obtener_usuario(nombre.strip())
                st.session_state.pantalla = "bienvenida"
                st.rerun()
            else:
                st.error(mensaje)

        if st.button("⬅️ Volver al menú"):
            st.session_state.pantalla = "menu"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_video:
        st.markdown(
            """
            <div class="video-card">
                <h3 style="text-align:center; color:#22c55e; margin-bottom:1rem;">
                    Vista previa del personaje
                </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <video autoplay loop muted playsinline>
                <source src="{VIDEO_PERSONAJE}" type="video/mp4">
                Tu navegador no soporta video HTML5.
            </video>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PANTALLA 3: INICIAR SESIÓN
# ============================================================

def pantalla_login():
    usuarios = cargar_usuarios()

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown(
            """
            <div class="register-card">
                <div class="register-title">Iniciar sesión 🌱</div>
                <div class="register-subtitle">
                    Selecciona tu usuario para continuar tu aventura.
                </div>
            """,
            unsafe_allow_html=True
        )

        if usuarios.empty:
            st.info("Todavía no hay usuarios registrados.")
        else:
            usuario_nombre = st.selectbox(
                "¿Quién está ingresando?",
                usuarios["nombre"].tolist()
            )

            if st.button("Entrar a LifeQuest"):
                st.session_state.usuario_actual = obtener_usuario(usuario_nombre)
                st.session_state.pantalla = "bienvenida"
                st.rerun()

        if st.button("⬅️ Volver"):
            st.session_state.pantalla = "menu"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PANTALLA 4: BIENVENIDA TEMPORAL
# ============================================================

def pantalla_bienvenida():
    usuario = st.session_state.usuario_actual

    if usuario is None:
        st.session_state.pantalla = "menu"
        st.rerun()

    st.markdown(
        f"""
        <div class="welcome-card">
            <div class="welcome-title">¡Bienvenida, {usuario["nombre"]}! 🦉</div>
            <p class="welcome-text">
                Tu personaje es: <strong>{usuario["personaje"]}</strong>
            </p>
            <p class="welcome-text">
                Nivel {int(usuario["nivel"])} · {int(usuario["xp_total"])} XP · 🔥 Racha {int(usuario["racha"])} días
            </p>
            <p class="welcome-text">
                Esta es solo la entrada. Luego conectamos las misiones, XP, rachas y reportes.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("Cerrar sesión"):
            st.session_state.usuario_actual = None
            st.session_state.pantalla = "menu"
            st.rerun()


# ============================================================
# CONTROL PRINCIPAL
# ============================================================

if st.session_state.pantalla == "menu":
    pantalla_menu()

elif st.session_state.pantalla == "registro":
    pantalla_registro()

elif st.session_state.pantalla == "login":
    pantalla_login()

elif st.session_state.pantalla == "bienvenida":
    pantalla_bienvenida()
