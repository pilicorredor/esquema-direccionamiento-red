import tkinter as tk
from tkinter import ttk

class ConfiguracionRed:
    def __init__(self):
        self.subredes = 0
        self.dispositivos_por_segmento = 0
        self.dispositivos_intermediacion = 0
        self.hosts_por_red = 0
        self.uso_dispositivos_personales = False
        self.numero_sedes = 0
        self.subred_por_sede = False
        self.crecimiento_red = 0

def guardar_configuracion():
    configuracion.subredes = int(subredes_entry.get())
    configuracion.dispositivos_por_segmento = int(dispositivos_por_segmento_entry.get())
    configuracion.dispositivos_intermediacion = int(dispositivos_intermediacion_entry.get())
    configuracion.hosts_por_red = int(hosts_por_red_entry.get())
    configuracion.uso_dispositivos_personales = uso_dispositivos_personales_var.get()
    configuracion.numero_sedes = int(numero_sedes_entry.get())
    configuracion.subred_por_sede = subred_por_sede_var.get()
    configuracion.crecimiento_red = float(crecimiento_red_entry.get())

    # Aquí puedes imprimir o manejar la configuración según tus necesidades
    print("\nConfiguración de la Red:")
    print(f"Subredes o segmentos: {configuracion.subredes}")
    print(f"Dispositivos por segmento: {configuracion.dispositivos_por_segmento}")
    print(f"Dispositivos de intermediación: {configuracion.dispositivos_intermediacion}")
    print(f"Hosts por red: {configuracion.hosts_por_red}")
    print(f"Uso de dispositivos personales: {configuracion.uso_dispositivos_personales}")
    print(f"Número de sedes: {configuracion.numero_sedes}")
    print(f"Subred por sede: {configuracion.subred_por_sede}")
    print(f"Crecimiento de la red en 5 años: {configuracion.crecimiento_red}%")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Configuración de Red")

# Crear objeto ConfiguracionRed
configuracion = ConfiguracionRed()

# Crear etiquetas y campos de entrada
subredes_label = ttk.Label(ventana, text="¿Cuántas subredes o segmentos que va a tener su red?: ")
subredes_entry = ttk.Entry(ventana)

dispositivos_por_segmento_label = ttk.Label(ventana, text="Cuántos dispositivos tendrá cada segmento de su red?: ")
dispositivos_por_segmento_entry = ttk.Entry(ventana)

dispositivos_intermediacion_label = ttk.Label(ventana, text="¿Cuántos dispositivos de intermediación utilizará?: ")
dispositivos_intermediacion_entry = ttk.Entry(ventana)

hosts_por_red_label = ttk.Label(ventana, text="¿Cuál es la cantidad de hosts que desea conectar a la red?: ")
hosts_por_red_entry = ttk.Entry(ventana)

uso_dispositivos_personales_label = ttk.Label(ventana, text="¿Los trabajadores pueden usar los dispositivos personales?: ")
uso_dispositivos_personales_var = tk.BooleanVar()
uso_dispositivos_personales_checkbox = ttk.Checkbutton(ventana, variable=uso_dispositivos_personales_var)

numero_sedes_label = ttk.Label(ventana, text="¿Cuántas sedes de la empresa tiene?: ")
numero_sedes_entry = ttk.Entry(ventana)

subred_por_sede_label = ttk.Label(ventana, text="¿Quiere que cada sede tenga una subred distinta?: ")
subred_por_sede_var = tk.BooleanVar()
subred_por_sede_checkbox = ttk.Checkbutton(ventana, variable=subred_por_sede_var)

crecimiento_red_label = ttk.Label(ventana, text="¿En un lapso de 5 años, cuál es el porcentaje de crecimiento para la red? (%):")
crecimiento_red_entry = ttk.Entry(ventana)

# Colocar etiquetas y campos de entrada en la ventana
subredes_label.grid(row=0, column=0, padx=10, pady=5, sticky="E")
subredes_entry.grid(row=0, column=1, padx=10, pady=5)

dispositivos_por_segmento_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
dispositivos_por_segmento_entry.grid(row=1, column=1, padx=10, pady=5)

dispositivos_intermediacion_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
dispositivos_intermediacion_entry.grid(row=2, column=1, padx=10, pady=5)

hosts_por_red_label.grid(row=3, column=0, padx=10, pady=5, sticky="E")
hosts_por_red_entry.grid(row=3, column=1, padx=10, pady=5)

uso_dispositivos_personales_label.grid(row=4, column=0, padx=10, pady=5, sticky="E")
uso_dispositivos_personales_checkbox.grid(row=4, column=1, padx=10, pady=5, sticky="W")

numero_sedes_label.grid(row=5, column=0, padx=10, pady=5, sticky="E")
numero_sedes_entry.grid(row=5, column=1, padx=10, pady=5)

subred_por_sede_label.grid(row=6, column=0, padx=10, pady=5, sticky="E")
subred_por_sede_checkbox.grid(row=6, column=1, padx=10, pady=5, sticky="W")

crecimiento_red_label.grid(row=7, column=0, padx=10, pady=5, sticky="E")
crecimiento_red_entry.grid(row=7, column=1, padx=10, pady=5)

# Botón para guardar configuración
guardar_boton = ttk.Button(ventana, text="Guardar Configuración", command=guardar_configuracion)
guardar_boton.grid(row=8, column=0, columnspan=2, pady=10)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
