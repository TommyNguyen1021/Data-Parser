import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="ims",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()

def contains_digits(input_string):
    # Use regular expression to check for any digits in the input string
    return bool(re.search(r'\d', input_string))

def main():
    headers = ["VDD", "VDD18", "vbl", "ims_errors", "read_disturb", "instance", "Lot_Bin_Wafer", "part", "Temp", "Date", "ppm", "Data"]
    
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
        t."Test" = 'ims'
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
    print(len(raw_data_files))

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
        t."Test" = 'ims'
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

    instance_num = []

    for checked_file in file_names_data:
        if("dat" in checked_file):
            instance_num.append(int(str(checked_file).split("_")[-2][1]))


    
    with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
        run_index = 0
        for file in raw_data_files:

        #     with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
            decoded_data = file.tobytes().decode('utf-8')
            writer = csv.DictWriter(save_file, fieldnames=headers, lineterminator = '\n')
            data_set = []
            
            dictionary = {}

            'Reads the lines and appends certain information into a dictionary for storing into the csv'
            for line_read in decoded_data.splitlines():
                
                line = line_read

                if re.search("DEBUG_MSG Received ", line):
                    line = line[47:]


                # This section adds a new line in the csv
                if "#D> " in line: 
                    dictionary["VDD"] = round(float(line.split()[1]), 2)
                    dictionary["VDD18"] = round(float(line.split()[2]), 2)
                    dictionary["vbl"] = line.split()[3]
                    dictionary["ims_errors"] = line.split()[4]
                    dictionary["read_disturb"] = line.split()[5]
                    dictionary["Data"] = line.split()[6]
                    dictionary["instance"] = instance_num[run_index]
                    dictionary["Temp"] = temp
                    dictionary["Lot_Bin_Wafer"] = part
                    dictionary["part"] = part_num
                    dictionary["Date"] = date
                    dictionary["ppm"] = round((int(line.split()[4]) * 1000000)/((2048*16*78) - int(line.split()[5])), 2)
                    
                    new_data = {}
                    new_data.update(dictionary)
                    data_set.append(new_data)
                    dictionary.clear()
            run_index = run_index + 1

            #writer.writeheader()
            for row in data_set:
                writer.writerow(row)
        save_file.close()
    print("Returned true")
    return True



#What Gui calls to run script
def run_script(chip, datapath, path_to_part, save, save_path, partNum):
    global CHIP, TEST, PATH_TO_DATA, path, save_name, save_directory, partNumber
    TEST = "ims"
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