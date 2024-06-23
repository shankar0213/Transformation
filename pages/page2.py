from navigation import make_sidebar
import streamlit as st

make_sidebar()

import streamlit as st
import pandas as pd
from faker import Faker
import numpy as np

# Function to generate data based on the data type
def generate_data(dtype, n):
    fake = Faker()
    data = []
    
    ddtype=dtype[:3]
    #print(ddtype)
    if dtype == 'int':
        data = np.random.randint(0, 100, size=n)
    elif dtype == 'float' or ddtype=='dou':
        data = np.random.uniform(0, 100, size=n)
    elif dtype == 'string':
        data = [fake.word() for _ in range(n)]
    elif dtype == 'bool':
        data = [fake.boolean() for _ in range(n)]
    elif dtype == 'date':
        data = [fake.date() for _ in range(n)]
    else:
        data = [fake.word() for _ in range(n)]  # Default case for unhandled dtypes
    return data

def create_hive_insert_query(table_name, df):
    columns = ", ".join(df.columns)
    values_list = []

    for _, row in df.iterrows():
        values = []
        for value in row:
            if isinstance(value, str):
                values.append(f"'{value}'")
            elif pd.isna(value):
                values.append('NULL')
            else:
                values.append(str(value))
        values_list.append(f"({', '.join(values)})")

    values_str = ",\n".join(values_list)
    query = f"INSERT INTO {table_name} ({columns}) VALUES\n{values_str};"
    return query

def main():
    st.title('CSV Column Config Viewer and Data Generator')

    # File uploader for the CSV config file
    uploaded_file = st.file_uploader("Upload a CSV config file", type=["csv"])
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Check if the required columns are present in the uploaded CSV
        if 'col_name' in df.columns and 'data_type' in df.columns:
            # Display the column names and data types
            st.write("### Column Names and Data Types from CSV")
            st.write(df[['col_name', 'data_type']])
            
            # Get the number of rows to generate from the user
            n = st.number_input("Enter the number of rows to generate", min_value=1, value=5, step=1)
            
            # Generate synthetic data for each column
            synthetic_data = {}
            for index, row in df.iterrows():
                column_name = row['col_name']
                data_type = row['data_type']
                synthetic_data[column_name] = generate_data(data_type, n)
            
            # Create a new DataFrame with the synthetic data
            synthetic_df = pd.DataFrame(synthetic_data)
            
            # Display the synthetic DataFrame
            st.write(f"### Showing the first {n} rows of synthetic data")
            st.dataframe(synthetic_df)
            
            # Get the table name from the user
            table_name = st.text_input("Enter the Hive table name")
            
            if table_name:
                # Create Hive insert query
                hive_query = create_hive_insert_query(table_name, synthetic_df)
                
                # Display the Hive insert query
                st.write("### Hive Insert Query")
                st.code(hive_query)
        else:
            st.error("The uploaded CSV file must contain 'col_name' and 'data_type' columns.")
    else:
        st.info("Please upload a CSV config file.")

if __name__ == "__main__":
    main()
