import os
import streamlit as st
from dotenv import load_dotenv
from supabase import Client, create_client
# Carga de variables de entorno
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SECRET_KEY")
# Conexión a la base de datos de Supabase
supabase: Client = create_client(url, key)
def get_todos():
    """Obtiene todos los registros de la tabla 'todos'."""
    response = supabase.table("todos").select("*").execute()
    return response.data

def add_todo(task):
    """Inserta una nueva tarea en la base de datos sin alterar
la clave 'task'."""
    supabase.table("todos").insert({"task": task}).execute()
# --- Interfaz de Usuario (GUI) en Español ---
st.title("Comprar en el super:")
# Campo de entrada para agregar tarea
task = st.text_input("Agregar que te falta:")
if st.button("Agregar"):
    if task:
        add_todo(task)
        st.success("¡Elemento agregada exitosamente!")
        st.rerun()  # Recarga la app para mostrar la nueva tarea inmediatamente
    else:
        st.warning("Por favor, ingresa una tarea antes de agregar.")
st.write("---")
st.write("### Lista de Compras:")
# Obtención y despliegue de tareas
todos = get_todos()
def delete_todo(todo_id):
	supabase.table("todos").delete().eq("id", todo_id).execute()

if todos:
	for todo in todos:
		col1, col2 = st.columns([4, 1])
		with col1:
			st.write(todo["task"])
		with col2:
			if st.button("✅", key=todo["id"]):
				delete_todo(todo["id"])
				st.rerun()
else:
	st.info("No hay compras pendientes.")
