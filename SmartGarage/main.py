import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VisualizacionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Visualización de Datos")
        self.root.geometry("1200x800")

        self.df = None
        self.current_plot = None
        self.mostrar_histograma = True  # Variable para alternar entre gráficos

        self.create_widgets()
        self.btn_siguiente = tk.Button(self.frame_graficas, text="Siguiente", command=self.toggle_grafico, font=("Helvetica", 10))
        self.btn_siguiente.pack(side=tk.TOP, anchor=tk.E)
        self.btn_siguiente.pack_forget()
        self.contador_graficos = 0
        root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)


    def cargar_datos(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if archivo:
            self.df = pd.read_csv(archivo, sep=';', header=None)
            self.df = self.df.head(200)
            # Eliminar las dos últimas columnas ("Colisión" y "Fecha")
            self.df = self.df.iloc[:, :-2]
            self.df.columns = ['Temperatura', 'Presion', 'Colision', 'Fecha']

        # Mostrar los botones de gráficos nuevamente
        self.btn_temperatura.pack(side=tk.LEFT, padx=5)
        self.btn_presion.pack(side=tk.LEFT, padx=5)
        self.btn_colision.pack(side=tk.LEFT, padx=5)

    def mostrar_histograma_temperatura(self):
        if self.current_plot is not None:
            self.current_plot.get_tk_widget().pack_forget()  # Oculta la gráfica actual

        # Crear el histograma de Temperatura
        fig = plt.figure(figsize=(10, 4))
        plt.hist(self.df['Temperatura'], bins=20, edgecolor='k')
        plt.title('Histograma de Temperatura')
        plt.xlabel('Temperatura')
        plt.ylabel('Frecuencia')

        # Agregar el gráfico al Canvas
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()

        self.current_plot = canvas  # Establecer la gráfica actual

        # Ocultar los botones de gráficos
        self.btn_temperatura.pack_forget()
        self.btn_presion.pack_forget()
        self.btn_colision.pack_forget()

        # Mostrar el botón "Siguiente"
        self.btn_siguiente.pack(side=tk.TOP, anchor=tk.E)

    def mostrar_grafico_linea_temperatura(self):
        if self.current_plot is not None:
            self.current_plot.get_tk_widget().pack_forget()  # Oculta la gráfica actual

        # Crear el gráfico de línea de Temperatura
        fig = plt.figure(figsize=(10, 3))
        plt.plot(self.df['Fecha'], self.df['Temperatura'], marker='o', linestyle='-')
        plt.title('Gráfico de Línea: Temperatura vs Fecha')
        plt.xlabel('Fecha')
        plt.ylabel('Temperatura')
        plt.grid(True)


        # Agregar el gráfico al Canvas
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()

        self.current_plot = canvas  # Establecer la gráfica actual

        # Ocultar el botón "Siguiente"
        self.btn_siguiente.pack_forget()

        # Mostrar el botón "Siguiente" para cambiar al histograma de temperatura
        self.btn_siguiente.config(command=self.toggle_grafico)
        self.btn_siguiente.pack(side=tk.TOP, anchor=tk.E)

    def mostrar_temperatura_vs_fecha(self):
        if self.current_plot is not None:
            self.current_plot.get_tk_widget().pack_forget()  # Oculta la gráfica actual

        # Crear el gráfico de Temperatura vs Fecha
        fig = plt.figure(figsize=(10, 3))
        plt.subplot(131)  # 1 fila, 3 columnas, posición 1
        plt.boxplot(self.df['Temperatura'])
        plt.title('Boxplot de Temperatura')
        plt.ylabel('Temperatura')


        # Agregar el gráfico al Canvas
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()

        self.current_plot = canvas  # Establecer la gráfica actual

        # Ocultar el botón "Siguiente"
        self.btn_siguiente.pack_forget()

        # Mostrar el botón "Siguiente" para volver al histograma de temperatura
        self.btn_siguiente.config(command=self.toggle_grafico)
        self.btn_siguiente.pack(side=tk.TOP, anchor=tk.E)

    def toggle_grafico(self):
        if self.contador_graficos == 0:
            self.mostrar_histograma_temperatura()
        elif self.contador_graficos == 1:
            self.mostrar_grafico_linea_temperatura()
        else:
            self.mostrar_temperatura_vs_fecha()
        self.contador_graficos = (self.contador_graficos + 1) % 3
            
    def mostrar_graficos_presion(self):
        if self.current_plot is not None:
            self.current_plot.get_tk_widget().pack_forget()  # Oculta la gráfica actual

        fig = plt.figure(figsize=(10, 4))
        plt.hist(self.df['Presion'], bins=20, edgecolor='k')
        plt.title('Histograma de Presión')
        plt.xlabel('Presión')
        plt.ylabel('Frecuencia')

        # Agrega el gráfico al Canvas
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()

        self.current_plot = canvas  # Establece la gráfica actual


    def mostrar_graficos_colision(self):
        if self.current_plot is not None:
            self.current_plot.get_tk_widget().pack_forget()  # Oculta la gráfica actual

        fig = plt.figure(figsize=(10, 2))
        plt.scatter(self.df['Presion'], self.df['Colision'], alpha=0.5)
        plt.title('Gráfico de Dispersión: Presión vs Colisión')
        plt.xlabel('Presión')
        plt.ylabel('Colisión')
        plt.grid(True)

        # Agrega el gráfico al Canvas
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()

        self.current_plot = canvas  # Establece la gráfica actual


    def cerrar_grafica(self):
        if self.current_plot is not None:
            self.current_plot.get_tk_widget().pack_forget()  # Oculta la gráfica actual
            self.current_plot = None

            # Mostrar los botones de gráficos nuevamente
            self.btn_temperatura.pack(side=tk.LEFT, padx=5)
            self.btn_presion.pack(side=tk.LEFT, padx=5)
            self.btn_colision.pack(side=tk.LEFT, padx=5)

            # Mostrar el botón "Siguiente" para cambiar entre gráficos
            self.btn_siguiente.pack(side=tk.TOP, anchor=tk.E)
    
    def cerrar_aplicacion(self):
        self.root.destroy()

    def create_widgets(self):
        # Coloca aquí la creación y configuración de los widgets
        # Por ejemplo:

        self.titulo_label = tk.Label(self.root, text="Monitoreo Smart Garage", font=("Helvetica", 25), fg="white", bg="#003A94")
        self.titulo_label.pack(fill=tk.X, pady=10)

        self.label_archivo = tk.Label(self.root, text="Selecciona un archivo CSV:", pady=5, font=("Helvetica", 12))
        self.label_archivo.pack()

        self.btn_cargar = tk.Button(self.root, text="Cargar Datos", command=self.cargar_datos, padx=10, pady=5, font=("Helvetica", 12), bg="#F95A00", fg="white")
        self.btn_cargar.pack(pady=20)

        # Frame para los botones de opciones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack()

        # Estilo para los botones
        boton_estilo = {
            'font': ('Helvetica', 12),
            'bg': '#005604',  # Cambia el color de fondo a azul para "Temperatura"
            'fg': 'white',  # Cambia el color del texto a blanco
            'padx': 10,
            'pady': 5,
        }

        self.btn_temperatura = tk.Button(frame_botones, text="Temperatura", command=self.mostrar_histograma_temperatura, **boton_estilo)
        self.btn_temperatura.pack(side=tk.LEFT, padx=5)

        # Agrega un espacio horizontal entre los botones
        tk.Label(frame_botones, text=" ").pack(side=tk.LEFT)

        self.btn_presion = tk.Button(frame_botones, text="Presión", command=self.mostrar_graficos_presion, **boton_estilo)
        self.btn_presion.pack(side=tk.LEFT, padx=5)

        # Agrega otro espacio horizontal entre los botones
        tk.Label(frame_botones, text=" ").pack(side=tk.LEFT)

        self.btn_colision = tk.Button(frame_botones, text="Colisión", command=self.mostrar_graficos_colision, **boton_estilo)
        self.btn_colision.pack(side=tk.LEFT, padx=5)

        # Frame para las gráficas con barra de desplazamiento
        self.frame_graficas = tk.Frame(self.root)
        self.frame_graficas.pack(fill=tk.BOTH, expand=True)

        # Reduzcamos el tamaño del frame para las gráficas y centrémoslo
        self.frame_graficas.config(width=400, height=100)
        self.frame_graficas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Configura una función para cerrar la gráfica al presionar el botón "X"
        btn_cerrar = tk.Button(self.frame_graficas, text="X", command=self.cerrar_grafica, font=("Helvetica", 10))
        btn_cerrar.pack(side=tk.TOP, anchor=tk.E)

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizacionApp(root)
    root.mainloop()
