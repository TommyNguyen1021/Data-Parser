import psycopg2
import os

conn = psycopg2.connect(host="localhost", dbname="data",  user ="postgres", password = "numem@184", port = 5432)

# Create cursor object
cur = conn.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS chip2 (
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

for chip in chip_types:
    if chip =='vili':
        chip_path = os.path.join(dp, chip)
        if os.path.exists(chip_path) and os.path.isdir(chip_path):
            for test in os.listdir(chip_path):
                test_path = os.path.join(chip_path, test)
                if os.path.exists(test_path) and os.path.isdir(test_path):
                    for lbw in os.listdir(test_path):
                        lbw_path = os.path.join(test_path, lbw)
                        lbw_parts = lbw.split('_')
                        # Extracting bin, lot, and wafer if available
                        if len(lbw_parts) >= 4:
                            lot = lbw_parts[0]
                            bin = lbw_parts[1] 
                            wafer = lbw_parts[2]
                            proc_corner = lbw_parts[3]
                        else:
                            bin = lbw
                            lot = None
                            wafer = None
                        
                    # Check if lbw_path exists and is a directory
                    if os.path.exists(lbw_path) and os.path.isdir(lbw_path):
                        
                        # Iterate over each part number directory under lbw_path
                        for part_num in os.listdir(lbw_path):
                            cur.execute("""
                            INSERT INTO chip2 ("Chip Type", "Lot", "Bin", "Wafer", "Part Number", "Process Corner")
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """, (chip, bin, lot, wafer, part_num, proc_corner))
                            conn.commit()
# Execute SQL statement to create table


# Commit changes to database
conn.commit()

# Close cursor and connection
cur.close()
conn.close()
        # if not process_corners:
        #     cur.execute("""
        #         INSERT INTO chip2 ("Chip Type", "Process Corner")
        #         VALUES (%s, %s)
        #     """, (chip_type, None))
        #     conn.commit()
        # else:
        #     # Insert each process corner into PostgreSQL table
        #     for process_corner in process_corners:
        #         cur.execute("""
        #             INSERT INTO chip2 ("Chip Type", "Process Corner")
        #             VALUES (%s, %s)
        #         """, (chip_type, process_corner))