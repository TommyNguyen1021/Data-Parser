import csv
import sys
import os
import re
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="meas_standby_Keithley",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()

def contains_digits(input_string):
    # Use regular expression to check for any digits in the input string
    return bool(re.search(r'\d', input_string))

def main():
    headers = ["Vdd[V]", "Vdd18[V]", "VddIO[V]", "Vdd Meas[V]", "Vdd18 Meas[V]", "VddIO Meas[V]", "Idd Offset[A]", "Idd18 Offset[A]", "IddIO Offset[A]", "Idd Standby[A]", "Idd Standby[µA/Mb]","Idd18 Standby[A]", "Idd18 Standby[µA/Mb]","IddIO Standby[A]", "IddIO Standby[µA/Mb]", "Lot Bin Wafer", "Process Corner", "Part Number", "Part ID", "Temp", "Date"]
    
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
        t."Test" = 'meas_standby_Keithley'
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
                
            expected_vdd = 0
            expected_vdd18 = 0
            expected_vddio = 0
            meas_vdd_voltage = 0
            meas_vdd18_voltage = 0
            meas_vddio_voltage = 0
            offset_vdd_current = 0
            offset_vdd18_current = 0
            offset_vddio_current = 0
            meas_vdd_current = 0
            meas_vdd18_current = 0
            meas_vddio_current = 0

            voltage_being_checked = ""
            measurement_type = ""



        # print(file)
    
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

                if "#< #Vdd =" in line:
                    expected_vdd = line.split()[-1]
                elif "#< #Vdd18 =" in line:
                    expected_vdd18 = line.split()[-1]
                elif "#< #VddIO =" in line:
                    expected_vddio = line.split()[-1]

                elif "set_keithley" in line:
                    voltage_being_checked = line.split()[-1]
                elif "meas_keithley_voltage" in line:
                    measurement_type = "voltage"
                elif "meas_keithley_current" in line:
                    measurement_type = "current"

                elif "#D> " in line:
                    if "Vdd18" in voltage_being_checked and measurement_type == "voltage":
                        meas_vdd18_voltage = line.split()[-1]
                    elif "Vdd18" in voltage_being_checked and measurement_type == "current":
                        meas_vdd18_current   = line.split()[-1]
                        offset_vdd18_current = line.split()[-2][:-1]
                        #offset_vdd18_current = line.split(",")[-2]
                        #offset_vdd18_current = offset_vdd18_current.split()[-1]
                    elif "VddIO" in voltage_being_checked and measurement_type == "voltage":
                        meas_vddio_voltage = line.split()[-1]
                    elif "VddIO" in voltage_being_checked and measurement_type == "current":
                        meas_vddio_current   = line.split()[-1]
                        offset_vddio_current = line.split()[-2][:-1]
                        #offset_vddio_current = line.split(",")[-2]
                        #offset_vddio_current = offset_vddio_current.split()[-1]

                        dictionary["Vdd[V]"] = expected_vdd
                        dictionary["Vdd18[V]"] = expected_vdd18
                        dictionary["VddIO[V]"] = expected_vddio
                        dictionary["Vdd Meas[V]"] = meas_vdd_voltage
                        dictionary["Vdd18 Meas[V]"] = meas_vdd18_voltage
                        dictionary["VddIO Meas[V]"] = meas_vddio_voltage
                        dictionary["Idd Offset[A]"] = offset_vdd_current
                        dictionary["Idd18 Offset[A]"] = offset_vdd18_current
                        dictionary["IddIO Offset[A]"] = offset_vddio_current
                        dictionary["Idd Standby[A]"] = meas_vdd_current
                        dictionary["Idd Standby[µA/Mb]"] = f"{float(meas_vdd_current) / 16 * 1000000:.2f}"
                        dictionary["Idd18 Standby[A]"] = meas_vdd18_current
                        dictionary["Idd18 Standby[µA/Mb]"] = f"{float(meas_vdd18_current) / 16 * 1000000:.2f}"
                        dictionary["IddIO Standby[A]"] = meas_vddio_current
                        dictionary["IddIO Standby[µA/Mb]"] = f"{float(meas_vddio_current) / 16 * 1000000:.2f}"

                        dictionary["Temp"] = temp
                        dictionary["Lot Bin Wafer"] = part
                        dictionary["Process Corner"] = part.split("_")[-1]
                        dictionary["Part Number"] = part_num
                        dictionary["Part ID"] = part.split("_")[-1] + "_" + part + "_" + part_num
                        dictionary["Date"] = date

                        # This section adds a new line in the csv
                        new_data = {}
                        new_data.update(dictionary)
                        data_set.append(new_data)
                        dictionary.clear()

                    elif "Vdd" in voltage_being_checked and measurement_type == "voltage":
                        meas_vdd_voltage = line.split()[-1]
                    elif "Vdd" in voltage_being_checked and measurement_type == "current":
                        meas_vdd_current   = line.split()[-1]
                        offset_vdd_current = line.split()[-2][:-1]
                        #offset_vdd_current = line.split(",")[-2]
                        #offset_vdd_current = offset_vdd_current.split()[-1]


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