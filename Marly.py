import streamlit as st

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="LifeQuest RPG",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# RUTA DEL VIDEO
# ============================================================

VIDEO_FEMENINO = "https://raw.githubusercontent.com/juandavdidtejedormedina-rgb/Marley/a921aa0a327ee38b440e666107c626c527e3b302/Personaje%201.mp4"

# Por ahora dejamos el masculino vacío hasta que subas el segundo video
VIDEO_MASCULINO = None


# ============================================================
# ESTADO DE SESIÓN
# ============================================================

if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

if "genero" not in st.session_state:
    st.session_state.genero = None


# ============================================================
# ESTILOS CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #050505;
        color: white;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 100%;
    }

    .main-layout {
        display: grid;
        grid-template-columns: 28% 72%;
        min-height: 88vh;
        background: radial-gradient(circle at 75% 45%, rgba(80,80,80,0.25), transparent 35%),
                    linear-gradient(90deg, #000000 0%, #050505 40%, #111111 100%);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .left-menu {
        padding: 3rem 2rem;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .game-title {
        font-size: 2.7rem;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
        color: #ffffff;
        text-transform: uppercase;
    }

    .game-subtitle {
        color: #b8a76a;
        font-size: 0.95rem;
        margin-bottom: 4rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .menu-button {
        display: block;
        width: 100%;
        background: transparent;
        border: none;
        color: #d4c17a;
        text-align: left;
        font-size: 0.95rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 0.75rem 0;
        cursor: pointer;
    }

    .menu-option {
        color: #d4c17a;
        font-size: 0.95rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 0.7rem 0;
        margin-bottom: 0.2rem;
    }

    .menu-option-active {
        color: #ffffff;
        font-size: 1rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 0.7rem 0;
        margin-bottom: 0.2rem;
        border-left: 3px solid #d4c17a;
        padding-left: 0.8rem;
    }

    .right-panel {
        position: relative;
        padding: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .character-box {
        width: 100%;
        height: 78vh;
        border-radius: 14px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.08);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .creation-card {
        background: rgba(10,10,10,0.88);
        border: 1px solid rgba(212,193,122,0.25);
        border-radius: 18px;
        padding: 2rem;
        width: 70%;
        box-shadow: 0 0 35px rgba(0,0,0,0.6);
    }

    .creation-title {
        font-size: 2rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        color: white;
    }

    .creation-text {
        color: #b8b8b8;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    .gender-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        transition: 0.3s;
    }

    .gender-card:hover {
        border-color: #d4c17a;
        background: rgba(212,193,122,0.08);
    }

    .gender-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .gender-title {
        color: white;
        font-size: 1.2rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    .gender-description {
        color: #a8a8a8;
        font-size: 0.9rem;
    }

    .video-title {
        position: absolute;
        top: 3rem;
        left: 3rem;
        z-index: 5;
        color: white;
    }

    .video-title h2 {
        font-size: 2rem;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }

    .video-title p {
        color: #d4c17a;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 0.9rem;
    }

    div[data-testid="stButton"] > button {
        background: transparent;
        border: 1px solid rgba(212,193,122,0.65);
        color: #d4c17a;
        border-radius: 0px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        padding: 0.7rem 1rem;
        width: 100%;
        transition: all 0.3s ease;
    }

    div[data-testid="stButton"] > button:hover {
        background: rgba(212,193,122,0.12);
        border-color: #d4c17a;
        color: white;
    }

    .stVideo {
        width: 100%;
    }

    video {
        width: 100% !important;
        height: 78vh !important;
        object-fit: cover !important;
        border-radius: 14px;
    }

    .small-note {
        color: #777;
        font-size: 0.85rem;
        margin-top: 1.5rem;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES DE NAVEGACIÓN
# ============================================================

def ir_inicio():
    st.session_state.pantalla = "inicio"
    st.session_state.genero = None


def ir_crear_personaje():
    st.session_state.pantalla = "crear_personaje"
    st.session_state.genero = None


def seleccionar_femenino():
    st.session_state.pantalla = "vista_personaje"
    st.session_state.genero = "femenino"


def seleccionar_masculino():
    st.session_state.pantalla = "vista_personaje"
    st.session_state.genero = "masculino"


# ============================================================
# MENÚ IZQUIERDO
# ============================================================

def menu_izquierdo():
    st.markdown(
        """
        <div class="left-menu">
            <div>
                <div class="game-title">LifeQuest ⚔️</div>
                <div class="game-subtitle">RPG Habit Creation Kit</div>
            </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.pantalla == "inicio":
        st.markdown('<div class="menu-option-active">Inicio</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="menu-option">Inicio</div>', unsafe_allow_html=True)

    if st.button("Ir al inicio"):
        ir_inicio()
        st.rerun()

    if st.session_state.pantalla in ["crear_personaje", "vista_personaje"]:
        st.markdown('<div class="menu-option-active">Crear personaje</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="menu-option">Crear personaje</div>', unsafe_allow_html=True)

    if st.button("Crear personaje"):
        ir_crear_personaje()
        st.rerun()

    st.markdown('<div class="menu-option">Misiones</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-option">Progreso</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-option">Reportes</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-option">Salir</div>', unsafe_allow_html=True)

    st.markdown(
        """
            <div class="small-note">
                Selecciona crear personaje para iniciar tu aventura.
                Luego podrás registrar hábitos, ganar XP y subir de nivel.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PANTALLA INICIAL
# ============================================================

def pantalla_inicio():
    st.markdown(
        """
        <div class="right-panel">
            <div class="creation-card">
                <div class="creation-title">Bienvenida a LifeQuest</div>
                <div class="creation-text">
                    Crea tu personaje y convierte tus hábitos diarios en una aventura.
                    Completa misiones, gana experiencia, desbloquea logros y sube de nivel.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Crear personaje ahora"):
            ir_crear_personaje()
            st.rerun()


# ============================================================
# PANTALLA CREAR PERSONAJE
# ============================================================

def pantalla_crear_personaje():
    st.markdown(
        """
        <div class="right-panel">
            <div class="creation-card">
                <div class="creation-title">Crear personaje</div>
                <div class="creation-text">
                    Elige el tipo de personaje que quieres usar en tu aventura.
                    Cada personaje tendrá su propia animación, estilo visual y experiencia.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_fem, col_masc = st.columns(2)

    with col_fem:
        st.markdown(
            """
            <div class="gender-card">
                <div class="gender-icon">🧝‍♀️</div>
                <div class="gender-title">Femenino</div>
                <div class="gender-description">
                    Personaje femenino estilo RPG.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Seleccionar femenino"):
            seleccionar_femenino()
            st.rerun()

    with col_masc:
        st.markdown(
            """
            <div class="gender-card">
                <div class="gender-icon">🧙‍♂️</div>
                <div class="gender-title">Masculino</div>
                <div class="gender-description">
                    Personaje masculino estilo RPG.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Seleccionar masculino"):
            seleccionar_masculino()
            st.rerun()


# ============================================================
# PANTALLA VIDEO PERSONAJE
# ============================================================

def pantalla_video_personaje():
    genero = st.session_state.genero

    if genero == "femenino":
        titulo = "Personaje femenino"
        subtitulo = "Guerrera de hábitos"
        video = VIDEO_FEMENINO

    elif genero == "masculino":
        titulo = "Personaje masculino"
        subtitulo = "Próximamente"
        video = VIDEO_MASCULINO

    else:
        ir_crear_personaje()
        st.rerun()

    st.markdown(
        f"""
        <div class="video-title">
            <h2>{titulo}</h2>
            <p>{subtitulo}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if video:
        st.video(video)

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if st.button("Confirmar personaje"):
                st.success("Personaje confirmado. Luego conectamos esta selección con el usuario registrado.")

        with col2:
            if st.button("Cambiar personaje"):
                ir_crear_personaje()
                st.rerun()

    else:
        st.markdown(
            """
            <div class="creation-card">
                <div class="creation-title">Video no disponible</div>
                <div class="creation-text">
                    Todavía no has subido el video del personaje masculino.
                    Cuando lo subas al repositorio, reemplazamos la ruta en VIDEO_MASCULINO.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Volver a elegir"):
            ir_crear_personaje()
            st.rerun()


# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

st.markdown('<div class="main-layout">', unsafe_allow_html=True)

col_menu, col_contenido = st.columns([1.1, 2.9])

with col_menu:
    menu_izquierdo()

with col_contenido:
    if st.session_state.pantalla == "inicio":
        pantalla_inicio()

    elif st.session_state.pantalla == "crear_personaje":
        pantalla_crear_personaje()

    elif st.session_state.pantalla == "vista_personaje":
        pantalla_video_personaje()

st.markdown('</div>', unsafe_allow_html=True)
