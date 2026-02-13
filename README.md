# EmmanuelBello-20241369-STP-Attack
# STP Claim Root Bridge Attack

**Estudiante:** Emmanuel Bello Sierra
**Matrícula:** 2024-1369
**Asignatura:** Seguridad en Redes (ITLA)

## 1. Descripción y Objetivo del Script
Este proyecto demuestra un ataque al protocolo **Spanning Tree Protocol (STP)**. El objetivo es forzar una re-convergencia de la topología de red de Capa 2 para que la máquina atacante sea elegida como el **Root Bridge** (Puente Raíz).

El script inyecta paquetes BPDU (Bridge Protocol Data Units) falsificados, anunciando una **Prioridad de Puente de 0** (la mejor posible) y un costo de ruta de 0. Dado que los switches Cisco por defecto tienen una prioridad de 32768, el switch legítimo cede su rol de Root, permitiendo al atacante atraer tráfico y controlar la topología.

## 2. Topología de Red
* **Switch Víctima:** Cisco IOS (Prioridad 32768).
* **Atacante:** Ubuntu con Scapy (Anuncia Prioridad 0).
* **Enlace:** Conexión troncal o de acceso en la interfaz `ens3`.

<img width="1090" height="634" alt="Captura de pantalla 2026-02-13 143348" src="https://github.com/user-attachments/assets/c6213eae-2dd4-418a-a9e6-47351912a0d1" />


## 3. Requisitos para Ejecutar
* **Python 3 + Scapy.**
* **Acceso a la red física** (o virtual en PNETLab).
* **Permisos de Root.**

## 4. Parámetros Utilizados
* **Interfaz:** `ens3`
* **Root ID (Priority):** `0` (Superior a 32768).
* **Bridge ID:** `0`
* **Path Cost:** `0`
* **BPDU Type:** Configuration BPDU (0x00).

## 5. Evidencia de Funcionamiento

### Estado Original (Root es Cisco)
<img width="594" height="354" alt="image" src="https://github.com/user-attachments/assets/121727a3-a999-4c33-8eb0-6a322b8ab51c" />


### Resultado (Root es el Atacante)
<img width="646" height="389" alt="image" src="https://github.com/user-attachments/assets/694baa2b-8652-4fa1-94f0-d647142ae990" />


## 6. Video Demostrativo
Explicación detallada y demostración del cambio de topología:
👉 https://www.youtube.com/watch?v=eUiK5xAz_TM

## 7. Medidas de Mitigación
Para evitar que dispositivos no autorizados alteren la topología STP, se deben implementar **Root Guard** y **BPDU Guard**.

**Configuración en Cisco IOS:**
```bash
! En puertos de acceso de usuarios finales
Switch(config)# interface Gi0/1
Switch(config-if)# spanning-tree bpduguard enable
! Si se recibe un BPDU, el puerto se apaga.

! En puertos donde podría conectarse otro switch pero no debe ser Root
Switch(config)# interface Gi0/2
Switch(config-if)# spanning-tree guard root
