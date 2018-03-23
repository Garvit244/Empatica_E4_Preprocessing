import matplotlib.pyplot as plt
import numpy as np

class visualize_feature:
    def plot_bar_x(self, label, values):
        index = np.arange(len(label))
        plt.bar(index, values)
        plt.xlabel('SCR', fontsize=10)
        plt.ylabel('Tags', fontsize=10)
        plt.xticks(index, label, fontsize=10, rotation=30)
        plt.show()