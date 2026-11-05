# Web Service con Python, Flask y Docker

Este proyecto implementa un servicio web (microservicio REST API) desarrollado en **Python** utilizando el framework **Flask**, y empaquetado para su distribución y despliegue aislado mediante **Docker**.

---

## 📁 Estructura del Proyecto

```text
web_service_python/
├── app.py                # Código fuente del servicio web (Flask)
├── requirements.txt      # Dependencias de Python (Flask, Gunicorn)
├── Dockerfile            # Instrucciones para la construcción de la imagen Docker
├── .dockerignore         # Archivos excluidos del contexto de Docker
├── docker-compose.yml    # Orquestación sencilla con Docker Compose
└── README.md             # Documentación del proyecto
```

---

## 🚀 1. Desarrollo: Endpoints del Web Service

La aplicación expone los siguientes endpoints HTTP:

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/` | Información general del servicio y catálogo de endpoints |
| `GET` | `/health` | Health check para orquestadores y monitoreo |
| `GET` | `/api/saludo?nombre=...` | Saludo personalizado dinámico (parámetro opcional `nombre`) |
| `GET` | `/api/info` | Información técnica del entorno de ejecución |

---

## 🐳 2. Contenerización y Ejecución

### Opción A: Ejecutar con Docker (Recomendado)

1. **Construir la imagen de Docker**:
   ```bash
   docker build -t web-service-flask .
   ```

2. **Ejecutar el contenedor**:
   ```bash
   docker run -d -p 5000:5000 --name mi_servicio_flask web-service-flask
   ```

3. **Verificar el estado del contenedor**:
   ```bash
   docker ps
   ```

4. **Ver los logs en tiempo real**:
   ```bash
   docker logs -f mi_servicio_flask
   ```

5. **Detener y eliminar el contenedor**:
   ```bash
   docker stop mi_servicio_flask && docker rm mi_servicio_flask
   ```

---

### Opción B: Ejecutar con Docker Compose

1. **Iniciar el servicio**:
   ```bash
   docker compose up -d --build
   ```

2. **Detener el servicio**:
   ```bash
   docker compose down
   ```

---

### Opción C: Ejecución Local Directa (Sin Docker)

1. **Crear y activar un entorno virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar la aplicación**:
   ```bash
   python app.py
   ```
   La aplicación quedará disponible en `http://localhost:5000`.

---

## 🧪 Pruebas del Servicio Web

Puedes probar los endpoints usando `curl` o desde cualquier navegador web:

```bash
# 1. Consulta al endpoint raíz
curl -s http://localhost:5000/ | jq

# 2. Comprobación de salud
curl -s http://localhost:5000/health | jq

# 3. Saludo personalizado
curl -s "http://localhost:5000/api/saludo?nombre=Estudiante" | jq

# 4. Información del entorno
curl -s http://localhost:5000/api/info | jq
```

---

## 🔒 Buenas Prácticas Aplicadas

- **Imagen base ligera (`python:3.12-slim`)**: Minimiza el tamaño de la imagen y reduce la superficie de ataque.
- **Usuario no privilegiado (`appuser`)**: El contenedor no se ejecuta como `root`.
- **Servidor WSGI de producción (`Gunicorn`)**: Manejo adecuado de concurrencia y conexiones en producción.
- **Healthcheck nativo**: Integrado en el `Dockerfile` para supervisión de salud.
- **Caché óptimo de capas**: Se copian las dependencias antes del código fuente.
