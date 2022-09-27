from datetime import date
import dbhelp

def create_output():
    #Create string to add to txt file
    output = 'Output file for ' + str(date.today())
    #logic for fecthing info from databse in dbhelp module
    outlist = dbhelp.get_info()
    
    #Add the info, broken into lines, to the output string
    for i in outlist:
        output += "\n" + str(i)
    return output
  
