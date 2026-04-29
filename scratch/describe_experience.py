import pymysql
import os
from dotenv import load_dotenv

load_dotenv(r"g:\Мой диск\Google AI Studio\AD ЕПВО\epvo_py\.env")

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

try:
    with conn.cursor() as cur:
        cur.execute("DESCRIBE accreditation_experience")
        print("Schema of accreditation_experience:")
        for row in cur.fetchall():
            print(row)
finally:
    conn.close()
