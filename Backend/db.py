import pyodbc

server = 'AZFRCER0300\DWK1' 
database = 'Wikilense' 
username = 'Wikilense' 
password = 'Qgx8NdQk5UKn49cKUVHgBfAd4nqeKZW6EbzkRjxS495ZDNhJw7' 
cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = cnxn.cursor()

def query_db(query, args=(), one=False):
    cursor.execute(query, args)
    rv = cursor.fetchall()
    return (rv[0] if rv else None) if one else rv
