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
    headers = ["Vdd", "Vdd18", "sys_osc_trim", "sys_osc_target_freq[MHz]", "sys_clk_period[ns]", "sys_clk_freq[MHz]", "pre-bck_grd_iddw[mA]", "pre-bck_grd_idd18w[mA]", "Vwl", "Vbl", "write speed[ns]", "write-data", "iddw[mA]", "idd18w[mA]", "Lot Bin Wafer", "Part Number", "Temp", "Date"]
    
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

    raw_data_files = os.listdir(data_path)
    raw_data_files = natsorted(raw_data_files)

    
    with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
        for file in raw_data_files:
            if("meas-BIST-write-current" in file and "dat_0" in file):
                # print(file)
            
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

                        # This section adds a new line in the csv
                        if "#DD>" in line: 
                            dictionary["Vdd"] = line.split(",")[1]
                            dictionary["Vdd18"] = line.split(",")[2]
                            dictionary["sys_osc_trim"] = line.split(",")[3]
                            dictionary["sys_osc_target_freq[MHz]"] = line.split(",")[4]
                            dictionary["sys_clk_period[ns]"] = line.split(",")[5]
                            dictionary["sys_clk_freq[MHz]"] = line.split(",")[6]
                            dictionary["pre-bck_grd_iddw[mA]"] = line.split(",")[7]
                            dictionary["pre-bck_grd_idd18w[mA]"] = line.split(",")[8]
                            dictionary["Vwl"] = line.split(",")[9]
                            dictionary["Vbl"] = line.split(",")[10]
                            dictionary["write speed[ns]"] = line.split(",")[11]
                            dictionary["write-data"] = line.split(",")[12]
                            dictionary["iddw[mA]"] = line.split(",")[13]
                            dictionary["idd18w[mA]"] = line.split(",")[14][:-1]

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
                    txt_file.close()
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



#if os.path.exists("parsed_data/" + save_name):
#        os.remove("parsed_data/" + save_name)
#main()