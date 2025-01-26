from flask import render_template, request, jsonify
import numpy as np
from src.gates import apply_gate
from src.emulator import measure_probabilities
from src.circuits import run_grover, run_deutsch_jozsa
from src.algorithms import solve_qubo

def register_routes(app):
    @app.route('/')
    def index():
        return "This is a simple response. Flask is working!"