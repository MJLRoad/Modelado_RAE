##### RAE => Economic real model ######

# used package 
using Random, CairoMakie

# Initial conditions
N_exp = 3
M_exp = 6
T_exp = 4
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
  Π::Float64 # quantity produced
  qᶜ::Float64 # quantity of equilibrium
  pᶜ::Float64 # quantity of equilibrium
end

list_agents = [Agent_RM(10.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) for _ in 1:10]

list_agents[1].β

A_idx = [i for i in 1:10]

pair = rand(1:10, 2)
e_idx, p_idx = pair[1], pair[2]
e_idx
p_idx
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

for i in 1:10
  list_agents[i].β = 0.8
  list_agents[i].η = 0.5
  list_agents[i].w = 10
  list_agents[i].r = 0.15
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

agent_capitalist(list_agents, 10, V)

list_agents