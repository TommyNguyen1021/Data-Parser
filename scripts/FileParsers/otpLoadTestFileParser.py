import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
from numpy import double
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="otp_load_test",  user ="postgres", password = "numem@184", port = 5432)

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
    tf."File Id"
    FROM 
        test_file tf
    INNER JOIN 
        test_file2 tf2 ON tf."File Id" = tf2."File Id"
    INNER JOIN 
        test t ON tf."Test Id" = t."Test Id"
    INNER JOIN 
        chip c ON c."Chip Id" = t."Chip Id"
    WHERE 
        t."Test" = 'otp_load_test'
        AND (c."Lot" = %s OR (c."Lot" IS NULL AND %s IS NULL))
        AND (c."Bin" = %s OR (c."Bin" IS NULL AND %s IS NULL))
        AND (c."Wafer" = %s OR (c."Wafer" IS NULL AND %s IS NULL))
        AND (c."Process Corner" = %s OR (c."Process Corner" IS NULL AND %s IS NULL))
        AND (t."Temp" = %s OR (t."Temp" IS NULL AND %s IS NULL))
        AND (t."Date" = %s OR (t."Date" IS NULL AND %s IS NULL))
        AND (c."Part Number" = %s OR (c."Part Number" IS NULL AND %s IS NULL))
        AND tf2."Test Data" = %s
    """, (lot, lot, bin, bin, wafer, wafer, process_corner, process_corner, temp, temp, date, date, part_num, part_num, file))
    files = cur.fetchall()
    raw_data_files = [file[0] for file in files]

    cur.execute("""
    SELECT 
        tf2."Test Data"
    FROM 
        test_file2 tf2
    INNER JOIN 
        test_file tf ON tf."File Id" = tf2."File Id"
    INNER JOIN 
        test t ON tf."Test Id" = t."Test Id"
    INNER JOIN 
        chip c ON c."Chip Id" = t."Chip Id"
    WHERE 
        t."Test" = 'otp_load_test'
        AND (c."Lot" = %s OR (c."Lot" IS NULL AND %s IS NULL))
        AND (c."Bin" = %s OR (c."Bin" IS NULL AND %s IS NULL))
        AND (c."Wafer" = %s OR (c."Wafer" IS NULL AND %s IS NULL))
        AND (c."Process Corner" = %s OR (c."Process Corner" IS NULL AND %s IS NULL))
        AND (t."Temp" = %s OR (t."Temp" IS NULL AND %s IS NULL))
        AND (t."Date" = %s OR (t."Date" IS NULL AND %s IS NULL))
        AND (c."Part Number" = %s OR (c."Part Number" IS NULL AND %s IS NULL))
        AND tf2."Test Data" = %s
    """, (lot, lot, bin, bin, wafer, wafer, process_corner, process_corner, temp, temp, date, date, part_num, part_num, file))
    files_names = cur.fetchall()
    file_names_data = [name[0] for name in files_names]

    for data_files, file in zip(raw_data_files, file_names_data):
        # Construct a unique file name based on the test_id or other properties
        save_name = f"{file}"  # You can customize the naming pattern here

        with open(f"./parsed_files/{CHIP}/{TEST}/{part}/{part_num}/{temp + "_" + date}/{save_name}.txt", "wb") as save_file:
            # Retrieve bytea data
            cur.execute('SELECT "Test Data" FROM test_file WHERE "File Id" = %s', (data_files,))
            test_data = cur.fetchone()

            if test_data:
                # Convert memoryview to bytes and then decode it
                byte_data = bytes(test_data[0])
                save_file.write(byte_data)  

def run_script(chip, datapath, path_to_part, save, save_path, partNum):
    global CHIP, TEST, PATH_TO_DATA, path, save_name, save_directory, partNumber
    TEST = "otp_load_test"
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

