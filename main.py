from dataframe_pcg import Dataframe,stats
import numpy

def main():
    # TODO: Read data
    
    datapath="data/titanic.csv"
    dtype="data/titanic_dtype.csv"
    
    df = Dataframe.read_csv(datapath, dtype) 
    # TODO: Fill missing values
    df.fillna(stats.get_col_mean, stats.get_col_mode)
    print(df.count_nulls())
    # Numeric columns → mean
    # Categorical columns → mode
    # TODO:Generate statistics file
    df.describe()
    # TODO:Write cleaned data to CSV
    df.to_csv("data/titanic_cleaned.csv")

if __name__ == "__main__":
    main()
