import csv

csv_file = input("Enter path to your CSV file: ")
name = input("Enter table name: ")
schema = input("Enter schema name: ")
comment = input("Enter table comment: ")
addAudit = input("Do you want to add audit columns (Yes or No): ")

if "." in csv_file and csv_file[-4:] != ".csv":
    raise ValueError("ERROR: File needs to be in .csv format")
elif csv_file[-4:] != ".csv":
    csv_file += ".csv"

output_file = name.lower() + ".tf"
schema = schema.upper()

with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    headers = csv_reader.fieldnames

with open(output_file, mode='w') as file:
    file.write(f'resource "snowflake_table" "{name}" {{\n')
    file.write(f'\tdatabase = local.database\n')
    file.write(f'\tschema = "{schema}"\n')
    file.write(f'\tname = "{name}"\n')
    file.write(f'\tcomment = "{comment}"\n')
    file.write(f'\n')
    for header in headers:
        file.write(f'\tcolumn {{\n')
        file.write(f'\t\tname = "{header}"\n')
        file.write(f'\t\ttype = "VARCHAR"\n')
        file.write(f'\t}}\n')
        file.write(f'\n')
    if addAudit.upper() == "YES":
        file.write(f'\tcolumn {{\n')
        file.write(f'\t\tname = "INGESTION_TIME"\n')
        file.write(f'\t\ttype = "VARCHAR"\n')
        file.write(f'\t}}\n')
        file.write(f'\n')
        file.write(f'\tcolumn {{\n')
        file.write(f'\t\tname = "INGESTION_FILE"\n')
        file.write(f'\t\ttype = "VARCHAR"\n')
        file.write(f'\t}}\n')
        file.write(f'\n')
    file.write('}')
    print('Finished!')