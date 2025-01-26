from flask import render_template, request, jsonify
import numpy as np
from src.gates import apply_gate
from src.emulator import measure_probabilities
from src.circuits import run_grover, run_deutsch_jozsa
from src.algorithms import solve_qubo

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/algorithms')
    def algorithms():
        return render_template('algorithms.html')

    @app.route('/run_algorithm', methods=['POST'])
    def run_algorithm():
        data = request.json
        algorithm = data['algorithm']
        num_qubits = int(data['num_qubits'])

        if algorithm == 'Grover':
            target_state = data['target_state']
            result = run_grover(target_state)
        elif algorithm == 'Deutsch-Jozsa':
            result = run_deutsch_jozsa(num_qubits)
        elif algorithm in ['QUBO', 'QAOA']:
            Q = np.array(data['Q'])
            p = data.get('p', 1)
            solution, cost = solve_qubo(Q, p)
            return jsonify({'solution': solution.tolist(), 'cost': cost})
        else:
            return jsonify({'error': 'Invalid algorithm selected.'})

        return jsonify({'result': result})

    @app.route('/run_circuit', methods=['POST'])
    def run_circuit():
        data = request.json
        num_qubits = data['num_qubits']
        circuit = data['circuit']

        state = np.zeros(2**num_qubits, dtype=complex)
        state[0] = 1

        for gate in circuit:
            if gate['type'] == 'CNOT':
                control = gate['qubit']
                target = (control + 1) % num_qubits
                state = apply_gate('CNOT', {'control': control, 'target': target}, state, num_qubits)
            else:
                state = apply_gate(gate['type'], {'qubit': gate['qubit']}, state, num_qubits)

        probabilities = measure_probabilities(state)
        results = [{'state': f"{i:0{num_qubits}b}", 'probability': float(prob)} for i, prob in enumerate(probabilities)]

        return jsonify(results)

    # Autres routes
    @app.route('/quantum_walk')
    def quantum_walk():
        return render_template('quantum_walk.html')
