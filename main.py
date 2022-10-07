import dbhelp
import output
import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QGridLayout, QWidget, QTextEdit
from PyQt6.QtGui import QIcon

#Check to see if the SQLite tables already exist - if not, create them. In dbhelp module.
dbhelp.table_check()

#The Gui version
def main():

    class windowOne(QMainWindow):
        def __init__(self):
            super(windowOne, self).__init__()

            #create window, add title and icon
            self.setWindowTitle('The ManageIt App!')
            self.setWindowIcon(QIcon("Icons/bug.png"))

            #Create layout and layout widget
            innerwin = QWidget()
            winlayout = QGridLayout()

            #Write explanatory information
            welcome = QLabel("Hi! The point of this little app is to give you some help managing your symptoms.\nYou can enter symptoms, how bad they are at the moment, and a little note on each one.\nIf you want, you can also create a .txt file to print out and show your doctor that has a brief history on it.\nFinally, you can get a hint as to whether your symptoms are worsening or not. You decide what to do with that information. ")
            welfont = welcome.font()
            welfont.setPointSize(12)
            welcome.setFont(welfont)
            welcome.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            
            #Label and textbox for symptom name
            entername = QLabel('Please enter a symptom name.')
            namefont = entername.font()
            namefont.setPointSize(10)
            entername.setFont(namefont)
            
            name = QLineEdit()
            name.setPlaceholderText('Symptom name...')
            
            #Label and textbox for rating. Textbox only accepts entries of numbers with 2 digits
            enterating = QLabel('Enter a rating for this symptom from 1-10. 10 is worst, 1 is feeling great')
            enterating.setFont(namefont)
            
            rating = QLineEdit()
            rating.setInputMask('00')

            #Label and textarea for notes
            enternotes = QLabel('Are there any notes you need to remember about this symptom from today/recently?')
            notefont = enternotes.font()
            notefont.setPointSize(10)
            enternotes.setFont(notefont)
            
            notes = QTextEdit()
            
            #Function and button to add symptom to database
            def submitSymptoms():
                dbhelp.insert_info(name.text(), int(rating.text()), notes.toPlainText())
                name.clear()
                rating.clear()
              
            submit = QPushButton("Submit")
            submit.clicked.connect(submitSymptoms)

            #Function and button to create output .txt file    
            def outputfile():
                final = output.create_output()
                f = open('output.txt', 'a')
                f.write('\n')
                f.write(final)
                f.close()
            
            outputone = QPushButton("Create .txt file")
            outputone.clicked.connect(outputfile)

            #Label and textbox for deleting a symptom
            deletename = QLabel("If you need to delete a symptom, enter its name here.")
            nametodelete = QLineEdit()
            deleteresult = QLabel()

            #Function and button to delete symptom
            def delsymptom():
                deleteresult.setText(dbhelp.delete_record(nametodelete.text()))
                nametodelete.clear()

            deletebutton = QPushButton("Delete")
            deletebutton.clicked.connect(delsymptom)
            
            #Label that will display list of symptom names in database
            allnames = QLabel()

            #function and button to display symptom names in database
            def show():
                n = dbhelp.ret_names()
                allnames.setText(str(n))
            
            display = QPushButton("Show all my symptoms")
            display.clicked.connect(show)

            #Separators, to make the gui easier on the eye    
            sepone = QLabel("_"*90)
            septwo = QLabel("_"*90)

            #Label, textbox for getting ratings
            getratlabel = QLabel("If you have built up a history of ratings, I can give you a general idea of how you're travelling.\nEnter symptoms, and hit 'Add'. When you're done, hit 'Get ratings'")
            ratlist = []
            ratlistnames = QLineEdit()

            #Function and button to add rating to list
            def addtolist():
                ratlist.append(ratlistnames.text())
                ratlistnames.clear()

            add = QPushButton("Add")
            add.clicked.connect(addtolist)

            #Function and button to get the ratings for symptoms in the list    
            def addall():
               showratings.setText(str(dbhelp.overall_rating(ratlist)))

            getratings = QPushButton("Get ratings")
            getratings.clicked.connect(addall)

            #Text that will display the rating info
            showratings = QLabel()
            showfont = showratings.font()
            showfont.bold()
            showfont.setPointSize(10)
            showratings.setFont(showfont)

            #Add all the bits to the layout
            winlayout.addWidget(welcome, 0, 0)
            winlayout.addWidget(entername, 1, 0)
            winlayout.addWidget(name, 1, 1)
            winlayout.addWidget(enterating, 2, 0)
            winlayout.addWidget(rating, 2, 1)
            winlayout.addWidget(enternotes, 3, 0)
            winlayout.addWidget(notes, 3, 1)
            winlayout.addWidget(submit, 4, 1)
            winlayout.addWidget(outputone, 5, 0)
            winlayout.addWidget(display, 5, 1)
            winlayout.addWidget(allnames, 6, 1)
            winlayout.addWidget(deletename, 7, 0)
            winlayout.addWidget(nametodelete, 7, 1)
            winlayout.addWidget(deleteresult, 8, 1)
            winlayout.addWidget(deletebutton, 8, 0)
            winlayout.addWidget(sepone, 9, 0)
            winlayout.addWidget(septwo, 10, 0)
            winlayout.addWidget(getratlabel, 11, 0)
            winlayout.addWidget(ratlistnames, 11, 1)
            winlayout.addWidget(add, 11, 2)
            winlayout.addWidget(getratings, 12, 0)
            winlayout.addWidget(showratings, 12, 1)
            innerwin.setLayout(winlayout)

            #Add the layout to the window
            self.setCentralWidget(innerwin)

            

    #Create the window, add styles, display the window and initiate the program loop              
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

#Run console version.
#console()

main()