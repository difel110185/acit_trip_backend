import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


# def insert_db(cursor, name: Str, description: Str, image_path: Str, country_id: Int):
#     pass

def get_countries_list(cursor):
    query = """SELECT * FROM countries"""
    cursor.execute(query)
    countries = cursor.fetchall()
    for row in countries:
        print("ID: =", row[0])
        print("Country name: =", row[1])


def getDbConnection():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='trippity',
                                             user='root',
                                             password='password')
        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to database {}".format(error))


def closeDbConnection(connection):
    try:
        connection.close()
    except mysql.connector.Error as error:
        print("Failed to close database connection {}".format(error))


if __name__ == "__main__":
    connection = getDbConnection()
    cursor = connection.cursor()
    get_countries_list(cursor)

    closeDbConnection(connection)
