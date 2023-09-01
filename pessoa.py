import mysql.connector as db
import csv 

class Config:
    def __init__(self):
        self.config = {
            "mysql": {
                "user": "root",
                "password": "Isa29052003_Belly",
                "host": "127.0.0.1",
                "port": "3306",
                "database": "exercicio"
            }
        }

class Connection(Config):
    def __init__(self):
        super().__init__()
        try:
            self.conn = db.connect(**self.config["mysql"])
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Erro na conexão", e)
            exit(1)

    def __enter__(self):
        return self
   
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
    
class Pessoa(Connection):
    def __init__(self):
        super().__init__()

    def insert(self, *args):
        try:
            sql = "INSERT INTO pessoa (nome) VALUES (%s)"
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            print("Erro ao inserir", e)

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["nome"])
                print("Registro Inserido")
        except Exception as e:
            print("Erro ao inserir csv", e)
    
    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM pessoa WHERE id = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar"
            sql_d = f"DELETE FROM pessoa WHERE id = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)
    
    def update(self, id, *args):
        try:
            sql = f"UPDATE pessoa SET nome = %s WHERE id = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

if __name__ == "__main__":
    pessoa = Pessoa()
    #pessoa.insert("Maria")
    pessoa.insert_csv("data.csv")
    #pessoa.delete(2)
    #pessoa.update(1, "Maria Antônio")