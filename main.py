import os
import streamlit as st
from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(url, key)

def delete_todo(todo_id):
    supabase.table("todos") \
        .delete() \
        .eq("id", todo_id) \
        .execute()

def add_todo(task, user_id):
    supabase.table("todos").insert({
        "task": task,
        "user_id": user_id
    }).execute()


st.title("🛒 Lista del Supermercado")

# LOGIN / REGISTRO

if "user" not in st.session_state:

    opcion = st.radio(
        "Selecciona una opción",
        ["Iniciar sesión", "Registrarse"]
    )

    email = st.text_input("Correo")
    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if opcion == "Registrarse":

        if st.button("Crear cuenta"):

            try:
                supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })

                st.success(
                    "Cuenta creada. Revisa tu correo y confirma la cuenta."
                )

            except Exception as e:
                st.error(str(e))

    else:

        if st.button("Entrar"):

            try:

                session = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                st.session_state.user = session.user

                st.rerun()

            except Exception:
                st.error("Correo o contraseña incorrectos")

    st.stop()

# USUARIO AUTENTICADO

user = st.session_state.user
user_id = user.id

st.success(f"Conectado como: {user.email}")

if st.button("Cerrar sesión"):
    del st.session_state.user
    st.rerun()

st.write("---")

# AGREGAR PRODUCTOS

task = st.text_input("Agregar que te falta:")

if st.button("Agregar"):

    if task:

        add_todo(task, user_id)

        st.success("Producto agregado")

        st.rerun()

# MOSTRAR SOLO LOS PRODUCTOS DE ESTE USUARIO

response = (
    supabase
    .table("todos")
    .select("*")
    .eq("user_id", user_id)
    .execute()
)

todos = response.data

st.write("### Lista de Compras")

if todos:

    for todo in todos:

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(todo["task"])

        with col2:
            if st.button("✅", key=f"delete_{todo['id']}"):
                delete_todo(todo["id"])
                st.rerun()

else:
    st.info("No hay productos.")

