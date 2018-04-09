from sklearn.feature_selection import RFE
from sklearn.svm import SVR
from sklearn.feature_selection import VarianceThreshold

class Features:
    def __init__(self, pd_data):
        self.pd_data = pd_data

    def variance_feature_selection(self, target, features):
        x = self.pd_data[features]
        y = self.pd_data[target]
        selector = VarianceThreshold()
        selector = selector.fit_transform(x, y)
        print selector[0]

    def RFECV_feature_selection(self, target, features):
        y = self.pd_data[target]
        x = self.pd_data[features]

        logreg = SVR(kernel='linear')

        rfe = RFE(logreg, 6)
        rfe = rfe.fit(x, y)
        # print logreg.fit(x, y)
        # print logreg.score(x, y)
        print rfe.support_
        print rfe.ranking_
        print rfe.estimator_
        return rfe.support_