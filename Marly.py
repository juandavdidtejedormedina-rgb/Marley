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

            with st.form("formulario_registro"):
                nombre_completo = st.text_input(
                    "Nombre completo",
                    placeholder="Ejemplo: Camila Tejedor"
                )

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
