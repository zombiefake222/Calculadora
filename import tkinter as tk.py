import tkinter as tk
from tkinter import ttk
import sqlite3
import os

# Archivo donde se guarda la contraseña
ARCHIVO_CONTRASEÑA = "contraseña.txt"

# Verificar si el archivo de contraseña existe, si no, crear con la contraseña por defecto "1234"
if not os.path.exists(ARCHIVO_CONTRASEÑA):
    with open(ARCHIVO_CONTRASEÑA, "w") as f:
        f.write("1234")

# Función para obtener la contraseña almacenada
def obtener_contraseña():
    with open(ARCHIVO_CONTRASEÑA, "r") as f:
        return f.read().strip()

# Función para cambiar la contraseña
def cambiar_contraseña():
    def guardar_nueva_contraseña():
        nueva = entrada_nueva.get()
        if nueva:
            with open(ARCHIVO_CONTRASEÑA, "w") as f:
                f.write(nueva)
            ventana_nueva_contraseña.destroy()
    
    ventana_nueva_contraseña = tk.Toplevel(ventana_historial)
    ventana_nueva_contraseña.title("Cambiar Contraseña")
    ventana_nueva_contraseña.geometry("300x150")
    
    etiqueta = tk.Label(ventana_nueva_contraseña, text="Nueva contraseña:")
    etiqueta.pack(pady=10)
    
    entrada_nueva = tk.Entry(ventana_nueva_contraseña, show="*")
    entrada_nueva.pack(pady=5)
    
    boton_guardar = tk.Button(ventana_nueva_contraseña, text="Guardar", command=guardar_nueva_contraseña)
    boton_guardar.pack(pady=5)

# Conectar a la base de datos
conexion = sqlite3.connect("historial_calculadora.db")
cursor = conexion.cursor()

# Crear la tabla para el historial si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operacion TEXT NOT NULL,
    resultado TEXT NOT NULL
)
''')
conexion.commit()

# Función para guardar en el historial
def guardar_historial(operacion, resultado):
    cursor.execute("INSERT INTO historial (operacion, resultado) VALUES (?, ?)", (operacion, resultado))
    conexion.commit()

# Función para eliminar el historial
def borrar_historial():
    cursor.execute("DELETE FROM historial")
    conexion.commit()
    tree.delete(*tree.get_children())

# Función para mostrar el historial
def mostrar_historial():
    global ventana_historial, tree

    def verificar_contraseña():
        if entrada_contraseña.get() == obtener_contraseña():
            ventana_contraseña.destroy()
            abrir_historial()
        else:
            etiqueta_error.config(text="Contraseña incorrecta")

    def abrir_historial():
        global ventana_historial
        ventana_historial = tk.Toplevel(ventana)
        ventana_historial.title("Historial")
        ventana_historial.geometry("450x350")

        tree = ttk.Treeview(ventana_historial, columns=("Operación", "Resultado"), show="headings")
        tree.heading("Operación", text="Operación")
        tree.heading("Resultado", text="Resultado")
        tree.column("Operación", width=200)
        tree.column("Resultado", width=150)
        tree.pack(expand=True, fill="both")

        cursor.execute("SELECT operacion, resultado FROM historial")
        registros = cursor.fetchall()
        
        for operacion, resultado in registros:
            tree.insert("", "end", values=(operacion, resultado))

        # Botón para borrar historial
        boton_borrar_historial = tk.Button(ventana_historial, text="Borrar Historial", bg="red", fg="white", command=borrar_historial)
        boton_borrar_historial.pack(pady=5)

        # Botón para cambiar contraseña
        boton_cambiar_contraseña = tk.Button(ventana_historial, text="Cambiar Contraseña", bg="blue", fg="white", command=cambiar_contraseña)
        boton_cambiar_contraseña.pack(pady=5)

    ventana_contraseña = tk.Toplevel(ventana)
    ventana_contraseña.title("Ingresar contraseña")
    ventana_contraseña.geometry("300x150")
    
    etiqueta = tk.Label(ventana_contraseña, text="Ingrese la contraseña:")
    etiqueta.pack(pady=10)
    
    entrada_contraseña = tk.Entry(ventana_contraseña, show="*")
    entrada_contraseña.pack(pady=5)
    
    boton_verificar = tk.Button(ventana_contraseña, text="Aceptar", command=verificar_contraseña)
    boton_verificar.pack(pady=5)
    
    etiqueta_error = tk.Label(ventana_contraseña, text="", fg="red")
    etiqueta_error.pack()

# Funciones de la calculadora
def click_boton(valor):
    pantalla.insert(tk.END, valor)

def calcular(*args):
    try:
        operacion = pantalla.get()
        resultado = eval(operacion)
        pantalla.delete(0, tk.END)
        pantalla.insert(0, str(resultado))
        guardar_historial(operacion, str(resultado))
    except Exception:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "Error")

def limpiar(*args):
    pantalla.delete(0, tk.END)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("300x400")
ventana.resizable(0, 0)
ventana.bind("<Return>", calcular)
ventana.bind("<BackSpace>", lambda event: pantalla.delete(len(pantalla.get())-1, tk.END))

# Pantalla de la calculadora
pantalla = tk.Entry(ventana, font=("Arial", 20), justify="right", bd=10, relief=tk.RIDGE)
pantalla.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Botones de la calculadora
botones = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
    ('=', 5, 0), ('Historial', 5, 3)
]

for (texto, fila, columna) in botones:
    if texto == '=':
        boton = tk.Button(ventana, text=texto, font=("Arial", 16), bg="lightblue", fg="black", command=calcular)
        boton.grid(row=fila, column=columna, columnspan=2, sticky="nsew", padx=5, pady=5)
    elif texto == 'C':
        boton = tk.Button(ventana, text=texto, font=("Arial", 16), bg="lightcoral", fg="black", command=limpiar)
        boton.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)
    elif texto == 'Historial':
        boton = tk.Button(ventana, text=texto, font=("Arial", 16), bg="lightgreen", fg="black", command=mostrar_historial)
        boton.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)
    else:
        boton = tk.Button(ventana, text=texto, font=("Arial", 16), bg="lightgray", fg="black", command=lambda valor=texto: click_boton(valor))
        boton.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)

for i in range(6):
    ventana.grid_rowconfigure(i, weight=1)
for j in range(4):
    ventana.grid_columnconfigure(j, weight=1)

ventana.mainloop()
conexion.close()
