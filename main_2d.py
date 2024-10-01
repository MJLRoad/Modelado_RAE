"""Este programa realiza una simulación basada en agentes
de un sistema económico más realista, con transacciones donde se conserva
el dinero.
Histogramas de:
a) dinero
b) veces que toca ser empresario
c) veces que toca ser prestamista
d) veces que toca ser trabajador
e) veces que toca ser comprador
"""

from economic_agent import CapitalistAgent_03
import matplotlib.pyplot as plt
import numpy as np

#TODO Paso 1 (parametros)
# Paso 1 (parametros)
Nexp = 4
N = int(10**Nexp) # número de agentes

T = 500 # esta cantidad garantiza que todos los agentes puedan ser prestamistas al inicio
W = 10 # Salario
M = N*T # cantidad total de dinero en el sistema
interest_range = (0.15,0.20)

texp = 3
t_steps = int(10**texp) # Pasos de tiempo para la simulación

# Se crean a los agentes
agents_list = np.array([CapitalistAgent_03(money=T) for i in range(N)])
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

# Datos para los histogramas
final_m_array = np.array([agent.money for agent in agents_list])
nb_m_bins = int(max(final_m_array))
final_e_array = np.array([agent.e for agent in agents_list])
nb_e_bins = int(max(final_e_array))
final_p_array = np.array([agent.p for agent in agents_list])
nb_p_bins = int(max(final_p_array))
final_w_array = np.array([agent.w for agent in agents_list])
nb_w_bins = int(max(final_w_array))
final_pu_array = np.array([agent.pu for agent in agents_list])
nb_pu_bins = int(max(final_pu_array))

# Distribución de Boltzmann-Gibbs
m_values = np.linspace(0,max(final_m_array),nb_m_bins)
P_values = N*(1/T)*np.exp(-m_values/T)

fig,ax = plt.subplots(3,2,figsize=(30,30))

fig.suptitle(f"N = 10^{Nexp}, M = {M}, time = 10^{texp}")

ax[0,0].hist(final_m_array, bins=range(nb_m_bins+1), label="Simulation", histtype='step', density=False)
ax[0,0].plot(m_values, P_values, label="B-G distribution")
ax[0,0].set_xlabel("Money m")
ax[0,0].set_ylabel("Distribution of agents")
ax[0,0].legend()

fig.delaxes(ax[0,1])

ax[1,0].hist(final_e_array, bins=range(nb_e_bins+1), label="Simulation", histtype='step', density=False)
ax[1,0].set_xlabel("Number of times an agent becomes a firm")
ax[1,0].set_ylabel("Distribution of agents")
ax[1,0].legend()

ax[1,1].hist(final_p_array, bins=range(nb_p_bins+1), label="Simulation", histtype='step', density=False)
ax[1,1].set_xlabel("Number of times an agent becomes a lender")
ax[1,1].set_ylabel("Distribution of agents")
ax[1,1].legend()

ax[2,0].hist(final_w_array, bins=range(nb_w_bins+1), label="Simulation", histtype='step', density=False)
ax[2,0].set_xlabel("Number of times an agent becomes a worker")
ax[2,0].set_ylabel("Distribution of agents")
ax[2,0].legend()

ax[2,1].hist(final_pu_array, bins=range(nb_pu_bins+1), label="Simulation", histtype='step', density=False)
ax[2,1].set_xlabel("Number of times an agent becomes a purchaser")
ax[2,1].set_ylabel("Distribution of agents")
ax[2,1].legend()

plt.tight_layout()
path = f"Realistic_extra_texp={texp}.png"
plt.savefig(path)
plt.show()