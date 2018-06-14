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

    def heatmap(self, pd_A, output_file, lap):
        fig, ax1 = plt.subplots()
        new_pd = pd.DataFrame()

        if lap == "Lap 1":
            segments = ["11", "12", "13", "14"]
        else:
            segments = ["21", "22", "23", "24"]

        for segment in segments:
            new_value = [0]*16
            for algo in ["LR", "RF", "Ridge", "Lasso"]:
                column = algo + "_" + lap + "_" + segment
                new_value +=(pd_A[column] == 1)*1

            new_pd = new_pd.append(pd.DataFrame(new_value).T)

        sns.heatmap(new_pd.T, cmap="YlGnBu", linewidths=2)
        plt.xlabel('Section')

        ax1.set_xticklabels(["Park", "Residential", "Shelterd Street", "Unsheltered Street"],  minor=False, rotation='horizontal', size=10)
        ax1.set_yticklabels(pd_A[0], minor=False, rotation='horizontal', size=10)
        plt.ylabel('Features')

        horizontal_lines = [5, 9]
        for line in horizontal_lines:
            ax1.axhline(line, 0, 1, linewidth=2, c='r')
        plt.show()
        # fig.set_size_inches(500, 600)
        plt.savefig(output_file, dpi=100)