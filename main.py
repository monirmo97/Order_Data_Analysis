import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from generateData import generate_data, clean_data, save_to_csv
from heapq import nlargest

def plot_bestselling_products(clean_data):
    # Create a bar plot of the best selling products
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Get the top 5 best-selling products
    best_selling = clean_data.groupby('Name Product')['Final Quantity'].sum().nlargest(5)
    
    # Plot the bar chart
    best_selling.plot(kind='bar', color='purple')
    
    # Formatting the y-axis labels as integers
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    
    # Set plot title and labels
    ax.set_title("Top 5 Best-Selling Products")
    ax.set_xlabel("Product Name")
    ax.set_ylabel("Total Quantity Sold")
    
    # Ensure tight layout and save the plot
    plt.tight_layout()
    plt.savefig('best_selling_products.png')
    plt.close()

def number_orders_month(clean_data):
    # Create a bar plot of the number of orders per month
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Count the number of orders for each month
    clean_data.groupby('Number Month')['Order Date'].count().plot(kind='bar', color='r')
    
    # Formatting the y-axis labels as integers
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    
    # Set plot title and labels
    ax.set_title("Number of Orders in Each Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Orders")
    
    # Ensure tight layout and save the plot
    plt.tight_layout()
    plt.savefig('number_of_orders.png')
    plt.close()

def plot_amount_sell(clean_data):
    # Create a bar plot for the amount of sales per month
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Calculate the total amount of sales for each month
    clean_data.groupby('Number Month')['Final Price'].sum().plot(kind='bar', color='g')
    
    # Formatting the y-axis labels as integers
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    
    # Set plot title and labels
    ax.set_title("Amount of Sales per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount of Sales")
    
    # Ensure tight layout and save the plot
    plt.tight_layout()
    plt.savefig('amount_of_sales.png')
    plt.close()

def main():
    # Set up argparse for command-line arguments
    parser = argparse.ArgumentParser(description='Generate and save order data to CSV file')
    parser.add_argument('--number_products', type=int, default=100, help='Number of products to generate')
    parser.add_argument('--item', type=int, default=3, help='Number of values per product')
    parser.add_argument('--path', type=str, default='csv_file.csv', help='Path to save the CSV file')
    parser.add_argument('-r', '--report', action='store_true', help='Generate additional reports')
    args = parser.parse_args()

    # Generate and save data to CSV
    data = generate_data(args.number_products, args.item)
    save_to_csv(args.path, data)

    # Read and clean the CSV data
    df = pd.read_csv(args.path, sep=',')
    
    cleaned_data = clean_data(df)
    
    clean_data_path = 'clean_data.csv'
    if os.path.exists(clean_data_path):
        save_to_csv(clean_data_path, cleaned_data)
    else:
        print('Error! The path does not exist')

    try:
        if args.report:
            # Generate additional reports if the -r option is provided
            plot_bestselling_products(cleaned_data)
            number_orders_month(cleaned_data)
            plot_amount_sell(cleaned_data)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
