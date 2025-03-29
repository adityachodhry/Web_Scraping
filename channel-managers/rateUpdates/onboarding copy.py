import pandas as pd

file_path = "C:\\Users\\Akshay\\Desktop\\Aditya\\leadDetails1.xlsx"

df = pd.read_excel(file_path, sheet_name='Lead Data')
# print(df)  

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

selected_columns = ['leadName', 'hotelName', 'initialTaskCreatedAt', 'expectedClosingDate', 'closingDate']
filtered_df = filtered_df[selected_columns]

initial_task_split = filtered_df['initialTaskCreatedAt'].str.split('T', expand=True)
final_task_split = filtered_df['expectedClosingDate'].str.split('T', expand=True) if filtered_df['expectedClosingDate'].str == None else filtered_df['closingDate'].str.split('T', expand=True)


filtered_df['initialTaskCreatedAt'] = initial_task_split[0]
filtered_df['expectedClosingDate'] = final_task_split[0]

filtered_df['initialTaskCreatedAt'] = pd.to_datetime(filtered_df['initialTaskCreatedAt']).dt.strftime('%Y-%m-%d')
filtered_df['expectedClosingDate'] = pd.to_datetime(filtered_df['expectedClosingDate']).dt.strftime('%Y-%m-%d')

filtered_df['difference'] = (pd.to_datetime(filtered_df['expectedClosingDate']) - pd.to_datetime(filtered_df['initialTaskCreatedAt'])).dt.days

filtered_file_path = "C:\\Users\\Akshay\\Desktop\\Aditya\\leadDetails(New).xlsx"
filtered_df.to_excel(filtered_file_path, index=False)

print("Filtered data with specific columns and date difference saved to:", filtered_file_path)
