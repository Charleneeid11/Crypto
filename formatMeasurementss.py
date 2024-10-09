import csv

def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read the header lines and store them
        header_long_msg = next(reader)
        subheader_long_msg = next(reader)
        data_long_msg = []
        
        # Read data until we encounter the second header
        for row in reader:
            if "Cycles/byte for 4096 bytes" in row[0]:
                break
            data_long_msg.append(row)
        
        # Now we are at the second header
        header_4096_bytes = row
        subheader_4096_bytes = next(reader)
        data_4096_bytes = list(reader)  # Read the remaining data

        # Combine headers and write them
        combined_header = [f"{header_long_msg[0]} {col}" for col in subheader_long_msg] + [f"{header_4096_bytes[0]} {col}" for col in subheader_4096_bytes]
        writer.writerow(combined_header)
        
        # Write combined data rows
        for i in range(min(len(data_long_msg), len(data_4096_bytes))):
            combined_row = data_long_msg[i] + data_4096_bytes[i]
            writer.writerow(combined_row)

# Specify your input and output file paths
input_file = 'results_1_measurements.csv'
output_file = 'output.csv'

# Call the function
process_file(input_file, output_file)
