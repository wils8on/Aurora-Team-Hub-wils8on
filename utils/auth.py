import streamlit as st


def esta_logado():

    try:
        return st.user.is_logged_in
    except Exception:
        return False


def obter_email_usuario():

    if not esta_logado():
        return None

    return st.user.get("email")


def obter_nome_usuario():

    if not esta_logado():
        return "Usuário"

    return st.user.get(
        "name",
        "Usuário"
    )


def usuario_autorizado():

    email = obter_email_usuario()

    emails_permitidos = st.secrets.get(
        "permissions",
        {}
    ).get(
        "allowed_emails",
        []
    )

    if not emails_permitidos:
        return True

    return email in emails_permitidos


def tela_login():

    st.markdown(
        """
        <div style="text-align:center; padding-top:80px;">
            <h1>🌅 Aurora Team Hub</h1>
            <h3>Centro inteligente de liderança e gestão de equipes</h3>
            <p style="color:#94a3b8;">
                Faça login com sua conta Google para acessar o sistema.
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
        if st.button(
            "Entrar com Google",
            use_container_width=True
        ):
            st.login("google")


def exigir_login():

    if not esta_logado():

        tela_login()
        st.stop()

    if not usuario_autorizado():

        st.error(
            "Seu e-mail não possui permissão para acessar este sistema."
        )

        st.caption(
            f"E-mail autenticado: {obter_email_usuario()}"
        )

        if st.button(
            "Sair",
            use_container_width=True
        ):
            st.logout()

        st.stop()


def mostrar_usuario_sidebar():

    if esta_logado():

        nome = obter_nome_usuario()
        email = obter_email_usuario()

        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**{nome}**")
        st.sidebar.caption(email)

        if st.sidebar.button("Sair"):
            st.logout()