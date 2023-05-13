import hcl2

def check_tf(filename, header):
    with open(filename, 'r') as f:
        dict = hcl2.load(f)

    snowflake = dict['resource'][0]['snowflake_table']
    table = list(snowflake.keys())[0]
    print(table)
    columns = [t['name'] for t in snowflake[table]['column']][:-3]
    return set(header) == set(columns)
