import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURACIÓN GENERAL DE LA APP
# ============================================================

st.set_page_config(
    page_title="LifeQuest",
    page_icon="🎮",
    layout="wide"
)

# ============================================================
# ARCHIVO DONDE SE GUARDAN LOS USUARIOS
# ============================================================

ARCHIVO_USUARIOS = Path("usuarios_lifequest.csv")


# ============================================================
# FUNCIONES PARA MANEJAR USUARIOS
# ============================================================

def cargar_usuarios():
    """
    Carga los usuarios registrados desde un archivo CSV.
    Si el archivo no existe, crea una tabla vacía.
    """
    if ARCHIVO_USUARIOS.exists():
        return pd.read_csv(ARCHIVO_USUARIOS)

    return pd.DataFrame(
        columns=[
            "nombre_completo",
            "avatar",
            "nivel",
            "xp_total",
            "xp_nivel_actual",
            "xp_siguiente_nivel",
            "racha_global"
        ]
    )


def guardar_usuarios(df):
    """
    Guarda la tabla de usuarios en un archivo CSV.
    """
    df.to_csv(ARCHIVO_USUARIOS, index=False)


def registrar_usuario(nombre_completo, avatar):
    """
    Registra un usuario nuevo si no existe.
    """
    usuarios = cargar_usuarios()

    nombre_limpio = nombre_completo.strip()

    usuario_existe = usuarios["nombre_completo"].str.lower().eq(
        nombre_limpio.lower()
    ).any()

    if usuario_existe:
        return False, "Este usuario ya está registrado."

    nuevo_usuario = pd.DataFrame(
        [
            {
                "nombre_completo": nombre_limpio,
                "avatar": avatar,
                "nivel": 1,
                "xp_total": 0,
                "xp_nivel_actual": 0,
                "xp_siguiente_nivel": 100,
                "racha_global": 0
            }
        ]
    )

    usuarios = pd.concat([usuarios, nuevo_usuario], ignore_index=True)
    guardar_usuarios(usuarios)

    return True, "Usuario registrado correctamente."


def obtener_usuario(nombre_completo):
    """
    Busca un usuario por nombre completo.
    """
    usuarios = cargar_usuarios()

    usuario = usuarios[
        usuarios["nombre_completo"].str.lower() == nombre_completo.lower()
    ]

    if usuario.empty:
        return None

    return usuario.iloc[0].to_dict()


# ============================================================
# ESTILOS VISUALES
# ============================================================

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f7fff7 0%, #eef5ff 100%);
    }

    .login-card {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border: 1px solid #edf0f7;
    }

    .title-lifequest {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0;
        color: #4c1d95;
    }

    .subtitle-lifequest {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-top: 0.3rem;
        margin-bottom: 2rem;
    }

    .avatar-card {
        background: #f8fafc;
        border-radius: 18px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        font-size: 1.1rem;
    }

    .welcome-box {
        background: linear-gradient(135deg, #22c55e, #84cc16);
        border-radius: 20px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }

    .small-muted {
        color: #64748b;
        font-size: 0.95rem;
        text-align: center;
    }

    div[data-testid="stButton"] > button {
        border-radius: 999px;
        font-weight: 700;
        border: none;
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        padding: 0.6rem 1.4rem;
    }

    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 999px;
        font-weight: 700;
        background: linear-gradient(135deg, #7c3aed, #4c1d95);
        color: white;
        border: none;
        padding: 0.6rem 1.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ESTADO DE SESIÓN
# ============================================================

if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = None

if "logueado" not in st.session_state:
    st.session_state.logueado = False


# ============================================================
# PANTALLA DE LOGIN / REGISTRO
# ============================================================

def pantalla_login():
    """
    Pantalla inicial para ingresar o registrarse.
    """

    st.markdown('<h1 class="title-lifequest">🎮 LifeQuest</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle-lifequest">Convierte tus hábitos diarios en misiones, XP, niveles y logros.</p>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="welcome-box">
                <h2>¿Quién eres?</h2>
                <p>Ingresa a tu aventura o crea un nuevo personaje.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        tab_ingresar, tab_registro = st.tabs(["🟢 Ingresar", "✨ Registrarse"])

        # ====================================================
        # TAB 1: INGRESAR
        # ====================================================

        with tab_ingresar:
            usuarios = cargar_usuarios()

            if usuarios.empty:
                st.info("Todavía no hay usuarios registrados. Crea tu personaje en la pestaña Registrarse.")
            else:
                lista_usuarios = usuarios["nombre_completo"].tolist()

                usuario_seleccionado = st.selectbox(
                    "Selecciona tu usuario",
                    lista_usuarios
                )

                datos_usuario = obtener_usuario(usuario_seleccionado)

                if datos_usuario:
                    st.markdown(
                        f"""
                        <div class="avatar-card">
                            <h1>{datos_usuario["avatar"]}</h1>
                            <h3>{datos_usuario["nombre_completo"]}</h3>
                            <p>Nivel {datos_usuario["nivel"]} · {datos_usuario["xp_total"]} XP · 🔥 {datos_usuario["racha_global"]} días de racha</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                if st.button("Entrar a mi aventura"):
                    st.session_state.usuario_actual = datos_usuario
                    st.session_state.logueado = True
                    st.rerun()

        # ====================================================
        # TAB 2: REGISTRARSE
        # ====================================================

        with tab_registro:
            st.markdown("### Crea tu personaje")

            avatares = {
                "🦉 Búho sabio": "🦉",
                "🐉 Dragón energético": "🐉",
                "🦊 Zorro estratégico": "🦊",
                "🐿️ Ardilla constante": "🐿️",
                "🐼 Panda tranquilo": "🐼",
                "🦋 Mariposa creativa": "🦋",
                "🧙‍♀️ Maga de hábitos": "🧙‍♀️",
                "🦸‍♀️ Heroína saludable": "🦸‍♀️"
            }

            with st.form("formulario_registro"):
                nombre_completo = st.text_input(
                    "Nombre completo",
                    placeholder="Ejemplo: Camila Tejedor"
                )

                avatar_nombre = st.selectbox(
                    "Elige tu avatar",
                    list(avatares.keys())
                )

                avatar = avatares[avatar_nombre]

                st.markdown(
                    f"""
                    <div class="avatar-card">
                        <h1>{avatar}</h1>
                        <h3>{avatar_nombre}</h3>
                        <p>Este será tu personaje dentro de LifeQuest.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                registrar = st.form_submit_button("Crear mi personaje")

                if registrar:
                    if not nombre_completo.strip():
                        st.warning("Debes escribir tu nombre completo.")
                    else:
                        exito, mensaje = registrar_usuario(nombre_completo, avatar)

                        if exito:
                            st.success(mensaje)
                            datos_usuario = obtener_usuario(nombre_completo)
                            st.session_state.usuario_actual = datos_usuario
                            st.session_state.logueado = True
                            st.rerun()
                        else:
                            st.error(mensaje)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <p class="small-muted">
        LifeQuest guarda los usuarios en un archivo local llamado usuarios_lifequest.csv.
        </p>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PANTALLA PRINCIPAL TEMPORAL
# ============================================================

def pantalla_inicio():
    """
    Pantalla inicial después de ingresar.
    Más adelante aquí conectamos el dashboard de misiones, XP y reportes.
    """

    usuario = st.session_state.usuario_actual

    st.sidebar.title("🎮 LifeQuest")
    st.sidebar.markdown(f"### {usuario['avatar']} {usuario['nombre_completo']}")
    st.sidebar.markdown(f"**Nivel:** {usuario['nivel']}")
    st.sidebar.markdown(f"**XP:** {usuario['xp_total']}")
    st.sidebar.markdown(f"**Racha:** 🔥 {usuario['racha_global']} días")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.usuario_actual = None
        st.session_state.logueado = False
        st.rerun()

    st.title(f"Bienvenida, {usuario['nombre_completo']} {usuario['avatar']}")

    st.markdown(
        """
        ## Tu aventura comienza aquí

        Ya ingresaste correctamente a LifeQuest.

        En el siguiente paso podemos crear el menú principal con:

        - Misiones diarias.
        - Captura de hábitos.
        - Cálculo de XP.
        - Barra de nivel.
        - Rachas.
        - Insignias.
        - Reportes visuales.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Nivel actual", usuario["nivel"])

    with col2:
        st.metric("XP acumulado", usuario["xp_total"])

    with col3:
        st.metric("Racha activa", f"{usuario['racha_global']} días")

    progreso = usuario["xp_nivel_actual"] / usuario["xp_siguiente_nivel"]

    st.progress(
        progreso,
        text=f"{usuario['xp_nivel_actual']} / {usuario['xp_siguiente_nivel']} XP para el siguiente nivel"
    )


# ============================================================
# CONTROL DE NAVEGACIÓN
# ============================================================

if st.session_state.logueado:
    pantalla_inicio()
else:
    pantalla_login()
