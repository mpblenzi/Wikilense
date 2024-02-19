import pyodbc

server = 'AZFRCER0300\DWK1' 
database = 'Wikilense' 
username = 'Wikilense' 
password = 'Qgx8NdQk5UKn49cKUVHgBfAd4nqeKZW6EbzkRjxS495ZDNhJw7'
dsn = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def query_db(query, args=(), one=False):
    cnxn = pyodbc.connect(dsn)
    cursor = cnxn.cursor()
    cursor.execute(query, args)
    columns = [column[0] for column in cursor.description]
    rv = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    cnxn.close()
    return (rv[0] if rv else None) if one else rv
