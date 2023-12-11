import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted

def contains_digits(input_string):
    # Use regular expression to check for any digits in the input string
    return bool(re.search(r'\d', input_string))

def main():
    headers = ["Vdd", "Data", "rd_cnt", "prg_vbl", "cycles", "err_cnt", "ppb", "Fail Count", "Instance", "Lot Bin Wafer", "Part Number", "Temp", "Date"]
    
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

    raw_data_files = os.listdir(data_path)
    raw_data_files = natsorted(raw_data_files)

    
    with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
        for file in raw_data_files:

            if("ser" in file and "dat_0" in file):
                fail_count = 0
                # print(file)
                instance = file.split("_")[-2][1]
                print("Instance: " + instance)
            
                with open(data_path + "/" + file , "r") as txt_file:
                #     with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
                    writer = csv.DictWriter(save_file, fieldnames=headers, lineterminator = '\n')
                    data_set = []
                    
                    dictionary = {}

                    'Reads the lines and appends certain information into a dictionary for storing into the csv'
                    for line_read in txt_file.readlines():
                        
                        line = line_read

                        if re.search("DEBUG_MSG Received ", line):
                            line = line[47:]

                        if "#>> Fail Count" in line:
                            fail_count = int(line.split()[3], 16)
                            print(fail_count)

                        # This section adds a new line in the csv
                        if "#D> " in line: 
                            dictionary["Vdd"] = line.split()[1]
                            dictionary["Data"] = line.split()[2]
                            dictionary["rd_cnt"] = line.split()[3]
                            dictionary["cycles"] = line.split()[4]
                            dictionary["err_cnt"] = int(line.split()[5], 16)
                            dictionary["ppb"] = line.split()[6]
                            dictionary["Instance"] = instance
                            dictionary["Temp"] = temp
                            dictionary["Lot Bin Wafer"] = part
                            dictionary["Part Number"] = part_num
                            dictionary["Date"] = date
                            dictionary["Fail Count"] = fail_count

                            new_data = {}
                            new_data.update(dictionary)
                            data_set.append(new_data)
                            dictionary.clear()

                    #writer.writeheader()
                    for row in data_set:
                        writer.writerow(row)
                    txt_file.close()
        save_file.close()
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



#if os.path.exists("parsed_data/" + save_name):
#        os.remove("parsed_data/" + save_name)
#main()