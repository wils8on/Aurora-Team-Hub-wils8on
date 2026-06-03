import streamlit as st


def esta_logado():

    return st.session_state.get(
        "aurora_logado",
        False
    )


def obter_nome_usuario():

    return st.session_state.get(
        "aurora_usuario",
        "Usuário"
    )


def tela_login():

    st.markdown(
        """
        <div style="text-align:center; padding-top:80px;">
            <h1>🌅 Aurora Team Hub</h1>
            <h3>Centro inteligente de liderança e gestão de equipes</h3>
            <p style="color:#94a3b8;">
                Acesse com suas credenciais para continuar.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        [
            1,
            1,
            1
        ]
    )

    with col2:

        usuario = st.text_input(
            "Usuário"
        )

        senha = st.text_input(
            "Senha",
            type="password"
        )

        if st.button(
            "Entrar",
            use_container_width=True
        ):

            usuario_correto = st.secrets.get(
                "login",
                {}
            ).get(
                "usuario",
                ""
            )

            senha_correta = st.secrets.get(
                "login",
                {}
            ).get(
                "senha",
                ""
            )

            if (
                usuario == usuario_correto
                and senha == senha_correta
            ):

                st.session_state["aurora_logado"] = True
                st.session_state["aurora_usuario"] = usuario

                st.rerun()

            else:

                st.error(
                    "Usuário ou senha inválidos."
                )


def exigir_login():

    if not esta_logado():

        tela_login()
        st.stop()


def mostrar_usuario_sidebar():

    if esta_logado():

        nome = obter_nome_usuario()

        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Usuário:** {nome}")

        if st.sidebar.button("Sair"):

            st.session_state["aurora_logado"] = False
            st.session_state["aurora_usuario"] = None

            st.rerun()