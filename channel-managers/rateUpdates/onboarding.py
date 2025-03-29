import pandas as pd

file_path = "C:\\Users\\Akshay\\Desktop\\Aditya\\leadDetails.xlsx"

df = pd.read_excel(file_path, sheet_name='Lead Data')  
print(df)

filtered_df = df[
    (df['status1'] == 'Customer') |
    (df['status2'] == 'Customer') |
    (df['status3'] == 'Customer') |
    (df['status4'] == 'Customer') |
    (df['status5'] == 'Customer') |
    (df['status6'] == 'Customer') |
    (df['status7'] == 'Customer') |
    (df['status8'] == 'Customer') |
    (df['status9'] == 'Customer') |
    (df['status10'] == 'Customer') |
    (df['status11'] == 'Customer')
]

selected_columns = ['leadName', 'hotelName', 'initialTaskCreatedAt',
                    'modifiedOn1', 'modifiedOn2', 'modifiedOn3',
                    'status1', 'status2', 'status3', 'status4', 'status5', 'status6', 'status7', 'status8', 'status9', 'status10', 'status11']
filtered_df = filtered_df[selected_columns]

initial_task_split = filtered_df['initialTaskCreatedAt'].str.split('T', expand=True)
filtered_df['initialTaskCreatedAt'] = initial_task_split[0]
filtered_df['initialTaskCreatedAt'] = pd.to_datetime(filtered_df['initialTaskCreatedAt']).dt.strftime('%Y-%m-%d')

def get_modified_date(row):
    for i in range(1, 12):
        status_col = f'status{i}'
        modified_col = f'modifiedOn{i}'
        if status_col in row and modified_col in row and row[status_col] == 'Customer':
            return row[modified_col]
    return pd.NaT

filtered_df['modifiedOn'] = filtered_df.apply(get_modified_date, axis=1)
filtered_df['modifiedOn'] = pd.to_datetime(filtered_df['modifiedOn']).dt.strftime('%Y-%m-%d')

filtered_df['difference'] = (pd.to_datetime(filtered_df['modifiedOn']) - pd.to_datetime(filtered_df['initialTaskCreatedAt'])).dt.days

filtered_df.drop(['modifiedOn1', 'modifiedOn2', 'modifiedOn3', 
                  'status1', 'status2', 'status3', 'status4', 'status5', 'status6', 'status7', 'status8', 'status9', 'status10', 'status11'], 
                 axis=1, inplace=True)

filtered_file_path = "C:\\Users\\Akshay\\Desktop\\Aditya\\filtered_leadDetails1.xlsx"
filtered_df.to_excel(filtered_file_path, index=False)

print("Filtered data with specific columns, date difference, and modified date saved to:", filtered_file_path)
