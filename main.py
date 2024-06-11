import tkinter as tk
from tkinter import scrolledtext

def distancia_manhattan(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def optimizar_concierto():

    entrada = textArea.get("1.0", tk.END).strip().split("\n")
    
    N = int(entrada[0]) #Tamaño del valle
    M = int(entrada[1]) #Numero de ciudades
    
    ciudades = {}
    for i in range(2, 2 + M):
        partes = entrada[i].split()
        nombre = partes[0]
        x = int(partes[1])
        y = int(partes[2])
        ciudades[nombre] = (x, y)
    
    mejor_ubicacion = None
    distancia_max_minima = float('inf')
    
    # Ubicaciones del concierto
    for conciertoX in range(1, N):
        for conciertoY in range(1, N):
            if (conciertoX, conciertoY) not in ciudades.values():  # Evitar ubicaciones dentro de las ciudades
                distancias = [distancia_manhattan(conciertoX, conciertoY, ciudadX, ciudadY) for ciudadX, ciudadY in ciudades.values()]
                distancia_maxima = max(distancias)
                
                # Actualizar la mejor ubicación si se tiene una distancia máxima menor
                if distancia_maxima < distancia_max_minima:
                    distancia_max_minima = distancia_maxima
                    mejor_ubicacion = (conciertoX, conciertoY)
    
    # Generar el código MiniZinc
    minizinc_code = f"""int: N = {N};
int: M = {M};

array[1..M, 1..2] of int: cities = array2d(1..M, 1..2, [
"""
    for i, (ciudad, (x, y)) in enumerate(ciudades.items()):
        minizinc_code += f"{x}, {y}"
        if i < M - 1:
            minizinc_code += ", "
    minizinc_code += "]);\n"

    minizinc_code += f"""
var 1..N: conciertoX;
var 1..N: conciertoY;
var int: Distancia;

% Restricciones
constraint conciertoX >= 0;
constraint conciertoY >= 0;


constraint forall(i in 1..M) (
    (conciertoX != cities[i, 1] \/ conciertoY != cities[i, 2])
);


constraint forall(i in 1..M) (
    Distancia >= abs(conciertoX - cities[i, 1]) + abs(conciertoY - cities[i, 2])
);

constraint forall(i in 1..M) (
    cities[i, 1] >= 1 /\ cities[i, 1] <= N /\ cities[i, 2] >= 1 /\ cities[i, 2] <= N
);


solve minimize Distancia;

output ["Concierto en X = ", show(conciertoX), " Concierto en Y = ", show(conciertoY), " Distancia = ", show(Distancia)];
"""
    resultado.delete("1.0", tk.END)
    resultado.insert(tk.END, minizinc_code)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Concierto Benito-G")

# Crear el TextArea para la entrada de datos
textArea = scrolledtext.ScrolledText(ventana, width=40, height=10)
textArea.pack(padx=10, pady=10)

boton = tk.Button(ventana, text="Solucionar", command=optimizar_concierto)
boton.pack(pady=10)

# Crear el TextArea para mostrar el resultado
resultado = scrolledtext.ScrolledText(ventana, width=65, height=20)
resultado.pack(padx=10, pady=10)

# Ejecutar la ventana principal
ventana.mainloop()