from Customer import Customer
import matplotlib.pyplot as plt
import numpy as np
import csv

class Simulator(object):
    def __init__(self, price):
        # staff
        self.num_funders = 5
        # how many box a staff can make per day
        self.work_capacity = 50
        # how many box a staff can make per month
        self.work_capacity_per_mon = self.work_capacity * 22
        # how man box the funders can make per month
        self.initial_capacity = self.num_funders * self.work_capacity_per_mon

        # staff salary per hour
        self.salary_per_hr = 22
        # staff salary per 
        self.salary_per_mon = self.salary_per_hr * 22 * 8

        # 1 = 1 month
        self.pred_length = 36

        # price for each box
        self.price = price
        # cost for per box
        self.food_cost = {
            'chicken': 7.115,
            'beef': 6.1697,
            'pasta': 5.9055
        }
        # the change range of food cost
        self.cost_offset = 1.0

        self.inception_cost = 10000
        self.fixed_cost_per_hr = 40
        self.fixed_cost_per_month = 30*24*self.fixed_cost_per_hr
        # predict customer amount
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
        return total_revenues, incomes, costs

    def __float_cost(self, i):
        offset = np.random.uniform(low=-self.cost_offset, high=self.cost_offset)
        food_cost = np.array([v for v in self.food_cost.values()]) + offset
        amount = np.around(np.random.dirichlet(np.ones(3),size=1) * self.customers[i])
        food_cost = np.sum(amount * food_cost)
        salary = 0
        # if the work capacity exceed the work capacity of funders, then need to hire new staff
        if self.customers[i] > self.initial_capacity:
            num_staff = np.ceil((self.customers[i] - self.initial_capacity) / self.work_capacity_per_mon)
            salary = num_staff * self.salary_per_mon
        
        return food_cost + salary


if __name__ == "__main__":
    import sys
    def save_csv(filename, source):
        with open(filename, 'w') as f:
            csv_writer = csv.writer(f)
            for row in source:
                csv_writer.writerow(row)

    price = float(sys.argv[1])
    revenue_result = []
    income_result = []
    cost_result = []
    for i in range(100):
        s = Simulator(price)
        r, i, c = s.simulate()
        revenue_result.append(r)
        income_result.append(i)
        cost_result.append(c)

    save_csv(f'revenu{price}.csv', revenue_result)
    save_csv(f'income{price}.csv', income_result)
    save_csv(f'cost{price}.csv', cost_result)

    avg_revenue = np.average(revenue_result, axis=0)
    avg_income = np.average(income_result, axis=0)
    avg_cost = np.average(cost_result, axis=0)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(np.zeros(avg_cost.shape[0]), 'r--')
    # green line is income 
    plt.plot(avg_income, 'g-')
    # red dash line is cost
    plt.plot(avg_cost, 'r--')
    # blue line is total revenue
    plt.plot(avg_revenue, 'b-')

    plt.subplot(212)
    plt.plot((avg_income-avg_cost)/avg_income)
    plt.plot(np.array([0.15]*avg_cost.shape[0]), 'g--')
    plt.plot(np.array([0.05]*avg_cost.shape[0]), 'g--')
    plt.plot(np.zeros(avg_cost.shape[0]), 'g--')
    plt.savefig(f'price_{price}.png')
    plt.show()
    




