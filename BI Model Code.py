import pandas as pd
import numpy as np

# Step 1: Load the data
file_path = r"YOUR_FILE_PATH_HERE.xlsx"  
data = pd.read_excel(file_path)

# Step 2: Clean up column names
# Remove leading and trailing spaces to prevent issues with column name mismatches
data.columns = data.columns.str.strip()

# Step 3: Verify column names
# Print column names to check for any discrepancies
print("Column names in the DataFrame:", data.columns)

# Step 4: Calculate L0 for each fish
# Make sure the column names match what you see in your DataFrame
data['L0_MM'] = data['L(CPT)_MM'] * (data['HATCH_UM'] / data['R(OP)_um'])

# Step 5: Initialize DataFrame to store back-calculated lengths
back_calculated_lengths = pd.DataFrame()

# Step 6: Convert R(OP)_MM to micrometers for consistency
data['R(OP)_UM'] = data['R(OP)_um'] * 1000

# Step 7: Back-calculate the size at age for each fish
for i, row in data.iterrows():
    Lc = row['L(CPT)_MM']
    Rc = row['R(OP)_UM']
    L0 = row['L0_MM']
    FishKey = row['FishKey']
    
    # Extract otolith intervals and convert to micrometers
    otolith_intervals = row.loc['1':'164'].dropna().values * 1000  
    
    # Initialize array to store back-calculated lengths
    Lt = np.zeros(len(otolith_intervals))
    
    # Perform back-calculation using the BI model
    for t, Rt in enumerate(otolith_intervals):
        Lt[t] = Lc - ((Rc - Rt) / Rc) * (Lc - L0)
    
    # Store back-calculated lengths in a new DataFrame
    fish_data = pd.DataFrame({
        'FishKey': [FishKey] * len(Lt),
        'Age': np.arange(len(Lt)),
        'Back_Calculated_Length_MM': Lt
    })
    
    back_calculated_lengths = pd.concat([back_calculated_lengths, fish_data], ignore_index=True)

# Step 8: Transform data for one row per fish
# Group by 'FishKey' and 'Age', then unstack to make each fish a single row
transformed_lengths = back_calculated_lengths.groupby(['FishKey', 'Age']).mean().unstack()

# Flatten the multi-level column index
transformed_lengths.columns = [f'Age_{int(col[1])}' for col in transformed_lengths.columns.values]

# Reset the index to make 'FishKey' a regular column
transformed_lengths.reset_index(inplace=True)

# Step 9: Save the transformed data to a CSV file
transformed_file_path = "OUTPUT FILE.csv"  
transformed_lengths.to_csv(transformed_file_path, index=False)
