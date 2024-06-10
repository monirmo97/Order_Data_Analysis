Order Data Analysis

This Python script is designed for generating and analyzing order data. It includes functionalities to generate synthetic order data, clean the data, and produce various visual reports. The primary features include:

Generating Data: 
You can specify the number of products and values per product to generate synthetic order data. The generated data is saved to a CSV file.

Cleaning Data: 
The script reads the generated CSV file, cleans the data by expanding rows for products with multiple values, and saves the cleaned data to a new CSV file.

Analyzing Data: 
The script allows users to analyze the data by providing a customer ID. It then generates and saves visual reports such as the number of purchases per month, the purchase amount per month, and the number of purchases for each product by the target customer.

Additional Reports: With the -r or --report option, the script generates three additional reports:

The top 5 best-selling products in one year.
The number of orders in each month.
The amount of sales per month.

Usage:
Install Dependencies: Make sure you have the required dependencies installed. You can install them using:
pip install -r requirements.txt
After that run the Script:
python main.py

File Descriptions:
main.py: Main script for generating, cleaning, and analyzing order data.
generateData.py: Module containing functions for generating synthetic order data.