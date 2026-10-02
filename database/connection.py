import os

import pyodbc
from dotenv import load_dotenv


load_dotenv()


DRIVER = os.getenv("DB_DRIVER")
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_DATABASE")


def get_connection():
    connection_string = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
    )

    return pyodbc.connect(connection_string)


if __name__ == "__main__":
    connection = get_connection()
    print("Connected to SQL Server successfully!")

    connection.close()