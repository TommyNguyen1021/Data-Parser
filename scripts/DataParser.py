import scripts.readShmooParser as read_shmoo
import scripts.writeShmooParser as write_shmoo
import scripts.htolParser as htol
import scripts.imsParser as ims
import scripts.upumpCharParser as upump_char
import scripts.internalBiasParser as internal_bias
import scripts.serParser as ser
import scripts.readDisturbParser as read_disturb
import scripts.partScreeningParser as part_screening
import scripts.measDeepSleepKeithleyParser as meas_deep_sleep_keithley
import scripts.measPowerLeakKeithleyParser as meas_power_leak_keithley
import scripts.measStandbyKeithleyParser as meas_standby_keithley
import scripts.measReadCurrParser as meas_read_curr
import scripts.measWriteCurrParser as meas_write_curr
import scripts.measDeepSleepCurrentParser as meas_deep_sleep
import scripts.measPowerLeakCurrentParser as meas_power_leak
import scripts.measStandbyCurrentParser as meas_standby


import os

def run_script(chip, test, datapath, part_list, save_name, save_path):
    print("running...")
    if not os.path.isdir("parsed_data"):
        os.mkdir("parsed_data")

    if os.path.exists("parsed_data/" + save_name):
        os.remove("parsed_data/" + save_name)

    # file = open("parsed_data/" + save_name, "w")
    # file.close()

    first = True
    # for path_to_part in part_list:
    for i in range(len(part_list)):
        path_to_part = part_list[i]
        print("Path to part: " + str(path_to_part))
        if test == "write_shmoo":
            print("HTOL")
            write_shmoo.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "read_shmoo" or test == "read_shmoo_pat":
            print("HTOL")
            read_shmoo.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "htol":
            print("HTOL")
            htol.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "ims":
            print("ims")
            ims.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "upump_char":
            print("upump_char")
            upump_char.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "internal_biases":
            print("internal_biases")
            internal_bias.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "ser":
            print("ser")
            ser.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "read_disturb":
            print("read_disturb")
            read_disturb.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "part_screening":
            print("part_screening")
            part_screening.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_deep_sleep_Keithley":
            print("meas_deep_sleep_Keithley")
            meas_deep_sleep_keithley.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_power_leak_Keithley":
            print("meas_power_leak_Keithley")
            meas_power_leak_keithley.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_standby_Keithley":
            print("meas_standby_Keithley")
            meas_standby_keithley.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_read_curr":
            print("meas_read_curr")
            meas_read_curr.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_write_curr":
            print("meas_write_curr")
            meas_write_curr.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_deep_sleep":
            print("meas_deep_sleep")
            meas_deep_sleep.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_power_leak":
            print("meas_power_leak")
            meas_power_leak.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_standby":
            print("meas_standby")
            meas_standby.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        first = False

    return