import mysql.connector
import sys


class DB_Connection:
    def __init__(self):
        self.connect_to_db()
        self.__result_set = None

    def connect_to_db(self):
        self.__conn_obj = mysql.connector.connect(
            user="root", host="localhost", database="emr"
        )
        self.__cursor = self.__conn_obj.cursor()

    def exec_sql(self, qry):
        self.__cursor.execute(qry)
        self.__result_set = self.__cursor.fetchall()
        self.__column_names = self.__cursor.description
        return self.__column_names, self.__result_set

    def close_connection(self):
        self.__cursor.close()
        self.__conn_obj.close()


if __name__ == "__main__":
    qry_lst = sys.argv[1:]
    qry = ";\n".join(qry_lst)
    connect_to_db(qry)
