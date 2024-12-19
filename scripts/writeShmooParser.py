import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
from numpy import double
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="write_shmoo",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor() 

def main():

    if not os.path.exists("./parsed_files/" + CHIP + "/" + TEST):
        os.mkdir("./parsed_files/" + CHIP + "/" + TEST)

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

    parts = part.split('_')

    lot = bin = wafer = process_corner = None
    
    # Assign values based on the number of parts
    if len(parts) >= 1:
        lot = parts[0]
    if len(parts) >= 2:
        bin = parts[1]
    if len(parts) >= 3:
        wafer = parts[2]
    if len(parts) == 4:
        process_corner = parts[3]

    cur.execute("""
    SELECT 
    tf."Test Id"
    FROM 
        test_file tf
    INNER JOIN 
        test t ON tf."Test Id" = t."Test Id"
    INNER JOIN 
        chip c ON c."Chip Id" = t."Chip Id"
    WHERE 
        t."Test" = 'write_shmoo'
        AND (c."Lot" = %s OR (c."Lot" IS NULL AND %s IS NULL))
        AND (c."Bin" = %s OR (c."Bin" IS NULL AND %s IS NULL))
        AND (c."Wafer" = %s OR (c."Wafer" IS NULL AND %s IS NULL))
        AND (c."Process Corner" = %s OR (c."Process Corner" IS NULL AND %s IS NULL))
        AND (t."Temp" = %s OR (t."Temp" IS NULL AND %s IS NULL))
        AND (t."Date" = %s OR (t."Date" IS NULL AND %s IS NULL))
        AND (c."Part Number" = %s OR (c."Part Number" IS NULL AND %s IS NULL))
    """, (lot, lot, bin, bin, wafer, wafer, process_corner, process_corner, temp, temp, date, date, part_num, part_num))
    files = cur.fetchall()
    test_id = [file[0] for file in files]

    for idx, files in enumerate(test_id):
        # Construct a unique file name based on the test_id or other properties
        save_name = f"test_file_{files}_{idx+1}"  # You can customize the naming pattern here

        with open(f"./parsed_files/{CHIP}/{TEST}/{save_name}.txt", "a") as save_file:
            # Retrieve bytea data
            cur.execute('SELECT "Test Data" FROM test_file WHERE "File Id" = %s', (files,))
            test_data = cur.fetchone()
            
            if test_data:
                # Assuming the test data is in a bytea format, you might need to decode it
                # Example: If it's byte data, you can decode it to a string or save as bytes.
                save_file.write(str(test_data[0]))  # or save_file.write(test_data[0].decode('utf-8')) if it's byte data



def run_script(chip, datapath, path_to_part, save, save_path, partNum):
    global CHIP, TEST, PATH_TO_DATA, path, save_name, save_directory, partNumber
    TEST = "write_shmoo"
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

