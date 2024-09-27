import psycopg2
import re
import os

conn = psycopg2.connect(host="localhost", dbname="data",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()

# Create chip table
cur.execute("""
    CREATE TABLE IF NOT EXISTS Chip (
        "Chip Id" SERIAL PRIMARY KEY,
        "Chip Type" VARCHAR,
        "Lot" VARCHAR,
        "Bin" VARCHAR,
        "Wafer" Varchar, 
        "Part Number" VARCHAR,
        "Process Corner" VARCHAR

            )
    """)

dp = "//DS220P/ds220_vol1/si_data/"
chip_types = ["loki2", "odin", "status", "thor", "unsorted", "vili"]

# Inputs data for Chip table
for chip in chip_types:
    if chip =='vili':
        chip_path = os.path.join(dp, chip)
        if os.path.exists(chip_path) and os.path.isdir(chip_path):
            for test in os.listdir(chip_path):
                if test == 'vili' or test == 'macros':
                    continue
                else:
                    test_path = os.path.join(chip_path, test)
                    if os.path.exists(test_path) and os.path.isdir(test_path):
                        for lbw in os.listdir(test_path):
                            lbw_path = os.path.join(test_path, lbw)
                            lbw_parts = lbw.split('_')
                            if lbw == 'OPEN_SOCKET' or lbw == 'Test_1' or lbw == 'Write_Shmoo_Test' or lbw == 'Write_Shmoo_Test_new' or lbw == 'Write_Shmoo_Test_new2' or lbw == 'Write_Shmoo_Test_orig' or lbw == 'sif_sif_1':  
                                lot = lbw
                                bin = None
                                wafer = None
                                proc_corner = None
                            elif 'Wr_Shmoo_Test' in lbw or 'Package' in lbw:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) == 3:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) >= 4 and lbw.startswith('P9'):
                                lot = lbw_parts[0]
                                bin = lbw_parts[1]
                                wafer = lbw_parts[2]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) >= 4 and not lbw.startswith('P9'):
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'vili_main_v2' and len(lbw_parts) >= 3:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'write_shmoo' and len(lbw_parts) >= 4:
                                lot = lbw_parts[-4]
                                bin = lbw_parts[-3]
                                wafer = lbw_parts[-2]
                                proc_corner = lbw_parts[-1]
                            else:
                                if len(lbw_parts) >= 4:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = lbw_parts[2]
                                    proc_corner = lbw_parts[3]
                                elif len(lbw_parts) >= 3:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = lbw_parts[2]
                                    proc_corner = None
                                elif len(lbw_parts) >= 2:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = None
                                    proc_corner = None
                                else:
                                    lot = lbw
                                    bin = None
                                    wafer = None
                                    proc_corner = None
                        
                            if os.path.exists(lbw_path) and os.path.isdir(lbw_path):
                                for part_num in os.listdir(lbw_path):
                                    cur.execute("""
                                        INSERT INTO Chip ("Chip Type", "Lot", "Bin", "Wafer", "Part Number", "Process Corner")
                                        VALUES (%s, %s, %s, %s, %s, %s)
                                    """, (chip, lot, bin, wafer, part_num, proc_corner))
                                    conn.commit()


cur.execute("""
CREATE TABLE IF NOT EXISTS Test (
    "Test Id" SERIAL PRIMARY KEY,
    "Chip Id" INTEGER,
    FOREIGN KEY ("Chip Id") REFERENCES Chip ("Chip Id"),
    "Test" VARCHAR,
    "Date" VARCHAR,
    "Temp" VARCHAR
)
    """)

for chip in chip_types:
    if chip =='vili':
        chip_path = os.path.join(dp, chip)
        if os.path.exists(chip_path) and os.path.isdir(chip_path):
            for test in os.listdir(chip_path):
                if test == 'vili' or test == 'macros' or test == 'otp_save_test':
                    continue
                else:
                    test_path = os.path.join(chip_path, test)
                    if os.path.exists(test_path) and os.path.isdir(test_path):
                        for lbw in os.listdir(test_path):
                            lbw_path = os.path.join(test_path, lbw)
                            lbw_parts = lbw.split('_')
                            if lbw == 'OPEN_SOCKET' or lbw == 'Test_1' or lbw == 'Write_Shmoo_Test' or lbw == 'Write_Shmoo_Test_new' or lbw == 'Write_Shmoo_Test_new2' or lbw == 'Write_Shmoo_Test_orig' or lbw == 'sif_sif_1':  
                                lot = lbw
                                bin = None
                                wafer = None
                                proc_corner = None
                            elif 'Wr_Shmoo_Test' in lbw or 'Package' in lbw:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) == 3:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) >= 4 and lbw.startswith('P9'):
                                lot = lbw_parts[0]
                                bin = lbw_parts[1]
                                wafer = lbw_parts[2]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) >= 4 and not lbw.startswith('P9'):
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'vili_main_v2' and len(lbw_parts) >= 3:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'write_shmoo' and len(lbw_parts) >= 4:
                                lot = lbw_parts[-4]
                                bin = lbw_parts[-3]
                                wafer = lbw_parts[-2]
                                proc_corner = lbw_parts[-1]
                            else:
                                if len(lbw_parts) >= 4:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = lbw_parts[2]
                                    proc_corner = lbw_parts[3]
                                elif len(lbw_parts) >= 3:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = lbw_parts[2]
                                    proc_corner = None
                                elif len(lbw_parts) >= 2:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = None
                                    proc_corner = None
                                else:
                                    lot = lbw
                                    bin = None
                                    wafer = None
                                    proc_corner = None
                            if os.path.exists(lbw_path) and os.path.isdir(lbw_path):
                                for part_num in os.listdir(lbw_path):
                                    part_num_path = os.path.join(lbw_path, part_num)
                                    if test == 'otp':
                                        temp = None
                                        date = None
                                        for otp_data in os.listdir(part_num_path):
                                            query = """
                                                SELECT "Chip Id" FROM Chip
                                                WHERE "Chip Type" = %s
                                                AND ("Lot" = %s OR ("Lot" IS NULL AND %s IS NULL))
                                                AND ("Bin" = %s OR ("Bin" IS NULL AND %s IS NULL))
                                                AND ("Wafer" = %s OR ("Wafer" IS NULL AND %s IS NULL))
                                                AND ("Part Number" = %s OR ("Part Number" IS NULL AND %s IS NULL))
                                                AND ("Process Corner" = %s OR ("Process Corner" IS NULL AND %s IS NULL))
                                            """
                                            params = (chip, lot, lot, bin, bin, wafer, wafer, part_num, part_num, proc_corner, proc_corner)

                                            cur.execute(query, params)
                                            chip_id = cur.fetchone()
                                            cur.execute("""
                                                INSERT INTO Test ("Test", "Date", "Temp", "Chip Id")
                                                VALUES (%s, %s, %s, %s)
                                            """, (test, date, temp, chip_id))
                                            conn.commit()
                                    elif os.path.exists(part_num_path) and os.path.isdir(part_num_path):
                                        for temp_date in os.listdir(part_num_path):
                                            if temp_date == 'vili_otp_savejj2.mac':
                                                continue
                                            elif temp_date == 'week1':
                                                temp = None
                                                date = 'week1'
                                            else:
                                                first_part = temp_date
                                                parts = first_part.split("_")
                                                if len(parts) > 1:
                                                    temp = parts[0]
                                                    date = parts[1]
                                                elif 'reload' in temp or 'bin' in temp or 'dat' in temp:
                                                    temp = None
                                                    date = None

                                            query = """
                                                SELECT "Chip Id" FROM Chip
                                                WHERE "Chip Type" = %s
                                                AND ("Lot" = %s OR ("Lot" IS NULL AND %s IS NULL))
                                                AND ("Bin" = %s OR ("Bin" IS NULL AND %s IS NULL))
                                                AND ("Wafer" = %s OR ("Wafer" IS NULL AND %s IS NULL))
                                                AND ("Part Number" = %s OR ("Part Number" IS NULL AND %s IS NULL))
                                                AND ("Process Corner" = %s OR ("Process Corner" IS NULL AND %s IS NULL))
                                            """
                                            params = (chip, lot, lot, bin, bin, wafer, wafer, part_num, part_num, proc_corner, proc_corner)

                                            cur.execute(query, params)
                                            chip_id = cur.fetchone()
                                            cur.execute("""
                                                INSERT INTO Test ("Test", "Date", "Temp", "Chip Id")
                                                VALUES (%s, %s, %s, %s)
                                            """, (test, date, temp, chip_id))
                                            conn.commit()



cur.execute("""
CREATE TABLE IF NOT EXISTS Test_File (
    "File Id" SERIAL PRIMARY KEY,
    "Test Id" INTEGER,
    FOREIGN KEY ("Test Id") REFERENCES Test ("Test Id"),
    "Test Data" BYTEA,
    "Instance Num" VARCHAR
)
     """) 

# find instance number
pattern = r'i(\d+)'                   
           
for chip in chip_types:
    if chip =='vili':
        chip_path = os.path.join(dp, chip)
        if os.path.exists(chip_path) and os.path.isdir(chip_path):
            for test in os.listdir(chip_path):
                if test == 'vili' or test == 'macros' or test == 'otp_save_test':
                    continue
                else:
                    test_path = os.path.join(chip_path, test)
                    if os.path.exists(test_path) and os.path.isdir(test_path):
                        for lbw in os.listdir(test_path):
                            lbw_path = os.path.join(test_path, lbw)
                            lbw_parts = lbw.split('_')
                            if lbw == 'OPEN_SOCKET' or lbw == 'Test_1' or lbw == 'Write_Shmoo_Test' or lbw == 'Write_Shmoo_Test_new' or lbw == 'Write_Shmoo_Test_new2' or lbw == 'Write_Shmoo_Test_orig' or lbw == 'sif_sif_1':  
                                lot = lbw
                                bin = None
                                wafer = None
                                proc_corner = None
                            elif 'Wr_Shmoo_Test' in lbw or 'Package' in lbw:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) == 3:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) >= 4 and lbw.startswith('P9'):
                                lot = lbw_parts[0]
                                bin = lbw_parts[1]
                                wafer = lbw_parts[2]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) >= 4 and not lbw.startswith('P9'):
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'vili_main_v2' and len(lbw_parts) >= 3:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'write_shmoo' and len(lbw_parts) >= 4:
                                lot = lbw_parts[-4]
                                bin = lbw_parts[-3]
                                wafer = lbw_parts[-2]
                                proc_corner = lbw_parts[-1]
                            else:
                                if len(lbw_parts) >= 4:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = lbw_parts[2]
                                    proc_corner = lbw_parts[3]
                                elif len(lbw_parts) >= 3:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = lbw_parts[2]
                                    proc_corner = None
                                elif len(lbw_parts) >= 2:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = None
                                    proc_corner = None
                                else:
                                    lot = lbw
                                    bin = None
                                    wafer = None
                                    proc_corner = None
                            if os.path.exists(lbw_path) and os.path.isdir(lbw_path):
                                for part_num in os.listdir(lbw_path):
                                    part_num_path = os.path.join(lbw_path, part_num)
                                    if test == 'otp':
                                        temp = None
                                        date = None
                                        for otp_data in os.listdir(part_num_path):
                                            if '.dat' in otp_data:
                                                match = re.search(pattern, otp_data)
                                                test_data = os.path.join(part_num_path, otp_data)
                                                instance_num = match.group(1) if match else None

                                                # Check if the file exists before attempting to open it
                                                if os.path.exists(test_data):
                                                    # Open the file in binary mode and read its contents
                                                    with open(test_data, 'rb') as f:
                                                        file_content = f.read()
                                                        
                                                query_chip_id = """
                                                SELECT "Chip Id" FROM Chip
                                                WHERE "Chip Type" = %s
                                                AND ("Lot" = %s OR ("Lot" IS NULL AND %s IS NULL))
                                                AND ("Bin" = %s OR ("Bin" IS NULL AND %s IS NULL))
                                                AND ("Wafer" = %s OR ("Wafer" IS NULL AND %s IS NULL))
                                                AND ("Part Number" = %s OR ("Part Number" IS NULL AND %s IS NULL))
                                                AND ("Process Corner" = %s OR ("Process Corner" IS NULL AND %s IS NULL))
                                                """
                                                params_chip_id = (chip, lot, lot, bin, bin, wafer, wafer, part_num, part_num, proc_corner, proc_corner)
                                                
                                                cur.execute(query_chip_id, params_chip_id)
                                                chip_id = cur.fetchone()
                                                
                                                if chip_id:
                                                    chip_id = chip_id[0]
                                                    # Find the corresponding Test Id
                                                    query_test_id = """
                                                    SELECT "Test Id" FROM Test
                                                    WHERE "Chip Id" = %s
                                                    AND "Test" = %s
                                                    AND ("Date" = %s OR ("Date" IS NULL AND %s IS NULL))
                                                    AND ("Temp" = %s OR ("Temp" IS NULL AND %s IS NULL))
                                                    """
                                                    params_test_id = (chip_id, test, date, date, temp, temp)
                                                    
                                                    cur.execute(query_test_id, params_test_id)
                                                    test_id = cur.fetchone()
                                                    
                                                    if test_id:
                                                        test_id = test_id[0]
                                                        # Insert the test data into Test_File2
                                                        cur.execute("""
                                                        INSERT INTO Test_File ("Test Data", "Instance Num", "Test Id")
                                                        VALUES (%s, %s, %s)
                                                        """, (file_content, instance_num, test_id))
                                                        
                                                        # Commit the transaction
                                                        conn.commit()

                                    elif os.path.exists(part_num_path) and os.path.isdir(part_num_path):
                                        for temp_date in os.listdir(part_num_path):
                                            if temp_date == 'vili_otp_savejj2.mac':
                                                continue
                                            elif temp_date == 'week1':
                                                temp = None
                                                date = 'week1'
                                            else:
                                                first_part = temp_date
                                                parts = first_part.split("_")
                                                if len(parts) > 1:
                                                    temp = parts[0]
                                                    date = parts[1]
                                                elif 'reload' in temp or 'bin' in temp or 'dat' in temp:
                                                    temp = None
                                                    date = None
                                            data_path = os.path.join(part_num_path, temp_date)
                                            if os.path.exists(data_path) and os.path.isdir(data_path):
                                                for data in os.listdir(data_path):
                                                    if '.dat' in data:
                                                        match = re.search(pattern, data)
                                                        test_data = os.path.join(data_path, data)
                                                        instance_num = match.group(1) if match else None
                                                        
                                                        # Check if the file exists before attempting to open it
                                                        if os.path.exists(test_data):
                                                            # Open the file in binary mode and read its contents
                                                            with open(test_data, 'rb') as f:
                                                                file_content = f.read()
                                                            
                                                            # Find the corresponding Chip Id
                                                            query_chip_id = """
                                                            SELECT "Chip Id" FROM Chip
                                                            WHERE "Chip Type" = %s
                                                            AND ("Lot" = %s OR ("Lot" IS NULL AND %s IS NULL))
                                                            AND ("Bin" = %s OR ("Bin" IS NULL AND %s IS NULL))
                                                            AND ("Wafer" = %s OR ("Wafer" IS NULL AND %s IS NULL))
                                                            AND ("Part Number" = %s OR ("Part Number" IS NULL AND %s IS NULL))
                                                            AND ("Process Corner" = %s OR ("Process Corner" IS NULL AND %s IS NULL))
                                                            """
                                                            params_chip_id = (chip, lot, lot, bin, bin, wafer, wafer, part_num, part_num, proc_corner, proc_corner)
                                                            
                                                            cur.execute(query_chip_id, params_chip_id)
                                                            chip_id = cur.fetchone()
                                                            
                                                            if chip_id:
                                                                chip_id = chip_id[0]
                                                                # Find the corresponding Test Id
                                                                query_test_id = """
                                                                SELECT "Test Id" FROM Test
                                                                WHERE "Chip Id" = %s
                                                                AND "Test" = %s
                                                                AND ("Date" = %s OR ("Date" IS NULL AND %s IS NULL))
                                                                AND ("Temp" = %s OR ("Temp" IS NULL AND %s IS NULL))
                                                                """
                                                                params_test_id = (chip_id, test, date, date, temp, temp)
                                                                
                                                                cur.execute(query_test_id, params_test_id)
                                                                test_id = cur.fetchone()
                                                                
                                                                if test_id:
                                                                    test_id = test_id[0]
                                                                    # Insert the test data into Test_File2
                                                                    cur.execute("""
                                                                    INSERT INTO Test_File ("Test Data", "Instance Num", "Test Id")
                                                                    VALUES (%s, %s, %s)
                                                                    """, (file_content, instance_num, test_id))
                                                                    
                                                                    # Commit the transaction
                                                                    conn.commit()


                                                        



# Define the folder path and file name
# folder_path = "C://Users//Jean Shin//Documents/file_clone/"
# file_name = 'file.txt'



# # Construct the full file path
# file_clone_path = os.path.join(folder_path, file_name)
# # Retrieve bytea data
# cur.execute('SELECT "Test Data" FROM test_file WHERE "File ID" = %s', (273671,))
# test_data = cur.fetchone()[0]


# # Process the binary data (e.g., write to a file)
# with open(file_clone_path, 'wb') as file:
#     file.write(test_data)




cur.execute("""
CREATE TABLE IF NOT EXISTS Test_File2 (
    "File Id" SERIAL PRIMARY KEY,
    "Test Id" INTEGER,
    FOREIGN KEY ("Test Id") REFERENCES Test ("Test Id"),
    "Test Data" VARCHAR,
    "Instance Num" VARCHAR
)
     """) 

# find instance number
pattern = r'i(\d+)'                   
           
for chip in chip_types:
    if chip =='vili':
        chip_path = os.path.join(dp, chip)
        if os.path.exists(chip_path) and os.path.isdir(chip_path):
            for test in os.listdir(chip_path):
                if test == 'vili' or test == 'macros' or test == 'otp_save_test':
                    continue
                else:
                    test_path = os.path.join(chip_path, test)
                    if os.path.exists(test_path) and os.path.isdir(test_path):
                        for lbw in os.listdir(test_path):
                            lbw_path = os.path.join(test_path, lbw)
                            lbw_parts = lbw.split('_')
                            if lbw == 'OPEN_SOCKET' or lbw == 'Test_1' or lbw == 'Write_Shmoo_Test' or lbw == 'Write_Shmoo_Test_new' or lbw == 'Write_Shmoo_Test_new2' or lbw == 'Write_Shmoo_Test_orig' or lbw == 'sif_sif_1':  
                                lot = lbw
                                bin = None
                                wafer = None
                                proc_corner = None
                            elif 'Wr_Shmoo_Test' in lbw or 'Package' in lbw:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) == 3:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) >= 4 and lbw.startswith('P9'):
                                lot = lbw_parts[0]
                                bin = lbw_parts[1]
                                wafer = lbw_parts[2]
                                proc_corner = None
                            elif test == 'read_shmoo' and len(lbw_parts) >= 4 and not lbw.startswith('P9'):
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'vili_main_v2' and len(lbw_parts) >= 3:
                                lot = lbw_parts[-3]
                                bin = lbw_parts[-2]
                                wafer = lbw_parts[-1]
                                proc_corner = None
                            elif test == 'write_shmoo' and len(lbw_parts) >= 4:
                                lot = lbw_parts[-4]
                                bin = lbw_parts[-3]
                                wafer = lbw_parts[-2]
                                proc_corner = lbw_parts[-1]
                            else:
                                if len(lbw_parts) >= 4:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = lbw_parts[2]
                                    proc_corner = lbw_parts[3]
                                elif len(lbw_parts) >= 3:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = lbw_parts[2]
                                    proc_corner = None
                                elif len(lbw_parts) >= 2:
                                    lot = lbw_parts[0]
                                    bin = lbw_parts[1]
                                    wafer = None
                                    proc_corner = None
                                else:
                                    lot = lbw
                                    bin = None
                                    wafer = None
                                    proc_corner = None
                            if os.path.exists(lbw_path) and os.path.isdir(lbw_path):
                                for part_num in os.listdir(lbw_path):
                                    part_num_path = os.path.join(lbw_path, part_num)
                                    if test == 'otp':
                                        temp = None
                                        date = None
                                        for otp_data in os.listdir(part_num_path):
                                            if '.dat' in otp_data:
                                                match = re.search(pattern, otp_data)
                                                test_data = os.path.join(part_num_path, otp_data)
                                                instance_num = match.group(1) if match else None
                                                file_content = otp_data

                                                query_chip_id = """
                                                SELECT "Chip Id" FROM Chip
                                                WHERE "Chip Type" = %s
                                                AND ("Lot" = %s OR ("Lot" IS NULL AND %s IS NULL))
                                                AND ("Bin" = %s OR ("Bin" IS NULL AND %s IS NULL))
                                                AND ("Wafer" = %s OR ("Wafer" IS NULL AND %s IS NULL))
                                                AND ("Part Number" = %s OR ("Part Number" IS NULL AND %s IS NULL))
                                                AND ("Process Corner" = %s OR ("Process Corner" IS NULL AND %s IS NULL))
                                                """
                                                params_chip_id = (chip, lot, lot, bin, bin, wafer, wafer, part_num, part_num, proc_corner, proc_corner)
                                                
                                                cur.execute(query_chip_id, params_chip_id)
                                                chip_id = cur.fetchone()
                                                
                                                if chip_id:
                                                    chip_id = chip_id[0]
                                                    # Find the corresponding Test Id
                                                    query_test_id = """
                                                    SELECT "Test Id" FROM Test
                                                    WHERE "Chip Id" = %s
                                                    AND "Test" = %s
                                                    AND ("Date" = %s OR ("Date" IS NULL AND %s IS NULL))
                                                    AND ("Temp" = %s OR ("Temp" IS NULL AND %s IS NULL))
                                                    """
                                                    params_test_id = (chip_id, test, date, date, temp, temp)
                                                    
                                                    cur.execute(query_test_id, params_test_id)
                                                    test_id = cur.fetchone()
                                                    
                                                    if test_id:
                                                        test_id = test_id[0]
                                                        # Insert the test data into Test_File2
                                                        cur.execute("""
                                                        INSERT INTO Test_File2 ("Test Data", "Instance Num", "Test Id")
                                                        VALUES (%s, %s, %s)
                                                        """, (file_content, instance_num, test_id))
                                                        
                                                        # Commit the transaction
                                                        conn.commit()

                                    elif os.path.exists(part_num_path) and os.path.isdir(part_num_path):
                                        for temp_date in os.listdir(part_num_path):
                                            if temp_date == 'vili_otp_savejj2.mac':
                                                continue
                                            elif temp_date == 'week1':
                                                temp = None
                                                date = 'week1'
                                            else:
                                                first_part = temp_date
                                                parts = first_part.split("_")
                                                if len(parts) > 1:
                                                    temp = parts[0]
                                                    date = parts[1]
                                                elif 'reload' in temp or 'bin' in temp or 'dat' in temp:
                                                    temp = None
                                                    date = None
                                            data_path = os.path.join(part_num_path, temp_date)
                                            if os.path.exists(data_path) and os.path.isdir(data_path):
                                                for data in os.listdir(data_path):
                                                    if '.dat' in data:
                                                        match = re.search(pattern, data)
                                                        test_data = os.path.join(data_path, data)
                                                        instance_num = match.group(1) if match else None
                                                        file_content = data
                                                            
                                                        # Find the corresponding Chip Id
                                                        query_chip_id = """
                                                        SELECT "Chip Id" FROM Chip
                                                        WHERE "Chip Type" = %s
                                                        AND ("Lot" = %s OR ("Lot" IS NULL AND %s IS NULL))
                                                        AND ("Bin" = %s OR ("Bin" IS NULL AND %s IS NULL))
                                                        AND ("Wafer" = %s OR ("Wafer" IS NULL AND %s IS NULL))
                                                        AND ("Part Number" = %s OR ("Part Number" IS NULL AND %s IS NULL))
                                                        AND ("Process Corner" = %s OR ("Process Corner" IS NULL AND %s IS NULL))
                                                        """
                                                        params_chip_id = (chip, lot, lot, bin, bin, wafer, wafer, part_num, part_num, proc_corner, proc_corner)
                                                        
                                                        cur.execute(query_chip_id, params_chip_id)
                                                        chip_id = cur.fetchone()
                                                        
                                                        if chip_id:
                                                            chip_id = chip_id[0]
                                                            # Find the corresponding Test Id
                                                            query_test_id = """
                                                            SELECT "Test Id" FROM Test
                                                            WHERE "Chip Id" = %s
                                                            AND "Test" = %s
                                                            AND ("Date" = %s OR ("Date" IS NULL AND %s IS NULL))
                                                            AND ("Temp" = %s OR ("Temp" IS NULL AND %s IS NULL))
                                                            """
                                                            params_test_id = (chip_id, test, date, date, temp, temp)
                                                            
                                                            cur.execute(query_test_id, params_test_id)
                                                            test_id = cur.fetchone()
                                                            
                                                            if test_id:
                                                                test_id = test_id[0]
                                                                # Insert the test data into Test_File2
                                                                cur.execute("""
                                                                INSERT INTO Test_File2 ("Test Data", "Instance Num", "Test Id")
                                                                VALUES (%s, %s, %s)
                                                                """, (file_content, instance_num, test_id))
                                                                
                                                                # Commit the transaction
                                                                conn.commit()


# Define the folder path and file name
# folder_path = "C://Users//Jean Shin//Documents/files/"
# file_name = 'file.txt'



# # # Construct the full file path
# file_clone_path = os.path.join(folder_path, file_name)
# # Retrieve bytea data
# cur.execute('''
#     SELECT tf."Test Data", t."Test", tf."File Id"   
#     FROM Test_File tf
#     JOIN Test t ON tf."Test Id" = t."Test Id"
#     JOIN Chip c ON t."Chip Id" = c."Chip Id"
#     WHERE c."Chip Type" = %s AND t."Test" = %s
# ''', ('vili', 'ser'))
# files = cur.fetchall()

# # Process each file
# for file in files:
#     file_data, test_name, file_id = file  # Unpack based on your query results
    
#     # Generate a unique file name
#     file_name = f"{test_name}_{file_id}.txt"
#     file_path = os.path.join(folder_path, file_name)
    
#     # Write binary data to file
#     with open(file_path, 'wb') as file_handle:
#         file_handle.write(file_data)
                           

# Commit changes to database
conn.commit()

# Close cursor and connection
cur.close()
conn.close()