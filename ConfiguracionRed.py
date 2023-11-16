import tkinter as tk
from tkinter import ttk, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from ipaddress import IPv4Network, IPv4Address

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

def calcular_direccionamiento(configuracion):
    
    subredes = []

    hosts_totales = int(configuracion.hosts_por_red + (configuracion.hosts_por_red * (configuracion.crecimiento_red / 100))+configuracion.dispositivos_intermediacion)
    print(f'hosts: {hosts_totales}')

    prefix_length = 32 - (hosts_totales - 2).bit_length() 
    mascara = IPv4Network(f"0.0.0.0/{prefix_length}", strict=False)

    # Calcular la dirección de red inicial
    network_address = IPv4Address("132.255.0.0")  
    network = IPv4Network(f"{network_address}/{mascara.prefixlen}", strict=False)

    for subred in network.subnets(new_prefix=mascara.prefixlen):
        subredes.append(subred)

    return subredes, mascara  

def generar_grafico(subredes):
    G = nx.Graph()
    labels = {}

    for i, subred in enumerate(subredes):
        G.add_node(f"Subred {i + 1}")
        labels[f"Subred {i + 1}"] = str(subred.network_address)


    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    plt.show()

def guardar_subredes(subredes, mascara):
    with open("posibles_subredes.txt", "w") as file:
        file.write("Network Address\tUsable Host Range\tBroadcast Address\tMascara:\n")
        for subred in subredes:
            usable_host_range = f"{subred.network_address + 1} - {subred.network_address + subred.num_addresses - 2}"
            file.write(f"{subred.network_address}\t{usable_host_range}\t{subred.network_address + subred.num_addresses - 1}\t/{mascara.prefixlen}\n")

def mostrar_configuraciones(subredes, mascara):
  
    ventana_configuraciones = tk.Tk()
    ventana_configuraciones.title("Configuraciones de Subredes")

 
    txt_configuraciones = scrolledtext.ScrolledText(ventana_configuraciones, width=80, height=20)
    txt_configuraciones.pack(padx=10, pady=10)

   
    txt_configuraciones.insert(tk.INSERT, "Network Address\tUsable Host Range\tBroadcast Address\tMascara:\n")
    for subred in subredes:
        usable_host_range = f"{subred.network_address + 1} - {subred.network_address + subred.num_addresses - 2}"
        txt_configuraciones.insert(tk.INSERT, f"{subred.network_address}\t{usable_host_range}\t{subred.network_address + subred.num_addresses - 1}\t/{mascara.prefixlen}\n")

    ventana_configuraciones.mainloop()

def guardar_configuracion():
    configuracion.dispositivos_intermediacion = int(dispositivos_intermediacion_entry.get())
    configuracion.hosts_por_red = int(hosts_por_red_entry.get())
    configuracion.uso_dispositivos_personales = uso_dispositivos_personales_var.get()
    configuracion.numero_sedes = int(numero_sedes_entry.get())
    configuracion.subred_por_sede = subred_por_sede_var.get()
    configuracion.crecimiento_red = float(crecimiento_red_entry.get())

   
    respuestas, mascara = calcular_direccionamiento(configuracion)


    generar_grafico(respuestas)

    
    guardar_subredes(respuestas, mascara)

   
    mostrar_configuraciones(respuestas, mascara)


ventana = tk.Tk()
ventana.title("Configuración de Red")


configuracion = ConfiguracionRed()


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


guardar_boton = ttk.Button(ventana, text="Guardar Configuración", command=guardar_configuracion)
guardar_boton.grid(row=8, column=0, columnspan=2, pady=10)


ventana.mainloop()
