import pyodbc

server = 'AZFRCER0300\DWK1' 
database = 'Wikilense' 
username = 'Wikilense' 
password = 'Qgx8NdQk5UKn49cKUVHgBfAd4nqeKZW6EbzkRjxS495ZDNhJw7'
dsn = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

#fonction pour exécuter les requêtes SQL
def query_db(query, args=(), one=False):
    cnxn = pyodbc.connect(dsn)
    cursor = cnxn.cursor()
    cursor.execute(query, args)
    
    #si la requête ne retourne pas de résultat (POST, PUT, DELETE)
    if cursor.description is None:
        cursor.commit()
        cursor.close()
        cnxn.close()
        return None
    #si la requête retourne un résultat (GET)
    else:
        columns = [column[0] for column in cursor.description]
        rv = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        cnxn.close()
        return (rv[0] if rv else None) if one else rv

def log (message):
    print("---------------------------------------")
    print(message)
    print("---------------------------------------")