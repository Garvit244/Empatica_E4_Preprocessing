import pandas as pd
from scipy import stats

class Anova:
    def __init__(self, file_path):
        self.pd_file = pd.read_csv(file_path)

    def plot(self, variable, grouping):
        self.pd_file.boxplot(variable, by=grouping, figsize=(12, 8))


    def anova(self, variable, grouping):
        groups = pd.unique(self.pd_file[grouping].values)
        d_data = {grp: self.pd_file[variable][self.pd_file[grouping] == grp] for grp in groups}

        for i in range(5):
            for j in range(i+1, 5):
                F, p = stats.f_oneway(d_data[i], d_data[j])
                KF, KP  = stats.kruskal(d_data[i], d_data[j])
                print "Segment ", i, " Segment ", j,  " F-measure ", F, " kH-measure ", KF


if __name__ == '__main__':
    anova_test = Anova('/home/striker/Downloads/Clustering.csv')
    anova_test.anova('EDA', 'Segments')