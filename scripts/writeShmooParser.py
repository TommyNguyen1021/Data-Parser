import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
from numpy import double

def contains_digits(input_string):
    # Use regular expression to check for any digits in the input string
    return bool(re.search(r'\d', input_string))

def main():
    headers = ["Lot_Bin_Wafer", "part", "instance", "temp", "date", "Data", "ivdd18/bit", "ivdd/bit", "VWL", "Vwl(meas)", "VBL", "Vbl(meas)", "PRG_CNT", "PRG_Time", 
               "Pulse1", "Pulse1(ECC)", "Pulse2", "Pulse2(ECC)", "Pulse3", "Pulse3(ECC)", "Pulse4", "Pulse4(ECC)", 
               "Pulse5", "Pulse5(ECC)", "Pulse6", "Pulse6(ECC)", "vdd", "vdd18"]
    
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

    raw_data_files = os.listdir(data_path)
    raw_data_files = natsorted(raw_data_files)

    
    with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
        
        for file in raw_data_files:

            if("prog_shmoo" in file and "dat_0" in file):
                print(file)
                instance = file.split("_")[-2][1]

                with open(data_path + "/" + file , "r") as txt_file:
                #     with open("./parsed_data/" + CHIP + "/" + TEST + "/" + save_name + ".csv", "a") as save_file:
                    writer = csv.DictWriter(save_file, fieldnames=headers, lineterminator = '\n')
                    data_set = []                    
                    dictionary = {}
                    vdd = 0
                    vdd18 = 0

                    'Reads the lines and appends certain information into a dictionary for storing into the csv'
                    for line_read in txt_file.readlines():
                        
                        line = line_read
                        

                        if re.search("DEBUG_MSG Received ", line):
                            line = line[47:]

                        if "#< set_vdd " in line:
                            vdd = line.split()[-1]
                            

                        if "#< set_vddbl " in line:
                            vdd18 = line.split()[-1]

                        # This section adds a new line in the csv
                        if line[0:5] == "0x00:" or line[0:5] == "0xff:":
                            dictionary["Data"] = line.split()[0][:-1]
                            dictionary["ivdd18/bit"] = line.split()[1]
                            dictionary["ivdd/bit"] = line.split()[2]
                            dictionary["VWL"] = line.split()[3]
                            dictionary["Vwl(meas)"] = line.split()[4]
                            dictionary["VBL"] = line.split()[5]
                            dictionary["Vbl(meas)"] = line.split()[6]
                            dictionary["PRG_CNT"] = line.split()[7]
                            dictionary["PRG_Time"] = line.split()[8]
                            
                            try:
                                dictionary["Pulse1"] = line.split()[9]
                                dictionary["Pulse1(ECC)"] = line.split()[10]
                                dictionary["Pulse2"] = line.split()[11]
                                dictionary["Pulse2(ECC)"] = line.split()[12]
                                dictionary["Pulse3"] = line.split()[13]
                                dictionary["Pulse3(ECC)"] = line.split()[14]
                                dictionary["Pulse4"] = line.split()[15]
                                dictionary["Pulse4(ECC)"] = line.split()[16]
                                dictionary["Pulse5"] = line.split()[17]
                                dictionary["Pulse5(ECC)"] = line.split()[18]
                                dictionary["Pulse6"] = line.split()[19]
                                dictionary["Pulse6(ECC)"] = line.split()[20]
                            except: 
                                dictionary["Pulse1"] = line.split()[9]
                                dictionary["Pulse2"] = line.split()[10]
                                dictionary["Pulse3"] = line.split()[11]
                                dictionary["Pulse4"] = line.split()[12]
                                dictionary["Pulse5"] = line.split()[13]
                                dictionary["Pulse6"] = line.split()[14]
                                dictionary["Pulse1(ECC)"] = ""
                                dictionary["Pulse2(ECC)"] = ""
                                dictionary["Pulse3(ECC)"] = ""
                                dictionary["Pulse4(ECC)"] = ""
                                dictionary["Pulse5(ECC)"] = ""
                                dictionary["Pulse6(ECC)"] = ""

                            dictionary["instance"] = instance
                            dictionary["temp"] = temp
                            dictionary["Lot_Bin_Wafer"] = part
                            dictionary["part"] = part_num
                            dictionary["date"] = date
                            dictionary["vdd"] = vdd
                            dictionary["vdd18"] = vdd18

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
    TEST = "write_shmoo"
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