#from economic_agent import CapitalistAgent_01
import matplotlib.pyplot as plt
import numpy as np
import time

class CapitalistAgent_01:

    def __init__(self, money, L, K, Q, R):
        self.money = money

        self.L_critical = L
        self.K_critical = K
        self.L = 0
        #self.K = 0.0

        self.Q = 0
        self.Q_c = Q
        self.R_c = R


    def take_loan(self):
        global p, agents_list
        delta_m = self.K_critical
        is_loan_taken = False
        if delta_m <= p.money:
            self.money += delta_m
            p.money -= delta_m
            is_loan_taken = True

        return is_loan_taken

    def hired_fraction(self):
        global W
        f_L = 1.0
        if self.money >= (self.L_critical)*W:
            self.L = self.L_critical
        else:
            f_L = (self.money)/((self.L_critical)*W)
            self.L = int((self.money)/(W))

        return f_L

    def produce(self):
        global workers, f_L, W, agents_list
        self.Q = int(f_L * (self.Q_c))
        delta_m = W
        for worker in workers:
            self.money -= delta_m
            worker.money += delta_m # Es costoso buscar en una lista de 500,000 agentes!

    def sells(self):
        global buyers, agents_list
        delta_m = self.R_c
        for buyer in buyers:
            if buyer.money >= delta_m: # Es costoso buscar en una lista de 500,000 agentes!
                buyer.money -= delta_m # Hay qué traer a los agentes, y no sus índices!
                self.money += delta_m

    def return_loan(self):
        global p, r, agents_list
        delta_m = (1.0+r)*self.K_critical
        if self.money >= delta_m:
            p.money += delta_m
            self.money -= delta_m



start = time.time()

#TODO Paso 1 (parametros)
Nexp = 3
N = int(5*(10**Nexp)) # número de agentes

Mexp = 7
M = 10**Mexp # cantidad total de dinero en el sistema

T = M/N # temperatura de dinero

W = 10.0 # Salario
# Optimización
r = 0.05
V,beta,eta = 100,0.8,0.5
f1 = (V*beta*(1-eta))
f1 /= W
f1 = f1**(1/eta)
f2 = W*(1-beta)
f2 /= (r*beta)
f2 = f2**(((1-beta)*(1-eta))/eta)
L_critical = int(f1*f2)
K_critical = (1-beta)*W*(L_critical)
K_critical /= (beta*r)
Q_c = int(((L_critical)**(beta))*((K_critical)**(1-beta)))
R_c = V/((Q_c)**eta)
print(f"Lc = {L_critical}, Kc = {K_critical}, Qc = {Q_c}, Rc = {R_c}")

texp = 4 # Se recomienda 6
t_steps = int(4*(10**texp)) # Pasos de tiempo para la simulación
# Mi pc tarda alrededor de 1.6*10^texp segundos en correr este programa

# Se crean a los agentes
agents_list = np.array([CapitalistAgent_01(money=T, L=L_critical, K=K_critical, Q=Q_c, R=R_c) for i in range(N)]) # Todos los agentes tienen la misma cantidad de dinero
A_idx = range(N)
# Simulación
for i in range(t_steps):
    #TODO Paso 2 (Préstamo)
    pair = np.random.choice(agents_list, size=2, replace=False)
    e,p = pair[0],pair[1]

    is_loan_taken = e.take_loan()

    if not is_loan_taken:
        continue

    #TODO Paso 3 (Contratación)
    B = np.array([a for a in agents_list if a not in [e,p]])
    f_L = e.hired_fraction()
    workers = np.random.choice(B, size=e.L, replace=False)
    #TODO Paso 4 (Producción)
    e.produce()
    #TODO Paso 5 (Venta)
    buyers = np.random.choice(B, size=e.Q, replace=False)
    e.sells()
    #TODO Paso 6 (Devolución)
    e.return_loan()

end = time.time()

print(f"Tiempo de ejecución: {end-start} s")

# Datos para el histograma
final_m_array = np.array([agent.money for agent in agents_list])
nb_bins = int(max(final_m_array))

# Distribución de Boltzmann-Gibbs
m_values = np.linspace(0,max(final_m_array),nb_bins)
P_values = N*(1/T)*np.exp(-m_values/T)

plt.hist(final_m_array, bins=range(nb_bins+2), label="Simulation", histtype='step')
plt.plot(m_values, P_values, label="B-G distribution")
plt.title(f"Money distribution \n N = 5*10^{Nexp}, M = 5*10^{Mexp}, time = 4*10^{texp}")
plt.xlabel("Money m")
plt.ylabel("Distribution of agents")
#plt.yscale('log')
plt.legend()
plt.show()