 🔹 **Servicio ssh (22)**
1. 🔍 **Herramientas y comandos de enumeración**: Utiliza `nmap` para obtener información básica sobre el servicio:
    ```
    nmap -p 22 <IP_REMOTA> --script ssh-brute,ssh-hostinfo,vuln
    ```
   - El script `ssh-brute` intentará acceder al servicio mediante enumeración de contraseñas.
   - `ssh-hostinfo` proporciona información general sobre el host y su configuración.
   - `vuln` busca vulnerabilidades conocidas en el servidor ssh.
2. 🧠 **Información que se puede obtener**: Obtendrá la versión del servicio OpenSSH (7.9p1 Debian 10+deb10u2), la configuración de la conexión, y posiblemente el nombre del sistema operativo (Debian).
3. 🧨 **Vectores de ataque ofensivos**:
   - Fuerza bruta contra las credenciales mediante `hydra` o `john the ripper`.
   - Exploitando vulnerabilidades conocidas en la versión del servicio ssh (cambia la fecha, abuso de SSHREF, etc.). Para esto, busca información sobre CVEs aplicables en el servidor utilizando `searchsploit`.
4. ⚠️ **Consideraciones prácticas**:
   - Intenta usar palabras pascales y listas de palabras comunes para la fuerza bruta. Evita intentos repetidos innecesarios que puedan alertar al sistema.
   - Prefiere atacar servicios no protegidos con encriptación o restringida a ciertos usuarios, y busca vulnerabilidades en el servidor ssh antes de intentar acceder mediante fuerza bruta.

---

🔹 **Servicio http (80)**
1. 🔍 **Herramientas y comandos de enumeración**: Utiliza `nmap` para obtener información básica sobre el servicio:
    ```
    nmap -p 80 <IP_REMOTA> --script http-methods,http-header,http-robots.txt
    ```
   - `http-methods` proporciona una lista de métodos HTTP y versiones del protocolo.
   - `http-header` busca información en los encabezados HTTP.
   - `http-robots.txt` identifica las direcciones prohibidas o limitadas para el roboteo.
2. 🧠 **Información que se puede obtener**: Obtendrá la versión del servidor Apache (2.4.38), información general sobre el servidor, y posiblemente directorios protegidos o prohibidos.
3. 🧨 **Vectores de ataque ofensivos**:
   - Exploitando vulnerabilidades conocidas en la versión del servidor Apache (cambia la fecha, inyección SQL, etc.). Para esto, busca información sobre CVEs aplicables en el servidor utilizando `searchsploit`.
   - Intentar obtener acceso mediante fuerza bruta o inyección de código, especialmente en las direcciones protegidas o prohibidas identificadas. Utiliza herramientas como `gobuster` para buscar directorios y archivos y `w3af` para realizar análisis avanzados en el servidor web.
4. ⚠️ **Consideraciones prácticas**:
   - Intenta obtener información adicional sobre el sitio web y sus posibles vulnerabilidades mediante la búsqueda de fuentes externas (Google Dorks, Shodan, Censys, etc.).
   - Prefiere atacar servicios no protegidos con encriptación o restringida a ciertos usuarios, y busca vulnerabilidades en el servidor antes de intentar acceder mediante fuerza bruta o inyección de código. 