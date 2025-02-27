import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="read_disturb",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()

def contains_digits(input_string):
    # Use regular expression to check for any digits in the input string
    return bool(re.search(r'\d', input_string))

def main():
    headers = ["rd_wr", "period", "osc_set", "count", "div", "period_delta", "cycles", "vgen", "Fail Count", "Instance", "Lot Bin Wafer", "Part Number", "Temp", "Date"]
    
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
        t."Test" = 'read_disturb'
        AND c."Lot" = %s 
        AND c."Bin" = %s
        AND c."Wafer" = %s
        AND c."Process Corner" = %s 
        AND t."Temp" = %s
        AND t."Date" = %s 
        AND c."Part Number" = %s
        AND tf."File Name" Like '%%_0'
    """, (lot, bin, wafer, process_corner, temp, date, part_num))
    files = cur.fetchall()
    raw_data_files = [file[0] for file in files]

    # Gets the file names
    cur.execute("""
    SELECT 
        tf."File Name"
    FROM 
        test_file tf
    INNER JOIN 
        test t ON tf."Test Id" = t."Test Id"
    INNER JOIN 
        chip c ON c."Chip Id" = t."Chip Id"
    WHERE 
        t."Test" = 'read_disturb'
        AND c."Lot" = %s 
        AND c."Bin" = %s
        AND c."Wafer" = %s
        AND c."Process Corner" = %s 
        AND t."Temp" = %s
        AND t."Date" = %s 
        AND c."Part Number" = %s
        AND tf."File Name" Like '%%_0'
    """, (lot, bin, wafer, process_corner, temp, date, part_num))
    files_names = cur.fetchall()
    file_names_data = [name[0] for name in files_names]

    instance_num = []
    cycles = []
    vgen = []

    for checked_file in file_names_data:
        if("read-disturb" in checked_file and "dat_0" in checked_file and "cycles" in checked_file):
            instance_num.append(int(str(checked_file).split("_")[-2][1]))
            cycles.append(checked_file.split("_")[1].split("-")[1])
            vgen.append(int(checked_file.split("_")[2].split("-")[1], 16))

    
    with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
        run_index = 0
        for file in raw_data_files:
            read_speeds_checked = False
            fail_count = 0

        #     with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
            decoded_data = file.tobytes().decode('utf-8')
            writer = csv.DictWriter(save_file, fieldnames=headers, lineterminator = '\n')
            data_set = []

            rd_wr = 0
            period = 0
            osc_set = 0
            count = 0
            div = 0
            period_delta = 0
            
            dictionary = {}

            'Reads the lines and appends certain information into a dictionary for storing into the csv'
            for line_read in decoded_data.splitlines():
                
                line = line_read

                if re.search("DEBUG_MSG Received ", line):
                    line = line[47:]

                if "#>> #D> rd_wr" in line and read_speeds_checked == False:
                    read_speeds_checked = True
                    rd_wr = line.split()[4][:-1]
                    period = line.split()[7]
                    osc_set = int(line.split()[11], 16)
                    count = int(line.split()[14], 16)
                    div = int(line.split()[17], 16)
                    period_delta = line.split()[20]


                # This section adds a new line in the csv
                if "#>> Fail Count:" in line: 
                    fail_count = int(line.split()[3], 16)
                    
            dictionary["cycles"] = cycles[run_index]
            dictionary["vgen"] = vgen[run_index]
            dictionary["rd_wr"] = rd_wr
            dictionary["period"] = period
            dictionary["osc_set"] = osc_set
            dictionary["count"] = count
            dictionary["div"] = div
            dictionary["period_delta"] = period_delta
            dictionary["Fail Count"] = fail_count
            dictionary["Instance"] = instance_num[run_index]
            dictionary["Temp"] = temp
            dictionary["Lot Bin Wafer"] = part
            dictionary["Part Number"] = part_num
            dictionary["Date"] = date
            dictionary["Fail Count"] = fail_count
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
    TEST = path_to_part.split("/")[6]
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