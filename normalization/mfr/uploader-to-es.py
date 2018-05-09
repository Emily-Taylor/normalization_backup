# coding: utf-8
"""A script to prepare json file for bulk upload into elastic search"""
import os
import json
import fire
import jsonlines


def create_file(filename, output_filename=None):
    if output_filename is None:
        output_filename = 'output.jsonl'
    
    post_command = { "index" : {"_type" : "mfr"} }
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname('./')))
    with open(os.path.join(__location__, filename), "r", encoding="utf-8") as f:
        data = json.load(f)
        with jsonlines.open(os.path.join(__location__, output_filename), mode='w') as writer:
            for line in data:
                if len(line) ==1:
                    data  = { "name": line[0], "alias": line[0]}
                    writer.write(post_command)
                    writer.write(data)
                elif  len(line) >1:
                    first = line[0]
                    for name in line:
                        #print("name: {0}".format(name))
                        #print("data: {0}".format(str(data)))
                        data  = { "name":first, "alias": name}
                        writer.write(post_command)
                        writer.write(data)
    with open(os.path.join(__location__, output_filename), "a") as myfile:
        myfile.write("\n")


if __name__ == '__main__':
    fire.Fire()