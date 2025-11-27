from aima.search import hill_climbing, simulated_annealing, exp_schedule
from azamon_problem import *
from azamon_state import *
from timeit import timeit
from abia_azamon import *
from azamon_problem_1 import *
from azamon_problem_2 import *
from azamon_problem_sa import *
from azamon_problem_sa_cost import *
from statistics import mean

import math
import random

'''def simulated_annealing_with_print(problem, schedule):
    current = problem.initial
    current_heuristic = problem.value(current)
    
    for t in range(1, 5001):  # Límite de iteraciones
        T = schedule(t)
        if T == 0:
            break
        
        next_state = random.choice(list(problem.neighbors(current)))
        next_heuristic = problem.value(next_state)
        delta_e = next_heuristic - current_heuristic
        probabilidad_aceptar_peor = math.exp(delta_e / T) if delta_e < 0 else 0

        # Decidir si se acepta el estado siguiente
        if delta_e > 0 or random.uniform(0, 1) < probabilidad_aceptar_peor:
            current = next_state
            current_heuristic = next_heuristic
            print(-current_heuristic)      

    return current

def exp_schedule1(t, k=1, lam=0.0005):
    return k * math.exp(-lam * t)'''


'''def hill_climbing(problem):
    current = problem.initial
    while True:
        neighbors = problem.neighbors(current)
        if not neighbors:
            break
        next_state = max(neighbors, key=lambda x: problem.value(x))
        
        # Imprimir el heurístico del vecino elegido
        print(-problem.value(next_state))
        
        if problem.value(next_state) <= problem.value(current):
            break
        current = next_state
    return current'''

def inspeccionar(list):
    for i in list:
        print(i)

if __name__ == '__main__':
    npaq = int(input("Numero de paquetes: "))
    semilla = int(input("Semilla aleatoria: "))
    paquetes = random_paquetes(npaq, semilla)
    ofertas = random_ofertas(paquetes, 1.2, 1234)
    inspeccionar(ofertas)
    inspeccionar(paquetes)
    estado_inicial = generate_initial_state(ofertas, paquetes)
    #times = [timeit(lambda: generate_initial_state(ofertas, paquetes), number=1) for _ in range(15)]
    #print(times, mean(times))
    print('ESTADO INICIAL ALEATORIO:')
    print(estado_inicial)
    print('Heurístico de costes del estado incial: ',estado_inicial.heuristic_costes())
    print('Heurístico de felicidad del estado incial: ',estado_inicial.heuristic_felicidad())
    print('Heurístico de costes y felicidad del estado incial: ',estado_inicial.heuristic())
    estado_inicial2 = generate_initial_state_ordenat(ofertas, paquetes)
    times = [timeit(lambda: generate_initial_state_ordenat(ofertas, paquetes), number=1) for _ in range(15)]
    print('ESTADO INICIAL ORDENADO:')
    print(estado_inicial2)
    print('Heurístico de costes del estado incial: ',estado_inicial2.heuristic_costes())
    print('Heurístico de felicidad del estado incial: ',estado_inicial2.heuristic_felicidad())
    print('Heurístico de costes y felicidad del estado incial: ',estado_inicial2.heuristic())
    print()

    print('**************************HILL CLIMBING***************************')
    n_h = hill_climbing(AzamonProblem(estado_inicial))
    #n_h1 = hill_climbing(AzamonProblem(estado_inicial2))
    n_fel_h = hill_climbing(AzamonProblem1(estado_inicial))
    n_cost_h = hill_climbing(AzamonProblem2(estado_inicial))
    print('SOLUCIÓN TENIENDO EN CUENTA COSTES Y FELICIDAD:')
    print(n_h)
    print('Heurístico: ', n_h.heuristic())
    print('SOLUCIÓN TENIENDO EN CUENTA COSTES:')
    print(n_cost_h)
    print('Heurístico: ', n_cost_h.heuristic_costes())    
    print('SOLUCIÓN TENIENDO EN CUENTA FELICIDAD:')
    print(n_fel_h)
    print('Heurístico: ', n_fel_h.heuristic_felicidad())   
    print()


    print('**************************SIMULATED ANNEALING***************************')
    n_sa = simulated_annealing(AzamonProblemSa(estado_inicial), schedule=exp_schedule(k=1, lam=0.0005, limit=5000))
    print('SOLUCIÓN TENIENDO EN CUENTA COSTES Y FELICIDAD:')
    print(n_sa)
    print('Heurístico: ', n_sa.heuristic())
    print()
    #n_sa_cost = simulated_annealing(AzamonProblemSaCost(estado_inicial), schedule=exp_schedule(k=1, lam=0.0005, limit=5000))


    print('!!!!!!!!!!!!!!!!!!!!!!!!!TEMPS EXECUCIO!!!!!!!!!!!!!!!!!!!!!')
    times = [timeit(lambda: generate_initial_state(ofertas, paquetes), number=1) for _ in range(15)]
    print('Generar estado inicial aleatorio', mean(times))
    times = [timeit(lambda: generate_initial_state_ordenat(ofertas, paquetes), number=1) for _ in range(15)]
    print('Generar estado inicial ordenado', mean(times))
    times = [timeit(lambda: hill_climbing(AzamonProblem(estado_inicial)), number=1) for _ in range(15)]
    print('Ejecutar Hill Climbing', mean(times))
    times = [timeit(lambda: hill_climbing(AzamonProblem2(estado_inicial)), number=1) for _ in range(15)]
    print('Ejecutar Hill Climbing teniendo en cuenta solo costes', mean(times))
    times = [timeit(lambda: hill_climbing(AzamonProblem1(estado_inicial)), number=1) for _ in range(15)]
    print('Ejecutar Hill Climbing teniendo en cuenta solo felicidad', mean(times))
    times = [timeit(lambda: simulated_annealing(AzamonProblemSaCost(estado_inicial), schedule=exp_schedule(k=1, lam=0.0005, limit=5000)), number=1)for _ in range(5)]
    print('Ejecutar Simulated Annealing',mean(times))
