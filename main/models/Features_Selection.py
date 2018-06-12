from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import RandomForestRegressor

class Features:
    def __init__(self, pd_data):
        self.pd_data = pd_data

    def variance_feature_selection(self, target, features):
        x = self.pd_data[features]
        y = self.pd_data[target]
        selector = VarianceThreshold()
        selector = selector.fit_transform(x, y)
        print selector[0]

    def RFECV_feature_selection(self, target, features, type):
        y = self.pd_data[target]
        x = self.pd_data[features]

        if type == "RF":
            logreg = RandomForestRegressor()
        elif type == "SVR":
            logreg = SVR(kernel='linear')
        elif type == "LR":
            logreg = LinearRegression()
        elif type == "Ridge":
            logreg = Ridge()
        elif type == 'Lasso':
            logreg = Lasso()

        rfe = RFE(logreg)
        rfe = rfe.fit(x, y)
        # print logreg.fit(x, y)
        # print logreg.score(x, y)
        # print rfe.support_
        # print rfe.ranking_
        return rfe.ranking_