from dataframe_pcg import Dataframe, stats


def main():
    """
    Main function to demonstrate dataframe operations:
    1. Read CSV data
    2. Fill missing values
    3. Generate statistics
    4. Write cleaned data
    """
    # Read data
    datapath = "data/titanic.csv"
    dtype = "data/titanic_dtype.csv"
    
    print("Loading data...")
    df = Dataframe.read_csv(datapath, dtype)
    
    print("\nNull counts before fillna:")
    print(df.count_nulls())
    
    # Fill missing values
    # Numeric columns → mean
    # Categorical columns → mode
    print("\nFilling missing values...")
    df.fillna(stats.get_col_mean, stats.get_col_mode)
    
    print("\nNull counts after fillna:")
    print(df.count_nulls())
    
    # Generate statistics file
    print("\nGenerating statistics...")
    df.describe()
    
    # Write cleaned data to CSV
    print("\nWriting cleaned data...")
    df.to_csv("data/titanic_cleaned.csv")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
