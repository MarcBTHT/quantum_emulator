from flask import Flask, render_template, request, jsonify
from src.routes import register_routes
import numpy as np

app = Flask(__name__)

# Gestion globale des erreurs
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {e}")
    return jsonify(error=str(e)), 500

# Définir les routes principales
register_routes(app)

if __name__ == "__main__":
    app.run(debug=False)