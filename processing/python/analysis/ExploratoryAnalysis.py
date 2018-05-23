import matplotlib.pyplot as plt
import numpy as np
import os

class Visualize:
    def __init__(self, file_dir):
        self.file_dir = file_dir

    def twoAxisPlot(self, pd_A, y1_label, y2_label, lap, cut_point, output_file):
        pd_A = pd_A[pd_A["Tags"] != 0]
        pd_A = pd_A[pd_A["Lap"] == lap]
        pd_A = pd_A[cut_point:]
        y1 = pd_A[y1_label]
        y1 = y1.replace(to_replace=0, value=np.nan)

        y2 = pd_A[y2_label]
        x = np.arange(1, len(pd_A)+1, 1)

        fig, ax1 = plt.subplots()
        ax1.plot(x, y1, 'b.')
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel(y1_label, color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ax2.plot(x, y2, 'r-')
        ax2.set_ylabel(y2_label, color='r')
        ax2.tick_params('y', colors='r')

        fig.tight_layout()

        tags = pd_A["Tags"].unique()[1:]
        if lap == "Lap 1":
            first_index = pd_A[pd_A["Tags"] == 10].index[0]
        else:
            first_index = pd_A[pd_A["Tags"] == 20].index[0]
        vertical_lines = []

        for tag in tags:
            index  = pd_A[pd_A["Tags"] == tag].index[0] - first_index
            vertical_lines.append(index)

        for vertical in vertical_lines:
            plt.axvline(x=vertical, color='k', linestyle='--')
        plt.axvspan(0, vertical_lines[0], alpha=0.5, color='grey')

        if lap == "Lap 2":
            plt.axvspan(vertical_lines[-1],len(pd_A), alpha=0.5, color='grey')

        plt.savefig(self.checkPath() + output_file,  dpi=150, format="png")


    def checkPath(self):
        if not os.path.exists(self.file_dir + '/Plots'):
            os.makedirs(self.file_dir + '/Plots' )
        return self.file_dir + '/Plots/'



