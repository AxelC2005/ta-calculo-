import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, integrate, parse_expr, pi, Abs
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
def mostrar_graficas_2d(f_expr, a, b, mostrar_area=True, eje='x', g_expr=None):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    x_vals = np.linspace(float(a) - 1, float(b) + 1, 500)
    f_vals = evaluar_funcion_segura(f_expr, x_vals, x)
    g_vals = evaluar_funcion_segura(g_expr, x_vals, x) if g_expr else None

    x_area = np.linspace(float(a), float(b), 500)
    f_area = evaluar_funcion_segura(f_expr, x_area, x)
    g_area = evaluar_funcion_segura(g_expr, x_area, x) if g_expr else None

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

# --- Visualización 3D entre dos funciones eje X o Y ---
def mostrar_volumen_entre_funciones_3d(f_expr, g_expr, a, b, eje='x'):
    theta = np.linspace(0, 2 * np.pi, 100)
    vals = np.linspace(float(a), float(b), 100)

    if eje == 'x':
        f_vals = evaluar_funcion_segura(f_expr, vals, x)
        g_vals = evaluar_funcion_segura(g_expr, vals, x)
        grid, theta_grid = np.meshgrid(vals, theta)
        f_grid, _ = np.meshgrid(f_vals, theta)
        g_grid, _ = np.meshgrid(g_vals, theta)

        X = grid
        Y_outer = f_grid * np.cos(theta_grid)
        Z_outer = f_grid * np.sin(theta_grid)
        Y_inner = g_grid * np.cos(theta_grid)
        Z_inner = g_grid * np.sin(theta_grid)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y_outer, Z_outer, color='pink', alpha=0.7)
        ax.plot_surface(X, Y_inner, Z_inner, color='yellow', alpha=1.0, edgecolor='none')
        ax.set_title(f"Sólido 3D entre f(x) y g(x) por revolución (eje X)")

    elif eje == 'y':
        f_vals = evaluar_funcion_segura(f_expr, vals, y)
        g_vals = evaluar_funcion_segura(g_expr, vals, y)
        grid, theta_grid = np.meshgrid(vals, theta)
        f_grid, _ = np.meshgrid(f_vals, theta)
        g_grid, _ = np.meshgrid(g_vals, theta)

        X_outer = f_grid * np.cos(theta_grid)
        Z_outer = f_grid * np.sin(theta_grid)
        X_inner = g_grid * np.cos(theta_grid)
        Z_inner = g_grid * np.sin(theta_grid)
        Y = grid

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X_outer, Y, Z_outer, color='pink', alpha=0.7)
        ax.plot_surface(X_inner, Y, Z_inner, color='yellow', alpha=1.0, edgecolor='none')
        ax.set_title(f"Sólido 3D entre f(y) y g(y) por revolución (eje Y)")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.tight_layout()
    plt.show()

# --- Visualización 3D de una sola función ---
def mostrar_volumen_3d(f_expr, a, b, eje='x'):
    theta = np.linspace(0, 2 * np.pi, 100)

    if eje == 'x':
        x_vals = np.linspace(float(a), float(b), 100)
        x_grid, theta_grid = np.meshgrid(x_vals, theta)
        r_vals = evaluar_funcion_segura(f_expr, x_vals, x)
        r_grid, _ = np.meshgrid(r_vals, theta)

        X = x_grid
        Y = r_grid * np.cos(theta_grid)
        Z = r_grid * np.sin(theta_grid)

    elif eje == 'y':
        y_vals = np.linspace(float(a), float(b), 100)
        y_grid, theta_grid = np.meshgrid(y_vals, theta)
        r_vals = evaluar_funcion_segura(f_expr, y_vals, y)
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

<<<<<<< HEAD:volumen.py
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

=======
# --- Menú interactivo ---
def menu_integrales_definidas():
    print("\n=== CÁLCULO DE INTEGRALES DEFINIDAS ===")
    print("1. Área bajo una curva")
    print("2. Área entre dos funciones")
    print("3. Sólido de revolución en 3D (una función)")
    print("4. Sólido de revolución en 3D (entre dos funciones)")

    opcion = input("Selecciona una opción (1 a 4): ")

    if opcion == '1':
        expr_str = input("\nIngresa la función f(x): ")
        a = float(input("Límite inferior a: "))
        b = float(input("Límite superior b: "))
        f_expr = parse_expr(expr_str)
        area = calcular_area(f_expr, a, b)
        print(f"✅ Área entre x = {a} y x = {b} es: {area} ≈ {float(area):.5f}")
        mostrar_graficas_2d(f_expr, a, b, mostrar_area=True)

    elif opcion == '2':
        expr1 = input("\nIngresa la primera función f(x): ")
        expr2 = input("Ingresa la segunda función g(x): ")
        a = float(input("Límite inferior a: "))
        b = float(input("Límite superior b: "))
        f_expr = parse_expr(expr1)
        g_expr = parse_expr(expr2)
        area = calcular_area_entre_funciones(f_expr, g_expr, a, b)
        print(f"✅ Área entre f(x) y g(x) en [{a}, {b}] es: {area} ≈ {float(area):.5f}")
        mostrar_graficas_2d(f_expr, a, b, mostrar_area=True, g_expr=g_expr)

    elif opcion == '3':
        expr_str = input("\nIngresa la función f(x) o f(y): ")
        a = float(input("Límite inferior a: "))
        b = float(input("Límite superior b: "))
        eje = input("👉 ¿Sobre qué eje deseas visualizar el sólido 3D? (x o y): ").strip().lower()
        f_expr = parse_expr(expr_str)

        if eje == 'x':
            var = x
        elif eje == 'y':
            var = y
        else:
            print("❌ Eje no válido.")
            return

        volumen = pi * integrate(f_expr**2, (var, a, b))
        print(f"✅ Volumen (teórico) entre {a} y {b} respecto al eje {eje} es: {volumen} ≈ {float(volumen):.5f}")
        mostrar_volumen_3d(f_expr, a, b, eje=eje)

    elif opcion == '4':
        expr1 = input("\nIngresa la función exterior f(x) o f(y): ")
        expr2 = input("Ingresa la función interior g(x) o g(y): ")
        a = float(input("Límite inferior a: "))
        b = float(input("Límite superior b: "))
        eje = input("👉 ¿Sobre qué eje deseas visualizar el sólido 3D? (x o y): ").strip().lower()
        f_expr = parse_expr(expr1)
        g_expr = parse_expr(expr2)

        if eje == 'x':
            var = x
        elif eje == 'y':
            var = y
        else:
            print("❌ Eje no válido.")
            return

        integrando = pi * (f_expr**2 - g_expr**2)
        volumen = integrate(integrando, (var, a, b))
        print(f"✅ Volumen por revolución entre funciones respecto al eje {eje}: {volumen} ≈ {float(volumen):.5f}")
        mostrar_volumen_entre_funciones_3d(f_expr, g_expr, a, b, eje=eje)

    else:
        print("❌ Opción inválida.")

# --- Inicio del programa ---
def main():
    print("====== CÁLCULO DE ÁREAS Y VOLÚMENES MEDIANTE INTEGRALES ======")
    menu_integrales_definidas()

if __name__ == "__main__":
    main()
>>>>>>> main:total.py
