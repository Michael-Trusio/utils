import csv

# Open the input and output files
with open('BV_240_DLY_PO_PLAN_TCIN_04062023_KW.txt', 'r') as input_file, open('BV_240_DLY_PO_PLAN_TCIN_04062023_KW.csv', 'w', newline='') as output_file:
   
    # Define the tab delimiter
    delimiter = '\t'
   
    # Create the csv reader object
    reader = csv.reader(input_file, delimiter=delimiter)
   
    # Create the csv writer object
    writer = csv.writer(output_file)
   
    # Read the existing headers from the input file
    existing_headers = next(reader)
   
    # Add the two new column headers
    new_headers = existing_headers + ['INGESTION_TIME', 'INGESTION_FILE']
   
    # Write the updated headers to the output file
    writer.writerow(new_headers)
   
    # Read each remaining line of the input file
    for line in reader:
       
        # Add the two new columns to the existing values
        new_values = line + ['', '']
       
        # Write the row to the output file
        writer.writerow(new_values)