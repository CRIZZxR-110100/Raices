from numpy import linspace as arr
from numpy import array as npArr
from numpy import ndarray, cos, exp, sin, log
import math as m
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

def calcRaiz(a, b, p0, p1, tol, n, opc, met):
  if met == 0:
    i = int(1)
    for j in range(i, (n+1)):
      p = (b + a)/2
      fp = calcFunc(p, opc)
      fa = calcFunc(a, opc)
      fb = calcFunc(b, opc)

      err = (b-a)/2
      
      if ( fp == 0 ) or ( err < tol ):
        print(p, fp)
        return p
      
      if ( calcFunc(a, opc) * fp) > 0:
        a = p
      else:
        b = p
  
  if met == 1:
    i = int (1)
    for j in range(1, (n+1)):
      p = p0 - (calcFunc(p0, opc) / derivada(p0, opc))
      print(p, )
      fp = calcFunc(p, opc)
      fp0 = calcFunc(p0, opc)

      err = abs( (p - p0) )

      if err < tol:
        print(p, fp)
        return p
      
      p0 = p
  
  if met == 2:
    print("Falta la función del Metodo de secante")

  if met == 3:
    print("Falta la función del Metodo de regla falsa")
  
  tk.messagebox.showerror("Error", f"El proceso fallo despues de {n} iteraciones")

def derivada(x, opc):
  if opc == 0:
    return ( 3*(x**2) + 2*(x) )
  
  if opc == 1:
    return ( 3*(x**2) - 4*(x) )
    
  if opc == 2:
    return ( 3*(x**2) + 6*(x) )
    
  if opc == 3:
    return ( 1 + sin(x) )

  if opc == 4:
    return ( (exp(x)) + (-2**(-x) * (log(2))) + (2*-sen(x)) )

def calcFunc(x, opc):
  if opc == 0:
    return ( (x**3) + 4*(x**2) - 10 )
  
  if opc == 1:
    return ( (x**3) - 2*(x**2) - 5 )
    
  if opc == 2:
    return ( (x**3) + 3*(x**2) - 1 )
    
  if opc == 3:
    if isinstance(x, (int, float)):
      return x - cos(x)
    elif isinstance(x, (list, tuple, ndarray)):
        y = npArr(x)
        return (y - cos(y))
    else:
        raise TypeError("Error con el valor de x, solo puede ser un numero o un arreglo")

  if opc == 4:
    if isinstance(x, (int, float)):
      return ( (exp(x)) + (2**(-x)) + (2*cos(x)) - 6 )
    elif isinstance(x, (list, tuple, ndarray)):
        y = npArr(x)
        return( (exp(y)) + (2**(-y)) + (2*cos(y)) - 6 )
    else:
        raise TypeError("Error con el valor de x, solo puede ser un numero o un arreglo")

  ### Fin de la función ###

def setGraph(a_ui, b_ui, p0_ui, p1_ui, tol_ui, n_ui, funcs_ui, mets_ui):
  global current_canvas
  err = int(0)
  opc, met = int(0), int(0)

  try:
    if (funcs_ui.current() > -1) and (mets_ui.current() > -1):
      opc = funcs_ui.current()
      met = mets_ui.current()
    else:
      tk.messagebox.showerror("Error", "Seleccione una función y un método válido de sus respectivas listas")
      err += 1

    a = float(a_ui.get())
    b = float(b_ui.get())
    p0 = float(p0_ui.get())
    p1 = float(p1_ui.get())
    tol = float(tol_ui.get())

    n = int(n_ui.get())

  except ValueError:
    tk.messagebox.showerror("Error", "Ingrese un número válido en los campos:\n• Los puntos a evualar pueden ser números reales\n• No pueden haber campos vacios")
    err += 1

  if err != 0:
    return
  
  x = arr(a, b, 250)
  org = calcFunc(x, opc)

  raiz = calcRaiz(a, b, p0, p1, tol, n, opc, met)

  # Destruir el canvas anterior si existe
  if current_canvas is not None:
    current_canvas.get_tk_widget().destroy()
  
  limY = [min(org)-(max(org)*0.25), max(org)*1.25]

  # Creación de la gráfica
  fig = Figure(figsize=(5, 4), dpi=100)
  ax = fig.add_subplot(111)

  ax.plot([min(x), max(x)], [0, 0], color="black", linewidth=1)
  ax.plot([0, 0], limY, color="black", linewidth=1)

  ax.plot(x, org, color="red")

  ax.set_ylim(limY[0], limY[1])
  ax.set_xlim(min(x), max(x))
  ax.grid(which="major", linestyle="dashed")

  # Dibujo del canva nuevo
  current_canvas = FigureCanvasTkAgg(fig, master=root)
  current_canvas.draw()
  current_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  ### Fin de la función ###


# Variable global, se usa para determinar si existe un grafico en la aplicación
current_canvas = None

## Ventana principal ##
root = tk.Tk()
root.wm_title("Cálculo de Raíces")

titulo = tk.Label(root, text="Cálculo de Raíces", font=("Arial", 20))
titulo.pack(pady=10, side=tk.TOP)

## Definición de variables de Tkinter ##
a_ui = tk.StringVar(value="")
b_ui = tk.StringVar(value="")
tol_ui = tk.StringVar(value="")
n_ui = tk.StringVar(value="")
p0_ui = tk.StringVar(value="")
p1_ui = tk.StringVar(value="")

# Panel con las opciones
opciones = tk.Frame(root, width=300, height=450, borderwidth=2, relief="sunken")
opciones.pack(padx=20, pady=10, side=tk.RIGHT)

# Lista de las funciones disponibles
etiquetaFunc = tk.Label(opciones, text="Funciones")
etiquetaFunc.pack(padx=10)
funcs = ttk.Combobox(
  opciones,
  state="readonly",
  values=["x^3 + 4x^2 - 10", "x^3 - 2x^2 - 5", "x^3 + 3x^2 - 1", "x - cos(x)", "e^x + 2-x + 2cos(x) - 6"]
)
funcs.pack(padx=10, pady=2)

# Lista de los métodos disponibles
etiquetaMet = tk.Label(opciones, text="Métodos")
etiquetaMet.pack(padx=10)
mets = ttk.Combobox(
  opciones,
  state="readonly",
  values=["Bisección", "Newton Raphson", "Secante", "Regla falsa"]
)
mets.pack(padx=10, pady=2)

# Campos de texto para los puntos [a, b] de la función
etiqueta1 = tk.Label(opciones, text="Puntos de la función [a, b]")
etiqueta1.pack(padx=10)
punto1 = tk.Entry(opciones, width=25, textvariable=a_ui)
punto1.pack(padx=10, pady=2)
punto2 = tk.Entry(opciones, width=25, textvariable=b_ui)
punto2.pack(padx=10, pady=2)

# Campos de texto para los puntos [p0, p1] del método
etiqueta2 = tk.Label(opciones, text="Puntos de la función [p0, p1]")
etiqueta2.pack(padx=10)
punto3 = tk.Entry(opciones, width=25, textvariable=p0_ui)
punto3.pack(padx=10, pady=2)
punto4 = tk.Entry(opciones, width=25, textvariable=p1_ui)
punto4.pack(padx=10, pady=2)

# Campo de texto para el valor de la tolerancia
etiqueta3 = tk.Label(opciones, text="Tolerancia")
etiqueta3.pack(padx=10)
punto5 = tk.Entry(opciones, width=25, textvariable=tol_ui)
punto5.pack(padx=10, pady=2)

# Campo de texto para el número máximo de iteraciones
etiqueta4 = tk.Label(opciones, text="N. máximo de iteraciones")
etiqueta4.pack(padx=10)
punto6 = tk.Entry(opciones, width=25, textvariable=n_ui)
punto6.pack(padx=10, pady=2)

# Boton que realiza el cálculo
calc = tk.Button(opciones, text="Calcular", width=20,command=lambda:setGraph(a_ui, b_ui, p0_ui, p1_ui, tol_ui, n_ui, funcs, mets) )
calc.pack(padx=20, pady=10)

# Inicio de la ventana maximizada
root.state("zoomed")
root.mainloop()