import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="meas_deep_sleep",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()

def contains_digits(input_string):
    # Use regular expression to check for any digits in the input string
    return bool(re.search(r'\d', input_string))

def main():
    headers = ["Vdd[V]", "Vdd18[V]", "VddIO[V]", "Idd Offset[mA]", "Idd18 Offset[mA]", "IddIO Offset[mA]", "Idd D-Sleep[mA]", "Idd D-Sleep[µA/Mb]", "Idd18 D-Sleep[mA]", "Idd18 D-Sleep[µA/Mb]", "IddIO D-Sleep[mA]", "Lot Bin Wafer", "Process Corner", "Part Number", "Part ID", "Temp", "Date"]
    
    writer = ""

    global CHIP, TEST

    if not os.path.exists("./parsed_data/" + CHIP + "/" + TEST):
        os.mkdir("./parsed_data/" + CHIP + "/" + TEST)

    
    data_path = path
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
        t."Test" = 'meas_deep_sleep'
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
    
    with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
        for file in raw_data_files:
            # print(file)
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
                if "#DD>" in line: 
                    dictionary["Vdd[V]"] = line.split(",")[1]
                    dictionary["Vdd18[V]"] = line.split(",")[2]
                    dictionary["VddIO[V]"] = line.split(",")[3]
                    dictionary["Idd Offset[mA]"] = line.split(",")[4]
                    dictionary["Idd18 Offset[mA]"] = line.split(",")[5]
                    dictionary["IddIO Offset[mA]"] = line.split(",")[6]
                    dictionary["Idd D-Sleep[mA]"] = line.split(",")[7]
                    dictionary["Idd D-Sleep[µA/Mb]"] = f"{float(line.split(",")[7]) / 16 * 1000:.2f}"
                    dictionary["Idd18 D-Sleep[mA]"] = line.split(",")[8]
                    dictionary["Idd18 D-Sleep[µA/Mb]"] = f"{float(line.split(",")[8]) / 16 * 1000:.2f}"
                    dictionary["IddIO D-Sleep[mA]"] = line.split(",")[9].strip()

                    dictionary["Temp"] = temp
                    dictionary["Lot Bin Wafer"] = part
                    dictionary["Process Corner"] = part.split("_")[-1]
                    dictionary["Part Number"] = part_num
                    dictionary["Part ID"] = part.split("_")[-1] + "_" + part + "_" + part_num
                    dictionary["Date"] = date

                    new_data = {}
                    new_data.update(dictionary)
                    data_set.append(new_data)
                    dictionary.clear()

            #writer.writeheader()
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