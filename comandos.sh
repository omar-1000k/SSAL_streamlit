python3 -m virtualenv venv

source venv/bin/activate

# comandos para instalar todas las dependencias para el proyecto
#dentro del archivo requierements se ponen las librerias pip de instalación
pip install -r requirements.txt

mkdir ~/.streamlit
nano ~/.streamlit/config.toml


## para poder debuguear con streamlit tienes que crear el archivo launch.json de VS code
# reemplazar por lo siguiente:
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [{
        "name": "Streamlit",
        "type": "python",
        "request": "launch",
        "module": "streamlit",
        "env": {
            "STREAMLIT_APP": "${file}",
            "STREAMLIT_ENV": "development"
        },
        "args": [
            "run",
            "${file}"
        ],
        "jinja": true
    }
   ]
}


docker create \
  --name=duckdns \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=America/Mexico_City \
  -e SUBDOMAINS=dbssal.duckdns.org \
  -e TOKEN=d146b234-36be-4b01-ad2c-b2ea23059187 \
  --restart unless-stopped \
  linuxserver/duckdns