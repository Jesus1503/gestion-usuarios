import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import Error
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer

# Crear un circuito de entrelazamiento (Estado de Bell)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Imprimir el circuito en texto dentro de la terminal
print(qc.draw('text'))

# ---------------------------------------------------------
# Conexión a PostgreSQL
# ---------------------------------------------------------
def conectar_db():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            port="5433",
            user="postgres",
            password="12345678",
            database="sistema_usuarios",
            client_encoding="utf-8"  # <--- Agrega esta línea
        )
        return conexion
    except Error as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a PostgreSQL:\n{e}")
        return None

# ---------------------------------------------------------
# Aplicación Principal (Tkinter)
# ---------------------------------------------------------
class AppUsuarios:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Usuarios - PostgreSQL")
        self.root.geometry("450x520")
        self.root.resizable(False, False)

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.mostrar_pantalla_registro()

    def limpiar_pantalla(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------
    # Pantalla 1: Registro
    # ---------------------------------------------------------
    def mostrar_pantalla_registro(self):
        self.limpiar_pantalla()

        tk.Label(self.container, text="Registro de Usuario", font=("Arial", 16, "bold")).pack(pady=15)

        form_frame = tk.Frame(self.container)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nombre completo:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nombre = tk.Entry(form_frame, width=30)
        self.entry_nombre.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Correo electrónico:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = tk.Entry(form_frame, width=30)
        self.entry_email.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Nombre de usuario:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_usuario = tk.Entry(form_frame, width=30)
        self.entry_usuario.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Contraseña:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_password = tk.Entry(form_frame, width=30, show="*")
        self.entry_password.grid(row=3, column=1, pady=5)

        tk.Button(self.container, text="Registrarse", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                  width=20, command=self.registrar_usuario).pack(pady=15)

        tk.Button(self.container, text="¿Ya tienes cuenta? Inicia Sesión", fg="blue", bd=0, 
                  cursor="hand2", command=self.mostrar_pantalla_login).pack(pady=5)
        
        tk.Button(self.container, text="Ver Usuarios Registrados", fg="gray", bd=0, 
                  cursor="hand2", command=self.mostrar_pantalla_lista).pack(pady=5)

    def registrar_usuario(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not nombre or not email or not usuario or not password:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        db = conectar_db()
        if db:
            try:
                cursor = db.cursor()
                sql = "INSERT INTO usuarios (nombre, email, usuario, password) VALUES (%s, %s, %s, %s)"
                valores = (nombre, email, usuario, password)
                cursor.execute(sql, valores)
                db.commit()
                
                messagebox.showinfo("Éxito", "¡Usuario registrado correctamente!")
                self.mostrar_pantalla_login()
            except Error as e:
                db.rollback()
                messagebox.showerror("Error", f"No se pudo registrar el usuario:\n{e}")
            finally:
                cursor.close()
                db.close()

    # ---------------------------------------------------------
    # Pantalla 2: Login
    # ---------------------------------------------------------
    def mostrar_pantalla_login(self):
        self.limpiar_pantalla()

        tk.Label(self.container, text="Iniciar Sesión", font=("Arial", 16, "bold")).pack(pady=20)

        form_frame = tk.Frame(self.container)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Usuario:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_login_usuario = tk.Entry(form_frame, width=30)
        self.entry_login_usuario.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Contraseña:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_login_password = tk.Entry(form_frame, width=30, show="*")
        self.entry_login_password.grid(row=1, column=1, pady=5)

        tk.Button(self.container, text="Ingresar", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), 
                  width=20, command=self.validar_login).pack(pady=15)

        tk.Button(self.container, text="¿No tienes cuenta? Regístrate aquí", fg="blue", bd=0, 
                  cursor="hand2", command=self.mostrar_pantalla_registro).pack(pady=5)
        
        
            

    def validar_login(self):
        usuario = self.entry_login_usuario.get().strip()
        password = self.entry_login_password.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Advertencia", "Ingresa usuario y contraseña.")
            return

        db = conectar_db()
        if db:
            try:
                cursor = db.cursor()
                sql = "SELECT nombre FROM usuarios WHERE usuario = %s AND password = %s"
                cursor.execute(sql, (usuario, password))
                resultado = cursor.fetchone()

                if resultado:
                    messagebox.showinfo("Bienvenido", f"¡Bienvenido de nuevo, {resultado[0]}!")
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            except Error as e:
                messagebox.showerror("Error", f"Error de consulta:\n{e}")
            finally:
                cursor.close()
                db.close()

    # ---------------------------------------------------------
    # Pantalla 3: Lista de Usuarios
    # ---------------------------------------------------------
    def mostrar_pantalla_lista(self):
        self.limpiar_pantalla()

        tk.Label(self.container, text="Lista de Usuarios", font=("Arial", 16, "bold")).pack(pady=10)

        columnas = ("ID", "Nombre", "Email", "Usuario")
        tabla = ttk.Treeview(self.container, columns=columnas, show="headings", height=10)

        tabla.heading("ID", text="ID")
        tabla.heading("Nombre", text="Nombre")
        tabla.heading("Email", text="Email")
        tabla.heading("Usuario", text="Usuario")

        tabla.column("ID", width=40)
        tabla.column("Nombre", width=120)
        tabla.column("Email", width=150)
        tabla.column("Usuario", width=90)

        tabla.pack(pady=10, fill="x", padx=10)

        db = conectar_db()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute("SELECT id, nombre, email, usuario FROM usuarios ORDER BY id ASC")
                filas = cursor.fetchall()
                for fila in filas:
                    tabla.insert("", tk.END, values=fila)
            except Error as e:
                messagebox.showerror("Error", f"Error al cargar usuarios:\n{e}")
            finally:
                cursor.close()
                db.close()

        tk.Button(self.container, text="Volver al Registro", command=self.mostrar_pantalla_registro).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppUsuarios(root)
    root.mainloop()