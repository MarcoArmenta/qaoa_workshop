from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from qiskit import QuantumCircuit
from qiskit.primitives import BackendEstimatorV2 as Estimator
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator


def test_function():
    print('Exercises ready!')


def print_solution_graph(graph, x):
    if len(x) != 5:
        raise TypeError('The bitstring x should be of length 5')

    edgecolors = ['#ED3624', '#FA9D00', '#FF00D4', '#006FFF', '#60BA46']
    colors = ['gray' if x[::-1][i] == '1' else 'white' for i in range(len(x))]

    fig, ax = plt.subplots(1, 1, figsize=(6, 6), frameon=False)
    ax.axis('off')
    ax.set_xlim((-1.2, 1.2))
    ax.set_ylim((-1.2, 1.2))

    pos = {
        0: np.array([-1, 0]),
        1: np.array([-0.31, 0.95]),
        2: np.array([-0.31, -0.95]),
        3: np.array([0.81, -0.59]),
        4: np.array([0.81, 0.59])}

    node_size = 1600
    nx.draw_networkx(graph, node_color=colors, node_size=node_size, alpha=1, ax=ax, pos=pos,
                     edgecolors=edgecolors, linewidths=5)


def exercise_superposition_state(qc):
    sol = QuantumCircuit(5)
    sol.h(2)
    sol.x([0, 3, 4])

    unitary_simulator = AerSimulator(method="unitary")

    sol.save_unitary()
    sol_unitary = unitary_simulator.run(sol).result().get_unitary()

    qc.save_unitary()
    qc_unitary = unitary_simulator.run(qc).result().get_unitary()

    if np.allclose(sol_unitary,qc_unitary):
        print("Yes! Your circuit is building the right superposition")

    else:
        print('Sorry! Try running the circuit with the code from the cell above to inspect the counts.')


def exercise_4(cut_value, solution):
    if not isinstance(solution, str):
        raise TypeError("Second variable must be a string.")

    if len(solution) != 5:
        raise TypeError("Second variable must be a string of size 5.")

    if not isinstance(cut_value, int):
        raise TypeError('First variable must be an integer.')

    if cut_value < 0:
        raise TypeError('First variable must be greater than zero.')

    graph = [(0, 1), (0, 2), (1, 2), (2, 3), (1, 4), (3, 4)]
    x = solution[::-1]
    cut = 0

    for i, j in graph:
        if x[i] != x[j]:
            cut += 1

    if abs(cut - cut_value) < 0.5:
        print('Yes! This is the cut value of the given solution.')

    else:
        print('Sorry! This is not the right answer. Try counting again!')


def eval_observable_on_state(observable, state_circuit, backend):
    estimator = Estimator(backend=backend)
    result = estimator.run([[state_circuit, observable]]).result()[0]
    return result.data.evs


def exercise_gain_operator(gain_op):
    data = ["IIIZZ", "IIZIZ", "IIZZI", "ZIIZI", "IZZII", "ZZIII", "IIIII"]
    coeffs = [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5*6]

    sol = SparsePauliOp(data=data, coeffs=coeffs)

    if gain_op == sol:
        print('Yes! This is the correct gain operator')

    else:
        print('Sorry! This is not the right operator')


def exercise_average_gain(average):
    if abs(average - 4.0) < 0.1:
        print('Yes! This is the correct circuit')

    else:
        print('Sorry! This is not the right answer. Remember you can print the circuit to inspect it.')
