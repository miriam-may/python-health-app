import dbhelp
import output
import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QGridLayout, QWidget, QTextEdit

#Check to see if the SQLite tables already exist - if not, create them. In dbhelp module.
dbhelp.table_check()

#The Gui version
def main():

    class windowOne(QMainWindow):
        def __init__(self):
            super(windowOne, self).__init__()
            self.setWindowTitle('The ManageIt App!')
            innerwin = QWidget()
            winlayout = QGridLayout()

            welcome = QLabel("Hi! The point of this little app is to give you some help managing your symptoms.\nYou can enter symptoms, how bad they are at the moment, and a little note on each one.\nIf you want, you can also create a .txt file to print out and show your doctor that has a brief history on it.\nFinally, you can get a hint as to whether your symptoms are worsening or not. You decide what to do with that information. ")
            welfont = welcome.font()
            welfont.setPointSize(12)
            welcome.setFont(welfont)
            welcome.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            
            entername = QLabel('Please enter a symptom name.')
            namefont = entername.font()
            namefont.setPointSize(10)
            entername.setFont(namefont)
            
            name = QLineEdit()
            name.setPlaceholderText('Symptom name...')
            
            enterating = QLabel('Enter a rating for this symptom from 1-10. 1 is worst, 10 is feeling great')
            enterating.setFont(namefont)
            
            rating = QLineEdit()
            rating.setInputMask('00')

            enternotes = QLabel('Are there any notes you need to remember about this symptom from today/recently?')
            notefont = enternotes.font()
            notefont.setPointSize(10)
            enternotes.setFont(notefont)
            
            notestext = QTextEdit()
            notes = notestext.toPlainText()
            def submitSymptoms():
                dbhelp.insert_info(name.text(), int(rating.text()), notes)
            submit = QPushButton("Submit")
            submit.clicked.connect(submitSymptoms)

            def outputfile():
                final = output.create_output()
                f = open('output.txt', 'a')
                f.write('\n')
                f.write(final)
                f.close()

            outputone = QPushButton("Create .txt file")
            outputone.clicked.connect(outputfile)

            deletename = QLabel("If you need to delete a symptom, enter its name here.")
            nametodelete = QLineEdit()
            deleteresult = QLabel()

            def delsymptom():
                deleteresult.setText(dbhelp.delete_record(nametodelete.text()))

            deletebutton = QPushButton("Delete")
            deletebutton.clicked.connect(delsymptom)
            

            allnames = QLabel()

            def show():
                n = dbhelp.ret_names()
                allnames.setText(str(n))
            
            display = QPushButton("Show all my symptoms")
            display.clicked.connect(show)

            winlayout.addWidget(welcome, 0, 0)
            winlayout.addWidget(entername, 1, 0)
            winlayout.addWidget(name, 1, 1)
            winlayout.addWidget(enterating, 2, 0)
            winlayout.addWidget(rating, 2, 1)
            winlayout.addWidget(enternotes, 3, 0)
            winlayout.addWidget(notestext, 3, 1)
            winlayout.addWidget(submit, 4, 1)
            winlayout.addWidget(outputone, 5, 0)
            winlayout.addWidget(display, 5, 1)
            winlayout.addWidget(allnames, 6, 1)
            winlayout.addWidget(deletename, 7, 0)
            winlayout.addWidget(nametodelete, 7, 1)
            winlayout.addWidget(deleteresult, 8, 1)
            winlayout.addWidget(deletebutton, 8, 0)
            
            innerwin.setLayout(winlayout)
            self.setCentralWidget(innerwin)

            

                  
    ManageItApp = QApplication(sys.argv)
    winone = windowOne()
    with open("styles.css", "r") as file:
        ManageItApp.setStyleSheet(file.read())
    winone.show()
    ManageItApp.exec()

#The console app version
def console():
    print("*"*15)
    print("Hi and welcome to ManageIt!")
    print()
    print("The point of this app is to give you a little help managing your symptoms.")
    print("You can enter symptoms, how bad they are at the moment, and a little note on each one.")
    print("If you want, you can also create a text file to print out and show your doctor that has a brief history on it")
    print("Finally, you can get a hint as to whether your symptoms are worsening or not. You decide what to do with that information.")
    print()
    print("*"*15)
    print("Let's get on with it then!")
    print()

    cont = True
    number = True
    #Loop so that user can enter multiple symptoms
    while cont:
        rating = ""
        name = input('Enter a symptom name. \n')

        #Loop until user enters a valid number
        while number: 
            rating = input('How bad is that symptom today out of 10? 1 is best, 10 is worst. \n')

            #Check symptom is a valid number
            if rating.isdigit():
                rating = int(rating)
                number = False
            else:
                print("Please enter a positive, whole number only")
                number = True   
        notes = input('Finally, enter any notes you want to remember about this. If you can\'t think of any, just type \'pass\' \n')
    
        #Populate tables with symptom info
        dbhelp.insert_info(name, rating, notes)

        #Give user the option to enter more symptoms, or not
        tocont = input("Do you have any other symptoms to enter? y/n \n")
        tocont = tocont[0]
        tocont = tocont.lower()
        if tocont == 'y':
            cont = True
        else:
            cont = False

    print('\n' + '\n')

    out = input('Would you like to create an output file for your doctor? y/n \n')

    out = out[0]
    out = out.lower()

    if out == 'y':
        final = output.create_output()
        f = open('output.txt', 'a')
        f.write('\n')
        f.write(final)
        f.close()
    elif out == 'n':
        print("No worries - we'll give you the option to do so every time. \n")
    #If not y or n:
    else:
        print("Whoops - looks like a typo. Never mind, you'll have that option presented to you again next time. \n")

    lst = input("Would you like to see a list of all your symptoms? y/n \n")

    lst = lst[0]
    lst = lst.lower()

    #Show user a list of the symptoms in their database if prompted to
    if lst == 'y':
        names = dbhelp.ret_names()
        print(str(names))

    #Offer to delete redundant symptoms
    delete = input("Do you need to delete any symptoms? y/n \n")
    delete = delete[0]
    delete = delete.lower()
    exit = True
    if delete == 'y':
        #Loop so that user can delete more than one symptom if they desire
        while exit:
            sympname = input("Please type the name of the symptom to delete \n")
            dbhelp.delete_record(sympname)
            toexit = input("Do you have any other symptoms you need to delete? y/n \n")
            if toexit == 'y':
                exit = True
            else:
                exit = False

    #Offer to generate a rating of symptoms
    getrating = input("If you have built up a history of ratings, I can give you a general idea of how you're trevelling. Would that be useful right now?")
    getrating = getrating[0]
    getrating=getrating.lower()

    if getrating == 'y':
        ratlist = []
        finalrat = True
        #Loop for multiple entries
        while finalrat:
            rat = input("Please enter the name of one of your worst symptoms \n" )
            ratlist.append(rat)
            fratexit = input("Are any other of your symptoms bad right now? y/n \n")
            fratexit=fratexit[0]
            fratexit.lower()
            if fratexit == 'y':
                finalrat = True
            else:
                finalrat = False

        print("We're going to calculate how you're going now. Hold on.")
        print("_"*20)
        print(dbhelp.overall_rating(ratlist))

    else:
        print("Well, that's it from me for now. Cheery-bye!")

#Run console version. Should work.
#console()

#Run GUI version. (Having some difficulties with that right now, so I'll just comment it out for Repliters)
main()