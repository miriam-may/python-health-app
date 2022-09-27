import dbhelp
import output

#Unfortunately, PySimpleGui is proving diffucult to get up and running.
#I have therefore kept the console application part intact
import PySimpleGUI as psg

#Check to see if the SQLite tables already exist - if not, create them. In dbhelp module.
dbhelp.table_check()

#The PySimpleGui version
def main():

    #list for later use
    ratinglist = []
    psg.theme('Dark Green 2')

    #create layout with input fields
    layout = [ [psg.Button('Exit')], 
            [psg.Text('Hi and welcome to ManageIt!')],
            [psg.Text('The point of this app is to give you a little help managing your symptoms.')],
            [psg.Text('You can enter symptoms, how bad they are at the moment, and a little note on each one.')],
            [psg.Text('If you want, you can also create a text file to print out and show your doctor that has a brief history on it.')],
            [psg.Text('Finally, you can get a hint as to whether your symptoms are worsening or not. You decide what to do with that information.')],
            [psg.Text('Let\'s get on with it then!')],

            #populate tables in databse with today's symptom information
            [psg.Text('Enter a symptom name')],
            [psg.Input(key='ipsymptom')],
            [psg.Text('How bad is that symptom today out of 10? 1 is best, 10 is worst. If you don\'t enter a valid number, we\'ll assume 5')],
            [psg.Input(key='iprating')],
            [psg.Text('Finally, make any short notes you want to remember about how that symptom is today')],
            [psg.Input(key='ipnotes')],
            [psg.Button('Submit')],

            #Generate rating for symptomes - are they getting better or worse? Logic in dbhelp module
            [psg.Text('Would you like a general indication of how your symptoms are going? If so, enter up to 4 symptom here')],
            [psg.Input(key='one')],
            [psg.Input(key='two')],
            [psg.Input(key='three')],
            [psg.Input(key='four')],
            [psg.Button('Go!')],
            [psg.Multiline(key='allratings')],

            #Generate output txt file for treating health professional. Logic in output module
            [psg.Text('Click this button to create an output file for your doctor:')],
            [psg.Button('outputtxt')],

            #Show user what symptom information they have entered so far
            [psg.Text('(Here\'s what you\'ve entered so far:)')],
            [psg.Multiline(key='symplist')]           
    ]

    #create GUI window
    window = psg.Window('ManageIt App - Symptom Helper', layout)

    #Loop window
    while True:
        event, values = window.Read()

        #End loop and close window if user chooses to exit
        if event == psg.WIN_CLOSED or event == 'Exit':
            break

        #Populate tables with symptom info on click of correct button
        if event == 'Submit':
            ipsymptom = values['ipsymptom']
            iprating = values['iprating']

            #make sure rating is a valid number
            if iprating.isdigit():
                iprating = int(iprating)
            else:
                iprating = 5

            ipnotes = values['ipnotes']
            allnames = dbhelp.ret_names()
            window['symplist'].update(allnames)
            dbhelp.insert_info(ipsymptom, iprating, ipnotes)

        #generate output txt file on click of correct button    
        if event == 'outputtxt':
            final = output.create_output()
            f = open('output.txt', 'a')
            f.write('\n')
            f.write(final)
            f.close()

        #generate rating on click of correct button    
        if event == 'Go!':
            sympone = values['one']
            symptwo = values['two']
            sympthree = values['three']
            sympfour = values['four']
            if sympone:
                ratinglist.append(sympone)
            if symptwo:
                ratinglist.append(symptwo)
            if sympthree:
                ratinglist.append(sympthree)
            if sympfour:
                ratinglist.append(sympfour)

            ratlist = dbhelp.overall_rating(ratinglist)
            window['allratings'].update(str(ratlist))

    #close window once loop is broken out of
    window.close()

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
console()

#Run GUI version. (Having some difficulties with that right now, so I'll just comment it out)
#main()