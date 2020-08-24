import sqlite3
from django import db

conn = sqlite3.connect('common_station_pairings.sqlite')


def create_table(c):
    cursor = c.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS station_pairs (
            "origin"	TEXT,
            "destination"	TEXT,
            "freq"	INTEGER,
            PRIMARY KEY("origin","destination"));''')


def delete_table(c):
    cursor = c.cursor()
    cursor.execute('''DROP TABLE IF EXISTS station_pairs;''')


# The origin, destination pair is inserted in the database, or - if it has been recorded as a journey before - the freq
# is incremented
def increment_or_insert(origin, destination, c):
    cursor = c.cursor()
    SQLStatement = '''SELECT * FROM station_pairs WHERE origin = '{0}' AND destination = '{1}';'''.format(origin,
                                                                                                          destination)
    print("SQL Statement is : " + SQLStatement)
    selected_rows = len(cursor.execute(SQLStatement).fetchall())
    if selected_rows == 0:
        insert(origin, destination, c)
    else:
        cursor = c.cursor()
        update_stmt = '''UPDATE station_pairs SET freq = freq + 1 WHERE origin = '{0}' AND destination = '{1}';'''.format(
            origin, destination)
        print(update_stmt)
        cursor.execute(update_stmt)
        c.commit()


def insert(origin, destination, c):
    cursor = c.cursor()
    SQLStatement = '''INSERT INTO station_pairs (origin,destination,freq) 
                        VALUES ('{0}', '{1}', 1);'''.format(origin, destination)
    cursor.execute(SQLStatement)
    print(SQLStatement)
    c.commit()


def offer_top_destinations(origin, c):
    cursor = c.cursor()
    SQLStatement = '''SELECT destination FROM station_pairs WHERE origin = '{0}' ORDER BY freq DESC;'''.format(origin)
    top_destinations = []
    for row in cursor.execute(SQLStatement):
        top_destinations.append(row[0])
    return top_destinations


if __name__ == '__main__':
    # delete_table()
    # create_table()
    increment_or_insert('Norwich', 'Liverpool Street', conn)
    increment_or_insert('Norwich', 'Wymondham', conn)
    increment_or_insert('Norwich', 'Liverpool Street', conn)
    increment_or_insert('Norwich', 'Colchester', conn)
    print(offer_top_destinations('Norwich', conn)[0])
    # insert('f','e')
    conn.close()
