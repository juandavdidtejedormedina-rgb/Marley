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
                "🦉 Búho sabio": {
                    "emoji": "🦉",
                    "descripcion": "Ideal para quienes quieren aprender y avanzar con calma."
                },
                "🐉 Dragón energético": {
                    "emoji": "🐉",
                    "descripcion": "Perfecto para personas activas y con mucha energía."
                },
                "🦊 Zorro estratégico": {
                    "emoji": "🦊",
                    "descripcion": "Para quienes planean sus hábitos con inteligencia."
                },
                "🐿️ Ardilla constante": {
                    "emoji": "🐿️",
                    "descripcion": "Representa disciplina, orden y pequeños avances diarios."
                },
                "🐼 Panda tranquilo": {
                    "emoji": "🐼",
                    "descripcion": "Para quienes quieren mejorar sus hábitos sin presión."
                },
                "🦋 Mariposa creativa": {
                    "emoji": "🦋",
                    "descripcion": "Ideal para quienes buscan cambios positivos y transformación."
                },
                "🧙‍♀️ Maga de hábitos": {
                    "emoji": "🧙‍♀️",
                    "descripcion": "Para quienes convierten sus rutinas en magia diaria."
                },
                "🦸‍♀️ Heroína saludable": {
                    "emoji": "🦸‍♀️",
                    "descripcion": "Para quienes quieren sentirse fuertes y motivadas."
                }
            }

            avatar_nombre = st.selectbox(
                "Elige tu avatar",
                options=list(avatares.keys()),
                key="avatar_seleccionado"
            )

            avatar_emoji = avatares[avatar_nombre]["emoji"]
            avatar_descripcion = avatares[avatar_nombre]["descripcion"]

            st.markdown(
                f"""
                <div class="avatar-card">
                    <h1 style="font-size: 4rem; margin-bottom: 0.5rem;">{avatar_emoji}</h1>
                    <h2>{avatar_nombre}</h2>
                    <p>{avatar_descripcion}</p>
                    <p><strong>Este será tu personaje dentro de LifeQuest.</strong></p>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.form("formulario_registro"):
                nombre_completo = st.text_input(
                    "Nombre completo",
                    placeholder="Ejemplo: Camila Tejedor"
                )

                registrar = st.form_submit_button("Crear mi personaje")

                if registrar:
                    if not nombre_completo.strip():
                        st.warning("Debes escribir tu nombre completo.")
                    else:
                        exito, mensaje = registrar_usuario(nombre_completo, avatar_emoji)

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
