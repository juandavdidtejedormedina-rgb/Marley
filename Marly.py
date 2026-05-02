import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard RPG de Bienestar", page_icon="⚔️", layout="wide")

USERS_FILE = Path("users.json")
AVATARS = ["🧙", "⚔️", "🛡️", "🏹", "🐉", "🦊", "🦁", "🦄"]


def load_users() -> list[dict]:
    if not USERS_FILE.exists():
        return []
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_users(users: list[dict]) -> None:
    USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")


def get_user_by_name(full_name: str, users: list[dict]) -> dict | None:
    key = full_name.strip().lower()
    for user in users:
        if user["nombre"].strip().lower() == key:
            return user
    return None


def register_panel(users: list[dict]) -> None:
    st.markdown("### 🆕 Crear cuenta")
    with st.form("register_form", clear_on_submit=False):
        full_name = st.text_input("Nombre completo", placeholder="Ej: Ana López García")
        avatar = st.selectbox("Elige tu avatar", AVATARS, index=0)
        submit = st.form_submit_button("Crear cuenta", use_container_width=True)

    if submit:
        if len(full_name.strip()) < 4:
            st.error("Tu nombre debe tener al menos 4 caracteres.")
            return

        if get_user_by_name(full_name, users):
            st.warning("Ya existe una cuenta con ese nombre. Inicia sesión.")
            return

        new_user = {
            "nombre": full_name.strip(),
            "avatar": avatar,
            "clase": "Explorador de Hábitos",
            "xp_total": 0,
            "xp_nivel_actual": 0,
            "xp_siguiente_nivel": 4000,
            "nivel": 1,
            "racha_global": 0,
        }
        users.append(new_user)
        save_users(users)
        st.session_state["user"] = new_user
        st.success("Cuenta creada con éxito. ¡Bienvenido/a!")
        st.rerun()


def login_panel(users: list[dict]) -> None:
    st.markdown("### 🔐 Iniciar sesión")
    with st.form("login_form", clear_on_submit=False):
        names = [u["nombre"] for u in users]
        selected_name = st.selectbox("Selecciona tu cuenta", names if names else ["Sin cuentas registradas"])
        submit = st.form_submit_button("Entrar", use_container_width=True)

    if submit:
        if not users:
            st.error("No hay cuentas registradas. Crea una primero.")
            return
        user = get_user_by_name(selected_name, users)
        if user:
            st.session_state["user"] = user
            st.success(f"Bienvenido/a, {user['nombre']}.")
            st.rerun()


def render_auth() -> None:
    users = load_users()
    st.markdown(
        """
        <style>
          .auth-wrap {
            max-width: 900px;
            margin: 0 auto;
            padding: 1.5rem;
            background: linear-gradient(135deg, #f6f3ff 0%, #ffffff 45%, #eef8ff 100%);
            border: 1px solid #e9e9e9;
            border-radius: 20px;
          }
          .hero-title {font-size: 2rem; font-weight: 800; color:#3d2fa8;}
          .hero-sub {color:#5f5f5f; margin-bottom: 1rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">🎮 Bienvenido al Dashboard RPG de Bienestar</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">¿Ya tienes cuenta o deseas crear una nueva? Elige una opción para continuar.</div>',
        unsafe_allow_html=True,
    )

    t1, t2 = st.tabs(["Ya tengo cuenta", "Deseo crear cuenta"])
    with t1:
        login_panel(users)
    with t2:
        register_panel(users)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Dashboard data mock
# -----------------------------
habitos_hoy = [
    {"habito": "Dormir 6h", "xp": 80, "completado": True, "icono": "😴"},
    {"habito": "Ejercicio 30 min", "xp": 120, "completado": True, "icono": "🏋️"},
    {"habito": "2L de agua", "xp": 60, "completado": True, "icono": "💧"},
    {"habito": "Lectura 20 min", "xp": 70, "completado": True, "icono": "📚"},
    {"habito": "Alimentación sana", "xp": 90, "completado": True, "icono": "🥗"},
    {"habito": "Tareas completadas", "xp": 100, "completado": False, "icono": "✅"},
]
insignias = ["💧 Hidratado", "🏃 Atleta", "📚 Sabio", "😴 Dormilón", "🔥 Racha 7d", "🥗 Nutritivo", "⚡ Racha 30d", "👑 Maestro"]
ranking_habitos = pd.DataFrame({"Hábito": ["Ejercicio", "Alimentación", "Lectura", "Agua", "Sueño"], "XP": [920, 780, 650, 550, 480]}).sort_values("XP", ascending=True)
rachas_activas = [{"h": "Ejercicio", "dias": 12, "mejor": 21}, {"h": "Agua", "dias": 9, "mejor": 14}, {"h": "Lectura", "dias": 7, "mejor": 7}, {"h": "Sueño", "dias": 5, "mejor": 18}]
actividad_semana = pd.DataFrame({"Día": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Hoy"], "Puntos": [6, 6, 4, 1, 6, 5, 5]})


def render_dashboard(user: dict) -> None:
    st.markdown(
        """
        <style>
        .card {background: #f7f7f7; border: 1px solid #e4e4e4; border-radius: 14px; padding: 1rem; height: 100%;}
        .title-lg { font-size: 1.35rem; font-weight: 800; }
        .muted { color: #666; font-size: 0.95rem; }
        .kpi { text-align: center; }
        .kpi h2 { margin-bottom: 0; color: #5c4bd8; }
        .badge {border: 1px solid #d8d8d8; border-radius: 12px; background: #fff; padding: .8rem; text-align:center; font-size: .95rem; min-height: 64px;}
        .habit-row {display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid #ececec; padding: .45rem 0; font-size: .98rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    top1, top2 = st.columns([9, 1])
    with top2:
        if st.button("Salir", use_container_width=True):
            st.session_state.pop("user", None)
            st.rerun()

    progress = user["xp_nivel_actual"] / max(user["xp_siguiente_nivel"], 1)
    with top1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 9])
        with c1:
            st.markdown(f"## {user['avatar']}")
            st.caption(f"Nv.{user['nivel']}")
        with c2:
            st.markdown(f'<div class="title-lg">{user["nombre"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="muted">Clase: {user["clase"]} · Racha activa: {user["racha_global"]} días</div>', unsafe_allow_html=True)
            st.progress(progress, text=f"{user['xp_nivel_actual']} XP  →  {user['xp_siguiente_nivel']} XP")
        st.markdown("</div>", unsafe_allow_html=True)

    completados = sum(1 for h in habitos_hoy if h["completado"])
    total_habitos = len(habitos_hoy)
    k1, k2, k3 = st.columns(3)
    k1.markdown(f'<div class="card kpi"><h2>{user["xp_total"]:,}</h2><div class="muted">XP total</div></div>'.replace(",", "."), unsafe_allow_html=True)
    k2.markdown(f'<div class="card kpi"><h2>{completados}/{total_habitos}</h2><div class="muted">Hoy completo</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="card kpi"><h2>🔥 {user["racha_global"]}</h2><div class="muted">Días de racha</div></div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("HÁBITOS DE HOY")
        for h in habitos_hoy:
            chk = "✅" if h["completado"] else "⬜"
            st.markdown(f'<div class="habit-row"><span>{chk} {h["icono"]} {h["habito"]}</span><strong>+{h["xp"]} XP</strong></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("INSIGNIAS")
        cols = st.columns(4)
        for i, badge in enumerate(insignias):
            cols[i % 4].markdown(f'<div class="badge">{badge}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("RANKING DE HÁBITOS")
        st.bar_chart(ranking_habitos, x="Hábito", y="XP", horizontal=True, color="#5c4bd8")
        st.markdown("</div>", unsafe_allow_html=True)
    with r2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("RACHAS ACTIVAS")
        for r in rachas_activas:
            st.markdown(f"🔥 **{r['h']}** — **{r['dias']} días**  \nMejor: {r['mejor']}d")
            st.divider()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("ACTIVIDAD DE LA SEMANA")
    st.line_chart(actividad_semana, x="Día", y="Puntos", color="#5c4bd8")
    st.markdown("</div>", unsafe_allow_html=True)


if "user" not in st.session_state:
    render_auth()
else:
    render_dashboard(st.session_state["user"])
