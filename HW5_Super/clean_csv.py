'''
This file is for cleaning the data within hero-network.csv. Each value is found within quotations, but there are commas within them and its parsing wrong.
The commas found within the quotations will be replaced with a different char so that the values are parsed correctly. The quotations will also be removed.
'''

#The commas within quotations will be replaced by this character
REPLACE_CHAR = ";"


#Open the file to clean
fin = open("hero-network.csv", "r")
fout = open("clean_data.csv", "w")


#Used for determining beginning and end of " seperated value.
withinQuotation = False
cleanLine = ""
#Loop through all the characters and replace commas that are within quotations with some other char
for line in fin:
    cleanLine = ""
    for char in line:
        if(char == "\""):
            withinQuotation = not withinQuotation
        elif(withinQuotation and char==","):
            cleanLine += REPLACE_CHAR
        else:
            cleanLine += char

    #Write out the cleaned line to the clean_csv file.
    fout.write(cleanLine)


fin.close()
fout.close()