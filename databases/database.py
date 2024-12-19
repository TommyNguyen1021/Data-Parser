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
                            if lbw == 'P9NV42_0a_5_TT_WrongParameters':
                                continue
                            elif lbw == 'OPEN_SOCKET' or lbw == 'Test_1' or lbw == 'Write_Shmoo_Test' or lbw == 'Write_Shmoo_Test_new' or lbw == 'Write_Shmoo_Test_new2' or lbw == 'Write_Shmoo_Test_orig' or lbw == 'sif_sif_1':  
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
                if test == 'vili' or test == 'macros':
                    continue
                else:
                    test_path = os.path.join(chip_path, test)
                    if os.path.exists(test_path) and os.path.isdir(test_path):
                        for lbw in os.listdir(test_path):
                            lbw_path = os.path.join(test_path, lbw)
                            lbw_parts = lbw.split('_')
                            if lbw == 'P9NV42_0a_5_TT_WrongParameters':
                                continue
                            elif lbw == 'OPEN_SOCKET' or lbw == 'Test_1' or lbw == 'Write_Shmoo_Test' or lbw == 'Write_Shmoo_Test_new' or lbw == 'Write_Shmoo_Test_new2' or lbw == 'Write_Shmoo_Test_orig' or lbw == 'sif_sif_1':  
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
                           
# Commit changes to database
conn.commit()

# Close cursor and connection
cur.close()
conn.close()