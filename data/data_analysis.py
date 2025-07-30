import pandas as pd

def csv_to_df(file):
    df = pd.read_csv(file)

    return df

# if __name__ == '__main__':
#     csv_to_df('countries.csv')