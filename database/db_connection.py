import pyodbc

server = 'host.docker.internal,1433'
database = 'FraudDetectionDB'
username = 'sa'
password = 'Mehtab@123'

conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    f'TrustServerCertificate=yes;'
)

print("Connected successfully!")