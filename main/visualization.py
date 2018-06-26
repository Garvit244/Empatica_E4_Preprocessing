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
        new_pd = pd.DataFrame()
        fig = plt.figure(figsize=(25,15))
        ax1 = fig.add_subplot(111)

        if lap == "Lap 1":
            segments = ["11", "12", "13", "14"]
        else:
            segments = ["21", "22", "23", "24"]

        for segment in segments:
            new_value = [0]*15
            for algo in ["LR", "RF", "Ridge", "Lasso"]:
                column = algo + "_" + lap + "_" + segment
                new_value += (pd_A[column] == 1)*1

            new_pd = new_pd.append(pd.DataFrame(new_value).T)

        sns.set(font_scale=3)
        axs = sns.heatmap(new_pd.T, cmap="YlGnBu", linewidths=2, vmin=0, vmax=4)
        cbar = axs.collections[0].colorbar
        cbar.set_ticks([0, 1, 2, 3, 4])
        cbar.set_ticklabels(['0', '1', '2', '3', '4'])

        plt.xlabel('Section', fontsize=30)

        ax1.set_xticklabels(["Park", "Residential", "Shelterd Street", "Unsheltered Street"],  minor=False, rotation='horizontal', size=30)
        ax1.set_yticklabels(pd_A[0], minor=False, rotation='horizontal', size=30)
        plt.ylabel('Features', fontsize=30)

        horizontal_lines = [6, 9]
        for line in horizontal_lines:
            ax1.axhline(line, 0, 1, linewidth=5, c='r')

        # plt.show()

        plt.tight_layout()
        plt.savefig(output_file)