import os
import argparse
import pandas as pd
import numpy as np
import random
from faker import Faker
from faker_food import FoodProvider

fake = Faker()
fake.add_provider(FoodProvider)


def generate_data(number_products, item):
    order_date = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    order_features = []

    for _ in range(number_products):
        # Generate random values for Order Date, Customer Id, Number Month
        order_date_value = pd.to_datetime(np.random.choice(order_date, size=1, replace=False)[0])
        customer_id_value = random.randint(1, 100)

        # Generate multiple values for 'Name Product', 'Basic Price', 'Final Quantity'
        name_products = [fake.fruit() for _ in range(item)]
        basic_prices = [random.uniform(100, 1000) for _ in range(item)]
        final_quantities = [random.randint(1, 20) for _ in range(item)]
        number_month_value = [random.randint(1, 12) for _ in range(item)] 
        
        # Calculate 'Final Price' for each set of values
        final_prices = [basic * quantity for basic, quantity in zip(basic_prices, final_quantities)]

        # Orders feature
        orders = {
            'Order Date': order_date_value,
            'Customer Id': customer_id_value,
            'Name Product': name_products,
            'Number Month': number_month_value,
            'Basic Price': basic_prices,
            'Final Quantity': final_quantities,
            'Final Price': final_prices
        }
        order_features.append(orders)

    return order_features


def clean_data(df):
    # Remove the quotation marks and square brackets from the columns that contain multiple values
    df['Name Product'] = df['Name Product'].str.strip('[]\"')
    df['Basic Price'] = df['Basic Price'].str.strip('[]\"')
    df['Final Quantity'] = df['Final Quantity'].str.strip('[]\"')
    df['Final Price'] = df['Final Price'].str.strip('[]\"')
    df['Number Month'] = df['Number Month'].str.strip('[]\"')

    # Split the columns by commas and create a list of values for each cell
    df['Name Product'] = df['Name Product'].apply(lambda x: [item.strip("'") for item in x.split(',')])
    df['Basic Price'] = df['Basic Price'].apply(lambda x: [float(item) for item in x.split(',')])
    df['Final Quantity'] = df['Final Quantity'].apply(lambda x: [int(item) for item in x.split(',')])
    df['Final Price'] = df['Final Price'].apply(lambda x: [float(item) for item in x.split(',')])
    df['Number Month'] = df['Number Month'].apply(lambda x: [int(item) for item in x.split(',')])

    # Create a new DataFrame to store the expanded rows
    expanded_rows = []

    # Iterate over rows
    for _, row in df.iterrows():
        for i in range(len(row['Name Product'])):
            expanded_rows.append([
                row['Order Date'],
                row['Customer Id'],
                row['Name Product'][i],
                row['Number Month'][i],
                row['Basic Price'][i],
                row['Final Quantity'][i],
                row['Final Price'][i]
            ])

    # Create a new DataFrame from the expanded rows
    result_df = pd.DataFrame(expanded_rows, columns=df.columns)
    # Drop NaN values
    result_df.dropna(inplace=True)

    # Drop duplicate rows
    result_df.drop_duplicates(inplace=True)

    return result_df


def save_to_csv(file_path, data):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f'Data saved to {file_path}')


def main():
    parser = argparse.ArgumentParser(description='Generate and save order data to CSV file')
    parser.add_argument('--number_products', type=int, default=10, help='Number of products to generate')
    parser.add_argument('--item', type=int, default=2, help='Number of values per product')
    parser.add_argument('--path', type=str, default='csv_file.csv', help='Path to save the CSV file')

    args = parser.parse_args()
    data = generate_data(args.number_products, args.item)
    save_to_csv(args.path, data)

    # Read csv file
    df = pd.read_csv(args.path, sep=',')

    # Call clean data function
    clean_data_path = 'clean_data.csv'
    if os.path.exists(clean_data_path):
        data = clean_data(df)
        save_to_csv(clean_data_path, data)
    else:
        print('Error! The path does not exist')


if __name__ == '__main__':
    main()
