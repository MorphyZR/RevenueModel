import numpy as np
import matplotlib.pyplot as plt
class Customer(object):
    def __init__(self):
        self.initial = 2200
        self.initial_loss = 0.1
        self.base_increment = 1000
        self.pred_length = 36
        self.brown_mean = 0.001
        self.brown_sd = 0.001
        self.a_mean = 0.05
        self.a_sd = 40

        self.lr = self.__lr_simu()
        self.increment_simu = self.__increment_simu()

    def __lr_simu(self):
        res = []
        x = -1
        for i in range(self.pred_length):
            while x <= 0:
                x = np.random.uniform(
                        self.initial_loss, 
                        self.initial_loss + self.__simple_brown(self.brown_mean, self.brown_sd) 
                ) 
            res.append(x)
        return res

    def __increment_simu(self):
        res = []
        x = -1
        for i in range(self.pred_length):
            while x < 0:
                x = np.random.uniform(
                    self.base_increment, 
                    self.base_increment + self.__simple_brown(self.a_mean, self.a_sd)
                ) 
            
            res.append(x)

        return res

    def __simple_brown(self, mean, sd):
        normal = np.random.normal(mean, sd, size=self.pred_length)
        return np.sum(normal)

    def __new_customer(self):
        # return self.
        print(round(self.increment * self.__simple_brown()))

    def predict(self):
        res = [self.initial]
        # loss_rate_simu = (self.initial_loss, self.initial_loss + self.__simple_brown())
        # new_customers_simu =(self.base_increment, self.base_increment *(1 + self.__simple_brown()))
        for i in range(1, self.pred_length):
            lr = np.random.beta(res[i-1]*self.lr[i], res[i-1]*(1 - self.lr[i]))
            new_customer = res[i-1] + self.increment_simu[i] - res[i-1] * lr
            res.append(new_customer)
        
        # plt.plot(res)
        # plt.show()

        return res

if __name__ == "__main__":
    customer = Customer()
    x = customer.predict()
    plt.plot(x)
    plt.show()
