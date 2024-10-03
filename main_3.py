"""Este programa realiza una simulación basada en agentes
de un sistema económico con transacciones donde se conserva
el dinero
"""

from economic_agent import Agent_debtor
from random import randint
import matplotlib.pyplot as plt
import numpy as np

# Parámetros
Nexp = 4
N = int(5*(10**Nexp)) # número de agentes

Mexp = 5
M = 5*10**Mexp # cantidad total de dinero en el sistema

#m_d = 8 # deuda máxima
m_d = 0
T = M/N + m_d # temperatura de dinero

texp = 5
t_steps = int(4*(10**texp)) # Pasos de tiempo de la simulación
# regla de intercambio
exchange_rules = ['small_constant', 'random_pair_average', 'random_system_average']
ex_order = 1
exchange_rule = exchange_rules[ex_order - 1]

# Creamos a los agentes
agents_list = [Agent_debtor(money=M/N, maximum_debt=m_d) for i in range(N)] # Todos los agentes tienen la misma cantidad de dinero
# Simulación
for i in range(t_steps):
    agent_i_index = randint(0,N-1)
    agent_j_index = randint(0,N-1) # se elige un par de agentes al azar para hacer transacción
    coin_flip = randint(0,1)
    loser_index = [agent_i_index,agent_j_index][coin_flip] # Uno de los agentes se selecciona al azar como el perdedor
    winner_index = [agent_i_index, agent_j_index][1-coin_flip]

    agents_list[loser_index].pay(agents_list[winner_index], transaction_type=exchange_rule, system_avg=M/N)

# Datos para el histograma
final_m_array = np.array([agent.money for agent in agents_list])
nb_bins = int(max(final_m_array)) + m_d
frq,edges = np.histogram(final_m_array, bins=nb_bins)

# Distribución de Boltzmann-Gibbs
m_values = np.linspace(-m_d,max(final_m_array),nb_bins)
P_values = N*(1/T)*np.exp(-(m_values+m_d)/T)

plt.bar(edges[:-1], frq, fill=False ,label=f"Model with debt (T = {T})")
plt.plot(m_values, P_values, label="B-G distribution")
ttl = ""
ttl += f"Money distribution (exchange rule: {exchange_rule})\n"
ttl += f"N = 5*10^{Nexp}, M = 5*10^{Mexp}, time = 4*10^{texp}\n"
ttl += f"Maximum debt = {m_d}"
plt.title(ttl)
plt.xlabel("Money m")
plt.ylabel("Distribution of agents")
#plt.yscale('log')
plt.legend()
plt.show()
