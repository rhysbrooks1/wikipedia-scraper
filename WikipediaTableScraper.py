import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_U.S._states_by_date_of_admission_to_the_Union'

page = requests.get(url)

soup = BeautifulSoup(page.text, features="html.parser")

# Set desired table in this case the table is the first on the page
table = soup.find_all('table')[0]

# Checks if the table exists
if table:
    # Extract column titles
    table_titles = table.find_all('th')
    table_column_titles = [title.text.strip() for title in table_titles]

    # Create an empty DataFrame with column titles
    df = pd.DataFrame(columns=table_column_titles)

    rows = []
 
    # Extract data from each row and add it to the DataFrame
    table_rows = table.find_all('tr')[1:]  # Start from the second row to skip the header
    for row in table_rows:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]
        rows.append(dict(zip(table_column_titles, individual_row_data)))

    df = pd.DataFrame(rows)

    # Display the DataFrame
    pd.set_option('display.max_rows', None)
    print(table_column_titles)
    print(df)
else:
    print("Table not found with the specified class.")
