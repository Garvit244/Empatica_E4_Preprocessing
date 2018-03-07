import pandas as pd
import matplotlib.pyplot as plt

class visualize:
    def __init__(self, eda_dir_path):
        self.eda_dir_path = eda_dir_path

    def time_poincare(self, ts):
        x = ts[0:-1]
        y = ts[1:]
        return x,y

    def show_poincare(self, ts):
        x,y = self.time_poincare(ts)
        plt.plot(x,y,'r.')
        plt.show()

    def plot_hr_poincare(self):
        pd_HR = pd.read_csv(self.eda_dir_path + '/HR.csv', header=None)
        pd_HR = pd_HR[2:].values.T.tolist()[0]
        self.show_poincare(pd_HR)

if __name__ == '__main__':
    eda_dir_path = '/home/striker/Downloads/Sun_plaza_21Feb'
    visualize_obj = visualize(eda_dir_path)
    visualize_obj.plot_hr_poincare()
