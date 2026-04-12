import pyodbc

server = 'MEHTAB_ANSARI\\MSSQL'   
database = 'FraudDetectionDB'

conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

cursor = conn.cursor()

print("Connected successfully!")