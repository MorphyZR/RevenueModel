from Customer import Customer
import matplotlib.pyplot as plt
import numpy as np

class Simulator(object):
    def __init__(self):
        # staff
        self.num_funders = 5
        self.work_capacity = 50
        self.work_capacity_per_mon = self.work_capacity * 22
        self.initial_capacity = self.num_funders * self.work_capacity_per_mon
        self.salary_per_hr = 22
        self.salary_per_mon = self.salary_per_hr * 22 * 8

        self.pred_length = 36
        self.price = 12.8
        self.inception_cost = 10000
        self.food_cost = {
            'chicken': 7.115,
            'beef': 6.1697,
            'pasta': 5.9055
        }
        self.fixed_cost_per_hr = 40
        self.fixed_cost_per_month = 30*24*self.fixed_cost_per_hr
        

        self.cost_offset = 1.0
        customer_predictor = Customer()
        self.customers = customer_predictor.predict()

        

    def simulate(self):
        total_revenues = []
        costs = []
        incomes = []
        total_revenue = -self.inception_cost
        for i in range(self.pred_length):
            income = self.customers[i] * self.price
            incomes.append(income)
            float = self.__float_cost(i)
            cost = self.fixed_cost_per_month + float
            total_revenue += income - cost
            total_revenues.append(total_revenue)
            costs.append(cost)
            # breakpoint()
        # breakpoint()
        plt.plot(total_revenues, 'y--')
        plt.plot(incomes, 'r-')
        plt.plot(costs, 'b-')
        plt.plot(np.zeros(self.pred_length), 'r--')
        plt.show()
        plt.cla()

        revenue_rate = (np.array(incomes) - np.array(costs)) / np.array(incomes)
        plt.plot(revenue_rate)
        plt.show()
    

    def __float_cost(self, i):
        offset = np.random.uniform(low=-self.cost_offset, high=self.cost_offset)
        food_cost = np.array([v for v in self.food_cost.values()]) + offset
        amount = np.around(np.random.dirichlet(np.ones(3),size=1) * self.customers[i])
        
        # breakpoint()
        food_cost = np.sum(amount * food_cost)
        salary = 0
        if self.customers[i] > self.initial_capacity:
            num_staff = np.ceil((self.customers[i] - self.initial_capacity) / self.work_capacity_per_mon)
            salary = num_staff * self.salary_per_mon
        
        # breakpoint()
        return food_cost + salary


if __name__ == "__main__":
    s = Simulator()
    s.simulate()



