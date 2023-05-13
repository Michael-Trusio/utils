# In this example, 'fixed_width.txt' looks like

# k12582927001611USNA
# k12582990001497INAS
# k12583053001161LNEU

# And it should be split to look like this

# k,1258292700,1611,US,NA

output_file = 'output.csv'
fields = [9,3,4,6,1,10,2,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,4,25]
filename = 'fixed_width.txt'
headers = ['BRICK_COD', 'REGI_COD', 'DIST_COD', 'TERR_COD', 'CLIE_LET', 'FCC_COD', 'REPO_COD', \
            'MONTH_1_UNITS', 'MONTH_2_UNITS', 'MONTH_3_UNITS', 'MONTH_4_UNITS', 'MONTH_5_UNITS', \
            'MONTH_6_UNITS', 'MONTH_7_UNITS', 'MONTH_8_UNITS', 'MONTH_9_UNITS', 'MONTH_10_UNITS', \
            'MONTH_11_UNITS', 'MONTH_12_UNITS', 'MONTH_13_UNITS', 'MONTH_14_UNITS', 'MONTH_15_UNITS', \
            'MONTH_16_UNITS', 'MONTH_17_UNITS', 'MONTH_18_UNITS', 'MONTH_19_UNITS', 'MONTH_20_UNITS', \
            'MONTH_21_UNITS', 'MONTH_22_UNITS', 'MONTH_23_UNITS', 'MONTH_24_UNITS', 'OUTLET_TYPE','CONTROL_UNITS_PERIOD' ]



def fixed_width_to_csv(filename, fields, output_file, headers=[]):

    with open(filename) as f, open(output_file, 'a') as o:
        if headers:
            o.write(','.join(headers) + '\n')
        for line in f:                      # avoids reading whole file into memory
            row = ""
            i = 0
            for field in fields:
                j = i+field                 # end point of substring
                substr = line[i:j]
                row += substr + ','
                i = j
            row = row[:-1]                  # remove trailing comma
            row += '\n'
            o.write(row)
