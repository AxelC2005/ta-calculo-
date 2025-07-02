import tkinter as tk
from tkinter import simpledialog, messagebox
from sympy import parse_expr, integrate, pi, symbols
from total import (
    calcular_area,
    calcular_area_entre_funciones,
    mostrar_graficas_2d,
    mostrar_volumen_3d,
    mostrar_volumen_entre_funciones_3d
)

x = symbols('x')  # variable global

# --- Área bajo una curva ---
def opcion_area_bajo_curva():
    try:
        f_str = simpledialog.askstring("Función", "Ingresa la función f(x):")
        a = float(simpledialog.askstring("Límite inferior", "Ingresa a:"))
        b = float(simpledialog.askstring("Límite superior", "Ingresa b:"))
        f_expr = parse_expr(f_str)
        area = calcular_area(f_expr, a, b)
        messagebox.showinfo("Resultado", f"Área ≈ {float(area):.5f}")
        mostrar_graficas_2d(f_expr, a, b, mostrar_area=True)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# --- Área entre dos funciones ---
def opcion_area_entre_funciones():
    try:
        f_str = simpledialog.askstring("Función f(x)", "Ingresa la primera función f(x):")
        g_str = simpledialog.askstring("Función g(x)", "Ingresa la segunda función g(x):")
        a = float(simpledialog.askstring("Límite inferior", "Ingresa a:"))
        b = float(simpledialog.askstring("Límite superior", "Ingresa b:"))
        f_expr = parse_expr(f_str)
        g_expr = parse_expr(g_str)
        area = calcular_area_entre_funciones(f_expr, g_expr, a, b)
        messagebox.showinfo("Resultado", f"Área ≈ {float(area):.5f}")
        mostrar_graficas_2d(f_expr, a, b, mostrar_area=True, g_expr=g_expr)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# --- Volumen generado por una sola función ---
def opcion_volumen_una_funcion():
    try:
        f_str = simpledialog.askstring("Función", "Ingresa la función f(x) o f(y):")
        a = float(simpledialog.askstring("Límite inferior", "Ingresa a:"))
        b = float(simpledialog.askstring("Límite superior", "Ingresa b:"))
        eje = simpledialog.askstring("Eje de revolución", "¿Eje de revolución? (x o y):").strip().lower()
        f_expr = parse_expr(f_str)
        if eje == 'x':
            volumen = integrate(pi * f_expr**2, (x, a, b))
        elif eje == 'y':
            y = symbols('y')
            f_expr = parse_expr(f_str, local_dict={'y': y})
            volumen = integrate(pi * f_expr**2, (y, a, b))
        else:
            raise ValueError("Eje no válido. Usa 'x' o 'y'.")
        messagebox.showinfo("Resultado", f"Volumen ≈ {float(volumen):.5f}")
        mostrar_volumen_3d(f_expr, a, b, eje=eje)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# --- Volumen entre dos funciones ---
def opcion_volumen_entre_funciones():
    try:
        f_str = simpledialog.askstring("Función exterior", "Ingresa f(x):")
        g_str = simpledialog.askstring("Función interior", "Ingresa g(x):")
        a = float(simpledialog.askstring("Límite inferior", "Ingresa a:"))
        b = float(simpledialog.askstring("Límite superior", "Ingresa b:"))
        eje = simpledialog.askstring("Eje", "¿Eje de revolución? (x o y):").strip().lower()
        f_expr = parse_expr(f_str)
        g_expr = parse_expr(g_str)
        integrando = pi * (f_expr**2 - g_expr**2)
        volumen = integrate(integrando, (x, a, b))
        messagebox.showinfo("Resultado", f"Volumen ≈ {float(volumen):.5f}")
        mostrar_volumen_entre_funciones_3d(f_expr, g_expr, a, b, eje=eje)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# --- Menú principal ---
def crear_menu():
    ventana = tk.Tk()
    ventana.title("Cálculo de Integrales Definidas")
    ventana.geometry("400x420")
    ventana.config(bg="#f9f9f9")

    tk.Label(
        ventana,
        text="Selecciona una operación:",
        font=("Arial", 16, "bold"),
        bg="#f9f9f9"
    ).pack(pady=20)

    botones = [
        ("Área bajo una curva", opcion_area_bajo_curva),
        ("Área entre dos funciones", opcion_area_entre_funciones),
        ("Volumen (una función)", opcion_volumen_una_funcion),
        ("Volumen (entre dos funciones)", opcion_volumen_entre_funciones),
        ("Salir", ventana.destroy)
    ]

    for texto, comando in botones:
        tk.Button(
            ventana,
            text=texto,
            command=comando,
            width=35,
            height=2,
            bg="#007acc",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=8)

    ventana.mainloop()
