import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

class Visualize:
    def __init__(self, file_dir):
        self.file_dir = file_dir
        self.pd_A = pd.read_csv(file_dir + "Merged_EDA.csv")
        self.pd_A.columns = ["Epoc_Time",
        "Readable_Time",
        "EDA",
        "Skin Temp",
        "HR",
        "Station Pressure",
        "Wind Speed",
        "WBGT",
        "Heat_Stress_Index",
        "Temperature",
        "Humidity",
        "Tags",
        "Lap",
        "SCR",
        "Count"]

    def twoAxisPlot(self, y1_label, y2_label, lap, output_file):
        self.pd_A = self.pd_A[self.pd_A["Tags"] != 0]
        self.pd_A = self.pd_A[self.pd_A["Lap"] == lap]
        y1 = self.pd_A[y1_label]
        y2 = self.pd_A[y2_label]
        x = np.arange(1, len(self.pd_A)+1, 1)

        fig, ax1 = plt.subplots()
        ax1.plot(x, y1, 'b-')
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel(y1_label, color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ax2.plot(x, y2, 'r-')
        ax2.set_ylabel(y2_label, color='r')
        ax2.tick_params('y', colors='r')

        fig.tight_layout()

        tags = self.pd_A["Tags"].unique()[1:]
        if lap == "Lap 1":
            first_index = self.pd_A[self.pd_A["Tags"] == 10].index[0]
        else:
            first_index = self.pd_A[self.pd_A["Tags"] == 20].index[0]
        vertical_lines = []

        for tag in tags:
            index  = self.pd_A[self.pd_A["Tags"] == tag].index[0] - first_index
            vertical_lines.append(index)

        for vertical in vertical_lines:
            plt.axvline(x=vertical, color='k', linestyle='--')

        plt.savefig(self.checkPath() + output_file,  dpi=150, format="png")


    def scatterPlot(self, lap):
        self.pd_A = self.pd_A[self.pd_A["Tags"] != 0]
        self.pd_A = self.pd_A[self.pd_A["Lap"] == lap]
        y1 = self.pd_A["SCR"]
        x = np.arange(1, len(y1) + 1, 1)
        y1[y1 == 0] = np.nan

        fig, ax1 = plt.subplots()
        ax1.plot(x, y1, 'r.')
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("SCR", color='r')
        ax1.tick_params('y', colors='r')
        plt.yticks(np.arange(0, 4, 0.25))
        plt.show()

    def checkPath(self):
        if not os.path.exists(self.file_dir + '/Plots'):
            os.makedirs(self.file_dir + '/Plots' )
        return self.file_dir + '/Plots/'

