import pandas as pd

file_path = 'downloads/macroeconomic_indicators.xlsx'

# Read the Excel file with all sheets
df = pd.read_excel(
    file_path,
    sheet_name=None,
    engine='openpyxl',
    header=3
)



for sheet_name, sheet_data in df.items():
    # Drop the 1st column from each sheet
    sheet_data = sheet_data.iloc[:, 1:]
    # Set the first column as index
    sheet_data.set_index(sheet_data.columns[0], inplace=True, drop=True)
    # Make the index a datetime index
    sheet_data.index = pd.to_datetime(sheet_data.index, errors='coerce')
    # Drop columns with Unnamed in the name
    sheet_data = sheet_data.loc[:, ~sheet_data.columns.str.contains('^Unnamed')]
    print(f"Sheet: {sheet_name}")
    print(sheet_data.head())  # Print the first few rows of each sheet
    print("\n")
    print(sheet_data.info())  # Print the info of each sheet

file_path = 'downloads/other_macroeconomic_indicators.xlsx'

# Read the Excel file with all sheets
df = pd.read_excel(
    file_path,
    sheet_name=None,
    engine='openpyxl',
    header=1
)

for sheet_name, sheet_data in df.items():
    # Drop the Unnamed: 0 column from each sheet
    sheet_data = sheet_data.iloc[:, 1:]
    # Drop the first 1 row
    sheet_data = sheet_data.drop(sheet_data.index[:1])
    # Set the first column as index
    sheet_data.set_index(sheet_data.columns[0], inplace=True, drop=True)
    # Make the index a datetime index
    sheet_data.index = pd.to_datetime(sheet_data.index, errors='coerce')
    # Drop columns with Unnamed in the name
    sheet_data = sheet_data.loc[:, ~sheet_data.columns.str.contains('^Unnamed')]
    print(f"Sheet: {sheet_name}")
    print(sheet_data.head())  # Print the first few rows of each sheet
    print("\n")
    print(sheet_data.info())  # Print the info of each sheet