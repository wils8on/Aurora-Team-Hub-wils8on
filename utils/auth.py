import streamlit as st


def esta_logado():

    return st.user.is_logged_in


def obter_email_usuario():

    if not st.user.is_logged_in:
        return None

    return st.user.get("email")


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


def exigir_login():

    if not esta_logado():

        st.warning(
            "Faça login com sua conta Google para acessar o Aurora Team Hub."
        )

        if st.button(
            "Entrar com Google",
            use_container_width=True
        ):
            st.login("google")

        st.stop()

    if not usuario_autorizado():

        st.error(
            "Seu e-mail não possui permissão para acessar este sistema."
        )

        if st.button(
            "Sair",
            use_container_width=True
        ):
            st.logout()

        st.stop()


def mostrar_usuario_sidebar():

    if st.user.is_logged_in:

        nome = st.user.get("name", "Usuário")
        email = st.user.get("email", "")

        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**{nome}**")
        st.sidebar.caption(email)

        if st.sidebar.button("Sair"):
            st.logout()