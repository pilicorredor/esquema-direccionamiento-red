import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ipaddress import IPv4Network, IPv4Address
import random
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class ConfiguracionRed:
    def __init__(self):
        self.numero_sedes = 0
        self.subred_por_sede = True
        self.configuraciones_sedes = []
        self.ipclasea = "10.4.1.0"
        self.ipclaseb = "144.168.1.0"
        self.ipclaseac = "192.168.1.0"
       

    def calcular_mascara_red(self, total_hosts):
        bits_necesarios = 0
        while 2 ** bits_necesarios - 2 < total_hosts:
            bits_necesarios += 1

        mascara_subred = 32 - bits_necesarios
        mascara = IPv4Network(f"0.0.0.0/{mascara_subred}", strict=False)
        return mascara

    def preguntar_empleados(self, sede, indice):
        if sede.uso_dispositivos_personales:
            sede.cantidad_empleados = simpledialog.askinteger(f"Sede {indice + 1}", f"Ingrese la cantidad de empleados en {sede.nombre_sede}:")

        sede.cantidad_dispositivos_intermediacion = simpledialog.askinteger(f"Sede {indice + 1}", f"Cantidad de dispositivos Gestionables de intermediación en {sede.nombre_sede}:")
        sede.crecimiento_5_anios = simpledialog.askfloat(f"Sede {indice + 1}", f"Crecimiento a 5 años en {sede.nombre_sede} (%):")

    def calcular_hosts_totales(self, sede):
        cantidad_base = sede.cantidad_hosts + sede.cantidad_dispositivos_intermediacion

        if sede.uso_dispositivos_personales:
            cantidad_base += sede.cantidad_empleados

        return cantidad_base * ( 1+sede.crecimiento_5_anios / 100)
    
    def generar_subred_personalizada(self, sede):
        ip_base = None
        clase = sede.clasificacion_ip

        if clase == 'A':
            ip_base = self.ipclasea
        elif clase == 'B':
            ip_base = self.ipclaseb
        elif clase == 'C':
            ip_base = self.ipclaseac
        else:
            return None

        ip_lista = list(map(int, ip_base.split('.')))

        for i in range(1, 4):
            ip_lista[i] = random.randint(1, 254)

        subred_personalizada = '.'.join(map(str, ip_lista))
        return subred_personalizada

    def verificar_y_mostrar_subredes(self):
        ventana_sedes = tk.Toplevel()
        ventana_sedes.title("Resumen de Configuraciones de Sedes")

        fig, ax = plt.subplots()

        for i, sede in enumerate(self.configuraciones_sedes):
            total_hosts = math.ceil(self.calcular_hosts_totales(sede))
            mascara = self.calcular_mascara_red(total_hosts)

            subred_personalizada = self.generar_subred_personalizada(sede)
            if not subred_personalizada:
                messagebox.showwarning("Advertencia", f"No se pudo generar la subred para la Sede {i + 1}")
                continue

            red = IPv4Network(f"{subred_personalizada}/{mascara.prefixlen}", strict=False)
            rango_hosts = f"{red.network_address + 1} - {red.broadcast_address - 1}"
            broadcast = red.broadcast_address
            sub= red.network_address
            th= red.num_addresses-2
            
            puerta_enlace = red.network_address + 1

            frame_sede = ttk.Frame(ventana_sedes)
            frame_sede.grid(row=i // 4, column=i % 4, padx=10, pady=5, sticky="W")

            texto_sede = (
                f"Sede {i + 1}\n"
                f"Nombre de Sede: {sede.nombre_sede}\n"
                f"Cantidad de Hosts: {sede.cantidad_hosts}\n"
                f"Los empleados pueden usar dispositivos: {'Sí' if sede.uso_dispositivos_personales else 'No'}\n"
            )

            if sede.uso_dispositivos_personales:
                texto_sede += (
                    f"Cantidad de Empleados: {sede.cantidad_empleados}\n"
                )
            texto_sede += f"Cantidad de Dispositivos de Intermediación Gestionables: {sede.cantidad_dispositivos_intermediacion}\n"
            texto_sede += f"Crecimiento a 5 años: {sede.crecimiento_5_anios}%\n"
            texto_sede += f"Clasificación IP: {sede.clasificacion_ip}\n"
            texto_sede += f"Número Total de Hosts de la red: {total_hosts}\n"
            texto_sede += f"Mascara Red: /{mascara.prefixlen}\n"
            texto_sede += f"Subred Asignada: {sub}\n"
            texto_sede += f"Rango de Hosts: {rango_hosts}\n"
            texto_sede += f"Broadcast de la Subred: {broadcast}\n"
            texto_sede += f"Puerta de Enlace de la Subred: {puerta_enlace}\n\n"

            sede_label = ttk.Label(frame_sede, text=texto_sede, justify="left")
            sede_label.grid(row=i % 4, column=0, padx=10, pady=5, sticky="W")

            datos = {
                'Nombre Subred': sede.nombre_sede,
                'IP Subred': sub,
                'Rango Subred': rango_hosts,
                'Broadcast': broadcast,
                'Mascara': f"/{mascara.prefixlen}",
                'Total ip usables': th,
                'Total hosts red': total_hosts
            }
            info = '\n'.join([f"{key}: {datos[key]}" for key in datos.keys()])
            circulo = Circle((i % 4 * 2.5, -i // 4 * 2.5), 0.8, color='#E1E6FA', fill=True, zorder=2)
            ax.add_patch(circulo)
            ax.text(i % 4 * 2.5, -i // 4 * 2.5, info, ha='center', va='center', fontsize=8, color='black', zorder=3)

        ax.set_xlim(-2, 12)
        ax.set_ylim(-6, 2)
        ax.set_aspect('equal', adjustable='datalim')
        ax.axis('off')

        plt.show()

    def guardar_configuracion(self):
        self.numero_sedes = int(numero_sedes_entry.get())
        self.subred_por_sede = self.subred_por_sede

        for i in range(self.numero_sedes):
            sede = ConfiguracionSede()
            sede.nombre_sede = simpledialog.askstring(f"Sede {i + 1}", f"Ingrese el nombre de la sede {i + 1}:")
            sede.cantidad_hosts = simpledialog.askinteger(f"Sede {i + 1}", f"Ingrese la cantidad de hosts para {sede.nombre_sede}:")
            sede.uso_dispositivos_personales = messagebox.askyesno(f"Sede {i + 1}", f"¿Las personas en {sede.nombre_sede} pueden usar dispositivos personales?")

            self.preguntar_empleados(sede, i)

            sede.clasificacion_ip = simpledialog.askstring(f"Sede {i + 1}", f"Seleccione la clasificación de IP para {sede.nombre_sede} (A, B, o C):")
            self.configuraciones_sedes.append(sede)

        if self.subred_por_sede:
            self.verificar_y_mostrar_subredes()

class ConfiguracionSede:
    def __init__(self):
        self.nombre_sede = ""
        self.cantidad_hosts = 0
        self.uso_dispositivos_personales = False
        self.cantidad_empleados = 0
        self.cantidad_dispositivos_intermediacion = 0
        self.crecimiento_5_anios = 0
        self.clasificacion_ip = ""

ventana = tk.Tk()
ventana.title("Configuración de Red")

numero_sedes_label = ttk.Label(ventana, text="¿Cuántas sedes tiene la empresa?:")
numero_sedes_label.grid(row=0, column=0, padx=10, pady=5, sticky="E")

numero_sedes_entry = ttk.Entry(ventana)
numero_sedes_entry.grid(row=0, column=1, padx=10, pady=5)


configuracion = ConfiguracionRed()

guardar_boton = ttk.Button(ventana, text="Guardar Configuración", command=configuracion.guardar_configuracion)
guardar_boton.grid(row=2, column=0, columnspan=2, pady=10)

ventana.mainloop()
