import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

class visualize_feature:
    def plot_bar_x(self, label, values):
        index = np.arange(len(label))
        plt.bar(index, values)
        plt.xlabel('SCR', fontsize=10)
        plt.ylabel('Tags', fontsize=10)
        plt.xticks(index, label, fontsize=10, rotation=30)
        plt.show()

    def heatmap(self, pd_A, output_file):
        fig, ax1 = plt.subplots()
        new_pd = pd.DataFrame()

        for segment in ["11", "12", "13", "14"]:
            new_value = [0]*14
            for algo in ["LR", "RF", "Ridge"]:
                column = algo + "_Lap 1_" + segment
                new_value += pd_A[column] * 1

            new_pd = new_pd.append(pd.DataFrame(new_value).T)

        sns.heatmap(new_pd.T, cmap="YlGnBu", linewidths=2)
        plt.xlabel('Section')

        ax1.set_xticklabels(["Park", "HDB", "StreetHDB", "Street"],  minor=False, rotation='horizontal', size=15)
        ax1.set_yticklabels(pd_A[0], minor=False, rotation='horizontal', size=10)
        plt.ylabel('Features')

        plt.show()
        fig.set_size_inches(500, 600)
        plt.savefig(output_file, dpi=100)