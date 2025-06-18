import pandas as pd
import matplotlib.pyplot as plt
#import os
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Open file 'customers.csv' if folder 'CSV' and convert it into df
#path = os.path.join('CSV', 'customers.csv')

# Open csv file as df and parse date column
df = pd.read_csv('customers.csv', parse_dates=['registration_date'])

# Check dtype of date column
print(f"\n{df['registration_date'].dtype}\n")

# Check missing values
missing_data = df.isnull()
for col in missing_data.columns.values.tolist():
    print(missing_data[col].value_counts())
    print("")

# Replace 'age' missing values with mean and turn in into 'int'
mean_age = df['age'].astype('float').mean(axis=0)
df['age'].replace(np.nan, mean_age, inplace=True)
df['age'] = df['age'].astype('int')

# Replace 'gender' missing values with 'Unknown'
df['gender'].replace(np.nan, 'Unknown', inplace=True)

# Binning of customers
bins = [df['purchase_amount'].min(), 100, 300, df['purchase_amount'].max()]
group_names = ['low', 'medium', 'high']
df['purchase_binned'] = pd.cut(df['purchase_amount'], bins, labels=group_names, include_lowest=True)

# Choose customers from USA having purchases > $100
USA_customers_more_100 = df[(df['country'] == 'USA') & (df['purchase_amount'] > 100)]
print(USA_customers_more_100)
print("")

# Average purchases amount by country
print(f"{df.groupby('country')['purchase_amount'].mean()}")
print("")

# Number of registered customers by year
df['registration_year'] = df['registration_date'].dt.year
print(df.groupby('registration_year').size())
print("")

# Number of customers registered less than a year ago
print(((pd.Timestamp.today().normalize() - df['registration_date']).dt.days < 365).sum())
print("")

# Total purchases per year bar plot
yearly_purchases = df.groupby('registration_year')['purchase_amount'].sum()
print(yearly_purchases)
plt.bar(yearly_purchases.index, yearly_purchases)
plt.style.use('ggplot')
plt.xlabel('Year')
plt.ylabel('Total amount')
plt.title('Total purchases per year')
plt.grid(True, axis='y')
plt.savefig('total_purchases_per_year.png')
plt.show()

# Save df to csv
df.to_csv('customers_cleaned.csv')