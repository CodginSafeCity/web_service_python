# Imagen base ligera oficial de Python
FROM python:3.12-slim

# Evitar la creación de archivos .pyc y asegurar salida directa de logs a la consola
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Directorio de trabajo de la aplicación
WORKDIR /app

# Crear un usuario no privilegiado para mayor seguridad
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Instalar dependencias primero para aprovechar el sistema de capas y caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la aplicación
COPY app.py .

# Asignar permisos al usuario no root
RUN chown -R appuser:appgroup /app
USER appuser

# Exponer el puerto configurado
EXPOSE 5000

# Comprobación de salud (Health Check) utilizando la librería estándar de Python
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Comando por defecto para iniciar la aplicación con Gunicorn (servidor WSGI para producción)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
