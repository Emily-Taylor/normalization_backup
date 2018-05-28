"""A script to convert tsv file to json"""
import csv
import json
import fire



def convert_tsv(filename, output_filename=None):
    """ 
    we take file with tabs and return a json array 
    with each array representing a single company.
    """
    data_json = []
    if output_filename is None:
        output_filename = 'companies-clean-array-v2.json'
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for line in reader:
            row = []
            for i in line:
                if i !='':
                    #print(i)
                    row.append(i)
            data_json.append(row)
        data_json_clean = [x for x in data_json if x != []]
        with open(output_filename, 'w') as outfile:
            json.dump(data_json_clean, outfile)
if __name__ == '__main__':
    fire.Fire()