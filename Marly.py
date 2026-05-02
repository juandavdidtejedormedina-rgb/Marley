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

PERSONAJES = {
    "🦉 Búho aventurero": {
        "nombre": "Búho aventurero",
        "video": "https://raw.githubusercontent.com/juandavdidtejedormedina-rgb/Marley/b82a6ebeb66d35db9a7caee17718dda8441ed88f/personaje%202.mp4",
        "descripcion": "Un compañero sabio, constante y motivador para iniciar tu aventura saludable."
    },
    "🐰 Conejito atleta": {
        "nombre": "Conejito atleta",
        "video": "https://raw.githubusercontent.com/juandavdidtejedormedina-rgb/Marley/b82a6ebeb66d35db9a7caee17718dda8441ed88f/personaje%203.mp4",
        "descripcion": "Ideal para quienes quieren moverse más, ganar energía y cumplir misiones activas."
    },
    "🦊 Zorrito estratega": {
        "nombre": "Zorrito estratega",
        "video": "https://raw.githubusercontent.com/juandavdidtejedormedina-rgb/Marley/b82a6ebeb66d35db9a7caee17718dda8441ed88f/personaje%204.mp4",
        "descripcion": "Perfecto para organizar metas, planear hábitos y avanzar con inteligencia."
    },
    "🐼 Panda tranquilo": {
        "nombre": "Panda tranquilo",
        "video": "https://raw.githubusercontent.com/juandavdidtejedormedina-rgb/Marley/b82a6ebeb66d35db9a7caee17718dda8441ed88f/personaje%205.mp4",
        "descripcion": "Un personaje calmado para trabajar descanso, equilibrio y autocuidado."
    }
}

ARCHIVO_USUARIOS = Path("usuarios_lifequest.csv")

COLUMNAS_USUARIOS = [
    "nombre",
    "personaje",
    "video_personaje",
    "nivel",
    "xp_total",
    "racha"
]


# ============================================================
# ESTADO DE SESIÓN
# ============================================================

if "pantalla" not in st.session_state:
    st.session_state.pantalla = "menu"

if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = None


# ============================================================
# FUNCIONES DE USUARIOS
# ============================================================

def crear_tabla_usuarios_vacia():
    return pd.DataFrame(columns=COLUMNAS_USUARIOS)


def normalizar_tabla_usuarios(df):
    """
    Corrige el archivo usuarios_lifequest.csv si viene de una versión anterior.
    """

    if df.empty:
        return crear_tabla_usuarios_vacia()

    if "nombre" not in df.columns and "nombre_completo" in df.columns:
        df["nombre"] = df["nombre_completo"]

    if "personaje" not in df.columns:
        if "avatar_nombre" in df.columns:
            df["personaje"] = df["avatar_nombre"]
        else:
            df["personaje"] = "Búho aventurero"

    if "video_personaje" not in df.columns:
        df["video_personaje"] = PERSONAJES["🦉 Búho aventurero"]["video"]

    if "nivel" not in df.columns:
        df["nivel"] = 1

    if "xp_total" not in df.columns:
        df["xp_total"] = 0

    if "racha" not in df.columns:
        if "racha_global" in df.columns:
            df["racha"] = df["racha_global"]
        else:
            df["racha"] = 0

    df = df[COLUMNAS_USUARIOS]

    df["nombre"] = df["nombre"].fillna("").astype(str)
    df["personaje"] = df["personaje"].fillna("Búho aventurero").astype(str)
    df["video_personaje"] = df["video_personaje"].fillna(PERSONAJES["🦉 Búho aventurero"]["video"]).astype(str)
    df["nivel"] = pd.to_numeric(df["nivel"], errors="coerce").fillna(1).astype(int)
    df["xp_total"] = pd.to_numeric(df["xp_total"], errors="coerce").fillna(0).astype(int)
    df["racha"] = pd.to_numeric(df["racha"], errors="coerce").fillna(0).astype(int)

    df = df[df["nombre"].str.strip() != ""]

    return df


def cargar_usuarios():
    if ARCHIVO_USUARIOS.exists():
        try:
            df = pd.read_csv(ARCHIVO_USUARIOS)
            df = normalizar_tabla_usuarios(df)
            guardar_usuarios(df)
            return df
        except Exception:
            return crear_tabla_usuarios_vacia()

    return crear_tabla_usuarios_vacia()


def guardar_usuarios(df):
    df.to_csv(ARCHIVO_USUARIOS, index=False)


def registrar_usuario(nombre, personaje, video_personaje):
    usuarios = cargar_usuarios()
    nombre_limpio = nombre.strip()

    if nombre_limpio == "":
        return False, "Debes escribir tu nombre."

    if not usuarios.empty:
        existe = usuarios["nombre"].str.lower().eq(nombre_limpio.lower()).any()

        if existe:
            return False, "Este usuario ya está registrado. Puedes iniciar sesión."

    nuevo_usuario = pd.DataFrame(
        [
            {
                "nombre": nombre_limpio,
                "personaje": personaje,
                "video_personaje": video_personaje,
                "nivel": 1,
                "xp_total": 0,
                "racha": 0
            }
        ]
    )

    usuarios = pd.concat([usuarios, nuevo_usuario], ignore_index=True)
    usuarios = normalizar_tabla_usuarios(usuarios)
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
# ESTILOS CSS
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

    .login-card {
        background: rgba(255,255,255,0.95);
        border-radius: 36px;
        padding: 3rem 2.5rem;
        box-shadow: 0 18px 45px rgba(91, 141, 239, 0.14);
        border: 1px solid #e8f5e9;
        text-align: center;
        min-height: 520px;
        display: flex;
        flex-direction: column;
        justify-content: center;
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
        color: #16a34a;
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 2rem;
    }

    .soft-divider {
        color: #86efac;
        font-size: 1.4rem;
        margin-bottom: 1.8rem;
    }

    .cute-note {
        margin-top: 2rem;
        color: #16a34a;
        font-weight: 900;
        font-size: 1.05rem;
        text-align: center;
    }

    .portada-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .portada-img {
        width: 100%;
        max-height: 780px;
        object-fit: contain;
        filter: drop-shadow(0 18px 35px rgba(15, 23, 42, 0.12));
    }

    .menu-button-wrapper {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-bottom: 1.2rem;
    }

    .menu-button-wrapper div[data-testid="stButton"] {
        width: 100%;
        display: flex;
        justify-content: center;
    }

    .menu-button-wrapper div[data-testid="stButton"] > button {
        width: 360px !important;
        height: 72px !important;
        border-radius: 999px !important;
        border: none !important;
        font-size: 1.25rem !important;
        font-weight: 900 !important;
        letter-spacing: 0.4px !important;
        white-space: nowrap !important;
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.12) !important;
        transition: all 0.2s ease !important;
    }

    .menu-button-wrapper div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 30px rgba(15, 23, 42, 0.16) !important;
    }

    .login-btn div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #86efac, #22c55e) !important;
        color: white !important;
    }

    .register-btn div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #fde68a, #fbbf24) !important;
        color: white !important;
    }

    div[data-testid="stButton"] > button {
        border-radius: 999px;
        border: none;
        min-height: 58px;
        font-size: 1rem;
        font-weight: 800;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.10);
        transition: all 0.2s ease;
    }

    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
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

    .personaje-info {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 22px;
        padding: 1rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    .personaje-info h3 {
        color: #16a34a;
        margin-bottom: 0.4rem;
    }

    .personaje-info p {
        color: #64748b;
        margin-bottom: 0;
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

        .menu-button-wrapper div[data-testid="stButton"] > button {
            width: 95% !important;
            font-size: 1rem !important;
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
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="menu-button-wrapper login-btn">', unsafe_allow_html=True)

        if st.button("👤 INICIAR SESIÓN", key="btn_ir_login"):
            st.session_state.pantalla = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="menu-button-wrapper register-btn">', unsafe_allow_html=True)

        if st.button("😊 REGISTRARSE", key="btn_ir_registro"):
            st.session_state.pantalla = "registro"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="cute-note">
                ✨ ¡Pequeños pasos, grandes cambios! ✨
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
            </div>
            """,
            unsafe_allow_html=True
        )

        nombre = st.text_input(
            "Tu nombre",
            placeholder="Ejemplo: Camila",
            key="nombre_registro"
        )

        personaje_seleccionado = st.selectbox(
            "Selecciona tu personaje",
            list(PERSONAJES.keys()),
            key="personaje_registro"
        )

        datos_personaje = PERSONAJES[personaje_seleccionado]
        nombre_personaje = datos_personaje["nombre"]
        video_personaje = datos_personaje["video"]
        descripcion_personaje = datos_personaje["descripcion"]

        st.markdown(
            f"""
            <div class="personaje-info">
                <h3>{personaje_seleccionado}</h3>
                <p>{descripcion_personaje}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

        if st.button("✨ Crear mi cuenta", key="btn_crear_cuenta"):
            exito, mensaje = registrar_usuario(
                nombre=nombre,
                personaje=nombre_personaje,
                video_personaje=video_personaje
            )

            if exito:
                st.success(mensaje)
                st.session_state.usuario_actual = obtener_usuario(nombre.strip())
                st.session_state.pantalla = "bienvenida"
                st.rerun()
            else:
                st.error(mensaje)

        st.markdown('<div style="height: 0.8rem;"></div>', unsafe_allow_html=True)

        if st.button("⬅️ Volver al menú", key="btn_volver_menu_registro"):
            st.session_state.pantalla = "menu"
            st.rerun()

    with col_video:
        datos_personaje = PERSONAJES[st.session_state.personaje_registro]
        video_actual = datos_personaje["video"]

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
                <source src="{video_actual}" type="video/mp4">
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
            </div>
            """,
            unsafe_allow_html=True
        )

        if usuarios.empty:
            st.info("Todavía no hay usuarios registrados. Primero debes registrarte.")
        else:
            usuario_nombre = st.selectbox(
                "¿Quién está ingresando?",
                usuarios["nombre"].tolist(),
                key="usuario_login"
            )

            if st.button("Entrar a LifeQuest", key="btn_entrar_lifequest"):
                st.session_state.usuario_actual = obtener_usuario(usuario_nombre)
                st.session_state.pantalla = "bienvenida"
                st.rerun()

        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

        if st.button("⬅️ Volver", key="btn_volver_menu_login"):
            st.session_state.pantalla = "menu"
            st.rerun()


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

    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("Cerrar sesión", key="btn_cerrar_sesion"):
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

else:
    st.session_state.pantalla = "menu"
    st.rerun()
