import pandas as pd

class Interpolate:
    def __init__(self, file_path, column_names):
        self.file_path = file_path
        self.column_names = column_names

    def interpolate(self):
        pd_output = pd.read_csv(self.file_path)

        pd_output[self.column_names] = pd_output[self.column_names].fillna(method='ffill')
        pd_output.to_csv(self.file_path, index=False)