"""Este programa realiza una simulación basada en agentes
de un sistema económico más realista, con transacciones donde se conserva
el dinero.
"""

from economic_agent import CapitalistAgent_02
import matplotlib.pyplot as plt
import numpy as np

#TODO Paso 1 (parametros)
# Paso 1 (parametros)
Nexp = 3
N = int(5*(10**Nexp)) # número de agentes

T = 500 # esta cantidad garantiza que todos los agentes puedan fungir como prestamistas al inicio
W = 10 # Salario
M = N*T # cantidad total de dinero en el sistema
interest_range = (0.15,0.20)

texp = 3
t_steps = int(4*(10**texp)) # Pasos de tiempo para la simulación

# Se crean a los agentes
agents_list = np.array([CapitalistAgent_02(money=T) for i in range(N)])
A_idx = range(N)
# Simulación
for i in range(t_steps):
    #TODO Paso 2 (Préstamo)
    pair = np.random.choice(A_idx, size=2, replace=False)
    e_idx,p_idx = pair[0],pair[1]
    is_loan_taken = agents_list[e_idx].take_loan(from_agent=p_idx, W=W, interest_range=interest_range, agents_list=agents_list)

    if not is_loan_taken:
        continue

    #TODO Paso 3 (Contratacion)
    B_idx = np.array([a for a in A_idx if a not in [e_idx,p_idx]])
    f_L = agents_list[e_idx].hired_fraction(W=W)
    workers_idx = np.random.choice(B_idx, size=agents_list[e_idx].L, replace=False)
    #TODO Paso 4 (Producción)
    agents_list[e_idx].produce(with_workers=workers_idx, fraction=f_L, wage=W, agents_list=agents_list)
    #TODO Paso 5 (Venta)
    buyers_idx = np.random.choice(B_idx, size=agents_list[e_idx].Q, replace=False)
    agents_list[e_idx].sells(to_buyers=buyers_idx, agents_list=agents_list)
    #TODO Paso 6 (Devolución)
    agents_list[e_idx].return_loan(to_agent=p_idx, agents_list=agents_list)

# Datos para el histograma
final_m_array = np.array([agent.money for agent in agents_list])
nb_bins = int(max(final_m_array))

# Distribución de Boltzmann-Gibbs
m_values = np.linspace(0,max(final_m_array),nb_bins)
P_values = N*(1/T)*np.exp(-m_values/T)

plt.hist(final_m_array, bins=range(nb_bins+2), label="Simulation", histtype='step', density=False)
plt.plot(m_values, P_values, label="B-G distribution")
plt.title(f"Money distribution \n N = 5*10^{Nexp}, M = {M}, time = 4*10^{texp}")
plt.xlabel("Money m")
plt.ylabel("Probability distribution of agents")
#plt.yscale('log')
plt.legend()
plt.show()