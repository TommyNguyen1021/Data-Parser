import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
import tempfile
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="ser",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()        

def contains_digits(input_string):
    # Use regular expression to check for any digits in the input string
    return bool(re.search(r'\d', input_string))

def main():
    headers = ["Vdd", "Vdd18", "Data", "rd_cnt", "prg_vbl", "cycles", "err_cnt", "ppb", "Fail Count", "Instance", "Lot Bin Wafer", "Part Number", "Temp", "Date", "Run #", "Sporatic Errors", "Sporatic ppb", "Hard Errors", "Hard ppb"]
    
    writer = ""

    global CHIP, TEST

    if not os.path.exists("./parsed_data/" + CHIP + "/" + TEST):
        os.mkdir("./parsed_data/" + CHIP + "/" + TEST)

    first_file = 1
    first_iter = 0
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

    if(partNumber == 0):
        if not os.path.exists("./parsed_data/" + CHIP + "/" + TEST):
            os.mkdir("./parsed_data/" + CHIP + "/" + TEST)
        with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "w") as new_file:
            writer = csv.DictWriter(new_file, fieldnames=headers, lineterminator = '\n')
            writer.writeheader()
            new_file.close()

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

    # Gets the file data
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
        t."Test" = 'ser'
        AND (c."Lot" = %s OR (c."Lot" IS NULL AND %s IS NULL))
        AND (c."Bin" = %s OR (c."Bin" IS NULL AND %s IS NULL))
        AND (c."Wafer" = %s OR (c."Wafer" IS NULL AND %s IS NULL))
        AND (c."Process Corner" = %s OR (c."Process Corner" IS NULL AND %s IS NULL))
        AND (t."Temp" = %s OR (t."Temp" IS NULL AND %s IS NULL))
        AND (t."Date" = %s OR (t."Date" IS NULL AND %s IS NULL))
        AND (c."Part Number" = %s OR (c."Part Number" IS NULL AND %s IS NULL))
    """, (lot, lot, bin, bin, wafer, wafer, process_corner, process_corner, temp, temp, date, date, part_num, part_num))
    files = cur.fetchall()
    raw_data_files = [file[0] for file in files]

    # Gets the file names
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
        t."Test" = 'ser'
        AND (c."Lot" = %s OR (c."Lot" IS NULL AND %s IS NULL))
        AND (c."Bin" = %s OR (c."Bin" IS NULL AND %s IS NULL))
        AND (c."Wafer" = %s OR (c."Wafer" IS NULL AND %s IS NULL))
        AND (c."Process Corner" = %s OR (c."Process Corner" IS NULL AND %s IS NULL))
        AND (t."Temp" = %s OR (t."Temp" IS NULL AND %s IS NULL))
        AND (t."Date" = %s OR (t."Date" IS NULL AND %s IS NULL))
        AND (c."Part Number" = %s OR (c."Part Number" IS NULL AND %s IS NULL))
    """, (lot, lot, bin, bin, wafer, wafer, process_corner, process_corner, temp, temp, date, date, part_num, part_num))
    files_names = cur.fetchall()
    file_names_data = [name[0] for name in files_names]

    max_number_runs = 0
    run_num =[]
    run_index = 0
    instance_num = []


    for checked_file in file_names_data:
        fail_count = 0
        if("ser_i" in checked_file and "dat" in checked_file):
            print(checked_file)
            run_num.append(int(str(checked_file).split("_")[-1]))
            instance_num.append(int(str(checked_file).split("_")[-2][1]))
            run_index = run_index + 1
            if (int(str(checked_file).split("_")[-1]) + 1) >  max_number_runs:
                max_number_runs  = int(str(checked_file).split("_")[-1]) + 1
    for i in range(len(run_num)):
        if run_num[i] == 0:
            run_num[i] = max_number_runs

    with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
        run_index = 0
        for file in raw_data_files:
            decoded_data = file.tobytes().decode('utf-8')
            writer = csv.DictWriter(save_file, fieldnames=headers, lineterminator='\n')
            data_set = []
            vdd18 = 1.8
            dictionary = {}

            # Split the decoded data into lines
            for line_read in decoded_data.splitlines():
                line = line_read

                if re.search("DEBUG_MSG Received ", line):
                    line = line[47:]

                if "#>> Fail Count" in line:
                    fail_count = int(line.split()[3], 16)

                if "#< set_vddbl " in line:
                    vdd18 = line.split()[-1]

                if "#D> " in line:
                    dictionary["Vdd"] = line.split()[1]
                    dictionary["Vdd18"] = vdd18
                    dictionary["Data"] = line.split()[2]
                    dictionary["rd_cnt"] = line.split()[3]
                    dictionary["cycles"] = line.split()[4]
                    dictionary["err_cnt"] = int(line.split()[5], 16)
                    dictionary["ppb"] = line.split()[6]
                    dictionary["Sporatic Errors"] = int(line.split()[7], 16)
                    dictionary["Sporatic ppb"] = line.split()[8]
                    dictionary["Hard Errors"] = int(line.split()[9], 16)
                    dictionary["Hard ppb"] = line.split()[10]
                    dictionary["Instance"] = instance_num[run_index]
                    dictionary["Temp"] = temp
                    dictionary["Lot Bin Wafer"] = part
                    dictionary["Part Number"] = part_num
                    dictionary["Date"] = date
                    dictionary["Fail Count"] = fail_count
                    dictionary["Run #"] = run_num[run_index]
                    new_data = {}
                    new_data.update(dictionary)
                    data_set.append(new_data)
                    dictionary.clear()
            run_index = run_index + 1
            for row in data_set:
                writer.writerow(row)
    print("Returned true")
    return True

#What Gui calls to run script
def run_script(chip, datapath, path_to_part, save, save_path, partNum):
    global CHIP, TEST, PATH_TO_DATA, path, save_name, save_directory, partNumber
    TEST = "ser"
    PATH_TO_DATA = datapath

    partNumber = partNum

    CHIP = chip
    path  = path_to_part

    save_name = save
    if(".csv" in save_name):
        save_name = save_name[:-4]
    save_directory = save_path
    main()
    return 

conn.commit()

#if os.path.exists("parsed_data/" + save_name):
#        os.remove("parsed_data/" + save_name)
#main()