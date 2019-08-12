# Easy Backup by Dan James 8/04/2019
# Command line backup script

import os, sys, shelve, re, distutils.dir_util
from pathlib import Path

DIRECTORIES = ('c:\Backups\defaultfrom', 'c:\Backups\defaultfrom2')
DESTINATIONS = ('c:\Backups\defaultto')
CONFILE = "bkconfig.dat"

theArgs = sys.argv

def loadConfig():
    loadeddirs, loadeddests = [], []
    shfile = shelve.open(CONFILE)
    listofkeys = list(shfile.keys())
    if listofkeys:
        loadeddirs = shfile['dirs']
        loadeddests = shfile['dests']
        dirscount = len(loadeddirs)
        destscount = len(loadeddests)
        print("Loaded " + str(dirscount) + " origin directories and " + str(destscount) + " destinations.")
    else:
        # No keys found, config file is empty or new. Load defaults.
        loadeddirs = DIRECTORIES
        loadeddests = DESTINATIONS
        shfile['dirs'] = loadeddirs
        shfile['dests'] = loadeddests
    shfile.close()

    return loadeddirs, loadeddests

def editConfig(option, argument):
    shfile = shelve.open(CONFILE)
    dirValues = shfile['dirs']
    destValues = shfile['dests']
    def remoVal(theList):
        if argument in theList:
            theList.remove(argument)
            print("Deleted entry " + argument + " from config values.")
            return theList
        else:
            print("No such directory found.")
            return theList

    def addVal(theList):
        if argument in theList:
            print("Directory is already added.")
        else:
            print("Appending " + str(argument) + " to list " + str(theList))
            theList.append(argument)
        return theList

    if option == "ao":
        shfile['dirs'] = addVal(dirValues)
    elif option == "ad":
        shfile['dests'] = addVal(destValues)
    elif option == "ro":
        shfile['dirs'] = remoVal(dirValues)
    elif option == "rd":
        shfile['dests'] = remoVal(destValues)
    else:
        print("What the fuck are you doing")
    shfile.close()

def doBackup(dirs, dests):
    print("dirs: " + str(dirs) + ", dests: " + str(dests))
    for dest in dests:
        for origin in dirs:
            if os.path.exists(origin):
                if os.path.isdir(origin):
                    distutils.dir_util.copy_tree(origin, dest, update=1)
                    print("Copied " + origin + " to " + dest)
                    return True
                elif os.path.isfile(origin):
                    distutils.file_util.copy_file(origin, dest, update=1)
                    print("Copied " + origin + " to " + dest)
                    return True
                else:
                    print(origin + " apparently is neither a path nor a file.")
                    return False
            else:
                print("Path " + origin + " does not exist.")
                return False

def validateArgs(args):
    selOption = ""
    if len(args) == 1:
        print("Usage: easybackup.py (option) [directory]")
        print("     -b     Perform the backup function. Use no third parameter.")
        print("     -a     Add an origin file or directory")
        print("     -d     Add a destination to which all origin folders will be copied")
        print("            Note: removable drives must be plugged in at the time they are added to be valid.")
        print("     -r     Remove an origin directory.")
        print("     -R     Remove a destination directory.")
        print("     -v     View current origin and destination directories.")
        print("\nExample: easybackup.py -a C:\\Users\\Default\\Music")
        exit()
    elif len(args) == 2:
        selOption = args[1]
    elif len(args) > 2:
        selOption = args[1]
        selDir = str(args[2])

    if selOption == "-a":
        if selDir:
            if os.path.exists(selDir):
                editConfig("ao", selDir)
                print("Origin path " + selDir + " added successfully.")
                return True
            else:
                print("provided path " + selDir + " does not exist.")
                return False
        else:
            print("Missing argument: Origin directory")
            return False
        return
    elif selOption == "-d":
        if selDir:
            filePath = Path(selDir)
            if filePath.exists():
                editConfig("ad", selDir)
                return True
            else:
                try:
                    os.mkdir(filePath)
                    editConfig("ad", selDir)
                    return True
                except:
                    print("File path was unable to be created, it is invalid.")
                    return False
        else:
            print("Missing argument: Destination directory")
            return False
        return
    elif selOption == "-b":
        dirsloaded, destsloaded = loadConfig()
        doBackup(dirsloaded, destsloaded)
    elif selOption == "-r":
        if selDir:
            editConfig("ro", selDir)
            return True
        else:
            print("Missing argument: Origin directory")
            return False
    elif selOption == "-R":
        if selDir:
            editConfig("rd", selDir)
            return True
        else:
            print("Missing argument: Destination directory")
            return False
    elif selOption == "-v":
        dirsloaded, destsloaded = loadConfig()
        print("Origin directories:")
        for item in dirsloaded:
            print(item)
        print("Destination directories:")
        for item in destsloaded:
            print(item)
        return True
    else:
        print("Invalid parameter.")
        print("selOption: " + selOption)
        return False

validateArgs(theArgs)
