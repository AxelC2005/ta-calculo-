import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, integrate, parse_expr, pi, Abs
from mpl_toolkits.mplot3d import Axes3D

x = symbols('x')

# --- Cálculos ---
def calcular_area(f, a, b):
    return integrate(f, (x, a, b))

def calcular_area_entre_funciones(f, g, a, b):
    return integrate(Abs(f - g), (x, a, b))

def calcular_volumen_proyeccion(f, a, b):
    return pi * integrate(f**2, (x, a, b))

def evaluar_funcion_segura(expr, valores):
    resultado = []
    for val in valores:
        res = expr.evalf(subs={x: val})
        if res.is_real:
            resultado.append(float(res))
        else:
            resultado.append(np.nan)
    return resultado

# --- Visualización 2D ---
def mostrar_graficas_2d(f_expr, a, b, mostrar_area=True, eje='x', g_expr=None):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    x_vals = np.linspace(float(a) - 1, float(b) + 1, 500)
    f_vals = evaluar_funcion_segura(f_expr, x_vals)
    g_vals = evaluar_funcion_segura(g_expr, x_vals) if g_expr else None

    x_area = np.linspace(float(a), float(b), 500)
    f_area = evaluar_funcion_segura(f_expr, x_area)
    g_area = evaluar_funcion_segura(g_expr, x_area) if g_expr else None

    axs[0].plot(x_vals, f_vals, color='blue', label=f'f(x) = {f_expr}')
    if g_expr:
        axs[0].plot(x_vals, g_vals, color='red', linestyle='--', label=f'g(x) = {g_expr}')
    axs[0].set_title("Funciones sin área")
    axs[0].set_xlabel("x")
    axs[0].set_ylabel("y")
    axs[0].grid(True)
    axs[0].legend()

    axs[1].plot(x_vals, f_vals, color='blue', label=f'f(x) = {f_expr}')
    if g_expr:
        axs[1].plot(x_vals, g_vals, color='red', linestyle='--', label=f'g(x) = {g_expr}')
        axs[1].fill_between(x_area, f_area, g_area, color='violet', alpha=0.5, label="Área entre funciones")
        axs[1].set_title("Área entre f(x) y g(x)")
    else:
        if mostrar_area:
            axs[1].fill_between(x_area, f_area, color='skyblue', alpha=0.5, label="Área bajo la curva")
            axs[1].set_title("Área bajo la curva")
        else:
            axs[1].fill_between(x_area, [0]*len(x_area), f_area, color='orange', alpha=0.5, label="Volumen proyectado")
            axs[1].set_title("Proyección del volumen")

    axs[1].set_xlabel("x")
    axs[1].set_ylabel("y")
    axs[1].grid(True)
    axs[1].legend()
    plt.tight_layout()
    plt.show()

# --- Visualización 3D de un sólido ---
def mostrar_volumen_3d(f_expr, a, b, eje='x'):
    theta = np.linspace(0, 2 * np.pi, 100)

    if eje == 'x':
        x_vals = np.linspace(float(a), float(b), 100)
        x_grid, theta_grid = np.meshgrid(x_vals, theta)
        f_fun = np.vectorize(lambda val: float(f_expr.evalf(subs={x: val})) if f_expr.evalf(subs={x: val}).is_real else np.nan)
        r_vals = f_fun(x_vals)
        r_grid, _ = np.meshgrid(r_vals, theta)

        X = x_grid
        Y = r_grid * np.cos(theta_grid)
        Z = r_grid * np.sin(theta_grid)

    elif eje == 'y':
        y_vals = np.linspace(float(a), float(b), 100)
        y_grid, theta_grid = np.meshgrid(y_vals, theta)
        f_fun = np.vectorize(lambda val: float(f_expr.evalf(subs={x: val})) if f_expr.evalf(subs={x: val}).is_real else np.nan)
        r_vals = f_fun(y_vals)
        r_grid, _ = np.meshgrid(r_vals, theta)

        X = r_grid * np.cos(theta_grid)
        Z = r_grid * np.sin(theta_grid)
        Y = y_grid

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8, edgecolor='none')

    ax.set_title(f"Sólido de revolución en 3D (eje {eje})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.tight_layout()
    plt.show()

# --- Visualización 3D entre dos funciones ---
def mostrar_volumen_entre_funciones_3d(f_expr, g_expr, a, b, eje='x'):
    theta = np.linspace(0, 2 * np.pi, 100)
    x_vals = np.linspace(float(a), float(b), 100)
    f_fun = np.vectorize(lambda val: float(f_expr.evalf(subs={x: val})) if f_expr.evalf(subs={x: val}).is_real else np.nan)
    g_fun = np.vectorize(lambda val: float(g_expr.evalf(subs={x: val})) if g_expr.evalf(subs={x: val}).is_real else np.nan)

    f_vals = f_fun(x_vals)
    g_vals = g_fun(x_vals)

    x_grid, theta_grid = np.meshgrid(x_vals, theta)
    f_grid, _ = np.meshgrid(f_vals, theta)
    g_grid, _ = np.meshgrid(g_vals, theta)

    X = x_grid
    Y_outer = f_grid * np.cos(theta_grid)
    Z_outer = f_grid * np.sin(theta_grid)

    Y_inner = g_grid * np.cos(theta_grid)
    Z_inner = g_grid * np.sin(theta_grid)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y_outer, Z_outer, color='limegreen', alpha=0.7)
    ax.plot_surface(X, Y_inner, Z_inner, color='white', alpha=1.0, edgecolor='none')

    ax.set_title(f"Sólido 3D entre f(x) y g(x) por revolución")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.tight_layout()
    plt.show()

