##### RAE => Economic real model ######

# used package 
using Random, CairoMakie

# Initial conditions
N_exp = 3
M_exp = 6
T_exp = 3
million = 1_000_000
N = Int(5 * 10^N_exp)  # numero de agentes   
M = Int(5 * 10^M_exp) # Dinero total en el sistema 
T = Int(4 * 10^T_exp) # tiempo
M_avg = Int(M/N) # temperatura del dinero

β = 0.8
η = 0.5 
V = 100
w = 10
r = 0.15

mutable struct Agent_RM
  money::Float64
  ϵ::Int64 # Agent index capitalist
  ρ::Int64 # Agent index bank 
  w::Float64 # Salary 
  r::Float64 # Interest rate 
  
  β::Float64 # participation factor rate
  η::Float64 # q rate 

  Lᶜ::Float64 # Labor of equilibrium
  Kᶜ::Float64 # Capital of equilibrium
  L::Float64 # Labor
  Π::Float64 # Benefits of firms
  q::Float64 # quantity sell
  qᶜ::Float64 # quantity of equilibrium
  pᶜ::Float64 # price of equilibrium
end

list_agents = [Agent_RM(0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) for _ in 1:N]

list_agents[1].β

A_idx = [i for i in 1:N]

rand(A_idx, 2)

pair = rand(A_idx, 2)
e_idx, p_idx = pair[1], pair[2]
e_idx
p_idx

B_idx = filter!(a -> !(a in [e_idx, p_idx]), A_idx)
# pair = []
# for i in 1:10
# p = rand((1:10), 2)
# push!(pair, p)
# end

ll = ((V * β *(1 - η)) / w)^(1 / η)  * ((w * (1 - β)) / (r * β))^(((1 - β)*(1 - η)) / η)

kk = ((1 - β) / β) * (w / r) *  ll

qq = ll^β * kk^(1-β)

pp = V/qq^η

pii = V * qq^(1 - η) - ll * w - r * kk

pair

round(ll)

round(2.51)

for i in 1:N
  list_agents[i].money = 1000
  list_agents[i].β = 0.8
  list_agents[i].η = 0.5
  list_agents[i].w = 10
  list_agents[i].r = 0.15 #rand((0.15:0.001:0.20))
end
list_agents

function agent_capitalist(x, N, V)
  for i in 1:N
  x[i].Lᶜ = ((V * x[i].β *(1 - x[i].η)) / x[i].w)^(1 / x[i].η)  * ((x[i].w * (1 - x[i].β)) / (x[i].r * x[i].β))^(((1 - x[i].β)*(1 - x[i].η)) / x[i].η)
  x[i].Lᶜ = round(x[i].Lᶜ)
  
  x[i].Kᶜ = ((1 - x[i].β) / x[i].β) * (x[i].w / x[i].r) *  x[i].Lᶜ  

  x[i].qᶜ = x[i].Kᶜ^(1-x[i].β) * x[i].Lᶜ^x[i].β
  
  x[i].pᶜ = V / x[i].qᶜ^x[i].η
  
  x[i].Π = V * x[i].qᶜ^(1 - x[i].η) - x[i].w * x[i].Lᶜ - x[i].r * x[i].Kᶜ 
  end
end

agent_capitalist(list_agents, N, V)

list_agents

function take_loan(x, p_idx, e_idx)
  delta_m = 0.0
  delta_m += x[e_idx].Kᶜ

  if delta_m <= x[p_idx].money
    x[e_idx].money += delta_m
    x[p_idx].money -= delta_m
  end
end

take_loan(list_agents, p_idx, e_idx)
list_agents

function hired_fraction(x, e_idx)
  f_L = 1.0
  if x[e_idx].money >= x[e_idx].Lᶜ * x[e_idx].w
    x[e_idx].L = x[e_idx].Lᶜ
  else 
    f_L = x[e_idx].money / (x[e_idx].Lᶜ * x[e_idx].w)
    x[e_idx].L = round(x[e_idx].money / x[e_idx].w)
  end
  return f_L
end

f_L = hired_fraction(list_agents, e_idx)

list_agents
list_agents[e_idx]
list_agents[e_idx].L


workers_idx = rand(B_idx, Int(list_agents[e_idx].L))
Int(list_agents[e_idx].L)
workers_idx

function produce(x, f_L, e_idx, workers_idx)
  x[e_idx].q = Int(round(f_L * x[e_idx].qᶜ))
  delta_m = x[e_idx].w 

  for i in workers_idx
    x[e_idx].money -= delta_m
    x[i].money += delta_m
  end

end

produce(list_agents, f_L, e_idx, workers_idx)

list_agents

buyers_idx = rand(B_idx, Int(list_agents[e_idx].q))

function sells(x, e_idx, buyers_idx)
  delta_m = x[e_idx].pᶜ

  for i in buyers_idx
    if x[i].money >= delta_m
      x[i].money -= delta_m
      x[e_idx].money += delta_m 
    end
  end
end

sells(list_agents, e_idx, buyers_idx)
list_agents

function return_loan(x, e_idx, p_idx)
  delta_m = (1.0 + x[e_idx].r) * x[e_idx].Kᶜ
  if x[e_idx].money >= delta_m
    x[p_idx].money += delta_m
    x[e_idx].r -= delta_m
  end
end

return_loan(list_agents, e_idx, p_idx)

list_agents

function idx(x, A_idx)
  pair = rand(A_idx, 2)
  e_idx, p_idx = pair[1], pair[2]

  if x[e_idx].Kᶜ <= x[p_idx].money
    e_idx, p_idx = pair[1], pair[2]
  else
    pair = rand(A_idx, 2)
    e_idx, p_idx = pair[1], pair[2]
  end
  
  return e_idx, p_idx

end

function simulation_RM(N, M_avg, T )
  list_agents = [Agent_RM(0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) for _ in 1:N]
  
  for i in 1:N
    list_agents[i].money = M_avg
    list_agents[i].β = 0.8
    list_agents[i].η = 0.5
    list_agents[i].w = 10.0
    list_agents[i].r = 0.15 #rand((0.15:0.001:0.20))
  end
  
  V = 100
  A_idx = [i for i in 1:N]
  agent_capitalist(list_agents, N, V)

  for t in 1:T
    pair = rand(A_idx, 2)
    e_idx, p_idx = idx(list_agents, A_idx)
    B_idx = filter!(a -> !(a in [e_idx, p_idx]), A_idx)

    take_loan(list_agents, p_idx, e_idx)

    f_L = hired_fraction(list_agents, e_idx)
    
    workers_idx = rand(B_idx, Int(list_agents[e_idx].L))
    
    produce(list_agents, f_L, e_idx, workers_idx)
    
    buyers_idx = rand(B_idx, Int(list_agents[e_idx].q))

    sells(list_agents, e_idx, buyers_idx)
    
    return_loan(list_agents, e_idx, p_idx)
  end

  wealth = [0.0 for i in 1:N]

  for i in 1:N
    wealth[i] = list_agents[i].money
  end

return wealth
end

xx = simulation_RM(1000, 1000, 1000)

maximum(xx)
minimum(xx)


f = Figure(size = (700, 500))
ax = Axis(f[1,1])
stephist!(xx, bins = 100)
f