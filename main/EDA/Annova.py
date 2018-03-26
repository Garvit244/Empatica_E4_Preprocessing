import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

class Annova:
    def __init__(self, pd_data, directory):
        self.pd_data = pd_data
        self.directory = directory

    def plot(self, variable, grouping):
        self.pd_data.boxplot(variable, by=grouping, figsize=(12, 8))
        plt.savefig(self.directory + variable + '.png')


    def anova(self, variable, grouping):
        groups = pd.unique(self.pd_data[grouping].values)

        print "Annova test for variable ", variable
        group_data = []
        for group  in groups:
            data = self.pd_data[self.pd_data[grouping] == group][variable]
            group_data.append([data])

        F, p = stats.f_oneway(group_data[0][0], group_data[1][0], group_data[2][0], group_data[3][0], group_data[4][0])
        KF, Kp = stats.kruskal(group_data[0][0], group_data[1][0], group_data[2][0], group_data[3][0], group_data[4][0])

        print  "Anova P-measure ", p, " Kruska P-measure ", Kp