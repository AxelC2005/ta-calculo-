import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, integrate, parse_expr,latex, pi, Abs
from mpl_toolkits.mplot3d import Axes3D

x, y = symbols('x y')

# --- Cálculos ---
def calcular_area(f, a, b):
    return integrate(f, (x, a, b))

def calcular_area_entre_funciones(f, g, a, b):
    return integrate(Abs(f - g), (x, a, b))

def evaluar_funcion_segura(expr, valores, var):
    resultado = []
    for val in valores:
        res = expr.evalf(subs={var: val})
        if res.is_real:
            resultado.append(float(res))
        else:
            resultado.append(np.nan)
    return resultado

# --- Visualización 2D ---
def mostrar_graficas_2d(f_expr, a, b, mostrar_area=True, eje='x', g_expr=None, mensaje_area=None):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    x_vals = np.linspace(float(a) - 1, float(b) + 1, 500)
    f_vals = evaluar_funcion_segura(f_expr, x_vals, x)
    g_vals = evaluar_funcion_segura(g_expr, x_vals, x) if g_expr else None

    x_area = np.linspace(float(a), float(b), 500)
    f_area = evaluar_funcion_segura(f_expr, x_area, x)
    g_area = evaluar_funcion_segura(g_expr, x_area, x) if g_expr else None

    axs[0].plot(x_vals, f_vals, color='blue', label=fr'$f(x) = {latex(f_expr)}$')
    if g_expr:
        axs[0].plot(x_vals, g_vals, color='red', linestyle='--',label=fr'$g(x) = {latex(g_expr)}$')
    axs[0].set_title("Funciones sin área")
    axs[0].set_xlabel("x")
    axs[0].set_ylabel("y")
    axs[0].grid(True)
    axs[0].legend()

    axs[1].plot(x_vals, f_vals, color='blue', label=fr'$f(x) = {latex(f_expr)}$')
    if g_expr:
        axs[1].plot(x_vals, g_vals, color='red', linestyle='--', label=fr'$g(x) = {latex(g_expr)}$')
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
    axs[1].legend(loc='upper center')

    # 👇 Mostrar el mensaje en la parte inferior del gráfico
    if mensaje_area:
        axs[1].text(0.0, 0.01, mensaje_area,
                    transform=axs[1].transAxes,
                    fontsize=12,
                    ha='center',
                    bbox=dict(boxstyle="round", facecolor="white", edgecolor="black"))

    plt.tight_layout()
    plt.show()
#mostrar volumen de una funcion       
def mostrar_volumen_entre_funciones_3d(f_expr, g_expr, a, b, eje='x', mensaje_volumen=None, legend=None):
    theta = np.linspace(0, 2 * np.pi, 100)
    vals = np.linspace(float(a), float(b), 100)
    var = x if eje == 'x' else y

    f_vals = evaluar_funcion_segura(f_expr, vals, var)
    g_vals = evaluar_funcion_segura(g_expr, vals, var)
    grid, theta_grid = np.meshgrid(vals, theta)
    f_grid, _ = np.meshgrid(f_vals, theta)
    g_grid, _ = np.meshgrid(g_vals, theta)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    if eje == 'x':
        X = grid
        Y_outer = f_grid * np.cos(theta_grid)
        Z_outer = f_grid * np.sin(theta_grid)
        Y_inner = g_grid * np.cos(theta_grid)
        Z_inner = g_grid * np.sin(theta_grid)
        ax.plot_surface(X, Y_outer, Z_outer, color='pink', alpha=0.7)
        ax.plot_surface(X, Y_inner, Z_inner, color='yellow', alpha=1.0, edgecolor='none')
    else:
        Y = grid
        X_outer = f_grid * np.cos(theta_grid)
        Z_outer = f_grid * np.sin(theta_grid)
        X_inner = g_grid * np.cos(theta_grid)
        Z_inner = g_grid * np.sin(theta_grid)
        ax.plot_surface(X_outer, Y, Z_outer, color='pink', alpha=0.7)
        ax.plot_surface(X_inner, Y, Z_inner, color='yellow', alpha=1.0, edgecolor='none')

    ax.set_title(f"Sólido 3D entre f({eje}) y g({eje}) por revolución (eje {eje})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    # Mostrar mensaje del volumen dentro de la figura 3D
    if mensaje_volumen:
     texto_funciones = f"$f({eje}) = {latex(f_expr)}$\n$g({eje}) = {latex(g_expr)}$\n{mensaje_volumen}"
    ax.text2D(0.0, 0.01, texto_funciones,
              transform=ax.transAxes,
              ha='left',
              fontsize=12,
              bbox=dict(boxstyle="round", facecolor="white", edgecolor="black"))
    plt.tight_layout()
    plt.show()


# --- Visualización 3D de una sola función ---
def mostrar_volumen_3d(f_expr, a, b, eje='x', mensaje_volumen1=None):
    theta = np.linspace(0, 2 * np.pi, 100)
    var = x if eje == 'x' else y

    if eje == 'x':
        x_vals = np.linspace(float(a), float(b), 100)
        x_grid, theta_grid = np.meshgrid(x_vals, theta)
        r_vals = evaluar_funcion_segura(f_expr, x_vals, var)
        r_grid, _ = np.meshgrid(r_vals, theta)

        X = x_grid
        Y = r_grid * np.cos(theta_grid)
        Z = r_grid * np.sin(theta_grid)

    elif eje == 'y':
        y_vals = np.linspace(float(a), float(b), 100)
        y_grid, theta_grid = np.meshgrid(y_vals, theta)
        r_vals = evaluar_funcion_segura(f_expr, y_vals, var)
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

    #  Mostrar mensaje si se proporciona
    if mensaje_volumen1:
     texto_funciones = fr"$f({eje}) = {latex(f_expr)}$" + "\n" + mensaje_volumen1
    ax.text2D(0.0, 0.01, texto_funciones,
              transform=ax.transAxes,
              ha='left',
              fontsize=12,
              bbox=dict(boxstyle="round", facecolor="white", edgecolor="black"))

    plt.tight_layout()
    plt.show()
