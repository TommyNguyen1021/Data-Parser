import psycopg2
import re
import os
import hashlib

conn = psycopg2.connect(host="localhost", dbname="ims",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()

dp = "//DS220P/ds220_vol1/si_data/"
chip_types = ["loki2", "odin", "status", "thor", "unsorted", "vili"]

# Create cursor object
cur = conn.cursor()

dp = "//DS220P/ds220_vol1/si_data/"
chip_types = ["loki2", "odin", "status", "thor", "unsorted", "vili"]

# Create the Chip table
cur.execute("""
CREATE TABLE IF NOT EXISTS Chip (
    "Chip Id" SERIAL PRIMARY KEY,
    "Chip Type" VARCHAR,
    "Lot" VARCHAR,
    "Bin" VARCHAR,
    "Wafer" VARCHAR,
    "Part Number" VARCHAR,
    "Process Corner" VARCHAR,
    CONSTRAINT unique_chip UNIQUE (
        "Chip Type", 
        "Lot", 
        "Bin", 
        "Wafer", 
        "Part Number", 
        "Process Corner"
    )
);
""")


# Inputs data for Chip table
for chip in chip_types:
    if chip == 'vili':
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

                            # Separate parts in lbw to be put into columns in the chip table
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

                            # Insert the values into the chip table
                            if os.path.exists(lbw_path) and os.path.isdir(lbw_path):
                                for part_num in os.listdir(lbw_path):

                                    # Insert the chips and ensures unique rows are inserted
                                    cur.execute("""
                                        INSERT INTO Chip ("Chip Type", "Lot", "Bin", "Wafer", "Part Number", "Process Corner")
                                        VALUES (%s, %s, %s, %s, %s, %s)
                                        ON CONFLICT ("Chip Type", "Lot", "Bin", "Wafer", "Part Number", "Process Corner")
                                        DO NOTHING
                                    """, (chip, lot, bin if bin else '', wafer if wafer else '', part_num if part_num else '', proc_corner if proc_corner else ''))

# Create the Test table
cur.execute("""
CREATE TABLE IF NOT EXISTS Test (
    "Test Id" SERIAL PRIMARY KEY,
    "Chip Id" INTEGER,
    "Test" VARCHAR,
    "Date" VARCHAR,
    "Temp" VARCHAR,
    FOREIGN KEY ("Chip Id") REFERENCES Chip ("Chip Id"),
    CONSTRAINT unique_test UNIQUE ("Chip Id", "Test", "Date", "Temp")
);
""")


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
                            # Seperates parts in lbw to be put into columns in the chip table
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

                            # Insert the values into the test table
                            if os.path.exists(lbw_path) and os.path.isdir(lbw_path):
                                for part_num in os.listdir(lbw_path):
                                    part_num_path = os.path.join(lbw_path, part_num)
                                    if test == 'otp' or test == 'otp_save_test':
                                        temp = None
                                        date = None
                                        for otp_data in os.listdir(part_num_path):

                                            chip = chip.strip()
                                            lot = lot.strip() if lot else ''
                                            bin = bin.strip() if bin else ''
                                            wafer = wafer.strip() if wafer else ''
                                            part_num = part_num.strip() if part_num else ''
                                            proc_corner = proc_corner.strip() if proc_corner else ''

                                            # Checks for chip id that corresponds to the test
                                            query = """
                                                SELECT "Chip Id" FROM Chip
                                                WHERE "Chip Type" = %s
                                                AND "Lot" = %s 
                                                AND "Bin" = %s 
                                                AND "Wafer" = %s 
                                                AND "Part Number" = %s 
                                                AND "Process Corner" = %s 
                                            """
                                            params = (chip, lot, bin, wafer, part_num, proc_corner)

                                            cur.execute(query, params)
                                            chip_id = cur.fetchone()

                                            # Ensures unique rows are inserted
                                            cur.execute("""
                                                INSERT INTO Test ("Test", "Date", "Temp", "Chip Id")
                                                VALUES (%s, %s, %s, %s)
                                                ON CONFLICT ("Test", "Date", "Temp", "Chip Id")
                                                DO NOTHING
                                            """, (test, date if date else '', temp if temp else '', chip_id))
                                            conn.commit()
                                    elif os.path.exists(part_num_path) and os.path.isdir(part_num_path):
                                        for temp_date in os.listdir(part_num_path):
                                            # Seperates the temp and date to be put into columns in the test table
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

                                            chip = chip.strip()
                                            lot = lot.strip() if lot else ''
                                            bin = bin.strip() if bin else ''
                                            wafer = wafer.strip() if wafer else ''
                                            part_num = part_num.strip() if part_num else ''
                                            proc_corner = proc_corner.strip() if proc_corner else ''

                                            # Checks for chip id that corresponds to the test
                                            query = """
                                                SELECT "Chip Id" FROM Chip
                                                WHERE "Chip Type" = %s
                                                AND "Lot" = %s 
                                                AND "Bin" = %s 
                                                AND "Wafer" = %s 
                                                AND "Part Number" = %s 
                                                AND "Process Corner" = %s 
                                            """
                                            params = (chip, lot, bin, wafer, part_num, proc_corner)

                                            cur.execute(query, params)
                                            chip_id = cur.fetchone()
                                            # Insert the tests and ensures unique rows are inserted
                                            cur.execute("""
                                                INSERT INTO Test ("Test", "Date", "Temp", "Chip Id")
                                                VALUES (%s, %s, %s, %s)
                                                ON CONFLICT ("Test", "Date", "Temp", "Chip Id")
                                                DO NOTHING
                                            """, (test, date if date else '', temp if temp else '', chip_id))

# Create the Test_File table
#Hash is required because the some files are too large to be indexed in the unique_test_file constraint
cur.execute("""
CREATE TABLE IF NOT EXISTS Test_File (
    "File Id" SERIAL PRIMARY KEY,
    "Test Id" INTEGER,
    FOREIGN KEY ("Test Id") REFERENCES Test ("Test Id"),
    "Test Data" BYTEA,  -- This column will store the binary content of the file
    "File Name" VARCHAR,  -- This column will store the name of the file
    "Instance Num" VARCHAR,
    "Data Hash" VARCHAR(32),  -- This column will store the MD5 hash of the file content
    CONSTRAINT unique_test_file UNIQUE ("Data Hash", "Instance Num", "File Name", "Test Id")  -- Use Data Hash instead of Test Data
)
""")

# find instance number
pattern = r'i(\d+)'                   
           
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
                            # Seperates parts in lbw to be put into columns in the chip table
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
                                    if os.path.exists(part_num_path) and os.path.isdir(part_num_path):
                                        if test == 'ims':
                                            for temp_date in os.listdir(part_num_path):
                                                # Seperates the temp and date to be put into columns in the table
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
                                                            instance_num = match.group(1) if match else ''
                                                            file_name = data
                                                            
                                                            # Check if the file exists before attempting to open it
                                                            if os.path.isfile(test_data):
                                                                # Open the file in binary mode and read its contents
                                                                with open(test_data, 'rb') as f:
                                                                    file_content = f.read()

                                                                chip = chip.strip()
                                                                lot = lot.strip() if lot else ''
                                                                bin = bin.strip() if bin else ''
                                                                wafer = wafer.strip() if wafer else ''
                                                                part_num = part_num.strip() if part_num else ''
                                                                proc_corner = proc_corner.strip() if proc_corner else ''
                                                                
                                                                # Find the corresponding Chip Id
                                                                query_chip_id = """
                                                                SELECT "Chip Id" FROM Chip
                                                                WHERE "Chip Type" = %s
                                                                AND "Lot" = %s 
                                                                AND "Bin" = %s 
                                                                AND "Wafer" = %s 
                                                                AND "Part Number" = %s 
                                                                AND "Process Corner" = %s
                                                                """
                                                                params_chip_id = (chip, lot, bin, wafer, part_num, proc_corner)

                                                                
                                                                cur.execute(query_chip_id, params_chip_id)
                                                                chip_id = cur.fetchone()
                                                                
                                                                if chip_id:
                                                                    chip_id = chip_id[0]

                                                                    test = test.strip() if test else ''
                                                                    date = date.strip() if date else ''
                                                                    temp = temp.strip() if temp else ''

                                                                    # Find the corresponding Test Id
                                                                    query_test_id = """
                                                                    SELECT "Test Id" FROM Test
                                                                    WHERE "Chip Id" = %s
                                                                    AND "Test" = %s
                                                                    AND "Date" = %s 
                                                                    AND "Temp" = %s 
                                                                    """
                                                                    params_test_id = (chip_id, test, date, temp,)
                                                                    
                                                                    cur.execute(query_test_id, params_test_id)
                                                                    test_id = cur.fetchone()
                                                                    
                                                                    if test_id:
                                                                        test_id = test_id[0]
                                                                        # Compute the MD5 hash of the file content
                                                                        md5_hash = hashlib.md5(file_content).hexdigest()
                                                                        
                                                                        # Insert the file data and ensures unique rows are inserted
                                                                        cur.execute("""
                                                                        INSERT INTO Test_File ("Test Data", "File Name", "Instance Num", "Test Id", "Data Hash")
                                                                        VALUES (%s, %s, %s, %s, %s)
                                                                        ON CONFLICT ("Instance Num", "File Name", "Test Id", "Data Hash") DO NOTHING
                                                                        """, (file_content, file_name, instance_num, test_id, md5_hash))
                                                                        
                                                                        # Commit the transaction
                                                                        conn.commit()





# Commit once after all inserts are completed
conn.commit()

# Close cursor and connection
cur.close()
conn.close()