import sqlite3
import statistics
from datetime import date

def table_check():

    sympdb = sqlite3.connect('symptom.db')
    sympcursor = sympdb.cursor()
       
    sympcursor.execute('''CREATE TABLE IF NOT EXISTS symptom (SymptomName TEXT (90) PRIMARY KEY)''')

    sympcursor.execute('''CREATE TABLE IF NOT EXISTS rating (RatingId INTEGER PRIMARY KEY,
    ratingnum INTEGER,
    note TEXT,
    date TEXT,
    SymptomName TEXT (90),
    CONSTRAINT fk_symptom
    FOREIGN KEY(SymptomName) REFERENCES symptom(SymptomName)
    ON DELETE CASCADE)''')

    sympdb.close()


def insert_info(name, rating, notes):
    sympdb = sqlite3.connect('symptom.db')
    today = "on " + str(date.today())
    sympcursor = sympdb.cursor()
    params = (rating, notes, today, name)
    checkname = sympcursor.execute('SELECT * FROM symptom WHERE SymptomName = :name', {'name': name}).fetchone()

    if checkname is None:
        sympcursor.execute('INSERT INTO symptom VALUES(?)', (name,))
        sympcursor.execute("INSERT INTO rating VALUES(null, ?, ?, ?, ?)", (params))
        sympdb.commit()
    else: 
        sympcursor.execute("INSERT INTO rating VALUES(null, ?, ?, ?, ?)", (params))
        sympdb.commit()
  
    sympdb.close()

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
    

def ret_names():
    sympdb = sqlite3.connect('symptom.db')
    sympcursor = sympdb.cursor()

    names = sympcursor.execute("SELECT symptom.SymptomName FROM symptom").fetchall()
    sympdb.close()
    return names

def delete_record(name):
    sympdb = sqlite3.connect('symptom.db')
    sympcursor = sympdb.cursor()
    checkname = sympcursor.execute('SELECT * FROM symptom WHERE SymptomName = :name', {'name': name}).fetchone()
    if checkname is None:
        print('That symptom doesn\'t seem to exist')  
    else:
        sympcursor.execute('DELETE FROM symptom WHERE SymptomName = :name', {'name': name})
        sympdb.commit()
        print('All done!')
    sympdb.close()
   

def means(meanlist):
    half = len(meanlist)//2
    return meanlist[half:], meanlist[:half]

def overall_rating(namelist):
    sympdb = sqlite3.connect('symptom.db')
    sympcursor = sympdb.cursor()
    list_of_ratings = []
    ratings = []
   
    for name in namelist:
        ratinglist = sympcursor.execute("SELECT rating.ratingnum FROM rating WHERE SymptomName = :name", {'name': name}).fetchall()
        for i in ratinglist:
            for n in i:
                list_of_ratings.append(n)       
        mean, meantwo = means(list_of_ratings)
        
        if mean > meantwo:
            ratings.append(name + " is a bit worrisome, seems to be getting worse")
        else:
            ratings.append(name + " is doing OK right now")

    sympdb.close()
    return ratings