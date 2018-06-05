import statsmodels.api as sm

class Regression_Models:
    def __init__(self, pd_data):
        self.pd_data = pd_data

    def linerar_regression(self, target, features):
        y = self.pd_data[target]
        x = self.pd_data[features]

        linear = sm.OLS(y, x)
        result = linear.fit()
        print result.summary()


