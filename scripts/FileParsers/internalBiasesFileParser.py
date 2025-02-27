import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
from numpy import double
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="internal_biases",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor() 

def main():
    data_path = path
    instance = "0"
    print(path)
    part = data_path.split("/")[7]
    print(part)
    part_num = data_path.split("/")[8]
    print(part_num)
    temp = data_path.split("/")[9].split("_")[0]
    print(temp)
    date = data_path.split("/")[9].split("_")[1]
    print(date)
    file = data_path.split("/")[10]
    print(file)

    parts = part.split('_')

    lot = bin = wafer = process_corner = ''
    
    # Assign values based on the number of parts
    if len(parts) >= 1:
        lot = parts[0]
    if len(parts) >= 2:
        bin = parts[1]
    if len(parts) >= 3:
        wafer = parts[2]
    if len(parts) == 4:
        process_corner = parts[3]

    # Gets the data files from the database
    cur.execute("""
    SELECT 
    tf."Test Data"
    FROM 
        test_file tf
    INNER JOIN 
        test t ON tf."Test Id" = t."Test Id"
    INNER JOIN 
        chip c ON c."Chip Id" = t."Chip Id"
    WHERE 
        t."Test" = 'internal_biases'
        AND c."Lot" = %s 
        AND c."Bin" = %s
        AND c."Wafer" = %s
        AND c."Process Corner" = %s 
        AND t."Temp" = %s
        AND t."Date" = %s 
        AND c."Part Number" = %s
        AND tf."File Name" = %s
    """, (lot, bin, wafer, process_corner, temp, date, part_num, file))
    files = cur.fetchall()
    raw_data_files = [data_files[0] for data_files in files]

    # Creates the files
    for data in raw_data_files:
        # Construct a unique file name based on the test_id or other properties
        save_name = f"{file}" 

        with open(f"./parsed_files/{CHIP}/{TEST}/{part}/{part_num}/{temp + "_" + date}/{save_name}.txt", "wb") as save_file:
            # Decodes the data and writes into the file
            byte_data = bytes(data)
            save_file.write(byte_data)   

def run_script(chip, datapath, path_to_part, save, save_path, partNum):
    global CHIP, TEST, PATH_TO_DATA, path, save_name, save_directory, partNumber
    TEST = "internal_biases"
    PATH_TO_DATA = datapath

    partNumber = partNum

    CHIP = chip
    path  = path_to_part

    save_name = save
    if(".txt" in save_name):
        save_name = save_name[:-4]
    save_directory = save_path
    main()
    return 

conn.commit()

