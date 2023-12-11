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

#input information
NUMBER_OF_INSTANCES = 8
CHIP = "vili"
TEST = "htol"
PATH_TO_DATA = "si_data/"
path  = "si_data/" + CHIP + '/' + TEST +  "/P9HT98_0p_1/P0003/125C_220630/"
save_name = "parsed_data.csv"
current_wordline = 0

#An array of lines that will be saved
data_list = []
first = True

#extracts the temperature and date from the file path
def get_temp_date():
    #separate each directory in the path
    path_list = path.split("/")
    for p in path_list:
        #if the directory contains the temp and date
        if re.search("\d\dC_\d\d\d\d\d\d",p):
            temp_date = p.split("_")
            data_list[0] += 'temp' + ',' + 'date' + ','
            return temp_date

#extracts the Lot_Bin_Wafer from the file path
def get_lbw():
    #separate each directory in the path
    path_list = path.split("/")
    for lbw in path_list:
        #if the directory contains the temp and date
        if re.search("\w\d\w\w\d\d_\d\w_\d",lbw):
            data_list.append("Lot_Bin_Wafer,")
            return lbw

#extracts the part number from the file path
def get_part():
    #separate each directory in the path
    path_list = path.split("/")
    for part in path_list:
        #if the directory contains the temp and date
        if re.search("P\d\d\d\d",part):
            data_list[0]+=("part,")
            return part



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

    #merge list into a new string
    new_line = list[(len(list)-1)].rstrip('\n')


    #merge list into a new string
    if first:
        new_col = ""
        for i in range(len(col_list)):
            new_col += col_list[i].rstrip('\n')
            if (i < len(col_list)-1):
                new_col += ','
            #elif '\n' not in new_col:
                #new_col += "\n"
        data_list[0] = new_col
    return new_line


def line_starter(temp_date:list, lbw:string, part:string, dma_type:string):
    #Add Test name
    data_list.append(TEST + '')
    #add lot_bin_wafer
    data_list[len(data_list)-1] += (lbw + ',')
    #add part number
    data_list[len(data_list)-1] += (part + ',')

        
    #add temp/dates
    data_list[len(data_list)-1] += temp_date[0] + ',' + temp_date[1] + ','

    #add DMA_TYPE number
    data_list[len(data_list)-1] += (dma_type + ',')

    #add_wordline
    data_list[len(data_list)-1] += (str(current_wordline) + ',')


#adds instance and temp/date to each line, then converts line to replace spaces with commas
bitline_iterator = 0
def check_data_output(line:string):
    global bitline_iterator
    if re.search("word\[\d",line):
        
        bits = bin(int(line.split(":")[1], 16))[2:].zfill(20*4)
        print(bits)
        for i in range(80):
            if i > 1:
                data_list[len(data_list)-1] += bits[i] +','   
        
    if line[0:len(OUTPUT) + 4] == OUTPUT + " dma":
        if first:
            
            data_list[0] += str(bitline_iterator) + ','
            bitline_iterator += 1
        line = line_breaker(line)

        #remove header
        data = line + ','

        
        #convert from space separated values to comma separated values
        data_list[len(data_list)-1] += (data.replace(" ", ","))

#save to an output
def write_output():
    print(data_list[0])
    file = open("parsed_data/" + save_name, "a")
    for i in range(len(data_list)):
        if (i == 0 and os.stat("parsed_data/" + save_name).st_size == 0) or i > 0:
            file.write(data_list[i])
    file.close()



#TODO: implement check to see if the instance file actually exists
def main():
    global first, data_list, current_wordline, bitline_iterator
    first = True
    data_list=[]
    lbw = get_lbw()
    part = get_part()
    #data_list[0] += "instance,"
    temp_date = get_temp_date()
    data_list[0] += "dma_type,"

    data_list[0] += "wordline,"

    #if the instance file actually exists

    if os.path.exists(path + 'dma0_rap_14u.dat_0'):
        print("Im in")
        #get data from file
        current_dat = 'dma0_rap_14u.dat_0'
        file = open(path +current_dat)

        line_starter(temp_date, lbw, part, "RAP-pre")
        #for each line
        for line in file:
            #check header
            if (line[0:3] == OUTPUT) and (re.search("^#< get_dma_3k", line)):
                bitline_iterator = 0
                data_list[len(data_list)-1] += "\n"
                line_starter(temp_date, lbw, part, "RAP")
                current_wordline = int(line[(len("^#< get_dma_3k")):len(line)])
                
            check_data_output(line.rstrip('\n'))
        file.close()
        first = False
    bitline_iterator = 0
    if os.path.exists(path + 'dma1_rp_14u.dat_0'):
            
        #get data from file
        current_dat = 'dma1_rp_14u.dat_0'
        file = open(path +current_dat)
        line_starter(temp_date, lbw, part, "RP")
        #for each line
        for line in file:
            #check header
            if (line[0:3] == OUTPUT) and (re.search("^#< get_dma_3k", line)):
                bitline_iterator = 0
                data_list[len(data_list)-1] += "\n"
                line_starter(temp_date, lbw, part, "RAP-pre")
                current_wordline = int(line[(len("^#< get_dma_3k")):len(line)])
            check_data_output(line.rstrip('\n'))
        file.close()
        first = False
        

    bitline_iterator = 0


    if os.path.exists(path + 'dma2_rap_14u.dat_0'):
            
        #get data from file
        current_dat = 'dma2_rap_14u.dat_0'
        file = open(path +current_dat)

        line_starter(temp_date, lbw, part, "RAP")
        #for each line
        for line in file:
            #check header
            if (line[0:3] == OUTPUT) and (re.search("^#< get_dma_3k", line)):
                bitline_iterator = 0
                data_list[len(data_list)-1] += "\n"
                line_starter(temp_date, lbw, part, "RAP-pre")
                current_wordline = int(line[(len("^#< get_dma_3k")):len(line)])
            check_data_output(line.rstrip('\n'))
        file.close()
    bitline_iterator = 0
    data_list[0] += "\n"
    data_list[1] += "\n"
    data_list[2] += "\n"
    data_list[3] += "\n"
    data_list[4] += "\n"
    write_output()



    return True


#What Gui calls to run script
def run_script(chip, datapath, path_to_part, save):
    print("running...")
    global CHIP, TEST, PATH_TO_DATA, path, save_name
    TEST = "htol"
    PATH_TO_DATA = datapath


    CHIP = chip
    path  = path_to_part
    save_name = save
    main()
    return 



#if os.path.exists("parsed_data/" + save_name):
#        os.remove("parsed_data/" + save_name)
#main()