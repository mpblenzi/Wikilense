import pyodbc

class DatabaseConnection:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn_str = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        self.conn = None
        self.cursor = None
        
    def connect(self):
        print(self.conn_str)
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.connect()
        self.cursor.execute(query)
        self.conn.commit()
        self.close()

    def close(self):
        self.cursor.close()
        self.conn.close()
        
    def insert_titre(self, titre):
        self.connect()
        self.cursor.execute("insert into [Wikilense].[dbo].[Article] values (?,36,3,'02-19-2024',0,0)", titre)
        self.conn.commit()
        self.close()

            
    def insert_partie(self, contenue, Postition, id_titre):
        self.connect()
        self.cursor.execute("insert into [Wikilense].[dbo].[Partie] values (?,?,?)",id_titre, contenue, Postition)
        self.conn.commit()
        self.close()

        
    def insert_Image(self, id_article, img_name, position):
        self.connect()
        self.cursor.execute("insert into [Wikilense].[dbo].[Image] values (?,?,?)",id_article, img_name, position)
        self.conn.commit()
        self.close()


    def get_id_article(self, titre):
        self.connect()
        self.cursor.execute("select ID from [Wikilense].[dbo].[Article] where Titre = ?", titre)
        return self.cursor.fetchone()[0]