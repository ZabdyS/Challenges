import requests
from collections import defaultdict
import re

# Descargar el archivo de registro
url = "https://pastebin.com/raw/gstGCJv4"
response = requests.get(url)
log_content = response.text

# Inicializar contadores
url_count = 0
non_200_count = 0
total_non_200_count = 0
put_request_count = 0
ip_address_count = defaultdict(int)

# Analizar el contenido del archivo de registro línea por línea
for line in log_content.split("\n"):
    if "/production/file_metadata/modules/ssh/sshd_config" in line:
        url_count += 1
        if " 200 " not in line:
            non_200_count += 1
    if "/dev/report/" in line and "PUT" in line:
        put_request_count += 1
    if re.match(r'^(\d{1,3}\.){3}\d{1,3}', line):  # Buscar dirección IP
        ip = re.match(r'^(\d{1,3}\.){3}\d{1,3}', line).group()
        ip_address_count[ip] += 1
        if "/dev/report/" in line and "PUT" in line:
            if " 200 " not in line:  # Verificar si el código de respuesta no es 200
                total_non_200_count += 1

# Imprimir resultados
print("URL '/production/file_metadata/modules/ssh/sshd_config' fetched:", url_count, "times")
print("Number of times the return code from Apache was not 200 for the URL:", non_200_count)
print("Total number of times Apache returned any code other than 200:", total_non_200_count)
print("Total number of times that any IP address sent a PUT request to a path under '/dev/report/':", put_request_count)
print("Breakdown of PUT requests by IP address:")
for ip, count in ip_address_count.items():
    print("IP:", ip, "- Count:", count)

# URL del archivo de registro
url = "https://pastebin.com/raw/gstGCJv4"

# Descargar el archivo de registro
log_file = descargar_archivo(url)

# Analizar el archivo de registro
analizar_archivo(log_file)
