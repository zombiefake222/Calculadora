import tkinter as tk
import sqlite3

# Conectar a la base de datos (o crearla si no existe)
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

# Función para guardar una operación en el historial
def guardar_historial(operacion, resultado):
    cursor.execute("INSERT INTO historial (operacion, resultado) VALUES (?, ?)", (operacion, resultado))
    conexion.commit()

# Función para mostrar el historial
def mostrar_historial():
    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("Historial")
    ventana_historial.geometry("300x400")

    # Crear un widget Text para mostrar el historial
    texto_historial = tk.Text(ventana_historial, font=("Arial", 12))
    texto_historial.pack(expand=True, fill="both")

    # Obtener los datos del historial
    cursor.execute("SELECT operacion, resultado FROM historial")
    registros = cursor.fetchall()

    # Mostrar los registros en el widget Text
    for operacion, resultado in registros:
        texto_historial.insert(tk.END, f"{operacion} = {resultado}\n")

# Función para actualizar la expresión en la pantalla
def click_boton(valor):
    current = pantalla.get()
    pantalla.delete(0, tk.END)
    pantalla.insert(0, current + valor)

# Función para evaluar la expresión
def calcular():
    try:
        operacion = pantalla.get()
        resultado = eval(operacion)
        pantalla.delete(0, tk.END)
        pantalla.insert(0, str(resultado))
        guardar_historial(operacion, str(resultado))  # Guardar en el historial
    except Exception as e:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "Error")

# Función para limpiar la pantalla
def limpiar():
    pantalla.delete(0, tk.END)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("300x400")
ventana.resizable(0, 0)  # Evita que la ventana sea redimensionable

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

# Crear y colocar los botones en la ventana
for (texto, fila, columna) in botones:
    if texto == '=':
        boton = tk.Button(ventana, text=texto, font=("Arial", 16), bg="lightblue", fg="black",
                          command=calcular)
        boton.grid(row=fila, column=columna, columnspan=2, sticky="nsew", padx=5, pady=5)
    elif texto == 'C':
        boton = tk.Button(ventana, text=texto, font=("Arial", 16), bg="lightcoral", fg="black",
                          command=limpiar)
        boton.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)
    elif texto == 'Historial':
        boton = tk.Button(ventana, text=texto, font=("Arial", 16), bg="lightgreen", fg="black",
                          command=mostrar_historial)
        boton.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)
    else:
        boton = tk.Button(ventana, text=texto, font=("Arial", 16), bg="lightgray", fg="black",
                          command=lambda valor=texto: click_boton(valor))
        boton.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)

# Ajustar el tamaño de las filas y columnas
for i in range(6):
    ventana.grid_rowconfigure(i, weight=1)
for j in range(4):
    ventana.grid_columnconfigure(j, weight=1)

# Iniciar la aplicación
ventana.mainloop()

# Cerrar la conexión a la base de datos al salir
conexion.close()