import pandas as pd

def find_amplitute(input_dir):
    users = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    output_file = input_dir + 'Amplitute.csv'
    output_file_reader = open(output_file, 'w')

    for user in users:
        input_file = input_dir + user + "/EDA/EDA_leda.csv"
        pd_input = pd.read_csv(input_file)
        amplitute =  round(pd_input.diff()[1:].abs().mean().values[0], 3)
        print amplitute
        output_file_reader.write(user + ',' + str(amplitute) + '\n')

if __name__ == '__main__':
    input_dir = "/home/striker/Dropbox/NSE_2018_e4/Experiment/"
    find_amplitute(input_dir)