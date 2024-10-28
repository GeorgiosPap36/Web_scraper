import mysql.connector

def FetchFromTable(tableName, tableCellValue):
    query = f"SELECT id FROM {tableName} WHERE name = %s"
    cursor.execute(query, (tableCellValue,))
    fetched_result = cursor.fetchone()
    
    if fetched_result:
        fetched_id = fetched_result[0]
    else:
        insert_query = f"INSERT INTO {tableName} (name) VALUES (%s)"
        cursor.execute(insert_query, (tableCellValue,))
        fetched_id = cursor.lastrowid 
    return fetched_id

def DropTableIfExists(tableName):
    query = f"DROP TABLE IF EXISTS {tableName}"
    cursor.execute(query)

def CreateTableIfNotExists(tableName):
    query = f"""
    CREATE TABLE IF NOT EXISTS {tableName} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE
    );
    """
    cursor.execute(query)

db = mysql.connector.connect(
    host="localhost",
    user="foo",
    password="foo",
    database="Movies"
)

cursor = db.cursor()

DropTableIfExists("Movies")
DropTableIfExists("Directors")
DropTableIfExists("Genres")
DropTableIfExists("Countries")
DropTableIfExists("AgeRatings")

CreateTableIfNotExists("Directors")
CreateTableIfNotExists("Genres")
CreateTableIfNotExists("Countries")
CreateTableIfNotExists("AgeRatings")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    duration INT NOT NULL, 
    release_year YEAR NOT NULL,
    score FLOAT NOT NULL,
    director_id INT NOT NULL,
    genre_id INT NOT NULL, 
    country_id INT NOT NULL,
    age_rating_id INT NOT NULL,           
    FOREIGN KEY (director_id) REFERENCES Directors(id),
    FOREIGN KEY (genre_id) REFERENCES Genres(id),
    FOREIGN KEY (country_id) REFERENCES Countries(id),
    FOREIGN KEY (age_rating_id) REFERENCES AgeRatings(id)
);
""")

with open('MovieStats.txt', 'r') as file:
    for line in file:
        asd = line.strip().split("- ")
        movie_stats = line.strip().split("- ")
        name, duration, age_rating, score, budget, revenue, release_year, country, genre, genre_2 = movie_stats[0:10]
        staff_1, staff_2, staff_3, staff_4 = movie_stats[-4:]

        director_id = FetchFromTable("Directors", staff_1)
        genre_id = FetchFromTable("Genres", genre)
        country_id = FetchFromTable("Countries", country)
        age_rating_id = FetchFromTable("AgeRatings", age_rating)

        try:
            cursor.execute("""
                INSERT INTO Movies (name, duration, release_year, score, director_id, genre_id, country_id, age_rating_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, duration, release_year, score, director_id, genre_id, country_id, age_rating_id))
        except Exception as e:
            print(f"Error inserting data: {e}")
            break

db.commit()

cursor.close()
db.close()

print("Data insertion complete.")
