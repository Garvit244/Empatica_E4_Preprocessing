import pandas as pd

def find_amplitute(input_dir):
    users = [ "Darshan", "Garvit", "Francisco", "Sarah"]
    # output_file = input_dir + 'Amplitute.csv'
    # output_file_reader = open(output_file, 'w')

    for user in users:
        input_file = input_dir + user + "/EDA_10min/EDA_leda.csv"
        pd_input = pd.read_csv(input_file)
        amplitute =  round(pd_input.diff()[1:].abs().mean().values[0], 3)
        # output_file_reader.write(user + ',' + str(amplitute) + '\n')

if __name__ == '__main__':
    input_dir = "/home/striker/Dropbox/NSE_2018_e4/Tampines/9_Feb/"
    find_amplitute(input_dir)