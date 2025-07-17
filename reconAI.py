#!/usr/bin/python3

import subprocess
import sys
import os
import signal
import time
import re 
import json
import threading
from datetime import datetime
from pyfiglet import Figlet

# Ctrl + C
def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def ShowBanner():
    width = 70
    f = Figlet(font='slant')
    banner = f.renderText('reconAI')

    # Añadir sangría
    banner_lines = banner.split('\n')
    centered_banner = '\n'.join(line.center(width) for line in banner_lines)
 
    # Texto adicional
    subtitulo_1 = "**Reconocimiento ofensivo con IA**".center(width)
    subtitulo_2 = "Versión 1.0".center(width)
    subtitulo_3 = "Desarrollado por d4vm4t".center(width)

    # Línea separadora
    separador = "=" * width

    # Mostrar en pantalla
    print(f"\n{separador}\n{centered_banner}\n{subtitulo_1}\n\n{subtitulo_2}\n{subtitulo_3}\n\n{separador}\n")

#Verifica si la IP objetivo esta activa
def CheckConnection(target_ip):
    result = subprocess.run(
        ["timeout", "2", "bash", "-c", f"ping -c 1 {target_ip}"],
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL
    )

    if result.returncode != 0:
        print(f"\n\n[!] La IP {target_ip} no está activa o no se puede establecer la conexión\n[!] Cancelando escaneo\n")
        sys.exit(1)


# Ejecuta el escaneo Nmap sobre la IP indicada
def NmapScan(target_ip, nmap_file):
    print(f"\n\n[+] Iniciando escaneo a {target_ip}...\n")

    nmap_options = ["-p-", "-O", "-sS", "-sC", "-sV", "--min-rate", "5000", "-n", "-Pn"]
    command = ["nmap"] + nmap_options + [target_ip, "-oN", nmap_file]

    # Ejecuta el comando redirigiendo la salida a un archivo
    subprocess.run(command, stdout=subprocess.DEVNULL)

# Extrae el sisitema operativo desde el output del escaneo
def ExtractOS(lines):
    for line in lines:
        if line.startswith("OS details:") or line.startswith("Running:"):
            return line.strip().split(":",1)[1].strip().split(" ",1)[0]
    return "Desconocido"

# Extrae los puertos abiertos, servicios y versión del output del escaneo
def ExtractPorts(lines):
    detected_services = []
    parsing = False

    for line in lines:
        if line.startswith("PORT"):
            parsing = True
            continue 

        if parsing:
            # Filtra por la lineas que contiene el numero del puerto
            if re.match(r"^\d+/[a-z]", line.strip()):
                parts = line.strip().split()
                port = parts[0].split("/")[0]
                service = parts[2]
                version = " ".join(parts[3:]) if len(parts) > 3 else "desconocido"
                
                # Agrega los datos extraidos a la lista de servicios detectados
                detected_services.append({
                    "puerto": port,
                    "servicio": service,
                    "version": version
                })

            elif line.strip() == "" or line.startswith("Service Info:") or line.startswith("Host script results:"):
                break
    
    if detected_services == []:
        print("\n[!] No se ha detectado ningún servicio abierto\n")
        sys.exit(1)

    return detected_services

# Muestra los resultados del escaneo al usuario 
def ShowResults(nmap_file):
    print("[+] Resultados del escaneo:\n")
    
    # Lee el archivo del escaneo 
    with open(nmap_file, "r") as f:
        lines = f.readlines()
    
    # Estrae el SO y los puertos detectados
    operative_system = ExtractOS(lines)
    services = ExtractPorts(lines)

    print(f"Sistema Operativo: {operative_system}\n")
    print(f"Puertos Abiertos:")

    for s in services:
        print(f" · {s['puerto'].ljust(7)}  {s['servicio'].ljust(8)}  {s['version']}")

    return operative_system, services
 
# Construye el prompt que recibira la IA
def BuildPrompt(operative_system, services):
    prompt = ""

    #Rol
    prompt += (
        "Rol:\n"
        "Actúas como un experto en seguridad ofensiva, especializado en pentesting profesional. Tu enfoque es técnico y está orientado a resultados prácticos.\n\n"
    )   

    #Entorno
    prompt += (
        "Entorno:\n"
        "Se ha realizado un escaneo Nmap sobre una máquina remota en un laboratorio de pruebas de pentesting."
        "Los servicios y versiones detectadas están disponibles. No se dispone de acceso físico, solo remoto. "
        "El objetivo es continuar el proceso de reconocimiento y ataque.\n\n"
    )
    
    # Agrega la información del sistema operativo si ha sido detectado
    if operative_system != "Desconocido":
        prompt += f"Sistema operativo detectado: {operative_system}\n\n"

    # Agrega la lista de servicios encontrados
    prompt += "Servicios expuestos:\n"
    for s in services:
        prompt += f" · {s['puerto']} {s['servicio']} {s['version']}\n"

    #Deber
    prompt += (
        "\nDeber:\n"
        "Para cada servicio identificado dentro de la captura de nmap aportada anteriormente, proporciona una guía técnica ofensiva (en base a al versión de los puertos y toda la información relevante que ha reportado el análisis con nmap) bien estructurada que ayude a un pentester a continuar con la fase de enumeración y explotación.\n\n"
    )
    #Instrucciones
    prompt += (
        "Instrucciones:\n"
        "Responde con un bloque para cada servicio, usando exactamente la siguiente estrucutura para cada uno:\n\n"
        "## 🔹 **Servicio <nombre> (<puerto>)**\n"
        "1. 🔍 **Herramientas y comandos de enumeración**: menciona herramientas clave en el ámbito ofensivo como:`nmap`, `hydra`, `gobuster`, `whatweb`, `john`, `burpsuite`, `wfuzz`, `wpscan`, `sqlmap`, `searchsploit`, `msfvenom`, `exploitdb`, `netcat`, `socat`, `chisel`, `impacket`, entre otras. Prioriza aquellas más relevantes y que tengan utilidz real en el servicio o protocolo detectado y proporciona ejemplos prácticos.\n"
        "2. 🧠 **Información que se puede obtener**: versión, usuarios, configuraciones, banners, etc.\n"
        "3. 🧨 **Vectores de ataque ofensivos**: técnicas reales, fuerza bruta, abuso de configuración, CVEs conocidas, etc.\n"
        "4. ⚠️ **Consideraciones prácticas**: consejos útiles para enfocar el servicio, evitar falsos positivos, o priorizar técnicas.\n\n"
        "- Evita redundancias y lenguaje genérico.\n"
        "- Usa bullets y exporta la respuesta en formato markdown siguiendo la estrucutra anterior\n" 
        "- Redacta como si asesoraras a un pentester real en una auditoría.\n\n"
        "- No omitas nigún servicio. Si hay 3 o más, tu respuesta debe contener un bloque con análisis completo por cada servicio. Continua mientras queden servicios por analizar"
    )
    #Feedback
    prompt += (
        "Feedback:\n"
        "Valora si la respuesta ayuda a avanzar técnicamente. Si no aporta valor práctico o no ofrece una estrategia clara, replantea la respuesta con más profundidad ofensiva."
    )    

    return prompt

# Precarga del modelo para una ejecución más rápida
def PreloadModel():
    try:
        subprocess.run(["ollama", "run", "mistral"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except Exception as e:
        print(f"[!] Error al precargar Mistral: {e}")

# Consulta a la IA con el prompt generado
def MistralConsult(prompt):
    try:
        ai_result = subprocess.run(
            ["ollama", "run", "mistral", "&"],
            input = prompt.encode(),
            stdout = subprocess.PIPE,
            stderr = subprocess.DEVNULL
        )

        response = ai_result.stdout.decode()
        return response.strip()

    except Exception as e:
        return f"[!] Error al consultar Mistral: {e}"

# Genera la ruta donde guardar los resutlados del escaneo 
def ScanResponse(results_folder, target_ip):
    os.makedirs(results_folder, exist_ok=True)

    file_name = f"nmap_{target_ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    nmap_file = os.path.join(results_folder, file_name)

    return nmap_file

# Guarda la repuesta de la IA en un archivo en la ruta generada anteriormente
def IAScanRespose(results_folder, response, target_ip):
    file_name = f"ia_recommendations_{target_ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    ai_file = os.path.join(results_folder, file_name)

    with open(ai_file, "w") as f:
        f.write(response)

    print(f"\n\n[+] Recomendaciones de la IA gurdadas en: {ai_file}\n")



def main():

    # Verifica si se ha indicado la IP objetivo como argumento
    if len(sys.argv) != 2:
        print(f"\n\n[+] Uso: python3 {sys.argv[0]} <IP_objetivo>\n")
        sys.exit(1)
       
    target_ip = sys.argv[1]
    results_folder = "results"

    ShowBanner()
    CheckConnection(target_ip)
    nmap_file = ScanResponse(results_folder, target_ip)    

    # Precarga el modelo de IA 
    preload_thread = threading.Thread(target=PreloadModel)
    preload_thread.start()

    # Inicia escaneo con nmap
    NmapScan(target_ip, nmap_file)
  
    # Espera a que cargue el modelo
    preload_thread.join(timeout=5)
    
    # Muestra los resultados y extrae la información 
    operative_system, services = ShowResults(nmap_file)
    print(f"\n[+] Escaneo finalizado. Resultados guardados en: {nmap_file}")
    
    # Construye el prompt
    prompt = BuildPrompt(operative_system, services)
    print("\n\n[+] Consultando a la IA...\n")

    # Consulta a la IA y muestra la respuesta al usuario
    response = MistralConsult(prompt)
    print("[+] Recomendaciones de la IA:\n")
    print(response)

    # Almacena la respuesta de la IA en un archivo
    IAScanRespose(results_folder, response, target_ip)

if __name__ == '__main__':
    main()
