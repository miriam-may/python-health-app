from datetime import date
import dbhelp

def create_output():
    
    output = 'Output file for ' + str(date.today())
    outlist = dbhelp.get_info()
    

    for i in outlist:
        output += "\n" + str(i)
    return output
  
