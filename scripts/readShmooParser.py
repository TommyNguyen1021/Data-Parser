import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
from numpy import double
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="read_shmoo_pat",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()  

def contains_digits(input_string):
    # Use regular expression to check for any digits in the input string
    return bool(re.search(r'\d', input_string))

def main():
    headers = ["Lot_Bin_Wafer", "part", "instance", "temp", "date", "block", "lfo_ovr", "Vdd", "rd_vbl", 
               "pattern", "idd/bit", "idd18/bit", "safv", "rd_count", "osc_setting", "osc_delta", "rd_delay", "err_cnt", "ppm", "ecc_err_cnt", "ppm(ecc)"]
    
    writer = ""

    global CHIP, TEST

    if not os.path.exists("./parsed_data/" + CHIP + "/" + TEST):
        os.mkdir("./parsed_data/" + CHIP + "/" + TEST)

    
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
        t."Test" = 'read_shmoo_pat'
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
        t."Test" = 'read_shmoo_pat'
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
                    dictionary["block"] = line.split()[1]
                    dictionary["lfo_ovr"] = line.split()[2]
                    dictionary["Vdd"] = line.split()[3]
                    dictionary["rd_vbl"] = line.split()[4]
                    dictionary["pattern"] = line.split()[5]
                    dictionary["idd/bit"] = line.split()[6]
                    dictionary["idd18/bit"] = line.split()[7]
                    dictionary["safv"] = line.split()[8]
                    dictionary["rd_count"] = line.split()[9]
                    dictionary["osc_setting"] = line.split()[10]
                    dictionary["osc_delta"] = line.split()[11]
                    dictionary["rd_delay"] = line.split()[12]
                    dictionary["err_cnt"] = line.split()[13]
                    dictionary["ppm"] = double(line.split()[13])*(1000000/(78*2048*16))

                    try:
                        dictionary["ecc_err_cnt"] = line.split()[14]
                        dictionary["ppm(ecc)"] = double(line.split()[14])*(1000000/(64*2048*16))
                    except:
                        dictionary["ecc_err_cnt"] = ""
                        dictionary["ppm(ecc)"] = ""

                    dictionary["instance"] = instance_num[run_index]
                    dictionary["temp"] = temp
                    dictionary["Lot_Bin_Wafer"] = part
                    dictionary["part"] = part_num
                    dictionary["date"] = date

                    new_data = {}
                    new_data.update(dictionary)
                    data_set.append(new_data)
                    dictionary.clear()
            run_index = run_index + 1
            for row in data_set:
                writer.writerow(row)
        save_file.close()
    print("Returned true")
    return True



#What Gui calls to run script
def run_script(chip, datapath, path_to_part, save, save_path, partNum):
    global CHIP, TEST, PATH_TO_DATA, path, save_name, save_directory, partNumber
    TEST = "read_shmoo_pat"
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