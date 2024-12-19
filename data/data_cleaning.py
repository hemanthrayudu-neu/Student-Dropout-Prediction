import pandas as pd

def clean_data(input_file, output_file):
    """
    Cleans the dataset:
    - Handles semicolon-separated files (can be adjusted for other delimiters).
    - Formats column names to be human-readable (spaces instead of underscores).
    - Converts columns with numeric data types where possible.
    - Handles missing values by filling them with appropriate strategies.
    - Saves the cleaned data to a new file.

    Parameters:
        input_file (str): Path to the raw dataset.
        output_file (str): Path to save the cleaned dataset.
    """
    try:
        # Load the dataset with the correct delimiter
        df = pd.read_csv(input_file, sep=';')

        # Clean and format column names
        df.columns = (
            df.columns
            .str.strip()                                # Remove leading/trailing spaces
            .str.replace(r'_', ' ', regex=True)        # Replace underscores with spaces
            .str.replace(r'\s+', ' ', regex=True)      # Normalize multiple spaces to single space
            .str.replace(r'[^\w\s]', '', regex=True)   # Remove special characters
        )

        # Convert columns to numeric where possible
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except ValueError:
                    pass  # Retain non-numeric if conversion fails

        # Handle missing values
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                # Fill numeric columns with mean
                df[col] = df[col].fillna(df[col].mean())
            else:
                # Fill non-numeric columns with 'Unknown'
                df[col] = df[col].fillna('Unknown')

        # Save the cleaned data
        df.to_csv(output_file, sep=',', index=False)
        print(f"Cleaned data saved to: {output_file}")

    except Exception as e:
        print(f"Error cleaning data: {e}")

if __name__ == "__main__":
    # Define input and output paths
    input_file = "data.csv"   # Replace with your actual path
    output_file = "cleaned_data.csv"

    # Call the cleaning function
    clean_data(input_file, output_file)
