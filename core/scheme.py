import math



class AbstractScheme:
    
    @staticmethod
    def create(**kwargs):
        pass
    
    def reset(self, cost_increment: float):
        pass
    
    def is_minimal(self) -> bool:
        pass
    
    def temperature(self) -> float:
        pass
    
    def decrease(self):
        pass



# T[n + 1] = Q * T[n]
class GeometricScheme(AbstractScheme):
    
    @staticmethod
    def create(**kwargs) -> AbstractScheme:
        return GeometricScheme(
            kwargs.get('n_epochs', 1000),
            kwargs.get('prob1',    0.95),
            kwargs.get('prob2',    0.05),
            kwargs.get('fraction', 0.0001)
        )
    
    def __init__(self, n_epochs: int, prob1: float, prob2: float, fraction: float):
        self.n_epochs = n_epochs
        self.prob1 = prob1
        self.prob2 = prob2
        self.fraction = fraction
        self.a = None # slope coefficient of the nested linear function in decrease()
        self.b = None # intercept coefficient of the nested linear function in decrease()
        self.epoch = None
        self.value = None
    
    def reset(self, cost_increment: float):
        
        temp1 = -cost_increment / math.log(self.prob1)
        temp2 = -cost_increment / math.log(self.prob2) * self.fraction
        
        self.b = math.log(temp1)
        self.a = (math.log(temp2) - self.b) / self.n_epochs
        self.value = temp1
        self.epoch = 0
    
    def is_minimal(self):
        return self.epoch == self.n_epochs
    
    def temperature(self):
        return self.value
    
    def decrease(self):
        if self.epoch < self.n_epochs:
            self.epoch += 1
            self.value = math.exp(self.a * self.epoch + self.b)



# 1/T[n+1] = 1/T[n] + beta
class LundyMeesScheme(AbstractScheme):
    
    @staticmethod
    def create(**kwargs) -> AbstractScheme:
        return GeometricScheme(
            kwargs.get('n_epochs', 1000),
            kwargs.get('prob1',    0.95),
            kwargs.get('prob2',    0.05),
            kwargs.get('fraction', 0.0001)
        )
    
    def __init__(self, n_epochs: int, prob1: float, prob2: float, fraction: float):
        self.n_epochs = n_epochs
        self.prob1 = prob1
        self.prob2 = prob2
        self.fraction = fraction
        self.coeff = None
        self.epoch = None
        self.value = None
    
    def reset(self, cost_increment: float):
        
        temp1 = -cost_increment / math.log(self.prob1)
        temp2 = -cost_increment / math.log(self.prob2) * self.fraction
        
        self.coeff = (temp1 - temp2) / ((self.n_epochs - 1) * temp1 * temp2)
        self.value = temp1
        self.epoch = 0
    
    def is_minimal(self):
        return self.epoch == self.n_epochs
    
    def temperature(self):
        return self.value
    
    def decrease(self):
        if self.epoch < self.n_epochs:
            self.epoch += 1
            self.value /= 1 + self.coeff * self.value



class LinearScheme(AbstractScheme):
    
    @staticmethod
    def create(**kwargs) -> AbstractScheme:
        return GeometricScheme(
            kwargs.get('n_epochs', 1000),
            kwargs.get('prob1',    0.95),
            kwargs.get('prob2',    0.05),
            kwargs.get('fraction', 0.0001)
        )
    
    def __init__(self, n_epochs: int, prob1: float, prob2: float, fraction: float):
        self.n_epochs = n_epochs
        self.prob1 = prob1
        self.prob2 = prob2
        self.fraction = fraction
        self.epoch = None
        self.value = None
        self.a = None
        self.b = None
    
    def reset(self, cost_increment: float):
        temp1 = -cost_increment / math.log(self.prob1)
        temp2 = -cost_increment / math.log(self.prob2) * self.fraction
        self.a = (temp2 - temp1) / self.n_epochs
        self.b = temp1
        self.value = temp1
        self.epoch = 0
    
    def is_minimal(self) -> bool:
        return self.epoch == self.n_epochs
    
    def temperature(self) -> float:
        return self.value
    
    def decrease(self):
        if self.epoch < self.n_epochs:
            self.epoch += 1
            self.value = self.a * self.epoch + self.b