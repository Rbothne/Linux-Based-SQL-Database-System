#Robert Bothne
#2/24/2022
#cs457.1001 - Dongfang Zhao
#Project 1 
#part 1 - base functionality, alter/parse/create/delete/use
#part 2 - additional functionality, delete from, insert into, select x & y, update 
#part 3 - additional functionality, inner join, left outer join
#part 4 - additional functionality, file locking for updates, done through seperate file and random num.

from re import I
from select import select
import sys
import os
from traceback import print_list
from uuid import uuid3
import random
parpat = os.getcwd() #current working directory set at start

def parsingInp(case,inp,select): #read user input given a case to find, input, and split to return as rest of string (note: returns tuple pass/fail + rest of string)
    inpMatch = inp.lower()
    location = inpMatch.find(case) #solve issue of upper/lower mismatch
    if location >= 0:#if found
        result = inp.split()[select] 
        oup=result.replace(" ", "")
        oups=oup.replace(";", "") 
        return 1, oups #tuple pass, remainder of string
    else:
        return 0, 'null' #tuple fail, null string

def createDatabase(inp): #if a directory does not exist, creates one
    if not os.path.exists(inp):
        os.makedirs(inp)
        print ("Database",inp," created.")
    else:
        print("!Failed to create database",inp, "because it already exists.")

def deleteDatabase(inp,parpat): #if a directory exists lower than original program directory, deletes it.
    path = os.path.join(parpat, inp)
    try:
        if os.path.isdir(path):
            if len(os.listdir(path)) == 0:
                os.rmdir(path)
            else:
                for f in os.listdir(path):
                    os.remove(os.path.join(inp, f))
            print ("Database",inp," deleted.")
        else:
            print("!Failed to delete",inp, "because it does not exist.")
    except:
        print("!Failed to delete",inp, "because it does not exist.")

def useDatabase(inp,parpat): #if a directory exists lower than original program directory, changes working directory.
    path = os.path.join(parpat, inp)
    if not os.path.isdir(path):
        print ("Database",inp," does not exist.")
    else:
        print("Using database",inp,".")
        os.chdir(path)
        
def createTable(tName,inp): #If a file does not exist, creates it with given parameters of form: create table tName (example,user,input);
    if os.path.exists(tName):
        print("!Failed to create table",tName, "because it already exists.")
    else:
        request = inp[12:] #remove "create table" 12 characters
        tData = request.replace(tName, "")
        tDatas=tData.replace(";", "")
        tLeft = tDatas.lstrip("(")
        tRight = tLeft[:-1]#remove )
        tMid = tRight.replace("(","",1)
        tWhole = tMid.split(",") #sort to a list
        with open(tName, 'w+') as f: #write to table what was in ()
            for item in tWhole:
                f.write("%s | " % item)
        print ("Table",tName," created.")

def deleteTable(inp): #If a file exists in current database, deletes it.
    if os.path.exists(inp):
        os.remove(inp)
        print ("Table",inp," deleted.")
    else:
        print("!Failed to delete",inp, "because it does not exist.")

def selectTable(inp): #If a file exists in current database, prints its contents to the prompt.
    parentPath = os.getcwd()
    path = os.path.join(parentPath, inp)
    if os.path.exists(inp):
        f = open(path, 'r')
        print('\n')
        print(f.read())
        f.close()
    else:
        print("!Failed to query table", inp, "because it does not exist.")

def alterTable(tName,inp): #If a file exists in current database, modifies table based on command
    if os.path.exists(tName):
        try:
            comd = inp.split()[3] #get 4th arg (command)
            domd = (inp.split()[4]) #get 5th arg (what to add/del)
            result = parsingInp("add",comd,0)#adding inputted string
            if result[0]==1:
                with open(tName, 'a') as f:
                    somd = (inp.split(comd)[1])
                    pomd = somd.replace(";", " |")
                    vomd = pomd.replace('\n', "")
                    f.write(vomd)
            result = parsingInp("delstring",comd,0)#deleting inputted string instances (dont think this is neccesary but I was having fun)
            if result[0]==1:
                with open(tName, 'r+') as f:
                    dels = f.readlines()
                    f.seek(0)
                    for line in dels:
                        if domd not in line:
                            f.write(line)
                    f.truncate()
                with open(tName, 'r+') as f: #removing empty lines,definitely not efficiently (dont think this is neccesary but I was having fun)
                    dels = f.readlines()
                    f.seek(0)
                    for line in dels:
                        if not line.isspace():
                            f.write(line)
            print("Table",tName,"modified.")
            return
        except:
            print("!Failed to alter table",tName,"due to improper command or modifiers")
            return 
    else:
        print("!Failed to alter table",tName,"because it does")

def insertTable(tName,inp): #If a file exists in current database, modifies table based on command
    if os.path.exists(tName):
        try:
            with open(tName, 'a') as f:
                lengths=18+len(tName)
                #print(lengths)
                request = inp[lengths:] #remove "insert into name values" characters
              #  print (request)
                tData = request.replace(tName, "")
                tDatas=tData.replace(";", "")
                tDatass=tDatas.replace("'", "").replace("(","").replace(")", "")
                #tDatasss=tDatass.replace(" ", "")
                tLeft = tDatass[2:]#remove two spaces and (
                #tRight = tLeft[:-1]#remove )
                tWhole = tLeft.split(",") #sort to a list
            
             #   print(tWhole)
                f.write('\n')
                for item in tWhole:
                    bitem=item.replace(" ","")
                    f.write("%s | " % bitem)
            print("1 new record inserted.")
            return
        except:
            print("!Failed to insert table",tName,"due to improper command or modifiers")
            return 
    else:
        print("!Failed to insert table",tName,"because it does")

def huTable(tName,inp,case): #helper to parse lines and return the proper row to search for a column
            
            result = parsingInp(case,inp,1)#column to check
            result2i = parsingInp(case,inp,3)# returns thing to be put in
            word=result2i[1].replace("'","")
            with open(tName,'r') as f:
                datums = f.read()
            datums.replace(" ","")
            lists = datums.split("|")
            sub = result[1]
            varsity =  next((s for s in lists if sub in s), None)
            splits = lists.index(varsity)
          #  print (splits) #columns to search in
            column = []
            with open(tName,'r') as f:
                for line in f:
                    column.append(line.split('|')[(splits)])#find the members of column
         #   print(word,column,splits)
            return (word,column,splits) #returns target word and column it should reside

def uTable(tName,uI,key,lock): #If a file exists in current database, updates table by setting value where search value is found by finding row/column and then changing the value
   #print(tName)
    if os.path.exists(tName):
        counter = 0   
        try:
            colSet= huTable(tName,uI,"set") #find value to set and column to set
            uI2 = input("--|")
            colWhere= huTable(tName,uI2,"where") #find value to change
            arrLines=[]
            with open(tName,'r') as f:
                for l in f:
                    arrLines.append(l) #read file line by line
            del colWhere[1][0] #remove first line (metadata)
            locationArr = []
            ranged = len(colWhere[1]) #ranged is amount of columns
            for i in range(ranged): # FIND THE ROW TO SHOW                           - finds the row locationArr
                test = colWhere[1][i].replace(" ","").replace(";","").replace("'","")
                if test == colWhere[0]: 
                    i+=1
                    locationArr.append(i) #append row # to list if found
            for i in range(len(locationArr)):
                listOfLines = arrLines[locationArr[i]].split("|")
                listOfLines[colSet[2]]=colSet[0] #set specific row and column to new value
                adds = ' | '.join(listOfLines) #rejoin the rows
                arrLines[locationArr[i]]=adds #put the line back in the list of all lines
                counter+=1
            inp = input("-->")
            result = parsingInp("commit",inp,0)
            if result[0] == 1: #check if comitting, should always be 1.
                with open(lock,'r') as f:
                    lines = f.read()
                if float(lines) == float(key): #if value stored in lock matches generated key, perform update
                    with open(tName, 'w+') as f: 
                        for item in arrLines:
                            f.write("%s" % item) #write lines back to file
                    print(counter,"record(s) were modified.")
                    os.remove(lock) #delete lock after modification
                    return
                elif float(lines) != float(key): #if value stored in lock does not match key, abort transaction as file is in use.
                    print("Error: Table", tName, "is locked!")
                    print("Transaction abort.")
        except:
            print("!Failed to update table",tName,"due to improper command or modifiers")
            return 
    else:
        print("!Failed to update table",tName,"because it does not exist")

def dfTable(tName,uI): #If a file exists in current database, modifies table based on command by finding specified row and changing it to null before resliding it into the array
    if os.path.exists(tName):
        try:
            counter = 0 #deletions made
            locationArr = [] 
            uI2 = input("--|")
            cEqual = parsingInp("=",uI2,2) 
            colWhere= huTable(tName,uI2,"where") #finding list of values and value to search
            arrLines=[]
            with open(tName,'r') as f:
                for l in f:
                    arrLines.append(l) #read file as lines into array
            del colWhere[1][0]
            cLess = parsingInp("<",uI2,2)             
            if cLess[0] == 1:               #if values are less than, delete row
                ranged = len(colWhere[1]) # number of rows to iterate
                for i in range(ranged):
                    test = colWhere[1][i].replace(" ","") 
                    if float(test) < float(colWhere[0]):  #test case vs our passed value
                        i+=1
                        locationArr.append(i)
                for i in range(len(locationArr)): 
                    lToDel = locationArr[i] #deciding which line to delete 
                    arrLines[lToDel]="" #deleting line
                    counter+=1
                with open(tName, 'w+') as f: 
                    for item in arrLines:
                        f.write("%s" % item) #writing back nondeleted lines
            cGreater = parsingInp(">",uI2,2)            
            if cGreater[0] == 1:               #if values are greater than, delete row
                ranged = len(colWhere[1])
                for i in range(ranged):
                    test = colWhere[1][i].replace(" ","")
                    if float(test) > float(colWhere[0]): 
                        i+=1
                      #  print(float(test),"versus", float(colWhere[0]))
                        locationArr.append(i)
                for i in range(len(locationArr)):
                    lToDel = locationArr[i]
                    arrLines[lToDel]=""
                    counter+=1
                with open(tName, 'w+') as f: 
                    for item in arrLines:
                        f.write("%s" % item)
            cNotE = parsingInp("!=",uI2,2)     #if values are not equal, delete row      
            if cNotE[0] == 1:
                ranged = len(colWhere[1])
                for i in range(ranged):
                    test = colWhere[1][i].replace(" ","")
                    if test != colWhere[0]: 
                        i+=1
                        locationArr.append(i)
                for i in range(len(locationArr)):
                    lToDel = locationArr[i]
                    arrLines[lToDel]=""
                    counter+=1
                #print(arrLines)
                with open(tName, 'w+') as f: 
                    for item in arrLines:
                        #print(item)
                        f.write("%s" % item)
            elif cEqual[0] == 1: #if values are equal, delete row
                ranged = len(colWhere[1])
                for i in range(ranged):
                    test = colWhere[1][i].replace(" ","")
                    if test == colWhere[0]: 
                        i+=1
                        locationArr.append(i)
                for i in range(len(locationArr)):
                    lToDel = locationArr[i]
                    arrLines[lToDel]=""
                    counter+=1
               # print(arrLines)
                with open(tName, 'w+') as f: 
                    for item in arrLines:
                       # print(item)
                        f.write("%s" % item)
            print(counter,"record(s) were deleted.")
            return
        except:
            print("failed to delete records due to improper command or modifiers")
           # print("!Failed to Delete Records in ",tName,"due to improper command or modifiers")
            return 
    else:
        print("!Failed to Delete Records in",tName,"because it does not exist")

def sFTable(uI): #If a file exists in current database, finds columns to display, then finds correct row to pull data from and prints to cmd.
    try:
   #######################################################PA3
        #print ("sel from T")
        joinType =0 #KEEP TRACK OF IF ITS AN OUTER JOIN
        lengths=7
        request = uI[lengths:] #remove "insert into name values" characters
        tDatas=request.replace(";", "")
        tDatass=tDatas.replace("'", "")
        tDatasss=tDatass.replace(" ", "")
        cDisplay = tDatasss.split(",") #sort to a list of equest cols to be displayed
        if (cDisplay[0]=="*" and len(cDisplay)==1):
            uI2 = input("--|")#take input for two tables IE: from Employee E, Sales S 
            uI2 = uI2[5:] #remove "from "
            result = parsingInp("left outer join",uI2,1) #if an outer join, mark it so
            if result[0] ==1:
                joinType =1
            if uI2.find(",") != -1 or uI2.find("inner join") !=-1 or uI2.find("left outer join") !=-1: #if a valid command
                if uI2.find("inner join"):
                    uI2 = uI2.replace("inner join",",") #convert to simple format
                if uI2.find("left outer join"):
                    uI2 = uI2.replace("left outer join",",") #convert to simple format
                tableInfos = uI2.split(",") #put into two tuples containing symbol and name
                table1 = tableInfos[0].split(" ")
                table2 = tableInfos[1].split(" ") #get table name and symbol into tuple
                if (os.path.exists(table1[0]) and os.path.exists(table2[1])):
                    t1 = [] #stores table 1 info
                    t2 = [] #stores table 2 info
                    newTable = [] #stores joined table info                 
                    uI3 = input("--|") #reads inputs : where E.id = S.employeeID; or on E.id = S.employeeID;
                    uI3= uI3.replace(";","")
                    uI3=uI3.replace(table1[1],"")
                    uI3=uI3.replace(table2[2],"")
                    uI3=uI3.replace(".","") #replacing  to clean string: where id = employeeID
                    
                    cleanUI3 = uI3.replace("inner join", "").replace("left outer join", "")
                    userWords = cleanUI3.replace(",","").split() #splitting to [where,id,=,employeeId]
                    with open (table1[0],'r') as f:
                        for line in f:
                            t1.append(line) 
                    with open (table2[1],'r') as fx:
                        for line in fx:
                            t2.append(line) 
                    table1C =  next((s for s in t1[0].split("|") if userWords[1] in s), None)    #find substring in each i in table
                    table2C =  next((s for s in t2[0].split("|") if userWords[3] in s), None)
                    table1Col = t1[0].split("|").index(table1C) #split header into columns, find where substring resides
                    table2Col = t2[0].split("|").index(table2C)
                    t1[0] = t1[0].rstrip('\n') #remove new lines in header
                    t2[0] = t2[0].rstrip('\n')
                    newTable.append(f"{t1[0]} | {t2[0]}") #add header
                    for t1i in range(1, len(t1)): #for every entry in table 1
                        t1[t1i] = t1[t1i].rstrip("\n")
                        for t2i in range(1, len(t2)): #compare to every entry in table 2
                            t2[t2i] = t2[t2i].rstrip('\n')
                            if (userWords[2] == "="): #if checking equal values
                                if (type(t2[t2i].split("|")[table2Col]) is str): #if the value of col # in t2i is string...
                                   # print(t2[t2i].split("|"),t1[t1i].split("|"))
                                    if (t2[t2i].split("|")[table2Col] == t1[t1i].split("|")[table1Col]): #and the equal to the value of col # in table 1...
                                        newTable.append(f'{t1[t1i]} | {t2[t2i]}') #append to joined table
                                else: #repeat for floats
                                    if (float(t2[t2i].split("|")[table2Col]) == float(t1[t1i].split("|")[table1Col])):
                                        newTable.append(f'{t1[t1i]} | {t2[t2i]}')
                            elif (userWords[2] == ">"): #Greater than
                                if (t2[t2i].split("|")[table2Col] > t1[t1i].split("|")[table1Col]):
                                    newTable.append(f'{t1[t1i]} | {t2[t2i]}')
                            elif (userWords[2] == "<"): #Less than
                                if (t2[t2i].split("|")[table2Col] < t1[t1i].split("|")[table1Col]):
                                    newTable.append(f'{t1[t1i]} | {t2[t2i]}')
                            elif (userWords[2] == "!="): #Not equal
                                if (t2[t2i].split("|")[table2Col] != t1[t1i].split("|")[table1Col]):
                                    newTable.append(f'{t1[t1i]} | {t2[t2i]}')
                              
                        if (joinType == 1): 
                            if (t1[t1i].split("|")[table1Col] not in newTable[-1].split("|")[table1Col]):
                                newTable.append(f"{t1[t1i]} | |") 
                    for iTable in newTable: #print all values of the joined table
                        print(iTable)

#####################################################################################
        else:
            uI2 = input("--|") #file name
            result = parsingInp("from",uI2,1)  #finding table name
            if result[0]==1: #
                tName = result[1].replace(" ","")
                if os.path.exists(tName):
                    try:
                        uI3 = input("--|") #getting operator and location
                        cEqual = parsingInp("=",uI3,2) 
                        colWhere= huTable(tName,uI3,"where")
                        print(colWhere)
                        colList =[]
                        for i in range(len(cDisplay)):  #FIND THE COLUMNS TO SHOW                 - finds the columns colList
                            word=cDisplay[i].replace("'","")
                            with open(tName,'r') as f:
                                datums = f.read() #read file data 
                            datums.replace(" ","")
                            lists = datums.split("|") #spliting by column
                            varsity =  next((s for s in lists if word in s), None)
                            splits = lists.index(varsity) #if a case is found mark the column
                            column = []
                            with open(tName,'r') as f:
                                for line in f:
                                    column.append(line.split('|')[(splits)]) 
                                    arrLines=[]
                                    with open(tName,'r') as f:
                                        for l in f:
                                            # print(l)
                                            arrLines.append(l)
                            colList.append(splits) #list of columns that need to be shown
                        del colWhere[1][0]
                        locationArr=[]
                        cGreater = parsingInp(">",uI3,2)
                        if cGreater[0] == 1: #if values are equal, delete row
                            ranged = len(colWhere[1]) #ranged is amount of columns
                            for i in range(ranged): # FIND THE ROW TO SHOW                           - finds the row locationArr
                                test = colWhere[1][i].replace(" ","")
                                if float(test) > float(colWhere[0]): 
                                    i+=1
                                    # print(float(test),"versus", float(colWhere[0]))
                                    locationArr.append(i)
                            for i in range(len(locationArr)):
                                lToShow = locationArr[i] 
                                listOfLines = arrLines[lToShow].split("|")   # row to modify
                                for x in range(len(colList)):
                                    print(listOfLines[colList[x]],end="")
                                    print("| ",end="")
                                print("") 
                            return      
                        cNotE = parsingInp("!=",uI3,2)
                        if cNotE[0] == 1: #if values are equal, delete row
                            ranged = len(colWhere[1]) #ranged is amount of columns
                            for i in range(ranged): # FIND THE ROW TO SHOW                           - finds the row locationArr
                                test = colWhere[1][i].replace(" ","")
                                if test != colWhere[0]: 
                                    #  print(test,"is compared to ",colWhere[0])
                                    i+=1
                                    locationArr.append(i)
                            # print(locationArr)
                            for i in range(len(locationArr)):#PRINT THE ROW AND COLUMN COMBO
                                lToShow = locationArr[i] 
                                listOfLines = arrLines[lToShow].split("|")   # row to modify
                                #  print(listOfLines)
                                for x in range(len(colList)):
                                    print(listOfLines[colList[x]],end="")
                                    print("| ",end="")
                                print("")
                                #  print("dsadasdas") 
                            return      
                        elif cEqual[0] == 1: #if values are equal, delete row
                            ranged = len(colWhere[1]) #ranged is amount of columns
                            for i in range(ranged): # FIND THE ROW TO SHOW                           - finds the row locationArr
                                test = colWhere[1][i].replace(" ","")
                                if test == colWhere[0]: 
                                    # print(test,"is compared to ",colWhere[0])
                                    i+=1
                                    locationArr.append(i)
                            for i in range(len(locationArr)):#PRINT THE ROW AND COLUMN COMBO
                                lToShow = locationArr[i] 
                                listOfLines = arrLines[lToShow].split("|")   # row to modify
                                for x in range(len(colList)):
                                    print(listOfLines[colList[x]],end="")
                                    print("| ",end="")
                                print("")
                        return
                    except:
                        print("!Failed to Select From Table",tName," due to improper command or modifiers")
                        return
    except:
        print("!Failed to Select From Table due to improper command or modifiers")
        return 

def test_input(inp): #runs through check of all user inputs in the program
    check_quit(inp) #quit program | .exit
    check_cDatabase(inp) #make database | create database name
    check_dDatabase(inp) #delete database | drop database name
    check_uDatabase(inp)#swap database| use name
    check_cTable(inp) #create table | create table name
    check_dTable(inp) #delete table | drop table name
    check_aTable(inp) #modify table | alter table name command content
    check_sTable(inp) #print table | select * from name
    check_Trans(inp)
    check_iTable(inp) #insert into name values
    check_uTable(inp) #update name
    check_dfTable(inp) #delete from name

def createLock(key,tName): #creates a lock with the name tNamelock, holds the key value inside lock
    paths = tName+"lock"
  #  print(paths)
    if os.path.exists(paths):
        return paths
    else:
         with open(paths, 'w+') as f: #write to table what was in ()
            f.write(str(key))
    return paths

def BeginTrans(): #prompt to update, generates key value and calls lock and uTable
    print("Transaction Starts.")
    inp = input("-->")
    result = parsingInp("update",inp,1)
    if result[0]==1:
        uI = input("--|")
        testSet = parsingInp("set",uI,1)
        if testSet[0]==1:
            key = random.random()
            lock =  createLock(key,result[1])
            uTable(result[1],uI,key,lock)

def check_quit(inp): 
    result = parsingInp(".exit",inp,0)
    if result[0]==1:
        print("All done")
        sys.exit(0)

def check_cDatabase(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("create database",inp,2)
    if result[0]==1:
        createDatabase(result[1])
def check_dDatabase(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("drop database",inp,2)
    if result[0]==1:
        deleteDatabase(result[1],parpat)
def check_uDatabase(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("use",inp,1)
    if result[0]==1:
        useDatabase(result[1],parpat)
def check_cTable(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("create table",inp,2)
    if result[0]==1:
        tName = result[1].split("(")[0]
        createTable(tName,inp)
def check_dTable(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("drop table",inp,2)
    if result[0]==1:
        deleteTable(result[1])

def check_sTable(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("select * from",inp,3)
    results = parsingInp("select ",inp,1)
    if result[0]==1:
        selectTable(result[1])
    elif results[0]==1:
        sFTable(inp)

def check_aTable(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("alter table",inp,2)
    if result[0]==1:
        alterTable(result[1],inp)

def check_dfTable(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("delete from",inp,2)
    if result[0]==1:
        dfTable(result[1],inp)       
def check_iTable(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("insert into",inp,2)
    if result[0]==1:
        insertTable(result[1],inp)
def check_uTable(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("update",inp,1)
    if result[0]==1:
        uI = input("--|")
        testSet = parsingInp("set",uI,1)
        if testSet[0]==1:
            uTable(result[1],uI)
def check_Trans(inp): #if parse input returns true, then calls function with (userinput - substring)
    result = parsingInp("begin transaction",inp,0)
    if result[0]==1:
        BeginTrans()   
def main(): #continuously seeks user input and tests against test cases
    while 1:
        uI = input("-->")
        test_input(uI)
if __name__=="__main__":
    main()