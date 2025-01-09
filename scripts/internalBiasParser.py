import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
import psycopg2
from decimal import Decimal
conn = psycopg2.connect(host="localhost", dbname="internal_biases",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()

def contains_digits(input_string):
    # Use regular expression to check for any digits in the input string
    return bool(re.search(r'\d', input_string))

def main():
    headers_bitline = ["vdd", "vdd18", "vwl", "vgen", "bitline_leakage(uA)", "Vss(V)", "Vrbl(V)", "Instance", "Lot Bin Wafer", "Part Number", "Temp", "Date"]
    headers_vbl = ["vdd", "vdd18", "Instance", "vbl", "tc_0", "tc_1", "tc_2", "tc_3", "tc_4", "tc_5", "tc_6", "tc_7", "tc_8", "tc_9", "Lot Bin Wafer", "Part Number", "Temp", "Date"]
    headers_vwl = ["vdd", "vdd18", "Instance", "vwl", "tc_0", "tc_1", "tc_2", "tc_3", "tc_4", "tc_5", "tc_6", "tc_7", "tc_8", "tc_9", "Lot Bin Wafer", "Part Number", "Temp", "Date"]


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
        if not os.path.exists("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name):
            os.mkdir("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name)
        with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + "/" + save_name + "_Data" + ".csv", "w") as new_file:
            writer = csv.DictWriter(new_file, fieldnames=headers_bitline, lineterminator = '\n')
            writer.writeheader()
        with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + "/" + save_name + "_VBL" + ".csv", "w") as new_file:
            writer = csv.DictWriter(new_file, fieldnames=headers_vbl, lineterminator = '\n')
            writer.writeheader()
        with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + "/" + save_name + "_VWL" + ".csv", "w") as new_file:
            writer = csv.DictWriter(new_file, fieldnames=headers_vwl, lineterminator = '\n')
            writer.writeheader()

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
        test_file2 tf2 ON tf."File Id" = tf2."File Id"
    INNER JOIN 
        test t ON tf."Test Id" = t."Test Id"
    INNER JOIN 
        chip c ON c."Chip Id" = t."Chip Id"
    WHERE 
        t."Test" = 'internal_biases'
        AND (c."Lot" = %s OR (c."Lot" IS NULL AND %s IS NULL))
        AND (c."Bin" = %s OR (c."Bin" IS NULL AND %s IS NULL))
        AND (c."Wafer" = %s OR (c."Wafer" IS NULL AND %s IS NULL))
        AND (c."Process Corner" = %s OR (c."Process Corner" IS NULL AND %s IS NULL))
        AND (t."Temp" = %s OR (t."Temp" IS NULL AND %s IS NULL))
        AND (t."Date" = %s OR (t."Date" IS NULL AND %s IS NULL))
        AND (c."Part Number" = %s OR (c."Part Number" IS NULL AND %s IS NULL))
        AND (
            tf2."Test Data" LIKE '%%vbl_meas%%' 
            OR tf2."Test Data" LIKE '%%vwl_meas%%'
            OR tf2."Test Data" LIKE '%%internal-biases%%'
        )
        AND tf2."Test Data" LIKE '%%dat_0%%'
    """, (lot, lot, bin, bin, wafer, wafer, process_corner, process_corner, temp, temp, date, date, part_num, part_num))
    files = cur.fetchall()
    raw_data_files = [file[0] for file in files]
    print(process_corner)

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
        t."Test" = 'internal_biases'
        AND (c."Lot" = %s OR (c."Lot" IS NULL AND %s IS NULL))
        AND (c."Bin" = %s OR (c."Bin" IS NULL AND %s IS NULL))
        AND (c."Wafer" = %s OR (c."Wafer" IS NULL AND %s IS NULL))
        AND (c."Process Corner" = %s OR (c."Process Corner" IS NULL AND %s IS NULL))
        AND (t."Temp" = %s OR (t."Temp" IS NULL AND %s IS NULL))
        AND (t."Date" = %s OR (t."Date" IS NULL AND %s IS NULL))
        AND (c."Part Number" = %s OR (c."Part Number" IS NULL AND %s IS NULL))
        AND (
            tf2."Test Data" LIKE '%%vbl_meas%%' 
            OR tf2."Test Data" LIKE '%%vwl_meas%%'
            OR tf2."Test Data" LIKE '%%internal-biases%%'
        )
        AND tf2."Test Data" LIKE '%%dat_0%%'
    """, (lot, lot, bin, bin, wafer, wafer, process_corner, process_corner, temp, temp, date, date, part_num, part_num))
    files_names = cur.fetchall()
    file_names_data = [name[0] for name in files_names]



    for data_files, file in zip(raw_data_files, file_names_data):

        if("vbl_meas" in file and "dat_0" in file):
            print(file)
            instance = file.split("_")[-6][1]
            # print("Instance: " + instance)
            vdd = file.split("_")[5]
            vdd18 = file.split("_")[7][:-4]
        # try:
            # with open("test.txt" , "r") as txt_file:
            with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + "/" + save_name + "_VBL" + ".csv", "a") as new_file:
                decoded_data = data_files.tobytes().decode('utf-8')
                writer = csv.DictWriter(new_file, fieldnames=headers_vbl, lineterminator = '\n')
                data_set = []
                
                dictionary = {}
                current_data = ""
                first_iter = 0

                'Reads the lines and appends certain information into a dictionary for storing into the csv'
                for line_read in decoded_data.splitlines():
                    
                    line = line_read

                    if re.search("DEBUG_MSG Received ", line):
                        line = line[47:]

                    # This section adds a new line in the csv
                    if "#D> " in line: 
                        dictionary["Instance"] = instance
                        dictionary["vdd"] = vdd
                        dictionary["vdd18"] = vdd18
                        dictionary["vbl"] = line.split()[1]
                        dictionary["tc_0"] = line.split()[2]
                        dictionary["tc_1"] = line.split()[3]
                        dictionary["tc_2"] = line.split()[4]
                        dictionary["tc_3"] = line.split()[5]
                        dictionary["tc_4"] = line.split()[6]
                        dictionary["tc_5"] = line.split()[7]
                        dictionary["tc_6"] = line.split()[8]
                        dictionary["tc_7"] = line.split()[9]
                        dictionary["tc_8"] = line.split()[10]
                        dictionary["tc_9"] = line.split()[11]
                        dictionary["Temp"] = temp
                        dictionary["Lot Bin Wafer"] = part
                        dictionary["Part Number"] = part_num
                        dictionary["Date"] = date

                        new_data = {}
                        new_data.update(dictionary)
                        data_set.append(new_data)
                        dictionary.clear()

                #writer.writeheader()
                for row in data_set:
                    writer.writerow(row)
                    

        elif("vwl_meas" in file and "dat_0" in file):
            print(file)
            instance = file.split("_")[-6][1]
            print("Instance: " + instance)
            vdd = file.split("_")[5]
            vdd18 = file.split("_")[7][:-4]
        
            with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + "/" + save_name + "_VWL" + ".csv", "a") as new_file:
                decoded_data = data_files.tobytes().decode('utf-8')
                writer = csv.DictWriter(new_file, fieldnames=headers_vwl, lineterminator = '\n')
                data_set = []
                
                dictionary = {}
                current_data = ""
                first_iter = 0

                'Reads the lines and appends certain information into a dictionary for storing into the csv'
                for line_read in decoded_data.splitlines():
                    
                    line = line_read

                    if re.search("DEBUG_MSG Received ", line):
                        line = line[47:]

                    # This section adds a new line in the csv
                    if "#D> " in line: 
                        dictionary["Instance"] = instance
                        dictionary["vdd"] = vdd
                        dictionary["vdd18"] = vdd18
                        dictionary["vwl"] = line.split()[1]
                        dictionary["tc_0"] = line.split()[2]
                        dictionary["tc_1"] = line.split()[3]
                        dictionary["tc_2"] = line.split()[4]
                        dictionary["tc_3"] = line.split()[5]
                        dictionary["tc_4"] = line.split()[6]
                        dictionary["tc_5"] = line.split()[7]
                        dictionary["tc_6"] = line.split()[8]
                        dictionary["tc_7"] = line.split()[9]
                        dictionary["tc_8"] = line.split()[10]
                        dictionary["tc_9"] = line.split()[11]
                        dictionary["Temp"] = temp
                        dictionary["Lot Bin Wafer"] = part
                        dictionary["Part Number"] = part_num
                        dictionary["Date"] = date

                        new_data = {}
                        new_data.update(dictionary)
                        data_set.append(new_data)
                        dictionary.clear()

                #writer.writeheader()
                for row in data_set:
                    writer.writerow(row)
                

        #----------------------------------------------------------------------------
        elif("internal-biases" in file and "dat_0" in file):
            print(file)
            instance = file.split("_")[-2][1]
            print("Instance: " + instance)
        # try:
            # with open("test.txt" , "r") as txt_file:
            with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + "/" + save_name + "_Data" + ".csv", "a") as new_file:
                decoded_data = data_files.tobytes().decode('utf-8')
                writer = csv.DictWriter(new_file, fieldnames=headers_bitline, lineterminator = '\n')
                data_set = []
                
                dictionary = {}
                current_data = ""
                first_iter = 0

                'Reads the lines and appends certain information into a dictionary for storing into the csv'
                for line_read in decoded_data.splitlines():
                    
                    line = line_read

                    if re.search("DEBUG_MSG Received ", line):
                        line = line[47:]

                    # This section adds a new line in the csv
                    if "#< # vdd vdd18 vwl loaded" in line and first_iter == 1: 
                        new_data = {}
                        new_data.update(dictionary)
                        data_set.append(new_data)
                        dictionary.clear()

                    # Checks for voltage values
                    elif "#< #" in line and contains_digits(line):
                        vdd = line.split()[2]
                        vdd18 = line.split()[3]
                        vwl = line.split()[4]
                        dictionary["vdd"] = vdd
                        dictionary["vdd18"] = vdd18
                        dictionary["vwl"] = vwl
                        # print(instance)
                    
                    # Checks for io number
                    elif "#D2>" in line:
                        first_iter = 1
                        vgen = line.split()[1]
                        bitline_leakage = line.split()[2]
                        vss = line.split()[3]
                        vrbl = line.split()[4]
                        dictionary["vgen"] = vgen
                        dictionary["bitline_leakage(uA)"] = bitline_leakage
                        dictionary["Vss(V)"] = vss
                        dictionary["Vrbl(V)"] = vrbl
                        dictionary["Instance"] = instance
                        dictionary["Temp"] = temp
                        dictionary["Lot Bin Wafer"] = part
                        dictionary["Part Number"] = part_num
                        dictionary["Date"] = date

                #writer.writeheader()
                for row in data_set:
                    writer.writerow(row)
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