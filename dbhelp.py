import sqlite3
import statistics
from datetime import date

#Create table at beginning of proogram if it doesn't exist. Called from main.py right at the start
def table_check():

    sympdb = sqlite3.connect('symptom.db')
    sympcursor = sympdb.cursor()

    #First table only has one column, the primary key which is the symptom name   
    sympcursor.execute('''CREATE TABLE IF NOT EXISTS symptom (SymptomName TEXT (90) PRIMARY KEY)''')

    #Table 2 is a child table of the first table, and populates the symptom names with their info. Cascade delete means
    #if a symptom name in the first table is deleted, all its info in the second table is deleted too
    sympcursor.execute('''CREATE TABLE IF NOT EXISTS rating (RatingId INTEGER PRIMARY KEY,
    ratingnum INTEGER,
    note TEXT,
    date TEXT,
    SymptomName TEXT (90),
    CONSTRAINT fk_symptom
    FOREIGN KEY(SymptomName) REFERENCES symptom(SymptomName)
    ON DELETE CASCADE)''')

    sympdb.close()

#Populate tables with info
def insert_info(name, rating, notes):
    sympdb = sqlite3.connect('symptom.db')
    today = "on " + str(date.today())
    sympcursor = sympdb.cursor()
    params = (rating, notes, today, name)
    checkname = sympcursor.execute('SELECT * FROM symptom WHERE SymptomName = :name', {'name': name}).fetchone()

    #Only create a new symptom if it does not exist. If it does, only add to its info in the second table
    if checkname is None:
        sympcursor.execute('INSERT INTO symptom VALUES(?)', (name,))
        sympcursor.execute("INSERT INTO rating VALUES(null, ?, ?, ?, ?)", (params))
        sympdb.commit()
    else: 
        sympcursor.execute("INSERT INTO rating VALUES(null, ?, ?, ?, ?)", (params))
        sympdb.commit()
  
    sympdb.close()

#Gets all the info from both tables, joined by the symptom name
def get_info():
    sympdb = sqlite3.connect('symptom.db')
    sympcursor = sympdb.cursor()

    out = []

    for row in sympcursor.execute('''SELECT symptom.SymptomName, rating.ratingnum, rating.note, rating.date
    FROM symptom
    INNER JOIN rating
    ON symptom.SymptomName = rating.SymptomName''').fetchall():
        out.append(row)

    sympdb.close()
    return out
    
#Get all the symptom names
def ret_names():
    sympdb = sqlite3.connect('symptom.db')
    sympcursor = sympdb.cursor()

    names = sympcursor.execute("SELECT symptom.SymptomName FROM symptom").fetchall()
    sympdb.close()
    return names

#Delete a symptom. Because of cascade delete, will delete all info linked to the symptom name
def delete_record(name):
    sympdb = sqlite3.connect('symptom.db')
    sympcursor = sympdb.cursor()

    #Make sure the symptom being deleted exists in the table
    checkname = sympcursor.execute('SELECT * FROM symptom WHERE SymptomName = :name', {'name': name}).fetchone()
    if checkname is None:
        print('That symptom doesn\'t seem to exist')  
    else:
        sympcursor.execute('DELETE FROM symptom WHERE SymptomName = :name', {'name': name})
        sympdb.commit()
        print('All done!')
    sympdb.close()
   
#Logic to rate symptoms. Splits list into two halves. Used in overall_rating function
def means(meanlist):
    half = len(meanlist)//2
    return meanlist[half:], meanlist[:half]

def overall_rating(namelist):
    sympdb = sqlite3.connect('symptom.db')
    sympcursor = sympdb.cursor()
    list_of_ratings = []
    ratings = []
   
    for name in namelist:
        #Get all ratings associates with symptom name
        ratinglist = sympcursor.execute("SELECT rating.ratingnum FROM rating WHERE SymptomName = :name", {'name': name}).fetchall()
        for i in ratinglist:
            for n in i:
                list_of_ratings.append(n) 
        #Split the list of ratings into two halves              
        mean, meantwo = means(list_of_ratings)

        #check the averages of the two halves. If the second half has a greater average, the symptom is getting worse
        if statistics.mean(mean) < statistics.mean(meantwo):
            ratings.append(name + " is a bit worrisome, seems to be getting worse")
        else:
            ratings.append(name + " is doing OK right now")

    sympdb.close()
    return ratings