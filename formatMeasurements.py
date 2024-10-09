import os
import re

# Define the pattern for the file name: results_*_measurements.csv where * is a digit
pattern = re.compile(r'results_\d+_measurements\.csv')

# Get the list of files in the current directory
files_in_directory = os.listdir('.')

# Check for files that match the pattern
matching_files = [f for f in files_in_directory if pattern.match(f)]

# Function to process the files
def process_file(file_path):
    header_1 = None
    header_2 = []
    previous_header_1 = None
    
    with open(file_path, 'r') as file:
        for line in file:
            # Strip whitespace from the beginning and end of the line
            line = line.strip()
            
            # If the line starts with letters (not numbers), it's Header 1
            if re.match(r'^[A-Za-z]', line):
                # If Header 1 is different from the previous one, print it and reset Header 2
                if line != header_1:
                    header_1 = line
                    header_2 = []
                    print(f"New Header 1: {header_1}")
                continue
            
            # If the line is the next after Header 1, assume it's Header 2 and split it by commas
            if header_1 and not header_2:
                header_2 = line.split(',')
                print(f"New Header 2: {header_2}")
                continue

# Iterate over all matching files and process them
for file_name in matching_files:
    process_file(file_name)
