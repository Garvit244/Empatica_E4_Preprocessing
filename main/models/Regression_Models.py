import statsmodels.api as sm


class Regression_Models:
    def __init__(self, pd_data):
        self.pd_data = pd_data

    def linerar_regression(self, target, features):
        print self.pd_data
        y = self.pd_data[target]
        x = self.pd_data[features]

        logit = sm.Logit(y, x)
        result = logit.fit()
        print result.summary()


