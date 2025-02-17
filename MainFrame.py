from numpy import linspace as arr
from numpy import array as npArr
from numpy import ndarray, cos, exp, sin, log
import math as m
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

def animacion(frame=0):
  global x, org, ax, raices, met, n

  if frame >= len(raices):
    calc.config(state=tk.NORMAL)
    return
  
  ## ax.clear()

  limY = [min(org) - (max(org) * 0.25), max(org) * 1.25]

  if frame == 0:
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.plot(x, org, color="red")

  if met == 0:
    ax.plot([raices[frame][1], raices[frame][1]], [0, raices[frame][2]], color="black")
    ax.plot([raices[frame][3], raices[frame][3]], [0, raices[frame][4]], color="black")

    ax.plot(raices[frame][0], 0, color="black", marker='o')
  elif met == 1:
    ax.plot([raices[frame][1], raices[frame][1]], [0, raices[frame][2]], color="black", linestyle="dashed")
    ax.plot([raices[frame][0], raices[frame][1]], [0, raices[frame][2]], color="black")

    ax.plot(raices[frame][0], 0, color="black", marker='o')
  else:
    ax.plot([raices[frame][1], raices[frame][1]], [0, raices[frame][2]], linestyle="dashed", color="black")
    ax.plot([raices[frame][3], raices[frame][3]], [0, raices[frame][4]], linestyle="dashed", color="black")
    ax.plot([raices[frame][1], raices[frame][3]], [raices[frame][2], raices[frame][4]], color="black")

    ax.plot(raices[frame][0], 0, color="black", marker='o', )

  ax.set_xlim(min(x), max(x))
  ax.set_ylim(limY[0], limY[1])
  ##ax.legend(loc="upper right", fontsize="small")
  ax.set_xlabel(f"x = {raices[frame][0]} (Iteración: {frame+1})")
  ax.grid(which="major", linestyle="dashed")

  current_canvas.draw()

  if len(raices) >= n:
    frameSup.after(50, animacion, frame + 1)
  else:
    frameSup.after(1000, animacion, frame + 1)

def funcCallback(a, b, p0, p1, tol, func):
  if func.current() == 0:
    a.delete(0, tk.END)
    a.insert(0, "1")

    b.delete(0, tk.END)
    b.insert(0, "3")

    p0.delete(0, tk.END)
    p0.insert(0, "1")

    p1.delete(0, tk.END)
    p1.insert(0, "2.5")

    tol.delete(0, tk.END)
    tol.insert(0, "0.00001")
  elif func.current() == 1:
    a.delete(0, tk.END)
    a.insert(0, "1")

    b.delete(0, tk.END)
    b.insert(0, "4")

    p0.delete(0, tk.END)
    p0.insert(0, "2.5")

    p1.delete(0, tk.END)
    p1.insert(0, "3")

    tol.delete(0, tk.END)
    tol.insert(0, f"{10**-4}")
  elif func.current() == 2:
    a.delete(0, tk.END)
    a.insert(0, "-4")

    b.delete(0, tk.END)
    b.insert(0, "0")

    p0.delete(0, tk.END)
    p0.insert(0, "-1")

    p1.delete(0, tk.END)
    p1.insert(0, "0")

    tol.delete(0, tk.END)
    tol.insert(0, f"{10**-4}")
  elif func.current() == 3:
    a.delete(0, tk.END)
    a.insert(0, "0")

    b.delete(0, tk.END)
    b.insert(0, f"{m.pi/2}")

    p0.delete(0, tk.END)
    p0.insert(0, "0.7854")

    p1.delete(0, tk.END)
    p1.insert(0, "1.5")

    tol.delete(0, tk.END)
    tol.insert(0, f"{10**-4}")
  elif func.current() == 4:
    a.delete(0, tk.END)
    a.insert(0, "1")

    b.delete(0, tk.END)
    b.insert(0, "2.5")

    p0.delete(0, tk.END)
    p0.insert(0, "1.5")

    p1.delete(0, tk.END)
    p1.insert(0, "2")

    tol.delete(0, tk.END)
    tol.insert(0, "0.00001")

def calcRaiz(a, b, p0, p1, tol, n, opc, met):
  global current_table
  raices = []

  if current_table is not None:
    current_table.destroy()

  if met == 0:
    headers = ("a", "b", "p", "f(a)", "f(b)", "f(p)", "Error")
    current_table = ttk.Treeview(tableFrame, columns=headers, show='headings')
    for item in headers:
      current_table.heading(item, text=item)
    current_table.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    i = int(1)
    for j in range(i, (n+1)):
      p = (b + a)/2
      fp = calcFunc(p, opc)
      fa = calcFunc(a, opc)
      fb = calcFunc(b, opc)
      err = (b-a)/2
      current_table.insert(parent='', index=tk.END, values=(a, b, p, fa, fb, fp, err))
      raices.append( (p, a, fa, b, fb) )

      if ( fp == 0 ) or ( err < tol ):
        return raices
      if ( calcFunc(a, opc) * fp) > 0:
        a = p
      else:
        b = p

  if met == 1:
    headers = ("Iteración", "p_i", "p_i+1", "f(p_i)", "f(p_i+1)", "Error")
    current_table = ttk.Treeview(tableFrame, columns=headers, show='headings')
    for item in headers:
      current_table.heading(item, text=item)
    current_table.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    i = int(1)
    for j in range(1, (n+1)):
      fp0 = calcFunc(p0, opc)
      p = p0 - (fp0 / derivada(p0, opc))
      fp = calcFunc(p, opc)
      err = abs( (p - p0) )
      current_table.insert(parent='', index=tk.END, values=(j, p0, p, fp0, fp, err))
      raices.append( (p, p0, fp0) )

      if ( fp == 0 ) or ( err < tol ):
        return raices
      p0 = p

  if met == 2:
    headers = ("Iteración", "p_i-1", "p_i", "p_i+1", "f(p_i)", "f(p_i+1)", "Error")
    current_table = ttk.Treeview(tableFrame, columns=headers, show='headings')
    for item in headers:
      current_table.heading(item, text=item)
    current_table.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    i = int(1)
    for j in range(1, (n+1)):
      fp0 = calcFunc(p0, opc)
      fp1 = calcFunc(p1, opc)
      p = p1 - ( (fp1*(p1 - p0))/(fp1 - fp0) )
      fp = calcFunc(p, opc)
      err = abs( (p - p0) )
      current_table.insert(parent='', index=tk.END, values=(j, p0, p, p1, fp, fp1, err))
      raices.append( (p, p0, fp0, p1, fp1) )

      if ( fp == 0 ) or ( err < tol ):
        return raices
      
      p0 = p1
      p1 = p

  if met == 3:
    headers = ("Iteración", "p_i-1", "p_i", "p_i+1", "f(p_i)", "f(p_i+1)", "Error")
    current_table = ttk.Treeview(tableFrame, columns=headers, show='headings')
    for item in headers:
      current_table.heading(item, text=item)
    current_table.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    i = int(1)
    for j in range(1, (n+1)):
      fp0 = calcFunc(p0, opc)
      fp1 = calcFunc(p1, opc)
      p = p1 - ( (fp1*(p1 - p0))/(fp1 - fp0) )
      fp = calcFunc(p, opc)
      err = abs( (p - p0) )
      current_table.insert(parent='', index=tk.END, values=(j, p0, p, p1, fp, fp1, err))
      raices.append( (p, p0, fp0, p1, fp1) )

      if ( fp == 0) or ( err < tol ):
        return raices

      if ( (fp * fp1) < 0 ):
        p0 = p
      else:
        p1 = p

  tk.messagebox.showerror("Error", f"El proceso fallo despues de {n} iteraciones")
  return raices

def derivada(x, opc):
  if opc == 0:
    return ( 3*(x**2) + 8*(x) )
  
  if opc == 1:
    return ( 3*(x**2) - 4*(x) )
    
  if opc == 2:
    return ( 3*(x**2) + 6*(x) )
    
  if opc == 3:
    return ( 1 + sin(x) )

  if opc == 4:
    return ( (exp(x)) + (-2**(-x) * (log(2))) + (2*-sin(x)) )

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
  global x, org, ax, raices, met, n
  
  err = int(0)
  opc, met = int(0), int(0)

  try:
    if (funcs_ui.current() > -1) and (mets_ui.current() > -1):
      opc = funcs_ui.current()
      met = mets_ui.current()
    else:
      tk.messagebox.showerror("Error", "Seleccione una función y/o un método válido de sus respectivas listas")
      err += 1

    a = float(a_ui.get())
    b = float(b_ui.get())
    p0 = float(p0_ui.get())
    p1 = float(p1_ui.get())
    tol = float(tol_ui.get())

    n = int(n_ui.get())

  except ValueError:
    tk.messagebox.showerror("Error", "Ingrese un número válido en los campos:\n• Los puntos a evualar pueden ser números reales\n• La cantidad máxima de iteraciones debe ser entera\n• No pueden haber campos vacios")
    err += 1

  if err != 0:
    return
  
  x = arr(a, b, 250)
  org = calcFunc(x, opc)  # Calculate the original function values
  raices = calcRaiz(a, b, p0, p1, tol, n, opc, met)

  # Destruir el canvas anterior si existe
  if current_canvas is not None:
    current_canvas.get_tk_widget().destroy()

  # Creación de la gráfica
  fig = Figure(figsize=(5, 4), dpi=100)
  ax = fig.add_subplot(111)

  # Dibujo del canva nuevo
  current_canvas = FigureCanvasTkAgg(fig, master=frameSup)
  current_canvas.draw()
  current_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

  frameSup.after(0, animacion, 0)
  calc.config(state=tk.DISABLED)
  ### Fin de la función ###


# Variable global, se usa para determinar si existe un grafico en la aplicación
current_canvas = None
current_table = None

## Ventana principal ##
root = tk.Tk()
root.wm_title("Cálculo de Raíces")

frameSup = tk.Frame(root)
frameSup.pack(padx=20, pady=5, side=tk.TOP, fill=tk.BOTH, expand=True)

# Panel de los elementos de la app
tableFrame = tk.Frame(root)
tableFrame.pack(padx=20, pady=5, side=tk.BOTTOM, fill=tk.BOTH, expand=True)

titulo = tk.Label(frameSup, text="Cálculo de Raíces", font=("Arial", 20))
titulo.pack(pady=10, side=tk.TOP)

## Definición de variables de Tkinter ##
a_ui = tk.StringVar(value="")
b_ui = tk.StringVar(value="")
tol_ui = tk.StringVar(value="")
n_ui = tk.StringVar(value="")
p0_ui = tk.StringVar(value="")
p1_ui = tk.StringVar(value="")

# Panel con las opciones
opciones = tk.Frame(frameSup, borderwidth=2, relief="sunken")
opciones.pack(padx=20, pady=10, side=tk.RIGHT)

# Lista de las funciones disponibles
etiquetaFunc = tk.Label(opciones, text="Funciones")
etiquetaFunc.pack(padx=10)
funcs = ttk.Combobox(
  opciones,
  state="readonly",
  values=["x^3 + 4x^2 - 10", "x^3 - 2x^2 - 5", "x^3 + 3x^2 - 1", "x - cos(x)", "e^x + 2-x + 2cos(x) - 6"]
)
funcs.bind("<<ComboboxSelected>>", lambda _ :funcCallback(punto1, punto2, punto3, punto4, tolerancia, funcs))
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
tolerancia = tk.Entry(opciones, width=25, textvariable=tol_ui)
tolerancia.pack(padx=10, pady=2)

# Campo de texto para el número máximo de iteraciones
etiqueta4 = tk.Label(opciones, text="N. máximo de iteraciones")
etiqueta4.pack(padx=10)
n_iter = tk.Entry(opciones, width=25, textvariable=n_ui)
n_iter.pack(padx=10, pady=2)

# Boton que realiza el cálculo
calc = tk.Button(opciones, text="Calcular", width=20,command=lambda:setGraph(a_ui, b_ui, p0_ui, p1_ui, tol_ui, n_ui, funcs, mets) )
calc.pack(padx=20, pady=10)

# Inicio de la ventana maximizada
root.state("zoomed")
root.mainloop()