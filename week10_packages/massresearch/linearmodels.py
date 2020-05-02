from sklearn.base import RegressorMixin, BaseEstimator
import numpy as np


class MetricError(Exception):
    print("")
    pass


class AwesomeRegression(RegressorMixin, BaseEstimator):
    
    def __init__(self, 
                 tol=1e-10, 
                 l2=0, 
                 l1=0,
                 lr=0.001,
                 num_iter=10000,
                 metric = "mse",
                 batch_size=100):
        
        # self.w = np.random.normal(size=(100))
        self.tol = tol
        self.l1 = l1
        self.l2 = l2
        self.num_iter = num_iter
        self.lr = lr
        self.iter = 0
        self.batch_size = batch_size
        self.metric = metric 
        self.history = [ ]
        
    def loss(self, X, y):
        if self.metric == "mse":
            mse = ((y - X @ self.w).T) @ (y - X @ self.w) / y.size    # RSS
            return mse
        elif self.metric == "mae":
            mae = np.mean(np.abs(y - X @ self.w))
            return mae
        else:
            raise MetricError("Пользуйтесь нормальными метриками!")

    def grad_loss(self, X, y):
        if self.metric == "mse":
            g = -2 * X.T@(y - X@self.w)
        elif self.metric == "mae":
            # (|y - Xw|)' = -X sign(y - Xw)
            g = -1*X.T@np.sign(y - X@self.w)
        else:
            raise MetricError("Пользуйтесь нормальными метриками!")
            
        # |w|' = 1, -1, 0 - не существует 
        # в 0 доопределяем производную, subgradient спуск 
        g_l1 = self.l1 * np.sign(self.w.T)
        g_l2 = 2 * self.l2*(self.w.T)
        return (g + g_l1 + g_l2)/y.size  
     
    def fit(self, X, y):  
        self.w = np.random.normal(size=(X.shape[1]))
        new_w = self.w - self.lr*self.grad_loss(X, y)

        while self.iter < self.num_iter and np.any(abs(new_w - self.w) > self.tol):
            
            self.history.append(self.loss(X,y))
            
            # одно рандомное наблюдение 
            ind_rand = np.random.choice(range(X.shape[0]), size=self.batch_size, replace=False)
            
            self.iter += 1
            self.w = new_w
            new_w = self.w - self.lr*self.grad_loss(X[ind_rand], y[ind_rand])
            
    def fit_formula(self, X, y):
        self.w = np.linalg.inv(X.T@X + self.l2*np.eye(X.shape[1]))@(X.T@y)
     
    def predict(self, X):
        return X@self.w
    
# - в любом модуле есть переменная __name__ 
# - если она равна main, значит файл не подгружен а запущен
# - код внутри условия будет исполнен

if __name__ == "__main__":
    # код внутри будет выполняться только при прямом вызове, при import не будет
    print("Hello, парни!") 
    print(__name__)
    
if __name__ == "massresearch.linearmodels":
    print("моделиии") 