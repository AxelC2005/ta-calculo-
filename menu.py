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

x, y = symbols('x y')  # variables globales

# --- Área bajo una curva ---
def opcion_area_bajo_curva():
    try:
        f_str = simpledialog.askstring("Función", "Ingresa la función f(x):")
        a = float(simpledialog.askstring("Límite inferior", "Ingresa a:"))
        b = float(simpledialog.askstring("Límite superior", "Ingresa b:"))
        f_expr = parse_expr(f_str, local_dict={'x': x, 'y': y})
        area = calcular_area(f_expr, a, b)
        
        mensaje = f"Área bajo la curva en [{a}, {b}] ≈ {float(area):.5f}"
        mostrar_graficas_2d(f_expr, a, b, mostrar_area=True, mensaje_area=mensaje)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
# --- Área entre dos funciones ---
def opcion_area_entre_funciones():
    try:
        f_str = simpledialog.askstring("Función f(x)", "Ingresa la primera función f(x):")
        g_str = simpledialog.askstring("Función g(x)", "Ingresa la segunda función g(x):")
        a = float(simpledialog.askstring("Límite inferior", "Ingresa a:"))
        b = float(simpledialog.askstring("Límite superior", "Ingresa b:"))
        f_expr = parse_expr(f_str, local_dict={'x': x, 'y': y})
        g_expr = parse_expr(g_str, local_dict={'x': x, 'y': y})
        
        area = calcular_area_entre_funciones(f_expr, g_expr, a, b)
        mensaje = f"Área entre funciones ≈ {float(area):.5f}"
        
        mostrar_graficas_2d(f_expr, a, b, mostrar_area=True, g_expr=g_expr, mensaje_area=mensaje)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


# --- Volumen generado por una sola función ---
def opcion_volumen_una_funcion(): 
    try:
        f_str = simpledialog.askstring("Función", "Ingresa la función f(x) o f(y):")
        a = float(simpledialog.askstring("Límite inferior", "Ingresa a:"))
        b = float(simpledialog.askstring("Límite superior", "Ingresa b:"))
        eje = simpledialog.askstring("Eje de revolución", "¿Eje de revolución? (x o y):").strip().lower()
        f_expr = parse_expr(f_str, local_dict={'x': x, 'y': y})

        if eje == 'x':
            volumen = integrate(pi * f_expr**2, (x, a, b))
        elif eje == 'y':
            volumen = integrate(pi * f_expr**2, (y, a, b))
        else:
            raise ValueError("Eje no válido. Usa 'x' o 'y'.")

        mensaje = f"Volumen ≈ {float(volumen):.5f}"
        mostrar_volumen_3d(f_expr, a, b, eje=eje, mensaje_volumen1=mensaje)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


# --- Volumen entre dos funciones ---
def opcion_volumen_entre_funciones():
    try:
        f_str = simpledialog.askstring("Función exterior", "Ingresa f(x) o f(y):")
        g_str = simpledialog.askstring("Función interior", "Ingresa g(x) o g(y):")
        a = float(simpledialog.askstring("Límite inferior", "Ingresa a:"))
        b = float(simpledialog.askstring("Límite superior", "Ingresa b:"))
        eje = simpledialog.askstring("Eje", "¿Eje de revolución? (x o y):").strip().lower()

        f_expr = parse_expr(f_str, local_dict={'x': x, 'y': y})
        g_expr = parse_expr(g_str, local_dict={'x': x, 'y': y})

        if eje == 'x':
            integrando = pi * (f_expr**2 - g_expr**2)
            volumen = integrate(integrando, (x, a, b))
        elif eje == 'y':
            integrando = pi * (f_expr**2 - g_expr**2)
            volumen = integrate(integrando, (y, a, b))
        else:
            raise ValueError("Eje no válido. Usa 'x' o 'y'.")

        volumen = pi * integrate(f_expr**2 - g_expr**2, (x, a, b))
        mensajito = f"Volumen ≈ {float(volumen):.5f}"
        mostrar_volumen_entre_funciones_3d(f_expr, g_expr, a, b, eje=eje,mensaje_volumen=mensajito)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# --- Menú principal ---
def crear_menu():
    ventana = tk.Tk()
    ventana.title("Cálculo de Integrales Definidas")
    ventana.geometry("400x420")
    ventana.config(bg="#c8f8cb")

    tk.Label(
        ventana,
        text="Selecciona una operación:",
        font=("Arial", 16, "bold"),
        bg="#c8f8cb",
    ).pack(pady=20)

    botones = [
        ("Área bajo una curva", opcion_area_bajo_curva),
        ("Área entre dos funciones", opcion_area_entre_funciones),
        ("Sólido de revolución (una función)", opcion_volumen_una_funcion),
        ("Sólido de revolución (entre dos funciones)", opcion_volumen_entre_funciones),
        ("Salir", ventana.destroy)
    ]

    for texto, comando in botones:
        tk.Button(
            ventana,
            text=texto,
            command=comando,
            width=35,
            height=2,
            bg="#bbb0f0",
            fg="black",
            font=("Arial", 12 , "bold")
        ).pack(pady=8)

    ventana.mainloop()