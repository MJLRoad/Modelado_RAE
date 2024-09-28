from random import uniform

class Agent:

    def __init__(self, money):
        self.money = money

    def pay(self, payee, transaction_type, system_avg):
        delta_m = 0.0

        if transaction_type == 'small_constant':
            delta_m += 1.0
        elif transaction_type == 'random_pair_average':
            avg = (self.money + payee.money)/2
            delta_m += (uniform(0.0,1.0))*avg
        elif transaction_type == 'random_system_average':
            delta_m += (uniform(0.0,1.0))*system_avg
        elif transaction_type == 'proportional':
            delta_m += 0.5*(self.money)
        else:
            pass

        if self.money >= delta_m:
            self.money -= delta_m
            payee.money += delta_m
        else:
            pass

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


    def take_loan(self, from_agent, agents_list):
        delta_m = self.K_critical
        is_loan_taken = False
        if delta_m <= agents_list[from_agent].money:
            self.money += delta_m
            agents_list[from_agent].money -= delta_m
            is_loan_taken = True

        return is_loan_taken

    def hired_fraction(self, W):
        f_L = 1.0
        if self.money >= (self.L_critical)*W:
            self.L = self.L_critical
        else:
            f_L = (self.money)/((self.L_critical)*W)
            self.L = int((self.money)/(W))

        return f_L

    #def produce(self, with_workers, fraction, wage, agents_list):
    def produce(self):
        global workers_idx
        global f_L
        global W
        global agents_list

        #self.Q = int(fraction*(self.Q_c))
        self.Q = int(f_L * (self.Q_c))
        #delta_m = wage
        delta_m = W
        for w in workers_idx:
            self.money -= delta_m
            agents_list[w].money += delta_m

    def sells(self, to_buyers, agents_list):
        delta_m = self.R_c
        for buyer in to_buyers:
            if agents_list[buyer].money >= delta_m:
                agents_list[buyer].money -= delta_m
                self.money += delta_m

    def return_loan(self, to_agent, r, agents_list):
        delta_m = (1.0+r)*self.K_critical
        if self.money >= delta_m:
            agents_list[to_agent].money += delta_m
            self.money -= delta_m


class CapitalistAgent_02:

    def __init__(self, money):
        self.money = money
        self.r = 0.0

        self.L_critical = 0
        self.K_critical = 0.0
        self.L = 0
        #self.K = 0.0

        self.Q = 0
        self.Q_c = 0
        self.R_c = 0.0


    def take_loan(self, from_agent, W, interest_range, agents_list):
        self.r = uniform(interest_range[0],interest_range[1])
        V,beta,eta = 100,0.8,0.5

        f1 = (V*beta*(1-eta))
        f1 /= W
        f1 = f1**(1/eta)
        f2 = W*(1-beta)
        f2 /= ((self.r)*beta)
        f2 = f2**(((1-beta)*(1-eta))/eta)
        self.L_critical = int(f1*f2)
        self.K_critical = (1-beta)*W*(self.L_critical)
        self.K_critical /= ((beta)*(self.r))

        self.Q_c = int(((self.L_critical)**(beta))*((self.K_critical)**(1-beta)))
        #print(self.r, self.K_critical, self.L_critical, self.Q_c)
        self.R_c = V/((self.Q_c)**eta)

        delta_m = 0.0
        #if self.K_critical <= agents_list[from_agent].money:
        #    self.K = self.K_critical
        #else:
        #    self.K = agents_list[from_agent].money
        delta_m += self.K_critical
        is_loan_taken = False
        if delta_m <= agents_list[from_agent].money:
            self.money += delta_m
            agents_list[from_agent].money -= delta_m
            is_loan_taken = True

        return is_loan_taken

    def hired_fraction(self, W):
        f_L = 1.0
        if self.money >= (self.L_critical)*W:
            self.L = self.L_critical
        else:
            f_L = (self.money)/((self.L_critical)*W)
            self.L = int((self.money)/(W))

        return f_L

    def produce(self, with_workers, fraction, wage, agents_list):
        self.Q = int(fraction*(self.Q_c))
        delta_m = wage
        for w in with_workers:
            self.money -= delta_m
            agents_list[w].money += delta_m

    def sells(self, to_buyers, agents_list):
        delta_m = self.R_c
        for buyer in to_buyers:
            if agents_list[buyer].money >= delta_m:
                agents_list[buyer].money -= delta_m
                self.money += delta_m

    def return_loan(self, to_agent, agents_list):
        delta_m = (1.0+self.r)*self.K_critical
        if self.money >= delta_m:
            agents_list[to_agent].money += delta_m
            self.money -= delta_m