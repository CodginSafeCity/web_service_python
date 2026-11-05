import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Ruta principal con información sobre el servicio web."""
    return jsonify({
        "servicio": "Web Service Flask",
        "descripcion": "Microservicio web desarrollado con Python y Flask",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "Información del servicio",
            "GET /health": "Verificación del estado del servicio (Health check)",
            "GET /api/saludo": "Retorna un saludo personalizado (?nombre=<tu_nombre>)",
            "GET /api/info": "Información básica del entorno de ejecución"
        }
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Endpoint de comprobación de salud para monitoreo y orquestación."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


@app.route("/api/saludo", methods=["GET"])
def saludo():
    """Endpoint que procesa un parámetro opcional en la query string."""
    nombre = request.args.get("nombre", "Mundo")
    return jsonify({
        "mensaje": f"¡Hola, {nombre}!",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


@app.route("/api/info", methods=["GET"])
def info():
    """Endpoint que retorna información técnica básica del contenedor/entorno."""
    return jsonify({
        "python_version": os.sys.version.split()[0],
        "entorno": os.getenv("FLASK_ENV", "production"),
        "hostname": os.uname().nodename
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Manejador para rutas no encontradas."""
    return jsonify({
        "error": "Recurso no encontrado",
        "status_code": 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Manejador para errores internos del servidor."""
    return jsonify({
        "error": "Error interno del servidor",
        "status_code": 500
    }), 500


if __name__ == "__main__":
    # Modo desarrollo (para ejecución directa con python app.py)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
