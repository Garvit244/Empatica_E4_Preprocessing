import pandas as pd
import re

class FileReader:
    def __init__(self, file_name):
        self.pd = pd.read_csv(file_name)

    def checkValidity(self ,row):
        for index, value in row.iterrows():
            value = str(value)
            if re.search('[a-zA-Z]+', value).group() != 'Name':
                return False
        return True

    def clean(self):
        columns, cleaned_df = pd.DataFrame(), pd.DataFrame()
        column_find  = False

        for index, row in self.pd.iterrows():
            row = pd.DataFrame(row)
            if columns.empty:
                columns = row
            else:
                if columns.isnull().values.any():
                    columns = row
                else:
                    if not column_find:
                        cleaned_df = cleaned_df.append(columns.T)
                        cleaned_df.columns = cleaned_df.iloc[0]
                        cleaned_df = cleaned_df.drop(cleaned_df.index[0])
                        column_find = True
                        if self.checkValidity(row):
                            cleaned_df = cleaned_df.append(row.T)
                    else:
                        if self.checkValidity(row):
                            cleaned_df = cleaned_df.append(row.T)

        print len(cleaned_df)

f = FileReader("/home/striker/Dropbox/NSE_2018_e4/Experiment/2/kestrel/Heat.csv")
f.clean()