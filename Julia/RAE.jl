using Random, Distributions, CairoMakie

mutable struct Agent
  money::Float64
end


lista = [Agent(10) for i in 1:15]

typeof(lista)
lista[1]
lista[1].money
lista[2].money 

agent_i = rand(1:15)
agent_j = rand(1:15)

coin_flit = rand(1:2)
loser_index = [agent_i, agent_j][coin_flit]
winner_index = [agent_i, agent_j][2-coin_flit+1]

lista[loser_index].money
lista[winner_index].money 

exchange_rules = ["small_constant", "random_pair_average", "random_system_average"]

ex_order = 1 # Regla
exchange_rule = exchange_rules[ex_order]

transaction_type = exchange_rule

delta_m = 0.0
if transaction_type == "small_constant"
  delta_m += 1.0
elseif transaction_type == "random_pair_average"
  avg = (lista[loser_index].money + lista[winner_index].money) / 2
  delta_m += rand(Uniform()) * avg
elseif transaction_type == "random_system_average"
  delta_m += rand(Uniform()) * system_avg
elseif transaction_type == "proportional"
  delta_m += 0.5 * lista.money
end
delta_m

if lista[loser_index].money >= delta_m
  lista[loser_index].money -= delta_m
  lista[winner_index].money += delta_m
end

lista
function pay(self, payee, transaction_type::String, system_avg::Float64)
  delta_m = 0.0

  if transaction_type == "small_constant"
      delta_m += 1.0
  elseif transaction_type == "random_pair_average"
      avg = (self.money + payee.money) / 2
      delta_m += rand(Uniform()) * avg
  elseif transaction_type == "random_system_average"
      delta_m += rand(Uniform()) * system_avg
  elseif transaction_type == "proportional"
      delta_m += 0.5 * self.money
  end

  if self.money >= delta_m
      self.money -= delta_m
      payee.money += delta_m
  end
end

function simulation(N, rule, T)
  Agentes = [Agent(10) for i in 1:N]
  exchange_rules = ["small_constant", "random_pair_average", "random_system_average"]
  transaction_type = exchange_rules[rule]

  for t in 1:T
    agent_i = rand(1:N)
    agent_j = rand(1:N)

    coin_flit = rand(1:2)
    loser_index = [agent_i, agent_j][coin_flit]
    winner_index = [agent_i, agent_j][2-coin_flit+1]

    delta_m = 0.0
    
    if transaction_type == "small_constant"
    delta_m += 1.0
    elseif transaction_type == "random_pair_average"
    avg = (Agentes[loser_index].money + Agentes[winner_index].money) / 2
    delta_m += rand(Uniform()) * avg
    elseif transaction_type == "random_system_average"
    delta_m += rand(Uniform()) * system_avg
    elseif transaction_type == "proportional"
    delta_m += 0.5 * lista.money
    end
    delta_m

    if Agentes[loser_index].money >= delta_m
      Agentes[loser_index].money -= delta_m
      Agentes[winner_index].money += delta_m
    end
  end

  wealth = [0.0 for i in 1:N]
  for i in 1:N
    wealth[i] = Agentes[i].money
  end

return wealth
end

xxx = @time simulation(500_000, 2, 10_000_000) 

maximum(xxx)

f = Figure(size = (700, 500))
ax = Axis(f[1,1])
hist!(xxx, bins = 100)
f