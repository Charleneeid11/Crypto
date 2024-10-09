import pandas as pd

# Load the two CSV files
output_df = pd.read_csv('output.csv')
res_df = pd.read_csv('res.csv')

# Ensure that both DataFrames have the same number of rows
if len(output_df) != len(res_df):
    print("Error: The two CSV files do not have the same number of rows.")
else:
    # Combine the two DataFrames side by side (horizontally)
    combined_df = pd.concat([output_df, res_df], axis=1)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('combined.csv', index=False)

    print("The files have been combined and saved as 'combined.csv'.")
