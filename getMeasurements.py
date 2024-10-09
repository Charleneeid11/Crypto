# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import os

# # Base URL for navigating the links
# base_url = 'https://bench.cr.yp.to/'

# # URLs to scrape
# urls = ['results-hash.html']
# #, 'results-stream.html', 'results-aead.html', 'results-dh.html', 'results-kem.html', 'results-sign.html'
# count = 1

# # Loop over URLs
# for entry in urls:
#     url = base_url + entry
#     # Send a GET request to the main page
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Find all links whose text contains "Measurements"
#     links = [base_url + a['href'] for a in soup.find_all('a') if 'Measurements' in a.text]

#     # Initialize an empty DataFrame to hold all table data
#     combined_df = pd.DataFrame()

#     # Loop over each link and scrape the table
#     for link in links:
#         page = requests.get(link)
#         page_soup = BeautifulSoup(page.content, 'html.parser')

#         # Find the table in the page
#         table = page_soup.find('table')
        
#         start_collecting = False
#         rows = []

#         if table:
#             for row in table.find_all('tr'):
#                 # Check if the row contains the trigger text
#                 if 'Cycles/byte for long messages' in row.get_text():
#                     start_collecting = True
#                     continue  # Skip this row as it is the header

#                 # Start collecting data after encountering the trigger
#                 if start_collecting:
#                     cells = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
#                     rows.append(cells)

#             # Convert the rows to a DataFrame
#             if rows:
#                 df = pd.DataFrame(rows)
#                 # Concatenate the fetched DataFrame to the combined DataFrame
#                 combined_df = pd.concat([combined_df, df], ignore_index=True)

#     # Save the combined DataFrame to a CSV file if it has data
#     if not combined_df.empty:
#         file_name = f'results_{count}_measurements.csv'
#         combined_df.to_csv(file_name, index=False)
#         print(f"Data has been saved to {file_name}")
#     else:
#         print(f"No data found for {entry}")

#     count += 1

#     # Stop after the first URL for demonstration purposes
#     break


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for navigating the links
base_url = 'https://bench.cr.yp.to/'

# URLs to scrape
urls = ['results-hash.html']
#, 'results-stream.html', 'results-aead.html', 'results-dh.html', 'results-kem.html', 'results-sign.html'
count = 1

# Loop over URLs
for entry in urls:
    url = base_url + entry
    # Send a GET request to the main page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links whose text contains "Measurements"
    links = [base_url + a['href'] for a in soup.find_all('a') if 'Measurements' in a.text]

    # Initialize an empty DataFrame to hold all table data
    combined_df = pd.DataFrame()

    # Loop over each link and scrape the table
    for link in links:
        page = requests.get(link)
        page_soup = BeautifulSoup(page.content, 'html.parser')

        # Find the table in the page
        table = page_soup.find('table')
        
        start_collecting = False
        rows = []

        if table:
            for row in table.find_all('tr'):
                # Check if the row contains the trigger text
                if 'Cycles/byte for long messages' in row.get_text():
                    start_collecting = True

                # Start collecting data including the trigger row
                if start_collecting:
                    cells = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                    rows.append(cells)

            # Convert the rows to a DataFrame
            if rows:
                df = pd.DataFrame(rows)
                # Concatenate the fetched DataFrame to the combined DataFrame
                combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Save the combined DataFrame to a CSV file if it has data
    if not combined_df.empty:
        file_name = f'results_{count}_measurements.csv'
        combined_df.to_csv(file_name, index=False)
        print(f"Data has been saved to {file_name}")
    else:
        print(f"No data found for {entry}")

    count += 1

    # Stop after the first URL for demonstration purposes
    break
