#HAHA

import string
from tkinter import *
from ttkwidgets.autocomplete import AutocompleteCombobox
import tkinter as tk
from tkinter import ttk
import scripts.DataParser as parser
import os
import subprocess
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="data",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()        

# ####################################################################################
#                             INITIALIZING WINDOWS AND WIDGETS
# ####################################################################################


#Main Window for Frame
main_window = tk.Tk()
main_window.rowconfigure(0, minsize=50, weight=0)
main_window.rowconfigure(1, minsize=50, weight=1)
main_window.rowconfigure(2, minsize=50, weight=1)
main_window.columnconfigure(0, minsize=50, weight=1)
main_window.title("Data Parser")
#main_window.resizable(width=False, height=False)
main_window.eval('tk::PlaceWindow . center')

#shell window frame for window and selection window
sw = tk.Frame(main_window, relief=tk.RAISED, bd=2,)
sw.grid(row=0,column=0,sticky= 'nsew')
sw.columnconfigure(0, minsize="520", weight=0)
sw.columnconfigure(1, minsize="300", weight=1)

#top Window frame
window = tk.Frame(sw, relief=tk.RAISED, bd=2)
window.grid(row=0,column=0, sticky= 'nsew')
window.columnconfigure(1, minsize=420, weight=1)
window.columnconfigure(0, minsize=90, weight=1)



#TODO: check if these are used
window.datapath = "//DS220P/ds220_vol1/si_data/"
#window.datapath = './si_data/'
window.chip_path = ""

#lists used to build option selects
window.chips = []
window.tests = []
window.lbw = []
window.parts = []
window.temp_dates = []

#selection window
selection_window = tk.Frame(sw,)
selection_window.grid(row=0,column=1, sticky= 'nsew')
selection_window.columnconfigure(0, weight=1 , minsize=300)
selection_window.rowconfigure(0, weight=1, minsize=300)
selection_window.part_list = []
selection_window.full_part_list = []


#button frame for the window
parent_btn_frame = tk.Frame(main_window, bd=2)
parent_btn_frame.columnconfigure(0, weight=2, minsize=400)
parent_btn_frame.columnconfigure(1, weight=2, minsize=200)
parent_btn_frame.rowconfigure(0, minsize=50, weight=1)
parent_btn_frame.grid(row=1,column=0, sticky='nsew')

#Grid to split button pane in the right side of the parent
split_btn_frame = tk.Frame(parent_btn_frame)
split_btn_frame.grid(row=0, column=1, sticky='nsew')
split_btn_frame.columnconfigure(0, weight=2, minsize=100)
split_btn_frame.rowconfigure(0, minsize=25, weight=1)
split_btn_frame.rowconfigure(1, minsize=25, weight=1)

# split_frame = tk.Frame(split_btn_frame)
# split_frame.grid(row=0, column=0, sticky='nsew')
# split_frame.columnconfigure(0, weight=2, minsize=100)
# split_frame.columnconfigure(1, weight=2, minsize=100)
# split_frame.rowconfigure(0, minsize=25, weight=1)

# select_btn_frame = tk.Frame(split_frame)
# select_btn_frame.grid(row=0, column=0, sticky='nsew')
# select_btn_frame.columnconfigure(0, weight=2, minsize=100)
# select_btn_frame.rowconfigure(0, minsize=25, weight=1)

reset_btn_frame = tk.Frame(split_btn_frame)
reset_btn_frame.grid(row=0, column=0, sticky='nsew')
reset_btn_frame.columnconfigure(0, weight=2, minsize=100)
reset_btn_frame.rowconfigure(0, minsize=25, weight=1)


bottom_right_btn_frame = tk.Frame(split_btn_frame)
bottom_right_btn_frame.grid(row=1, column=0, sticky='nsew')
bottom_right_btn_frame.rowconfigure(0, minsize=25, weight=1)
bottom_right_btn_frame.columnconfigure(0, weight=1)


#Console frame
console_frame = tk.Frame(main_window, relief=tk.RAISED)
console_frame.grid(row=2,column=0, sticky= 'nsew')
console_frame.rowconfigure(0, weight=1)
console_frame.columnconfigure(0, weight=1)

#place frames in grid
#btn_frame.grid(row=1,column=0, sticky='nsew')
#variables that store the selected value of option selects
chip_selected = tk.StringVar()
test_selected = tk.StringVar()
lbw_selected = tk.StringVar()
part_no_selected = tk.StringVar()
temp_date_selected = tk.StringVar()
file_name_entry = tk.StringVar()
remove_part_selected = tk.StringVar()
date_selected =tk.StringVar()
temp_selected =tk.StringVar()

window_inner_frame = tk.Frame(window)

total_file_count = 0


# ####################################################################################
#                            Selection Window Functiobtn_select_partns
# ####################################################################################





def write_selection(text:string):

    """"
    while len(text) > 40:
        sub_text = text[0:text[0:40].rfind(' ')]
        selection_screen.insert("end", sub_text + "\n")
        text = text[len(sub_text) + 1 : len(text)]

    selection_screen.insert("end", text)
    selection_screen.insert("end", "\n\n")
    """
    selection_screen.insert(selection_screen.size(), (text))

def clear_selection():
    selection_screen.delete(0, selection_screen.size())

def add_newline_to_list(strings_list):
    return [s + '\n' for s in strings_list]

def trim_part_list(part_list, test_selected_value):
    trimmed_list = []
    for part in part_list:
        index = part.find(test_selected_value)
        if index != -1:
            trimmed_str = part[index + len(test_selected_value):].lstrip('/')
            trimmed_list.append(trimmed_str)
        else:
            trimmed_list.append(part)
    return trimmed_list


def pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no
):
    # Disable buttons for the duration of processing
    for btn in window.grid_slaves():
        if int(btn.grid_info()["row"]) < 3 and int(btn.grid_info()["column"]) == 1:
            btn["state"] = "disabled"

    parse_button_on()

    # Collect the current selections
    chip_sel = chip_selected.get()
    test_sel = test_selected.get()
    lbw_sel = lbw_selected.get()
    part_sel = part_no_selected.get()
    temp_date_sel = temp_date_selected.get()

    btn_remove_part["state"] = "normal"
    btn_reset_select["state"] = "normal"

    # Create a new list for paths
    new_paths = []

    # Determine which paths to add based on the current selections
    if lbw_sel == "" and date_selected.get() == "" and temp_selected.get() == "" and part_sel == "" and temp_date_sel == "":
        new_paths = test
    elif lbw_sel != "" and date_selected.get() == "" and temp_selected.get() == "" and part_sel == "" and temp_date_sel == "":
        new_paths = lbw
    elif date_selected.get() != "" and lbw_sel == "" and temp_selected.get() == "" and part_sel == "" and temp_date_sel == "":
        new_paths = date
    elif temp_selected.get() != "" and date_selected.get() == "" and lbw_sel == "" and part_sel == "" and temp_date_sel == "":
        new_paths = temp
    elif lbw_sel == "" and date_selected.get() == "" and temp_selected.get() == "" and part_sel != "" and temp_date_sel == "":
        new_paths = part_num
    elif date_selected.get() != "" and lbw_sel == "" and temp_selected.get() != "" and part_sel == "" and temp_date_sel == "":
        new_paths = date_temp
    elif lbw_sel == "" and date_selected.get() != "" and temp_selected.get() == "" and part_sel != "" and temp_date_sel == "":
        new_paths = date_part_no
    elif lbw_sel == "" and date_selected.get() == "" and temp_selected.get() != "" and part_sel != "" and temp_date_sel == "":
        new_paths = temp_part_no
    elif lbw_sel == "" and date_selected.get() != "" and temp_selected.get() != "" and part_sel != "" and temp_date_sel == "":
        new_paths = temp_date_part_no
    elif lbw_sel != "" and date_selected.get() != "" and temp_selected.get() == "" and part_sel == "" and temp_date_sel == "":
        new_paths = lbw_date
    elif lbw_sel != "" and date_selected.get() == "" and temp_selected.get() != "" and part_sel == "" and temp_date_sel == "":
        new_paths = lbw_temp
    elif lbw_sel != "" and date_selected.get() != "" and temp_selected.get() != "" and part_sel == "" and temp_date_sel == "":
        new_paths = lbw_temp_date
    elif lbw_sel != "" and date_selected.get() == "" and temp_selected.get() == "" and part_sel != "" and temp_date_sel == "":
        new_paths = lbw_part_no
    elif lbw_sel != "" and date_selected.get() == "" and temp_selected.get() != "" and part_sel != "" and temp_date_sel == "":
        new_paths = lbw_temp_part_no
    elif lbw_sel != "" and date_selected.get() != "" and temp_selected.get() == "" and part_sel != "" and temp_date_sel == "":
        new_paths = lbw_date_part_no
    elif lbw_sel != "" and date_selected.get() != "" and temp_selected.get() != "" and part_sel != "" and temp_date_sel == "":
        new_paths = lbw_temp_date_part_no
    
    for path in new_paths:
        selection_window.full_part_list.append(path)

    # Append new paths to the part list
    for path in new_paths:
        selection_window.part_list.append(path)

    # Trim all paths in selection_window.part_list
    trimmed_paths = trim_part_list(selection_window.part_list, test_sel)

    # Update selection_window.part_list to the trimmed paths
    selection_window.part_list = trimmed_paths

    # Check if any files were added
    if not new_paths:
        write_console("Path does not exist")
    else:
        update_selection_window()
        clear_console()
        write_console(f"{len(new_paths)} Files collected")
        write_console(f"{len(selection_window.full_part_list)} Total files collected")
        write_console("You can now parse your listed parts by pressing \"Parse Data\" or you can add more.")



def pressed_select_all():
    test = []
    lbw= []
    date = []
    temp = []
    part_num =[]
    date_temp = []
    date_part_no =[]
    temp_part_no = []
    temp_date_part_no=[]
    lbw_date = []
    lbw_temp = []
    lbw_temp_date = []
    lbw_part_no =[]
    lbw_temp_part_no =[]
    lbw_date_part_no= []
    lbw_temp_date_part_no= []

    #selected only test
    if(lbw_selected.get() == "" and date_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        print("test")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s;
            """, (test_selected.get(),))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s;
            """, (test_selected.get(),))
        
        test_path = cur.fetchall()
        test = [all_test[0] for all_test in test_path]
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)
           
        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return
    
    #selected only lbw
    if(lbw_selected.get() != "" and date_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        print("lbw")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s;
            """, (test_selected.get(),))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s;
            """, (test_selected.get(),))

        lbw_path = cur.fetchall()
        for row in lbw_path:
            # Assuming 'row' is a tuple with a single element (unique_id)
            full_path = row[0]
            # Check if lbw_selected.get() is a part of the path
            if lbw_selected.get() in full_path:
                lbw.append(full_path)
        print(lbw)
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return
    
    #selected lbw and date
    if(lbw_selected.get() != "" and date_selected.get() != "" and temp_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        print("lbw and date")
        if (test_selected.get() != 'otp'):
            cur.execute("""
                SELECT DISTINCT
                    '//DS220P/ds220_vol1/si_data/' ||
                    COALESCE(chip."Chip Type", '') ||
                    '/' ||
                    COALESCE(test."Test", '') ||
                    '/' ||
                        chip."Lot" || 
                        CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                        CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                        CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                        '/' || 
                        COALESCE(chip."Part Number", '') ||
                        '/' || 
                        COALESCE(test."Temp", '') || 
                        '_' || 
                        COALESCE(test."Date", ''),
                        -- Remove underscore before the first slash
                        '_/',  -- Match an underscore followed by a slash
                        '/'  -- Replace it with a single slash
                    || '/' AS unique_id  -- Append a slash at the end
                FROM 
                    chip
                JOIN 
                    test ON chip."Chip Id" = test."Chip Id"
                WHERE test."Test" = %s
                    AND test."Date" = %s;
                """, (test_selected.get(),date_selected.get(),))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
                WHERE test."Test" = %s
                    AND test."Date" = %s;
                """, (test_selected.get(),date_selected.get(),))

        lbw_path = cur.fetchall()
        for row in lbw_path:
            # Assuming 'row' is a tuple with a single element (unique_id)
            full_path = row[0]
            # Check if lbw_selected.get() is a part of the path
            if lbw_selected.get() in full_path:
                lbw_date.append(full_path)
        print(lbw)
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return

    #selected lbw and temp
    if(lbw_selected.get() != "" and date_selected.get() == "" and temp_selected.get() != "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        print("lbw and temp")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Temp" = %s;
            """, (test_selected.get(),temp_selected.get(),))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
                WHERE test."Test" = %s
                    AND test."Date" = %s;
                """, (test_selected.get(),date_selected.get(),))


        lbw_path = cur.fetchall()
        for row in lbw_path:
            # Assuming 'row' is a tuple with a single element (unique_id)
            full_path = row[0]
            # Check if lbw_selected.get() is a part of the path
            if lbw_selected.get() in full_path:
                lbw_temp.append(full_path)
        print(lbw)
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return
    
    #selected lbw and temp and date
    if(lbw_selected.get() != "" and date_selected.get() != "" and temp_selected.get() != "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        print("lbw and temp and date")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Temp" = %s
                AND test."Date" = %s;
            """, (test_selected.get(),temp_selected.get(),date_selected.get()))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Temp" = %s
                AND test."Date" = %s;
            """, (test_selected.get(),temp_selected.get(),date_selected.get()))

        lbw_path = cur.fetchall()
        for row in lbw_path:
            # Assuming 'row' is a tuple with a single element (unique_id)
            full_path = row[0]
            # Check if lbw_selected.get() is a part of the path
            if lbw_selected.get() in full_path:
                lbw_temp_date.append(full_path)
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return
    
    #selected temp and date
    if(date_selected.get() != "" and lbw_selected.get() == "" and temp_selected.get() != "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Date" = %s
                AND test."Temp" = %s
        """, (test_selected.get(), date_selected.get(), temp_selected.get()))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Date" = %s
                AND test."Temp" = %s
        """, (test_selected.get(), date_selected.get(), temp_selected.get()))
       
        date_temp_path = cur.fetchall()
        date_temp = [all_temp_date[0] for all_temp_date in date_temp_path]
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return

    #selected only date
    if(date_selected.get() != "" and lbw_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        print("date")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Date" = %s;
        """, (test_selected.get(), date_selected.get()))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Date" = %s;
        """, (test_selected.get(), date_selected.get()))
       
        date_path = cur.fetchall()
        date = [all_date[0] for all_date in date_path]
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
    
        return

    #selected only temp
    if(temp_selected.get() != "" and date_selected.get() == "" and lbw_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        print("temp")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Temp" = %s;
        """, (test_selected.get(), temp_selected.get()))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Temp" = %s;
        """, (test_selected.get(), temp_selected.get()))
        temp_path = cur.fetchall()
        temp = [all_temp[0] for all_temp in temp_path]
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return

    #selected lbw and part no.
    if(lbw_selected.get() != "" and date_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        print("lbw and part no.")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND chip."Part Number" = %s;
            """, (test_selected.get(),part_no_selected.get(),))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND chip."Part Number" = %s;
            """, (test_selected.get(),part_no_selected.get(),))

        lbw_path = cur.fetchall()
        for row in lbw_path:
            # Assuming 'row' is a tuple with a single element (unique_id)
            full_path = row[0]
            # Check if lbw_selected.get() is a part of the path
            if lbw_selected.get() in full_path:
                lbw_part_no.append(full_path)
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return
    
    #selected date and part no.
    if(lbw_selected.get() == "" and date_selected.get() != "" and temp_selected.get() == "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        print("date and part no.")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Date" = %s
                AND chip."Part Number" = %s;
        """, (test_selected.get(), date_selected.get(), part_no_selected.get()))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Date" = %s
                AND chip."Part Number" = %s;
        """, (test_selected.get(), date_selected.get(), part_no_selected.get()))

       
        date_part_no_path = cur.fetchall()
        date_part_no = [all_date_part_no[0] for all_date_part_no in date_part_no_path]
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return
    
    #selected temp and part no.
    if(lbw_selected.get() == "" and date_selected.get() == "" and temp_selected.get() != "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        print("temp and part no.")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Temp" = %s
                AND chip."Part Number" = %s;
        """, (test_selected.get(), temp_selected.get(), part_no_selected.get()))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Temp" = %s
                AND chip."Part Number" = %s;
        """, (test_selected.get(), temp_selected.get(), part_no_selected.get()))
       
        temp_part_no_path = cur.fetchall()
        temp_part_no = [all_temp_part_no[0] for all_temp_part_no in temp_part_no_path]
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return
    
    #selected lbw and temp and part no.
    if(lbw_selected.get() != "" and date_selected.get() == "" and temp_selected.get() != "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        print("lbw and temp and part no.")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Temp" = %s
                AND chip."Part Number" = %s;
            """, (test_selected.get(),temp_selected.get(),part_no_selected.get(),))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Temp" = %s
                AND chip."Part Number" = %s;
            """, (test_selected.get(),temp_selected.get(),part_no_selected.get(),))

        lbw_path = cur.fetchall()
        for row in lbw_path:
            # Assuming 'row' is a tuple with a single element (unique_id)
            full_path = row[0]
            # Check if lbw_selected.get() is a part of the path
            if lbw_selected.get() in full_path:
                lbw_temp_part_no.append(full_path)
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)
                            
        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return
    
    #selected lbw and date and part no.
    if(lbw_selected.get() != "" and date_selected.get() != "" and temp_selected.get() == "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        print("lbw and date and part no.")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Date" = %s
                AND chip."Part Number" = %s;
            """, (test_selected.get(),date_selected.get(),part_no_selected.get(),))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Temp" = %s
                AND chip."Part Number" = %s;
            """, (test_selected.get(),temp_selected.get(),part_no_selected.get(),))

        lbw_path = cur.fetchall()
        for row in lbw_path:
            # Assuming 'row' is a tuple with a single element (unique_id)
            full_path = row[0]
            # Check if lbw_selected.get() is a part of the path
            if lbw_selected.get() in full_path:
                lbw_date_part_no.append(full_path)
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)
                            
        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return

    #selected temp and date and part no.
    if(lbw_selected.get() == "" and date_selected.get() != "" and temp_selected.get() != "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        print("temp and date and part no.")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Temp" = %s
                AND test."Date" = %s
                AND chip."Part Number" = %s;
        """, (test_selected.get(), temp_selected.get(), date_selected.get(),part_no_selected.get()))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE 
                test."Test" = %s
                AND test."Temp" = %s
                AND test."Date" = %s
                AND chip."Part Number" = %s;
        """, (test_selected.get(), temp_selected.get(), date_selected.get(),part_no_selected.get()))
       
        temp_date_part_no_path = cur.fetchall()
        temp_date_part_no = [all_temp_date_part_no[0] for all_temp_date_part_no in temp_date_part_no_path]
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)

        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return
    
    #selected lbw and date and temp and part no.
    if(lbw_selected.get() != "" and date_selected.get() != "" and temp_selected.get() != "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        print("lbw and date and temp and part no.")
        if (test_selected.get() != 'otp'):
            cur.execute("""
            SELECT DISTINCT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' || 
                    COALESCE(test."Temp", '') || 
                    '_' || 
                    COALESCE(test."Date", ''),
                    -- Remove underscore before the first slash
                    '_/',  -- Match an underscore followed by a slash
                    '/'  -- Replace it with a single slash
                || '/' AS unique_id  -- Append a slash at the end
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Temp" = %s
                AND test."Date" = %s
                AND chip."Part Number" = %s;
            """, (test_selected.get(),temp_selected.get(),date_selected.get(),part_no_selected.get(),))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Temp" = %s
                AND test."Date" = %s
                AND chip."Part Number" = %s;
            """, (test_selected.get(),temp_selected.get(),date_selected.get(),part_no_selected.get(),))

        lbw_path = cur.fetchall()
        for row in lbw_path:
            # Assuming 'row' is a tuple with a single element (unique_id)
            full_path = row[0]
            # Check if lbw_selected.get() is a part of the path
            if lbw_selected.get() in full_path:
                lbw_temp_date_part_no.append(full_path)
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):        
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)  
                            
        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return

    # dp += lbw_selected.get() + '/'

    # selected only part no.
    if(lbw_selected.get() == "" and date_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        print("only part no.")
        if (test_selected.get() != 'otp'):
            cur.execute("""
                SELECT DISTINCT
                    '//DS220P/ds220_vol1/si_data/' ||
                    COALESCE(chip."Chip Type", '') ||
                    '/' ||
                    COALESCE(test."Test", '') ||
                    '/' ||
                        chip."Lot" || 
                        CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                        CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                        CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                        '/' || 
                        COALESCE(chip."Part Number", '') ||
                        '/' || 
                        COALESCE(test."Temp", '') || 
                        '_' || 
                        COALESCE(test."Date", ''),
                        -- Remove underscore before the first slash
                        '_/',  -- Match an underscore followed by a slash
                        '/'  -- Replace it with a single slash
                    || '/' AS unique_id  -- Append a slash at the end
                FROM 
                    chip
                JOIN 
                    test ON chip."Chip Id" = test."Chip Id"
                WHERE 
                    test."Test" = %s
                    AND chip."Part Number" = %s;
                ;
            """, (test_selected.get(), part_no_selected.get()))
        else:
            cur.execute("""
            SELECT
                '//DS220P/ds220_vol1/si_data/' ||
                COALESCE(chip."Chip Type", '') ||
                '/' ||
                COALESCE(test."Test", '') ||
                '/' ||
                    chip."Lot" || 
                    CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                    CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END ||
                    '/' || 
                    COALESCE(chip."Part Number", '') ||
                    '/' 
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE test."Test" = %s
                AND test."Temp" = %s
                AND test."Date" = %s
                AND chip."Part Number" = %s;
            """, (test_selected.get(),temp_selected.get(),date_selected.get(),part_no_selected.get(),))
        part_num_path = cur.fetchall()
        part_num = [all_part_num[0] for all_part_num in part_num_path]
        if check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):
            pressed_add_part(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no)
                        
        file_select = tk.Entry(window, textvariable=file_name_entry)
        file_select.grid(row=6,column=1, sticky='ew')
        file_select["font"]=("helvetica",10)
        file_label = tk.Label(window,text="save file name")
        file_label.grid(row=6,column=0)
        file_label["font"]=("helvetica",10)
        file_name_entry.set(chip_selected.get() + '_' + test_selected.get())
        write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + " have been selected.")
        return

    # if(part_no_selected.get() == ""):
    #     print("E")
    #     part_list = os.listdir(dp)
    #     for part in part_list:
    #         dp = (window.datapath + chip_selected.get() + '/' + test_selected.get() + '/' + lbw_selected.get() + '/' + part + '/')
    #         temp_date_list = os.listdir(dp)
    #         for temp_date in temp_date_list:
    #             dp = (window.datapath + chip_selected.get() + '/' + test_selected.get() + '/' + lbw_selected.get() + '/' + part + '/' + temp_date + '/')
    #             if check_enable_selection(chip_selected.get(), test_selected.get(), lbw_selected.get(), part, temp_date):
    #                 pressed_add_part(chip_selected.get(), test_selected.get(), lbw_selected.get(), part, temp_date)
    #     file_select = tk.Entry(window, textvariable=file_name_entry)
    #     file_select.grid(row=6,column=1, sticky='ew')
    #     file_select["font"]=("helvetica",10)
    #     file_label = tk.Label(window,text="save file name")
    #     file_label.grid(row=6,column=0)
    #     file_label["font"]=("helvetica",10)
    #     file_name_entry.set(chip_selected.get() + '_' + lbw_selected.get() + '_' + test_selected.get())
    #     write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + '/' + lbw_selected.get() + " have been selected.")
    #     return
    
    # if(temp_date_selected.get() != "" and part_no_selected.get() == ""):
    #     print("F")
    #     lbw_list = os.listdir(dp)
    #     for lbw in lbw_list:
    #         dp = (window.datapath + chip_selected.get() + '/' + test_selected.get() + '/' + lbw + '/')
    #         part_list = os.listdir(dp)
    #         for part in part_list:
    #             dp = (window.datapath + chip_selected.get() + '/' + test_selected.get() + '/' + lbw + '/' + part + '/')
    #             temp_date_list = os.listdir(dp)
    #             for temp_date in temp_date_list:
    #                 if temp_date == temp_date_selected.get():
    #                     dp = (window.datapath + chip_selected.get() + '/' + test_selected.get() + '/' + lbw + '/' + part + '/' + temp_date + '/')
    #                     if check_enable_selection(chip_selected.get(), test_selected.get(), lbw, part, temp_date):
    #                         pressed_add_part(chip_selected.get(), test_selected.get(), lbw, part, temp_date)  

    #     file_select = tk.Entry(window, textvariable=file_name_entry)
    #     file_select.grid(row=6,column=1, sticky='ew')
    #     file_select["font"]=("helvetica",10)
    #     file_label = tk.Label(window,text="save file name")
    #     file_label.grid(row=6,column=0)
    #     file_label["font"]=("helvetica",10)
    #     file_name_entry.set(chip_selected.get() + '_' + lbw_selected.get() + '_' + part_no_selected.get() + '_' + test_selected.get())
    #     write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + '/' + lbw_selected.get() + '/' + part_no_selected.get() + " have been selected.")
    #     return



    # if(temp_date_selected.get() == ""):
    #     print("G")
    #     temp_date_list = os.listdir(dp)
    #     for temp_date in temp_date_list:
    #         dp = (window.datapath + chip_selected.get() + '/' + test_selected.get() + '/' + lbw_selected.get() + '/' + part_no_selected.get() + '/' + temp_date + '/')
    #         if check_enable_selection(chip_selected.get(), test_selected.get(), lbw_selected.get(), part_no_selected.get(), temp_date):
    #             pressed_add_part(chip_selected.get(), test_selected.get(), lbw_selected.get(), part_no_selected.get(), temp_date)
    #     file_select = tk.Entry(window, textvariable=file_name_entry)
    #     file_select.grid(row=6,column=1, sticky='ew')
    #     file_select["font"]=("helvetica",10)
    #     file_label = tk.Label(window,text="save file name")
    #     file_label.grid(row=6,column=0)
    #     file_label["font"]=("helvetica",10)
    #     file_name_entry.set(chip_selected.get() + '_' + lbw_selected.get() + '_' + part_no_selected.get() + '_' + test_selected.get())
    #     write_console("All parts within " + chip_selected.get() + '/' + test_selected.get() + '/' + lbw_selected.get() + '/' + part_no_selected.get() + " have been selected.")
    #     return

def update_selection_window():
    clear_selection()
    for part in selection_window.part_list:
        write_selection(part)

    if selection_screen.size() == 0:
            for btn in window.grid_slaves():
                if int(btn.grid_info()["row"]) < 3 and int(btn.grid_info()["column"]) == 1:
                    btn["state"] = "normal"


def update_filters(temp_combobox, dates_combobox, parts_combobox,lbw_combobox):

    # Clear existing options
    window.temp.clear()
    window.dates.clear()
    window.lbw.clear()
    window.parts.clear()

    lbw_parts = lbw_selected.get().split('_')
    # Use list unpacking with defaults
    lot, bin, wafer, proc_corner = (lbw_parts + [''] * 4)[:4]

    #selected only lbw
    if(lbw_selected.get() != "" and date_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):

        cur.execute("""
            SELECT DISTINCT "Temp"
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL);
        """,(test_selected.get(), lot,bin, wafer, proc_corner))
        temp = cur.fetchall()

        # Update the window.dates list
        window.temp = [""] + [temp_type[0] for temp_type in temp]

        # Update existing combobox values
        temp_combobox['values'] = window.temp

        cur.execute("""
            SELECT DISTINCT "Date"
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL);
        """,(test_selected.get(), lot,bin, wafer, proc_corner))
        date = cur.fetchall()

        # Update the window.dates list
        window.dates = [""] + [date_type[0] for date_type in date]

        # Update existing combobox values
        dates_combobox['values'] = window.dates

        cur.execute("""
        SELECT DISTINCT "Part Number" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL);
        """,(test_selected.get(), lot,bin, wafer, proc_corner))
        parts = cur.fetchall()

        # Update the window.dates list
        window.parts = [""] + [part_type[0] for part_type in parts]
        

        # Update existing combobox values
        parts_combobox['values'] = window.parts

    #selected lbw and date
    if(lbw_selected.get() != "" and date_selected.get() != "" and temp_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        cur.execute("""
            SELECT DISTINCT "Temp"
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL)
            AND "Date" = %s;
        """,(test_selected.get(), lot,bin, wafer, proc_corner, date_selected.get()))
        temp = cur.fetchall()

        # Update the window.dates list
        window.temp = [""] + [temp_type[0] for temp_type in temp]

        # Update existing combobox values
        temp_combobox['values'] = window.temp

        cur.execute("""
        SELECT DISTINCT "Part Number" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL)
            AND "Date" = %s;
        """,(test_selected.get(), lot,bin, wafer, proc_corner, date_selected.get()))
        parts = cur.fetchall()

        # Update the window.dates list
        window.parts = [""] + [part_type[0] for part_type in parts]
        
        # Update existing combobox values
        parts_combobox['values'] = window.parts

    #selected lbw and temp
    if(lbw_selected.get() != "" and date_selected.get() == "" and temp_selected.get() != "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):

        cur.execute("""
        SELECT DISTINCT "Date" 
        FROM test 
        JOIN chip ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL)
            AND "Temp" = %s;
        """,(test_selected.get(), lot,bin, wafer, proc_corner, temp_selected.get()))
        date = cur.fetchall()

        # Update the window.dates list
        window.dates = [""] + [date_type[0] for date_type in date]
        

        # Update existing combobox values
        dates_combobox['values'] = window.dates

        cur.execute("""
        SELECT DISTINCT "Part Number" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL)
            AND "Temp" = %s;
        """,(test_selected.get(), lot,bin, wafer, proc_corner, temp_selected.get()))
        parts = cur.fetchall()

        # Update the window.dates list
        window.parts = [""] + [part_type[0] for part_type in parts]
        

        # Update existing combobox values
        parts_combobox['values'] = window.parts

    #selected lbw and part no.
    if(lbw_selected.get() != "" and date_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):

        cur.execute("""
            SELECT DISTINCT "Temp"
            FROM 
                chip
            JOIN 
                test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL)
            AND "Part Number" = %s;
        """,(test_selected.get(), lot,bin, wafer, proc_corner, part_no_selected.get()))
        temp = cur.fetchall()

        # Update the window.dates list
        window.temp = [""] + [temp_type[0] for temp_type in temp]

        # Update existing combobox values
        temp_combobox['values'] = window.temp

        cur.execute("""
        SELECT DISTINCT "Date" 
        FROM test 
        JOIN chip ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL)
            AND "Part Number" = %s;
        """,(test_selected.get(), lot,bin, wafer, proc_corner, part_no_selected.get()))
        date = cur.fetchall()

        # Update the window.dates list
        window.dates = [""] + [date_type[0] for date_type in date]
        

        # Update existing combobox values
        dates_combobox['values'] = window.dates

    #selected lbw and temp and date
    if(lbw_selected.get() != "" and date_selected.get() != "" and temp_selected.get() != "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):
        cur.execute("""
        SELECT DISTINCT "Part Number" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL)
            And "Date" = %s
            AND "Temp" = %s;
        """,(test_selected.get(), lot,bin, wafer, proc_corner, date_selected.get(),temp_selected.get()))
        parts = cur.fetchall()

        # Update the window.dates list
        window.parts = [""] + [part_type[0] for part_type in parts]
        

        # Update existing combobox values
        parts_combobox['values'] = window.parts

    #selected only temp
    if(temp_selected.get() != "" and date_selected.get() == "" and lbw_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):

        cur.execute("""
            SELECT DISTINCT "Date" 
            FROM test 
            JOIN chip ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s AND "Temp" = %s
        """,(test_selected.get(), temp_selected.get()))
        date = cur.fetchall()

        # Update the window.dates list
        window.dates = [""] + [date_type[0] for date_type in date]
        

        # Update existing combobox values
        dates_combobox['values'] = window.dates

        cur.execute("""
        SELECT DISTINCT "Part Number" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
        WHERE "Test" = %s AND "Temp" = %s
        """, (test_selected.get(), temp_selected.get()))
        parts = cur.fetchall()

        # Update the window.dates list
        window.parts = [""] + [part_type[0] for part_type in parts]
        

        # Update existing combobox values
        parts_combobox['values'] = window.parts

        cur.execute("""
        SELECT DISTINCT 
            chip."Lot" || 
            CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
            CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
            CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END
        FROM Test
        JOIN Chip ON test."Chip Id" = chip."Chip Id"
        WHERE test."Test" = %s AND "Temp" = %s
        """, (test_selected.get(), temp_selected.get()))
        window.lbw.append("")
        lbw = cur.fetchall()
        for row in lbw:
            combined_info = row[0] if row[0] is not None else ""
            window.lbw.append(combined_info)

        # Update existing combobox values
        lbw_combobox['values'] = window.lbw

    #selected only date
    if(date_selected.get() != "" and lbw_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):

        cur.execute("""
            SELECT DISTINCT "Temp" 
            FROM test 
            JOIN chip ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s AND "Date" = %s
        """,(test_selected.get(), date_selected.get()))
        temp = cur.fetchall()

        # Update the window.dates list
        window.temp = [""] + [temp_type[0] for temp_type in temp]
        

        # Update existing combobox values
        temp_combobox['values'] = window.temp

        cur.execute("""
        SELECT DISTINCT "Part Number" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
        WHERE "Test" = %s AND "Date" = %s
        """, (test_selected.get(), date_selected.get()))
        parts = cur.fetchall()

        # Update the window.dates list
        window.parts = [""] + [part_type[0] for part_type in parts]
        

        # Update existing combobox values
        parts_combobox['values'] = window.parts

        cur.execute("""
        SELECT DISTINCT 
            chip."Lot" || 
            CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
            CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
            CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END
        FROM Test
        JOIN Chip ON test."Chip Id" = chip."Chip Id"
        WHERE test."Test" = %s AND "Date" = %s
        """, (test_selected.get(), date_selected.get()))
        window.lbw.append("")
        lbw = cur.fetchall()
        for row in lbw:
            combined_info = row[0] if row[0] is not None else ""
            window.lbw.append(combined_info)

        # Update existing combobox values
        lbw_combobox['values'] = window.lbw

    # selected only part no.
    if(lbw_selected.get() == "" and date_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        cur.execute("""
        SELECT DISTINCT "Temp" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
        WHERE "Test" = %s AND "Part Number" = %s
        """,(test_selected.get(), part_no_selected.get()))
        temp = cur.fetchall()

        # Update the window.dates list
        window.temp = [""] + [temp_type[0] for temp_type in temp]
        

        # Update existing combobox values
        temp_combobox['values'] = window.temp

        cur.execute("""
        SELECT DISTINCT "Date" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
        WHERE "Test" = %s AND "Part Number" = %s
        """,(test_selected.get(), part_no_selected.get()))
        date = cur.fetchall()

        # Update the window.dates list
        window.dates = [""] + [date_type[0] for date_type in date]
        

        # Update existing combobox values
        dates_combobox['values'] = window.dates

        cur.execute("""
        SELECT DISTINCT 
            chip."Lot" || 
            CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
            CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
            CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END
        FROM Test
        JOIN Chip ON test."Chip Id" = chip."Chip Id"
        WHERE test."Test" = %s AND "Part Number" = %s
        """, (test_selected.get(), part_no_selected.get()))
        window.lbw.append("")
        lbw = cur.fetchall()
        for row in lbw:
            combined_info = row[0] if row[0] is not None else ""
            window.lbw.append(combined_info)

        # Update existing combobox values
        lbw_combobox['values'] = window.lbw

    #selected temp and date
    if(date_selected.get() != "" and lbw_selected.get() == "" and temp_selected.get() != "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):

        cur.execute("""
        SELECT DISTINCT "Part Number" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
        WHERE "Test" = %s AND "Temp" = %s AND "Date" = %s
        """, (test_selected.get(), temp_selected.get(), date_selected.get()))
        parts = cur.fetchall()

        # Update the window.dates list
        window.parts = [""] + [part_type[0] for part_type in parts]
        

        # Update existing combobox values
        parts_combobox['values'] = window.parts

        cur.execute("""
        SELECT DISTINCT 
            chip."Lot" || 
            CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
            CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
            CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END
        FROM Test
        JOIN Chip ON test."Chip Id" = chip."Chip Id"
        WHERE "Test" = %s AND "Temp" = %s AND "Date" = %s
        """, (test_selected.get(), temp_selected.get(), date_selected.get()))
        window.lbw.append("")
        lbw = cur.fetchall()
        for row in lbw:
            combined_info = row[0] if row[0] is not None else ""
            window.lbw.append(combined_info)

        # Update existing combobox values
        lbw_combobox['values'] = window.lbw

    #selected date and part no.
    if(lbw_selected.get() == "" and date_selected.get() != "" and temp_selected.get() == "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):

        cur.execute("""
        SELECT DISTINCT "Temp" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
        WHERE "Test" = %s AND "Date" = %s AND "Part Number" = %s
        """, (test_selected.get(), date_selected.get(), part_no_selected.get()))
        date = cur.fetchall()

        # Update the window.dates list
        window.dates = [""] + [date_type[0] for date_type in date]
        

        # Update existing combobox values
        dates_combobox['values'] = window.dates

        cur.execute("""
        SELECT DISTINCT 
            chip."Lot" || 
            CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
            CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
            CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END
        FROM Test
        JOIN Chip ON test."Chip Id" = chip."Chip Id"
        WHERE "Test" = %s AND "Date" = %s AND "Part Number" = %s
        """, (test_selected.get(), date_selected.get(), part_no_selected.get()))

        window.lbw.append("")
        lbw = cur.fetchall()
        for row in lbw:
            combined_info = row[0] if row[0] is not None else ""
            window.lbw.append(combined_info)

        # Update existing combobox values
        lbw_combobox['values'] = window.lbw

    #selected temp and part no.
    if(lbw_selected.get() == "" and date_selected.get() == "" and temp_selected.get() != "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):

        cur.execute("""
        SELECT DISTINCT "Date" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
        WHERE "Test" = %s AND "Temp" = %s AND "Part Number" = %s
        """, (test_selected.get(), temp_selected.get(), part_no_selected.get()))
        date = cur.fetchall()

        # Update the window.dates list
        window.dates = [""] + [date_type[0] for date_type in date]
        

        # Update existing combobox values
        dates_combobox['values'] = window.dates

        cur.execute("""
        SELECT DISTINCT 
            chip."Lot" || 
            CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
            CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
            CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END
        FROM Chip
        JOIN Test ON test."Chip Id" = chip."Chip Id"
        WHERE "Test" = %s AND "Temp" = %s AND "Part Number" = %s
        """, (test_selected.get(), temp_selected.get(), part_no_selected.get()))

        window.lbw.append("")
        lbw = cur.fetchall()
        for row in lbw:
            combined_info = row[0] if row[0] is not None else ""
            window.lbw.append(combined_info)

        # Update existing combobox values
        lbw_combobox['values'] = window.lbw

    #selected temp and date and part no.
    if(lbw_selected.get() == "" and date_selected.get() != "" and temp_selected.get() != "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        
        cur.execute("""
        SELECT DISTINCT 
            chip."Lot" || 
            CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
            CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
            CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END
        FROM Chip
        JOIN Test ON test."Chip Id" = chip."Chip Id"
        WHERE "Test" = %s AND "Temp" = %s AND "Date" = %s AND "Part Number" = %s
        """, (test_selected.get(), temp_selected.get(), date_selected.get(), part_no_selected.get()))

        window.lbw.append("")
        lbw = cur.fetchall()
        for row in lbw:
            combined_info = row[0] if row[0] is not None else ""
            window.lbw.append(combined_info)

        # Update existing combobox values
        lbw_combobox['values'] = window.lbw

    #selected lbw and temp and part no.
    if(lbw_selected.get() != "" and date_selected.get() == "" and temp_selected.get() != "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):
        cur.execute("""
        SELECT DISTINCT "Date" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL)
            AND "Temp" = %s
            And "Part Number" = %s;
        """,(test_selected.get(), lot,bin, wafer, proc_corner, temp_selected.get(), part_no_selected.get()))
        date = cur.fetchall()

        # Update the window.dates list
        window.dates = [""] + [date_type[0] for date_type in date]

        # Update existing combobox values
        dates_combobox['values'] = window.dates

    #selected lbw and date and part no.
    if(lbw_selected.get() != "" and date_selected.get() != "" and temp_selected.get() == "" and part_no_selected.get() != "" and temp_date_selected.get() == ""):

        cur.execute("""
        SELECT DISTINCT "Temp" 
        FROM chip 
		JOIN 
        test ON chip."Chip Id" = test."Chip Id"
            WHERE "Test" = %s
            AND "Lot" = %s
            AND ("Bin" = %s OR "Bin" IS NULL)
            AND ("Wafer" = %s OR "Wafer" IS NULL)
            AND ("Process Corner" = %s OR "Process Corner" IS NULL)
            AND "Date" = %s
            And "Part Number" = %s;
        """,(test_selected.get(), lot,bin, wafer, proc_corner, date_selected.get(), part_no_selected.get()))
        temp = cur.fetchall()

        # Update the window.dates list
        window.temp = [""] + [temp_type[0] for temp_type in temp]
        

        # Update existing combobox values
        temp_combobox['values'] = window.temp

    # all empty
    if(lbw_selected.get() == "" and date_selected.get() == "" and temp_selected.get() == "" and part_no_selected.get() == "" and temp_date_selected.get() == ""):

        cur.execute(""" 
            SELECT DISTINCT 
                chip."Lot" || 
                CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
                CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
                CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END
            FROM Test
            JOIN Chip ON test."Chip Id" = chip."Chip Id"
            WHERE test."Test" = %s;
        """, (test_selected.get(),))

        window.lbw.append("")
        lbw = cur.fetchall()
        for row in lbw:
            combined_info = row[0] if row[0] is not None else ""
            window.lbw.append(combined_info)

        window.lbw = list(set(window.lbw))  # Remove duplicates
        window.lbw.sort()  # Sort the list

        lbw_combobox['values'] = window.lbw

        cur.execute(""" 
            SELECT DISTINCT "Date" FROM test WHERE "Test" = %s
        """, (test_selected.get(),))
        date = cur.fetchall()

        # Update the window.dates list
        window.dates = [""] + [date_type[0] for date_type in date]
        window.dates.sort()  # Sort the list

        # Update existing combobox values
        dates_combobox['values'] = window.dates


        cur.execute("""
            SELECT DISTINCT "Temp" FROM test WHERE "Test" = %s
        """, (test_selected.get(),))
        temp = cur.fetchall()
        # Update the window.dates list
        window.temp = [""] + [temp_type[0] for temp_type in temp]
        window.temp.sort()  # Sort the list

        # Update existing combobox values
        temp_combobox['values'] = window.temp

        cur.execute("""
        SELECT DISTINCT chip."Part Number" FROM Test JOIN Chip ON test."Chip Id" = chip."Chip Id" WHERE test."Test" = %s
        """, (test_selected.get(),))
        parts = cur.fetchall()

        # Update the window.dates list
        window.parts = [""] + [part_type[0] for part_type in parts]
        window.parts.sort()  # Sort the list
        

        # Update existing combobox values
        parts_combobox['values'] = window.parts





def check_enable_selection(test, lbw, date, temp, part_num, date_temp, date_part_no, temp_part_no, temp_date_part_no, lbw_date, lbw_temp, lbw_temp_date, lbw_part_no, lbw_temp_part_no, lbw_date_part_no, lbw_temp_date_part_no):

    # Initialize selected paths list
    selected_paths = []

    # Construct paths based on provided parameters
    if test:
        selected_paths.extend(test)
    if date:
        selected_paths.extend(date)
    if lbw:
        selected_paths.extend(lbw)
    if temp:
        selected_paths.extend(temp)
    if part_num:
        selected_paths.extend(part_num)
    if date_temp:
        selected_paths.extend(date_temp)
    if date_part_no:
        selected_paths.extend(date_part_no)
    if temp_part_no:
        selected_paths.extend(temp_part_no)
    if temp_date_part_no:
        selected_paths.extend(temp_date_part_no)
    if lbw_date:
        selected_paths.extend(lbw_date)
    if lbw_temp:
        selected_paths.extend(lbw_temp)
    if lbw_temp_date:
        selected_paths.extend(lbw_temp_date)
    if lbw_part_no:
        selected_paths.extend(lbw_part_no)
    if lbw_temp_part_no:
        selected_paths.extend(lbw_temp_part_no)
    if lbw_date_part_no:
        selected_paths.extend(lbw_date_part_no)
    if lbw_temp_date_part_no:
        selected_paths.extend(lbw_temp_date_part_no)

    # Check for already selected paths
    existing_paths = set(selection_window.full_part_list)
    # List to collect duplicate paths
    duplicates = []
    
    for path in selected_paths:
        if path in existing_paths:
            duplicates.append(path)
    
    # Check if there are duplicates
    if duplicates:
        write_console("Paths already selected:\n" + "\n".join(duplicates))
        return False

    
    if(temp_date_selected.get() != ""): 
        btn_select_all["state"] = "disabled"
    
    return True

def reset_selection():
    global total_file_count
    total_file_count = 0
    btn_reset_select["state"] = "disabled"
    selection_window.part_list = []
    selection_window.full_part_list = []
    parse_button_off()
    delete_remove_part()
    update_selection_window()
    write_console("All parts are removed")

def parse_button_on():
    global btn_parse_data
    btn_parse_data["bg"] = "#3DED97"
    btn_parse_data["state"] = "normal"

def parse_button_off():
    global btn_parse_data
    btn_parse_data["bg"] = "#E97F7F"
    btn_parse_data["state"] = "disabled"

#part selection reset button
btn_reset_select = tk.Button(reset_btn_frame, text="Reset Selection", command=reset_selection)
btn_reset_select.grid(row=0,column=0, sticky='nsew')
btn_reset_select["state"] = "disabled"

#part select all button
btn_select_all = tk.Button(bottom_right_btn_frame, text="Select Parts", command=pressed_select_all)
btn_select_all.grid(sticky='nsew')
btn_select_all["state"] = "disabled"



#def enable_remove(event):
    #btn_remove_part["state"] = "normal"

def pressed_remove():
    print(selection_screen.curselection())
    tuple = selection_screen.curselection()
    for selected_part in range(len(tuple)):   
        for part in range(len(selection_window.part_list)):
            try:
                if selection_window.part_list[part] == selection_screen.get(tuple[selected_part]):
                    del selection_window.part_list[part]
                    del selection_window.full_part_list[part]
                    write_console("Part Removed")
                    break
            except:
                write_console("No part selected")
                write_console("You must click on a part that is listed on the righthand side")
    update_selection_window()
    if (selection_window.part_list == []):
        delete_remove_part()
        return


def delete_remove_part():
    parse_button_off()
    btn_reset_select["state"] = "disabled"
    btn_remove_part["state"] = "disabled"

#text area for selectionn screen
selection_screen = tk.Listbox(selection_window,font=("helvetica",12),selectmode=tk.MULTIPLE)
selection_screen.grid(row=0,column=0, sticky="nswe")
# Create a Scrollbar widget
scrollbar = tk.Scrollbar(selection_window, orient=tk.VERTICAL)
scrollbar.config(command=selection_screen.yview)
scrollbar.grid(row=0, column=1, sticky="ns")



# Configure resizing behavior
selection_window.grid_rowconfigure(0, weight=1)
selection_window.grid_columnconfigure(0, weight=1)

            

btn_remove_part = tk.Button(selection_window, text="Remove Part", command=pressed_remove)
btn_remove_part.grid(row=1,column=0, sticky='ew')
btn_remove_part["state"] = "disabled"


# ####################################################################################
#                                  Console Functions
# ####################################################################################

console = tk.Text(console_frame, font=("Arial", 13), state="disabled")
console.grid(row=0,column=0, sticky="nswe")
console['height'] = 10

def write_console(text:string):
    console.configure(state='normal')
    console.insert("end", text)
    console.insert("end", "\n")
    console.configure(state='disabled')

def clear_console():
    console.configure(state='normal')
    console.delete('1.0' , END)
    console.configure(state='disabled')


# ####################################################################################
#                                      SI_DATA
# ####################################################################################
# if os.path.isdir("/mnt/nfs/si_data"):
#     window.datapath = "/mnt/nfs/si_data/"
# elif os.path.isdir("./../si_data"):
#     window.datapath = "./../si_data/"
# elif os.path.isdir("./../../si_data"):
#     window.datapath = "./../../si_data/"
# elif os.path.isdir("./si_data"):
#     window.datapath = "./si_data/"

# ####################################################################################
#                                   EVENT FUNCTIONS
# ####################################################################################
#used to remove items in rows greater than the given row
def remove_options(window, row):
    for label in window.grid_slaves():
        if int(label.grid_info()["row"]) > row:
            label.grid_forget()
            label["text"] = ""

def chip_supported():
    if chip_selected.get() == 'vili':
        return True
    return False

def change_option_size(label, combobox):
    # Adjust font for the dropdown menu of the combobox
    style = ttk.Style()
    style.configure('TCombobox', font=('helvetica', 12))
    combobox.config(font=('helvetica', 12))
    label.config(font=('helvetica', 12))



#Event function for when a chip option is selected
def pressed(event):
    #reset all values that were previously selected for rows below chip 
    test_selected.set("")
    lbw_selected.set("")
    part_no_selected.set("")
    temp_date_selected.set("")
    date_selected.set("")

    clear_console()



    #disable the select all button
    btn_select_all["state"] = "disabled"

    if (not chip_supported()):
        remove_options(window, 1)
        write_console("WARNING: This chip is NOT supported. Please select a different chip.")
        return

    #enter chip directory
    # item = chip_selected.get()
    # window.chip_path = item + '/'
    # new_dp = window.datapath + window.chip_path
    # #empty tests and add test directorys to test option select
    # window.tests = []
    # window.tests.append("")
    # for name in os.listdir(new_dp):
    #     if os.path.isdir(new_dp + name):
    #         window.tests.append(name)

    cur.execute("""
        SELECT DISTINCT "Test" FROM test JOIN chip ON test."Chip Id" = chip."Chip Id" WHERE chip."Chip Type" = %s
    """, (chip_selected.get(),))

    tests = cur.fetchall()
    window.tests = [test_type[0] for test_type in tests]
    window.tests.append("")
    
    #if there are no tests in chip directory
    if not window.tests:
        remove_options(window, 1)
        test_label = tk.Label(window,text="select tests")
        test_label.grid(row=2,column=0)
        test_label = tk.Label(window,text="main has no tests")
        test_label.grid(row=2,column=1)
        write_console("No test data can be found for that chip")
        return
    #label for test select
    test_label = tk.Label(window,text="select test")
    test_label.grid(row=2,column=0)

    test_combobox = AutocompleteCombobox(window, completevalues=window.tests, textvariable=test_selected)
    test_combobox.grid(row=2, column=1, sticky='ew')

    # Define a function to handle the Enter key press event
    def handle_enter(event):
        if event.keysym == "Return":
            pressed_test(test_combobox.get())
   
    # Bind events
    test_combobox.bind("<Return>", handle_enter)
    test_combobox.bind("<<ComboboxSelected>>", lambda event: pressed_test(test_combobox.get()))
    change_option_size(test_label, test_combobox)
    remove_options(window, 2)
    write_console("Supported Tests:\n write_shmoo\n read_shmoo\n read_shmoo_pat\n htol\n ims\n upump_char\n internal_bias\n ser\n read_disturb")
    
#Event function for when a test option is selected
def pressed_test(event):
    global window_inner_frame
    
    # Reset all values that were previously selected for rows below test 
    lbw_selected.set("")
    part_no_selected.set("")
    temp_date_selected.set("")
    temp_selected.set("")
    date_selected.set("")

    clear_console()
    btn_reset_select["state"] = "normal"

    # Enter test directory
    item = test_selected.get() or ""
    new_dp = window.datapath + chip_selected.get() + '/' + item + '/'
    print(new_dp)

    # Empty LBW (Lot/Bin/Wafer) and add LBW directories to LBW option select
    window.lbw = [""]
    
    # Fetch distinct LBWs from the database
    cur.execute(""" 
        SELECT DISTINCT 
            chip."Lot" || 
            CASE WHEN COALESCE(chip."Bin", '') <> '' THEN '_' || chip."Bin" ELSE '' END ||
            CASE WHEN COALESCE(chip."Wafer", '') <> '' THEN '_' || chip."Wafer" ELSE '' END ||
            CASE WHEN COALESCE(chip."Process Corner", '') <> '' THEN '_' || chip."Process Corner" ELSE '' END
        FROM Test
        JOIN Chip ON test."Chip Id" = chip."Chip Id"
        WHERE test."Test" = %s;
    """, (item,))
    lbw = cur.fetchall()
    for row in lbw:
        combined_info = row[0] if row[0] is not None else ""
        window.lbw.append(combined_info)
    window.lbw.append("")

    # Remove duplicates and sort the list
    window.lbw = list(set(window.lbw))  # Remove duplicates
    window.lbw.sort()  # Sort the list
    
    # If there are no LBWs available in the directory
    if not window.lbw:
        remove_options(window_inner_frame, 2)
        lbw_label = tk.Label(window_inner_frame, text="select LBW")
        lbw_label.grid(row=3, column=5)
        lbw_label = tk.Label(window_inner_frame, text="main has no LBW")
        lbw_label.grid(row=3, column=4)
        write_console("No Lots/Wafer/Bins that had that ran that test can be found")
        return

    # Creating a frame inside the 'window' frame
    window_inner_frame = tk.Frame(window)
    window_inner_frame.grid(row=3, column=0, columnspan=2, sticky='nsew')
    window_inner_frame.columnconfigure(1, minsize=50, weight=1)
    window_inner_frame.columnconfigure(3, minsize=50, weight=1)
    
    # LBW option select
    lbw_combobox = AutocompleteCombobox(window_inner_frame, completevalues=window.lbw, textvariable=lbw_selected)
    lbw_combobox.grid(row=0, column=1, sticky='we')
    
    # Bind events
    lbw_combobox.bind("<<ComboboxSelected>>", lambda event: update_filters(temp_combobox, dates_combobox, parts_combobox, lbw_combobox))

    # Label for LBW selection
    lbw_label = tk.Label(window_inner_frame, text="select LBW")
    lbw_label.grid(row=0, column=0)

    # Gather all dates for the selected test
    cur.execute(""" 
        SELECT DISTINCT "Date" FROM test WHERE "Test" = %s
    """, (test_selected.get(),))
    date = cur.fetchall()
    window.dates = [date_type[0] for date_type in date if date_type[0] is not None]
    window.dates.append("")

    # If there are no dates
    if not window.dates:
        remove_options(window_inner_frame, 2)
        dates_label = tk.Label(window_inner_frame, text="select dates")
        dates_label.grid(row=0, column=0)
        dates_label = tk.Label(window_inner_frame, text="main has no dates")
        dates_label.grid(row=0, column=1)
        write_console("There are no parts that were ran under a specific date")
        return

    # Date option select
    dates_combobox = AutocompleteCombobox(window_inner_frame, completevalues=window.dates, textvariable=date_selected)
    dates_combobox.grid(row=0, column=5, sticky='we')

    # Bind events
    dates_combobox.bind("<<ComboboxSelected>>", lambda event: update_filters(temp_combobox, dates_combobox, parts_combobox, lbw_combobox))

    dates_label = tk.Label(window_inner_frame, text="select date")
    dates_label.grid(row=0, column=4)
    remove_options(window_inner_frame, 3)

    # window.temp = []
    # window.temp.append("")
    # for lbw_name in os.listdir(new_dp):
    #     lbw_path = os.path.join(new_dp, lbw_name)
    #     if os.path.isdir(lbw_path):
    #         for part_name in os.listdir(lbw_path):
    #             part_path = os.path.join(lbw_path, part_name)
    #             if os.path.isdir(part_path):
    #                 for temp_date_name in os.listdir(part_path):
    #                     temp_date_path = os.path.join(part_path, temp_date_name)
    #                     if os.path.isdir(temp_date_path):
    #                         try:
    #                             temp_part = temp_date_name.split('_')[0]
    #                             window.temp.append(temp_part)
    #                             if temp_part[-1] != 'C' or not any(char.isdigit() for char in temp_part):
    #                                 raise ValueError(temp_part + "must contain numbers and end with 'C")
    #                         except (IndexError, ValueError) as e:
    #                             print(f"Warning: {e}")
    cur.execute("""
        SELECT DISTINCT "Temp" FROM test WHERE "Test" = %s
    """, (test_selected.get(),))
    temp = cur.fetchall()
    window.temp = [temp_type[0] for temp_type in temp if temp_type[0] is not None]
    window.temp.append("")


    # If there are no temp
    if not window.temp:
        remove_options(window_inner_frame, 2)
        temp_label = tk.Label(window_inner_frame, text="select temp")
        temp.grid(row=0, column=2)
        temp = tk.Label(window_inner_frame, text="main has no temp")
        temp.grid(row=0, column=3)
        write_console("There are no parts that were ran under a specific temperature")
        return

    # Remove duplicates from temp list
    # temp_options = list(OrderedDict.fromkeys(window.temp))

    # temp option select
    temp_combobox = AutocompleteCombobox(window_inner_frame, completevalues=window.temp,textvariable=temp_selected)
    temp_combobox.grid(row=0, column=3, sticky='we')
    # Bind events
    temp_combobox.bind("<<ComboboxSelected>>", lambda event: update_filters(temp_combobox, dates_combobox, parts_combobox,lbw_combobox))

    temp_label = tk.Label(window_inner_frame, text="select temp")
    temp_label.grid(row=0, column=2)
    remove_options(window_inner_frame, 3)

    btn_select_all["state"] = "normal"

    #reset all values that were previously selected for rows below LBW 
    part_no_selected.set("")
    temp_date_selected.set("")

    clear_console()


    #enable select all button
    btn_select_all["state"] = "normal"

    #empty Part list and add part number directorys to part number option select
    # window.parts = []
    # window.parts.append("")
    # for lbw_name in os.listdir(new_dp):
    #     lbw_path = os.path.join(new_dp, lbw_name)
    #     if os.path.isdir(lbw_path):
    #         for part_name in os.listdir(lbw_path):
    #             part_path = os.path.join(lbw_path, part_name)
    #             if os.path.isdir(part_path):
    #                 window.parts.append(part_name)

    cur.execute("""
    SELECT DISTINCT chip."Part Number" FROM Test JOIN Chip ON test."Chip Id" = chip."Chip Id" WHERE test."Test" = %s
    """, (test_selected.get(),))
    parts = cur.fetchall()
    window.parts = [part[0] for part in parts if part[0] is not None]
    window.parts.append("")
    
    #if no part numbers were found
    if not window.parts:
        remove_options(window, 3)
        parts_label = tk.Label(window,text="select parts")
        parts_label.grid(row=4,column=0)
        parts_label = tk.Label(window,text="main has no parts")
        parts_label.grid(row=4,column=1)
        write_console("There is no data on parts from that Lot/Wafer/Bin")
        return
    
    # part_options = list(OrderedDict.fromkeys(window.parts))

    #part option select
    parts_label = tk.Label(window,text="select part no.")
    parts_label.grid(row=4,column=0)
    parts_combobox = AutocompleteCombobox(window, completevalues=window.parts ,textvariable=part_no_selected)
    parts_combobox.grid(row=4, column=1, sticky='ew')

    # Bind events
    parts_combobox.bind("<<ComboboxSelected>>", lambda event: update_filters(temp_combobox, dates_combobox, parts_combobox,lbw_combobox))

    change_option_size(parts_label, parts_combobox)
    remove_options(window_inner_frame, 4)

    #reset all values that were previously selected for rows below Part number 
    temp_date_selected.set("")

    clear_console()


    #enable select all button
    btn_select_all["state"] = "normal"


#enables the parse data button when temp/date is selected
def pressed_temp_date(event):
    clear_console()
    if check_enable_selection():
        write_console("All of the necessary information has been gathered")
        write_console("")
        write_console("You can rename the file containing the parsed data")
        write_console("Press \"Select Part\" to add your part to the list of data to be parsed")
    
#function that actually runs the parser.
#called in pressed_parse_data
def parse_data():
    dp = (window.datapath + chip_selected.get() + '/' + test_selected.get() + '/' + lbw_selected.get() +
    '/' + part_no_selected.get() + '/' + temp_date_selected.get() + '/')

    save_name = file_name_entry.get() + ".csv"

    path = "./parsed_data/" + chip_selected.get() + '/' + test_selected.get() + '/'
    # Check if chip directory exists
    if not os.path.exists(path):
        new_path = os.path.join("./parsed_data/", chip_selected.get(), test_selected.get())
        os.makedirs(new_path)
        print("Directory created")
    
    parser.run_script(chip_selected.get(), test_selected.get(), window.datapath, selection_window.full_part_list, save_name, path)
    write_console("Done")
    write_console("Parsed data is located in Data_Parser\parsed_data")
    btn_parse_data["state"] = "normal"



    # if os.name == 'nt':
    path = './Excel_Parsers.xlsm'
    subprocess.Popen(f'explorer {os.path.realpath(path)}')

    

#the parse data button was pressed
def pressed_parse_data():
    btn_parse_data["state"] = "disabled"

    write_console("Running...")

    #essentially used to force asynchronicity 
    main_window.after(100, parse_data)

    
    
    

# ####################################################################################
#                            BUILDING WINDOWS AND WIDGETS
# ####################################################################################

# print(window.datapath)

#populate chip option select
# for name in os.listdir(window.datapath):
#     if os.path.isdir(window.datapath + name):
#         window.chips.append(name)
cur.execute("""
    SELECT DISTINCT "Chip Type" FROM chip
""", )

chips = cur.fetchall()
window.chips = [chip_type[0] for chip_type in chips]
window.chips.append("")
print(window.chips)

write_console("Data Parser Initiated")
write_console("start by selecting the chip")

#chip option select
chip_combobox = AutocompleteCombobox(window, completevalues = window.chips ,textvariable=chip_selected)
chip_combobox.grid(row=0, column=1, sticky='we')

def handle_enter(event):
    if event.keysym == "Return":
        pressed(chip_combobox.get())

# Bind events
chip_combobox.bind("<Return>", handle_enter)
chip_combobox.bind("<<ComboboxSelected>>", lambda event: pressed(chip_combobox.get()))        

chip_label = tk.Label(window,text="select chip")
chip_label.grid(row=0,column=0)
change_option_size(chip_label, chip_combobox)


#Parse data button
btn_parse_data = tk.Button(parent_btn_frame, text="Parse Data", command=pressed_parse_data)
#btn_parse_data.bind('<ButtonRelease-1>', pressed_parse_data)
btn_parse_data.grid(row=0,column=0, sticky='nsew')
btn_parse_data.config(width="20")
btn_parse_data["font"]= ("Arial", 13)
parse_button_off()
#LOOP
# Commit changes to database
conn.commit()

# Close cursor and connection

main_window.mainloop()