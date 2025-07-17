# ReconAI
**Reconocimiento ofensivo asisitdo por IA**

## ¿Qué es reconAI?
`reconAI` es una herramienta que automatiza la fase de reconocimiento ofensivo mediante un escaneo avanzado con `nmap`, extrayendo información clave (sistema operativo, servicios, versiones) y generando un análisis técnico mediante IA (modelo Mistral) para ayudar al pentester a continuar con la fase de enumeración y explotación de forma estructurada y eficaz.

## Requisitos
- Python 3.x
- [Nmap](https://nmap.org/)
- [Ollama](https://ollama.com/) con el modelo Mistral disponible

## Instalación
```bash
git clone https://github.com/d4vm4t/reconAI
cd reconAI
pip install -r requirements.txt
```

### Instalación y configuración de Ollama + Mistral
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
Después, ejecuta:
```bash
ollama pull mistral
```
  Este comando descargará y preparará el modeo de IA `Mistral`, que será usado localmente por la herramienta.

## Ejecución
```bash
python3 reconAI.py <IP_objetivo>
```
Ejemplo:
```bash
python3 reconAI.py 10.10.10.123
```

Al finalizar el escaneo se generarán dos archivos diferentes almacenados en la carpeta `results`:
- La captura de Nmap: `nmap_<IP>_<timestamp>.txt`
- La guía técnica generada por la IA: `ia_recommendations_<IP>_<timestamp>.md`

## Model IA
Este proyecto utiliza el modelo de Inteligencia Artifical Mistral vía Ollama para interpretar y ofrecer sugerencias técnicas ofensivas en formato Markdown. La estructura de salida está formada por herramientas, vectores de ataque y consideraciones específicas para cada servicio identificado.
