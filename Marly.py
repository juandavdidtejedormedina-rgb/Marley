import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard RPG de Bienestar", page_icon="⚔️", layout="wide")

# -----------------------------
# Datos base (puedes reemplazarlos por DB/API)
# -----------------------------
user = {
    "nombre": "Guerrero del Bienestar",
    "clase": "Explorador de Hábitos",
    "xp_total": 2880,
    "xp_nivel_actual": 2880,
    "xp_siguiente_nivel": 4000,
    "nivel": 14,
    "racha_global": 12,
}

habitos_hoy = [
    {"habito": "Dormir 6h", "xp": 80, "completado": True, "icono": "😴"},
    {"habito": "Ejercicio 30 min", "xp": 120, "completado": True, "icono": "🏋️"},
    {"habito": "2L de agua", "xp": 60, "completado": True, "icono": "💧"},
    {"habito": "Lectura 20 min", "xp": 70, "completado": True, "icono": "📚"},
    {"habito": "Alimentación sana", "xp": 90, "completado": True, "icono": "🥗"},
    {"habito": "Tareas completadas", "xp": 100, "completado": False, "icono": "✅"},
]

insignias = [
    "💧 Hidratado",
    "🏃 Atleta",
    "📚 Sabio",
    "😴 Dormilón",
    "🔥 Racha 7d",
    "🥗 Nutritivo",
    "⚡ Racha 30d",
    "👑 Maestro",
]

ranking_habitos = pd.DataFrame(
    {
        "Hábito": ["Ejercicio", "Alimentación", "Lectura", "Agua", "Sueño"],
        "XP": [920, 780, 650, 550, 480],
    }
).sort_values("XP", ascending=True)

rachas_activas = [
    {"h": "Ejercicio", "dias": 12, "mejor": 21},
    {"h": "Agua", "dias": 9, "mejor": 14},
    {"h": "Lectura", "dias": 7, "mejor": 7},
    {"h": "Sueño", "dias": 5, "mejor": 18},
]

actividad_semana = pd.DataFrame(
    {
        "Día": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Hoy"],
        "Puntos": [6, 6, 4, 1, 6, 5, 5],
    }
)

# -----------------------------
# Estilos
# -----------------------------
st.markdown(
    """
    <style>
    .card {
        background: #f7f7f7;
        border: 1px solid #e4e4e4;
        border-radius: 14px;
        padding: 1rem;
        height: 100%;
    }
    .title-lg { font-size: 1.35rem; font-weight: 800; }
    .muted { color: #666; font-size: 0.95rem; }
    .kpi { text-align: center; }
    .kpi h2 { margin-bottom: 0; color: #5c4bd8; }
    .badge {
        border: 1px solid #d8d8d8;
        border-radius: 12px;
        background: #fff;
        padding: .8rem;
        text-align:center;
        font-size: .95rem;
        min-height: 64px;
    }
    .habit-row {
        display:flex;
        justify-content:space-between;
        align-items:center;
        border-bottom: 1px solid #ececec;
        padding: .45rem 0;
        font-size: .98rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header perfil
# -----------------------------
progress = user["xp_nivel_actual"] / user["xp_siguiente_nivel"]
col_header = st.container()
with col_header:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 9])
    with c1:
        st.markdown("## ⚔️")
        st.caption(f"Nv.{user['nivel']}")
    with c2:
        st.markdown(f'<div class="title-lg">{user["nombre"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="muted">Clase: {user["clase"]} · Racha activa: {user["racha_global"]} días</div>',
            unsafe_allow_html=True,
        )
        st.progress(progress, text=f"{user['xp_nivel_actual']} XP  →  {user['xp_siguiente_nivel']} XP")
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# KPIs
# -----------------------------
completados = sum(1 for h in habitos_hoy if h["completado"])
total_habitos = len(habitos_hoy)

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(
        f'<div class="card kpi"><h2>{user["xp_total"]:,}</h2><div class="muted">XP total</div></div>'.replace(",", "."),
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f'<div class="card kpi"><h2>{completados}/{total_habitos}</h2><div class="muted">Hoy completo</div></div>',
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f'<div class="card kpi"><h2>🔥 {user["racha_global"]}</h2><div class="muted">Días de racha</div></div>',
        unsafe_allow_html=True,
    )

# -----------------------------
# Bloque central
# -----------------------------
left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("HÁBITOS DE HOY")
    for h in habitos_hoy:
        chk = "✅" if h["completado"] else "⬜"
        st.markdown(
            f'<div class="habit-row"><span>{chk} {h["icono"]} {h["habito"]}</span><strong>+{h["xp"]} XP</strong></div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("INSIGNIAS")
    cols = st.columns(4)
    for i, badge in enumerate(insignias):
        with cols[i % 4]:
            st.markdown(f'<div class="badge">{badge}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Ranking + rachas
# -----------------------------
r1, r2 = st.columns([1, 1])

with r1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("RANKING DE HÁBITOS")
    st.bar_chart(ranking_habitos, x="Hábito", y="XP", horizontal=True, color="#5c4bd8")
    st.markdown("</div>", unsafe_allow_html=True)

with r2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("RACHAS ACTIVAS")
    for r in rachas_activas:
        st.markdown(
            f"🔥 **{r['h']}** — **{r['dias']} días**  \\nMejor: {r['mejor']}d"
        )
        st.divider()
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Actividad semanal
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("ACTIVIDAD DE LA SEMANA")
st.line_chart(actividad_semana, x="Día", y="Puntos", color="#5c4bd8")
st.markdown("</div>", unsafe_allow_html=True)

st.caption("Tip: reemplaza estos datos mock por tus datos reales desde una base de datos o API.")
