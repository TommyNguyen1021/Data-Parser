import string
import sys
import os
import re
from numpy import double, empty

from pyparsing import col

arg_length = len(sys.argv)

#Line starters
HEADER_INPUT = "#<"
OUTPUT = '#>>'
DATA_OUTPUT = "#D>"

#input information
NUMBER_OF_INSTANCES = 8
CHIP = "vili"
TEST = "read_shmoo"
PATH_TO_DATA = "si_data/"
path  = "si_data/" + CHIP + '/' + TEST +  "/P9HK27_0j_07/P0021/085C_210908/" + TEST + '_i'
save_name = "parsed_data.csv"
save_directory = "parsed_data/CHIP/TEST/LBW/PART_NUM/TEMP_DATE"

#An array of lines that will be saved
data_list = []
first = True

#extracts the temperature and date from the file path
def get_temp_date():
    temp_date = [path.split("/")[9].split("_")[0], path.split("/")[9].split("_")[1]]
    data_list[0] += "temp" + ',' + "date" + ','
    return temp_date

#extracts the Lot_Bin_Wafer from the file path
def get_lbw():
    data_list.append("Lot_Bin_Wafer,")
    return path.split("/")[7]

#extracts the part number from the file path
def get_part():
    data_list[0]+=("part,")
    return path.split("/")[8]


#the Data column is normally written as 0x00 or 0xff
#this function converts it so that it is saved as 0 or 1 instead
def convert_data(list, col_list):
    #This contains instance, Temp, and Date currently, so the line and column list are misaligned
    # EX:
    # 0: #D>        1: block   2: lfo_ovr    3: vdd     4: rd_vbl    5: Data
    # 0: LBW        2:Part     2:instance    3: temp    4: date       5: block   6: lfo_ovr   7: vdd     8: rd_vbl  9:  Data

    for i in range(len(col_list)):
        if (re.search('Data', col_list[i])):
            
            #i-4 realigns the 2 lists

            #Replace 0x00 with 0
            if re.search('0x00', list[i-4]):
                list[i-4] = "0"
            #replace with 1
            else:
                list[i-4] = "1"

#calculate the ppm using error count
#currently only calculates the ppm of the specific instance
def calculate_ppm(list, col_list):
    global first, path
    for i in range(len(col_list)):
        if (re.search('err_cnt', col_list[i])):
            #error count multiplied by
            if '\n' in list[i-4]:
                list[i-4] = list[i-4].rstrip('\n')
            ppm = double(list[i-4])*(1000000/(78*2048*16))
            
            if "_pat_" in path:
                list.insert(i-3, str(ppm)+"\n")
                if(first):
                    if '\n' in col_list[i]:
                        #remove \n
                        col_list[i] = "err_cnt"    
                    col_list.insert(i+1, "ppm\n")
            else:
                list.insert(i-3, str(ppm))
                if(first):
                    if '\n' in col_list[i]:
                        #remove \n
                        col_list[i] = "err_cnt"    
                    col_list.insert(i+1, "ppm")

#this function breaks apart a line and edits each line to make sure it has the proper values
def line_breaker(line:string):
    global first
    #separate each value in the line. This line still contains the Line Starter
    list = line.split(' ')

    #separate the column names.
    #This contains instance, Temp, and Date currently, so the line and column list
    #are misaligned
    # #D>        block   lfo_ovr    vdd     rd_vbl  Data
    # instance   temp    date       block   lfo_ovr vdd     rd_vbl   Data
    col_list = data_list[0].split(',')

    convert_data(list, col_list)
    calculate_ppm(list,col_list)
    #merge list into a new string
    new_line = ""
    for i in range(len(list)):
        new_line += list[i]
        if (i < len(list)-1):
            new_line += ' '

    #merge list into a new string
    if (first):
        new_col = ""
        for i in range(len(col_list)):
            new_col += col_list[i]
            if (i < len(col_list)-1):
                new_col += ','
            elif '\n' not in new_col:
                new_col += "\n"
        data_list[0] = new_col
        first = False
    return new_line


            
#adds instance and temp/date to each line, then converts line to replace spaces with commas
def check_data_output(line:string, instance:int, temp_date:list, lbw:string, part:string):
    if line[0:len(DATA_OUTPUT)] == DATA_OUTPUT:
        line = line_breaker(line)

        #remove header
        data = line[len(DATA_OUTPUT) + 1: len(line)]

        #add lot_bin_wafer
        data_list.append(lbw + ',')
        #add part number
        data_list.append(part + ',')
        #add instance
        data_list.append(str(instance) + ',')
        #add temp/dates
        data_list[len(data_list)-1] += temp_date[0] + ',' + temp_date[1] + ','
        #convert from space separated values to comma separated values
        data_list[len(data_list)-1] += (data.replace(" ", ","))

#save to an output
def write_output():
    #file = open("parsed_data/" + save_name, "a")
    if partNumber == 0:
        file = open(save_directory + save_name, "w")
    else:
        file = open(save_directory + save_name, "a")
    for i in range(len(data_list)):
        if (i == 0 and os.stat(save_directory + save_name).st_size == 0) or i > 0:
            file.write(data_list[i])
    file.close()

#TODO: implement check to see if the instance file actually exists
def main():
    global first, data_list
    first = True
    data_list=[]
    lbw = get_lbw()
    part = get_part()
    data_list[0] += "instance,"
    temp_date = get_temp_date()
    #loop for each instance
    for inst in range(NUMBER_OF_INSTANCES):
        #if the instance file actually exists
        if os.path.exists(path + str(inst) + '.dat_0'):
            #get data from file
            current_dat = str(inst) + '.dat_0'
            file = open(path +current_dat)
            #for each line
            for line in file:
                #check header
                if (line[0:3] == OUTPUT) and (re.search("^#>> block ", line)) and first:
                    categories = line[(len(DATA_OUTPUT) + 1):len(line)]
                    data_list[0] += (categories.replace(" ",","))
                check_data_output(line, inst, temp_date, lbw, part)
            file.close()
        else:
            print("There are missing files")
            break
    write_output()
    return True


#What Gui calls to run script
def run_script(chip, datapath, path_to_part, save, save_path, partNum):
    print("running...")
    global CHIP, TEST, PATH_TO_DATA, path, save_name, save_directory, partNumber
    TEST = "read_shmoo_i"
    PATH_TO_DATA = datapath

    partNumber = partNum

    CHIP = chip
    path  = path_to_part + TEST
    if not os.path.exists(path + str(0) + ".dat_0"):
        path = path_to_part + "read_shmoo_pat_i"
    save_name = save
    save_directory = save_path
    main()
    return 



#if os.path.exists("parsed_data/" + save_name):
#        os.remove("parsed_data/" + save_name)
#main()