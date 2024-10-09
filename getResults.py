import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#Base URL for navigating the links
base_url = 'https://bench.cr.yp.to/'

#URLs to scrape
urls = ['results-hash.html']
#'results-stream.html', 'results-aead.html', 'results-dh.html', 'results-kem.html', 'results-sign.html'
count = 1
#Loop over urls
for entry in urls:
    url = base_url + entry
    #Send a GET request to the main page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    #Find all links to the "Test results" pages
    links = [base_url + a['href'] for a in soup.find_all('a') if 'crypto_' in a['href']]

    #Initialize an empty dataFrame to hold all table data
    combined_df = pd.DataFrame()

    #Loop over each link and scrape the table
    for link in links:
        page = requests.get(link)
        page_soup = BeautifulSoup(page.content, 'html.parser')
        
        #Find the table in the page
        table = page_soup.find('table')
        
        #Extract rows
        rows = []
        for row in table.find_all('tr'):
            cells = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
            rows.append(cells)
        
        #Convert the rows to a DataFrame
        df = pd.DataFrame(rows)
        
        #Concatenate this DataFrame to the combined DataFrame
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    #Save the combined DataFrame to a CSV file
    file_name = 'results' + str(count) + '.csv'
    combined_df.to_csv(file_name, index=False)
    print("Data has been saved to " + file_name)
    count = count + 1

# List to hold DataFrames
dfs = []

# Loop over the created CSV files and read them
for i in range(1, count):
    file_name = 'results' + str(i) + '.csv'
    
    # Check if the file exists before reading it
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        dfs.append(df)

# Concatenate all DataFrames into one
final_df = pd.concat(dfs, ignore_index=True)

# Save the concatenated DataFrame to a new CSV file
final_df.to_csv('combined_results.csv', index=False)

print("All CSV files have been concatenated and saved to 'combined_results.csv'.")