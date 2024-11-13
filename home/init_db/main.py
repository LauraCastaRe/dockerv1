import psycopg2

connection = psycopg2.connect(
    host="172.18.0.2", database="root", user="root", password="root"
)


cursor = connection.cursor()
cursor.execute("SELECT version()")
record = cursor.fetchone()

print(record)

