import streamlit as st
import pandas as pd
from pathlib import Path
from urllib.parse import quote
import streamlit.components.v1 as components


# ============================================================
# 1. CONFIGURACIÓN GENERAL DE LA APLICACIÓN
# ============================================================

st.set_page_config(
    page_title="LifeQuest",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. CONSTANTES DEL PROYECTO
# ============================================================

APP_NOMBRE = "LifeQuest"
APP_SUBTITULO = "Tu juego de hábitos saludables 💗"
APP_FRASE = "✨ ¡Pequeños pasos, grandes cambios! ✨"

ARCHIVO_USUARIOS = Path("usuarios_lifequest.csv")

COLUMNAS_USUARIOS = [
    "nombre",
    "personaje",
    "video_personaje",
    "nivel",
    "xp_total",
    "racha"
]

IMAGEN_PORTADA = (
    "https://raw.githubusercontent.com/"
    "juandavdidtejedormedina-rgb/app-streamlite/"
    "cbeea9b924f7db779843abdef9922e7fcf3c649d/"
    "Imagen%20portada.png"
)

PERSONAJES = {
    "🦉 Búho aventurero": {
        "nombre": "Búho aventurero",
        "video": (
            "https://raw.githubusercontent.com/"
            "juandavdidtejedormedina-rgb/Marley/"
            "b82a6ebeb66d35db9a7caee17718dda8441ed88f/"
            "personaje%202.mp4"
        ),
        "descripcion": "Un compañero sabio, constante y motivador para iniciar tu aventura saludable."
    },
    "🐰 Conejito atleta": {
        "nombre": "Conejito atleta",
        "video": (
            "https://raw.githubusercontent.com/"
            "juandavdidtejedormedina-rgb/Marley/"
            "b82a6ebeb66d35db9a7caee17718dda8441ed88f/"
            "personaje%203.mp4"
        ),
        "descripcion": "Ideal para quienes quieren moverse más, ganar energía y cumplir misiones activas."
    },
    "🦊 Zorrito estratega": {
        "nombre": "Zorrito estratega",
        "video": (
            "https://raw.githubusercontent.com/"
            "juandavdidtejedormedina-rgb/Marley/"
            "b82a6ebeb66d35db9a7caee17718dda8441ed88f/"
            "personaje%204.mp4"
        ),
        "descripcion": "Perfecto para organizar metas, planear hábitos y avanzar con inteligencia."
    },
    "🐼 Panda tranquilo": {
        "nombre": "Panda tranquilo",
        "video": (
            "https://raw.githubusercontent.com/"
            "juandavdidtejedormedina-rgb/Marley/"
            "b82a6ebeb66d35db9a7caee17718dda8441ed88f/"
            "personaje%205.mp4"
        ),
        "descripcion": "Un personaje calmado para trabajar descanso, equilibrio y autocuidado."
    }
}


# ============================================================
# 3. INICIALIZACIÓN DEL ESTADO DE SESIÓN
# ============================================================

def inicializar_estado():
    """
    Crea variables de sesión para controlar la navegación
    y el usuario activo dentro de la aplicación.
    """

    if "pantalla" not in st.session_state:
        st.session_state.pantalla = "menu"

    if "usuario_actual" not in st.session_state:
        st.session_state.usuario_actual = None


# ============================================================
# 4. FUNCIONES PARA MANEJO DE USUARIOS
# ============================================================

def crear_tabla_usuarios_vacia():
    """
    Crea una tabla vacía con las columnas necesarias
    para guardar los usuarios registrados.
    """

    return pd.DataFrame(columns=COLUMNAS_USUARIOS)


def normalizar_tabla_usuarios(df):
    """
    Ajusta la tabla de usuarios para que siempre tenga
    las columnas correctas.

    Esta función evita errores si el archivo CSV fue creado
    con una versión anterior del código.
    """

    if df.empty:
        return crear_tabla_usuarios_vacia()

    if "nombre" not in df.columns and "nombre_completo" in df.columns:
        df["nombre"] = df["nombre_completo"]

    if "personaje" not in df.columns:
        df["personaje"] = "Búho aventurero"

    if "video_personaje" not in df.columns:
        df["video_personaje"] = PERSONAJES["🦉 Búho aventurero"]["video"]

    if "nivel" not in df.columns:
        df["nivel"] = 1

    if "xp_total" not in df.columns:
        df["xp_total"] = 0

    if "racha" not in df.columns:
        df["racha"] = 0

    df = df[COLUMNAS_USUARIOS]

    df["nombre"] = df["nombre"].fillna("").astype(str)
    df["personaje"] = df["personaje"].fillna("Búho aventurero").astype(str)
    df["video_personaje"] = df["video_personaje"].fillna(
        PERSONAJES["🦉 Búho aventurero"]["video"]
    ).astype(str)

    df["nivel"] = pd.to_numeric(df["nivel"], errors="coerce").fillna(1).astype(int)
    df["xp_total"] = pd.to_numeric(df["xp_total"], errors="coerce").fillna(0).astype(int)
    df["racha"] = pd.to_numeric(df["racha"], errors="coerce").fillna(0).astype(int)

    df = df[df["nombre"].str.strip() != ""]

    return df


def cargar_usuarios():
    """
    Carga los usuarios guardados en usuarios_lifequest.csv.
    Si el archivo no existe, crea una tabla vacía.
    """

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
    """
    Guarda la tabla de usuarios en un archivo CSV local.
    """

    df.to_csv(ARCHIVO_USUARIOS, index=False)


def registrar_usuario(nombre, personaje, video_personaje):
    """
    Registra un usuario nuevo con su personaje seleccionado.
    """

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
    """
    Busca un usuario registrado por nombre.
    """

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
# 5. FUNCIONES DE NAVEGACIÓN
# ============================================================

def cambiar_pantalla(nombre_pantalla):
    """
    Cambia la pantalla actual de la aplicación.
    """

    st.session_state.pantalla = nombre_pantalla
    st.rerun()


def cerrar_sesion():
    """
    Limpia el usuario activo y vuelve al menú principal.
    """

    st.session_state.usuario_actual = None
    cambiar_pantalla("menu")


# ============================================================
# 6. ESTILOS CSS DE LA APLICACIÓN
# ============================================================

def aplicar_estilos():
    """
    Aplica los estilos CSS personalizados de la aplicación.
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

        .video-title-card {
            background: rgba(255,255,255,0.97);
            border-radius: 34px;
            padding: 2rem;
            box-shadow: 0 18px 45px rgba(91, 141, 239, 0.14);
            border: 1px solid #dcfce7;
            text-align: center;
            margin-bottom: 1rem;
        }

        .video-title-card h2 {
            color: #22c55e;
            font-size: 2rem;
            font-weight: 900;
            margin: 0;
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
# 7. COMPONENTES VISUALES REUTILIZABLES
# ============================================================

def mostrar_logo_lifequest():
    """
    Muestra la tarjeta principal de LifeQuest.
    """

    st.markdown(
        f"""
        <div class="login-card">
            <div class="logo-circle">🏁</div>
            <div class="life-title">
                <span class="life">Life</span><span class="quest">Quest</span>
            </div>
            <div class="subtitle">
                {APP_SUBTITULO}
            </div>
            <div class="soft-divider">— 🌱 —</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_imagen_portada():
    """
    Muestra la imagen decorativa principal del búho.
    """

    st.markdown(
        f"""
        <div class="portada-box">
            <img class="portada-img" src="{IMAGEN_PORTADA}">
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_boton_menu(texto, clave, pantalla_destino, clase_css):
    """
    Muestra un botón principal del menú.
    """

    st.markdown(f'<div class="menu-button-wrapper {clase_css}">', unsafe_allow_html=True)

    if st.button(texto, key=clave):
        cambiar_pantalla(pantalla_destino)

    st.markdown('</div>', unsafe_allow_html=True)


def mostrar_video_personaje(video_url, personaje_key):
    """
    Muestra el video del personaje seleccionado.

    Se usa components.html para forzar que el navegador
    actualice el video cuando cambia el personaje.
    """

    video_url_forzado = f"{video_url}?reload={quote(personaje_key)}"

    html_video = f"""
    <div style="
        background:white;
        border-radius:30px;
        padding:14px;
        border:1px solid #dcfce7;
        box-shadow:0 12px 30px rgba(34,197,94,0.10);
    ">
        <video 
            key="{quote(personaje_key)}"
            autoplay 
            loop 
            muted 
            playsinline 
            controls
            style="
                width:100%;
                height:430px;
                object-fit:cover;
                border-radius:24px;
                display:block;
            "
        >
            <source src="{video_url_forzado}" type="video/mp4">
        </video>
    </div>
    """

    components.html(html_video, height=470, scrolling=False)


def mostrar_tarjeta_titulo_registro():
    """
    Muestra la tarjeta superior de la pantalla de registro.
    """

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


def mostrar_tarjeta_titulo_video():
    """
    Muestra el título de la vista previa del personaje.
    """

    st.markdown(
        """
        <div class="video-title-card">
            <h2>Vista previa del personaje</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_info_personaje(personaje_key, descripcion):
    """
    Muestra nombre y descripción del personaje elegido.
    """

    st.markdown(
        f"""
        <div class="personaje-info">
            <h3>{personaje_key}</h3>
            <p>{descripcion}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 8. PANTALLAS DE LA APLICACIÓN
# ============================================================

def pantalla_menu():
    """
    Pantalla inicial con dos opciones:
    iniciar sesión o registrarse.
    """

    col_izquierda, col_derecha = st.columns([1, 1.15], vertical_alignment="center")

    with col_izquierda:
        mostrar_logo_lifequest()

        mostrar_boton_menu(
            texto="👤 INICIAR SESIÓN",
            clave="btn_ir_login",
            pantalla_destino="login",
            clase_css="login-btn"
        )

        mostrar_boton_menu(
            texto="😊 REGISTRARSE",
            clave="btn_ir_registro",
            pantalla_destino="registro",
            clase_css="register-btn"
        )

        st.markdown(
            f"""
            <div class="cute-note">
                {APP_FRASE}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_derecha:
        mostrar_imagen_portada()


def pantalla_registro():
    """
    Pantalla para registrar un usuario nuevo.
    Permite escribir el nombre y seleccionar un personaje.
    """

    col_formulario, col_video = st.columns([1, 1.1], vertical_alignment="center")

    with col_formulario:
        mostrar_tarjeta_titulo_registro()

        nombre = st.text_input(
            "Tu nombre",
            placeholder="Ejemplo: Camila",
            key="nombre_registro"
        )

        personaje_seleccionado = st.selectbox(
            "Selecciona tu personaje",
            options=list(PERSONAJES.keys()),
            key="selector_personaje"
        )

        datos_personaje = PERSONAJES[personaje_seleccionado]
        nombre_personaje = datos_personaje["nombre"]
        video_personaje = datos_personaje["video"]
        descripcion_personaje = datos_personaje["descripcion"]

        mostrar_info_personaje(
            personaje_key=personaje_seleccionado,
            descripcion=descripcion_personaje
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
                cambiar_pantalla("bienvenida")
            else:
                st.error(mensaje)

        st.markdown('<div style="height: 0.8rem;"></div>', unsafe_allow_html=True)

        if st.button("⬅️ Volver al menú", key="btn_volver_menu_registro"):
            cambiar_pantalla("menu")

    with col_video:
        mostrar_tarjeta_titulo_video()

        mostrar_video_personaje(
            video_url=video_personaje,
            personaje_key=personaje_seleccionado
        )


def pantalla_login():
    """
    Pantalla para iniciar sesión con un usuario registrado.
    """

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
                cambiar_pantalla("bienvenida")

        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

        if st.button("⬅️ Volver", key="btn_volver_menu_login"):
            cambiar_pantalla("menu")


def pantalla_bienvenida():
    """
    Pantalla temporal que aparece después de iniciar sesión
    o registrarse correctamente.
    """

    usuario = st.session_state.usuario_actual

    if usuario is None:
        cambiar_pantalla("menu")

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
            cerrar_sesion()


# ============================================================
# 9. CONTROL PRINCIPAL DE LA APLICACIÓN
# ============================================================

def ejecutar_app():
    """
    Función principal que ejecuta toda la aplicación.
    """

    inicializar_estado()
    aplicar_estilos()

    pantalla_actual = st.session_state.pantalla

    if pantalla_actual == "menu":
        pantalla_menu()

    elif pantalla_actual == "registro":
        pantalla_registro()

    elif pantalla_actual == "login":
        pantalla_login()

    elif pantalla_actual == "bienvenida":
        pantalla_bienvenida()

    else:
        cambiar_pantalla("menu")


# ============================================================
# 10. EJECUCIÓN DEL PROGRAMA
# ============================================================

ejecutar_app()
