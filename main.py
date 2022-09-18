import dbhelp
import output

dbhelp.table_check()

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

while cont:

    name = input('Enter a symptom name. \n')
    rating = int(input('How bad is that symptom today out of 10? 1 is best, 10 is worst. \n'))
    notes = input('Finally, enter any notes you want to remember about this. If you can\'t think of any, just type \'pass\' \n')

    dbhelp.insert_info(name, rating, notes)

    tocont = input("Do you have any other symptoms to enter? y/n \n")
    if tocont == 'y':
        cont = True
    else:
        cont = False

print('\n' + '\n')

out = input('Would you like to create an output file for your doctor? y/n \n')
if out == 'y':
    final = output.create_output()
    f = open('output.txt', 'a')
    f.write('\n')
    f.write(final)
    f.close()
elif out == 'n':
    print("No worries - we'll give you the option to do so every time. \n")
else:
    print("Whoops - looks like a typo. Never mind, you'll have that option presented to you again. \n")

lst = input("Would you like to see a list of all your symptoms? y/n \n")

if lst == 'y':
    names = dbhelp.ret_names()
    print(str(names))

delete = input("Do you need to delete any symptoms? y/n \n")
exit = True
if delete == 'y':
    while exit:
        sympname = input("Please type the name of the symptom to delete \n")
        dbhelp.delete_record(sympname)
        toexit = input("Do you have any other symptoms you need to delete? y/n \n")
        if toexit == 'y':
            exit = True
        else:
            exit = False

ratlist = []
finalrat = True
while finalrat:
    rat = input("Please enter the name of one of your worst symptoms \n" )
    ratlist.append(rat)
    fratexit = input("Are any other of your symptoms bad right now? y/n \n")
    if fratexit == 'y':
        finalrat = True
    else:
        finalrat = False

print("We're going to calculate how you're going now. Hold on.")
print("_"*20)
print(dbhelp.overall_rating(ratlist))