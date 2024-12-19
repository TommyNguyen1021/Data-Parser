import FileParsers.binBregCheckFileParser as bin_breg_check
import FileParsers.dieIdFileParser as die_id
import FileParsers.engFuncFileParser as eng_func
import FileParsers.engFuncKeithleyFileParser as eng_func_Keithley
import FileParsers.htdrFileParser as htdr
import FileParsers.htolFileParser as htol
import FileParsers.imsFileParser as ims
import FileParsers.imsSearchFileParser as ims_search
import FileParsers.imsSearchWithSaoffsetFileParser as ims_search_with_saoffset
import FileParsers.internalBiasesFileParser as internal_biases
import FileParsers.ltdrFileParser as ltdr
import FileParsers.measDeepSleepFileParser as meas_deep_sleep
import FileParsers.measDeepSleepKeithleyFileParser as meas_deep_sleep_Keithley
import FileParsers.measPowerLeakFileParser as meas_power_leak
import FileParsers.measPowerLeakKeithleyFileParser as meas_power_leak_Keithley
import FileParsers.measReadCurrFileParser as meas_read_curr
import FileParsers.measStandbyFileParser as meas_standby
import FileParsers.measStandbyKeithleyFileParser as meas_standby_Keithley
import FileParsers.measWriteCurrFileParser as meas_write_curr
import FileParsers.otpFileParser as otp
import FileParsers.otpLoadTestFileParser as otp_load_test
import FileParsers.otpSaveTestFileParser as otp_save_test
import FileParsers.partScreeningFileParser as part_screening
import FileParsers.measVblVwlInstOscFileParser as meas_vbl_vwl_inst_osc
import FileParsers.printSaTrimFileParser as print_sa_trim
import FileParsers.readDisturbFileParser as read_disturb
import FileParsers.readShmooFileParser as read_shmoo
import FileParsers.readShmooPatFileParser as read_shmoo_pat
import FileParsers.serFileParser as ser
import FileParsers.upumpCharFileParser as upump_char
import FileParsers.viliMainV2FileParser as vili_main_v2
import FileParsers.viliMainV2OtpBkdnFileParser as vili_main_v2_otp_bkdn
import FileParsers.writeEnduranceFileParser as write_endurance
import FileParsers.writeShmooFileParser as write_shmoo

import os

def run_script(chip, test, datapath, part_list, save_name, save_path):
    print("running...")
    if not os.path.isdir("parsed_files"):
        os.mkdir("parsed_files")

    if os.path.exists("parsed_files/" + save_name):
        os.remove("parsed_files/" + save_name)

    # file = open("parsed_data/" + save_name, "w")
    # file.close()

    first = True
    # for path_to_part in part_list:
    for i in range(len(part_list)):
        path_to_part = part_list[i]
        print("Path to part: " + str(path_to_part))
        if test == "bin_breg_check":
            print("bin_breg_check")
            bin_breg_check.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "die_id":
            print("die_id")
            die_id.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "eng_func":
            print("eng_func")
            eng_func.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "eng_func_Keithley":
            print("eng_func_Keithley")
            eng_func_Keithley.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "htdr":
            print("htdr")
            htdr.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "htol":
            print("htol")
            htol.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "ims":
            print("ims")
            ims.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "ims_search":
            print("ims_search")
            ims_search.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "ims_search_with_saoffset":
            print("ims_search_with_saoffset")
            ims_search_with_saoffset.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "internal_biases":
            print("internal_biases")
            internal_biases.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "ltdr":
            print("ltdr")
            ltdr.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_deep_sleep":
            print("meas_deep_sleep")
            meas_deep_sleep.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_deep_sleep_Keithley":
            print("meas_deep_sleep_Keithley")
            meas_deep_sleep_Keithley.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_power_leak":
            print("meas_power_leak")
            meas_power_leak.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_power_leak_Keithley":
            print("meas_power_leak_Keithley")
            meas_power_leak_Keithley.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_read_curr":
            print("meas_read_curr")
            meas_read_curr.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_standby":
            print("meas_standby")
            meas_standby.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_standby_Keithley":
            print("meas_standby_Keithley")
            meas_standby_Keithley.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_vbl_vwl_inst_osc":
            print("meas_vbl_vwl_inst_osc")
            meas_vbl_vwl_inst_osc.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "meas_write_curr":
            print("meas_write_curr")
            meas_write_curr.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "otp":
            print("otp")
            otp.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "otp_load_test":
            print("otp_load_test")
            otp_load_test.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "otp_save_test":
            print("otp_save_test")
            otp_save_test.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "part_screening":
            print("part_screening")
            part_screening.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "print_sa_trim":
            print("print_sa_trim")
            print_sa_trim.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "read_disturb":
            print("read_disturb")
            read_disturb.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "read_shmoo":
            print("read_shmoo")
            read_shmoo.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "read_shmoo_pat":
            print("read_shmoo_pat")
            read_shmoo_pat.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "ser":
            print("ser")
            ser.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "upump_char":
            print("upump_char")
            upump_char.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "vili_main_v2":
            print("vili_main_v2")
            vili_main_v2.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "vili_main_v2_otp_bkdn":
            print("vili_main_v2_otp_bkdn")
            vili_main_v2_otp_bkdn.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "write_endurance":
            print("write_endurance")
            write_endurance.run_script(chip, datapath, path_to_part, save_name, save_path, i)
        if test == "write_shmoo":
            print("write_shmoo")
            write_shmoo.run_script(chip, datapath, path_to_part, save_name, save_path, i)


        first = False

    return