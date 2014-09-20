#!/usr/bin/env python

# This Python executes a sequence of shell-commands reading
# them from text files.
#
# You can pass to it multiple text file to be executed in sequence as in:
#      python execute textfile1 textfile2 textfile3
#
# In the case of the script to prepare the SD card, it accomadates it by passing the
# SD card device following the corresponding text file which, so this function work,
# must have the variable "card" assigned to a dummy text inside it, in the same way
# a shell variable is set (Eg: card=/dev/sdc). An example of this command line is:
#      python execute sd_textfile /dev/sdc
#
# Its current limitation is that each shell-command is limited to only one line
#
# When it stops in a shell-command because of failure, or when it stops because
# a reboot has executed, it saves the command-line parameters in a special text file,
# as well as the file and the line which is next to be executed, so you can contunue it
# by not passing any parameters to "execute", as in:
#      python execute
#
# On a commands file like "edxPRE" the variable "replacementsFile" sets an XML file with
# text replacements (See: "text_replacements.xml"). Then in the same commands file you
# can use "replacetext" to replace one or more texts in the given text file.
# See "edxPRE" for examples.
#
# A function for now not too practical and which has to be modified to be clean,
# is that when a shell-commands text file has the substring "RETRY" on its name,
# it will be only executed when the execution of a previous shell-commands text file
# has been failed. In this case there will be a reboot and you have to continue running
# it with:  "python execute"
# This function would work better when "RETRY" isn't part of the file name, but added
# in the command-line at the end of the correponding file name so it is executed this way.
# Symilarly a function "CONTINUE" when failure may be useful. Eg: When you need to undo
# some things, or some commands are not that important
#
# Implementing automatic reboot-and-continue may be desirable down the road

### On a high level, I'm not sure what the purpose of this file
### is. Why not just run the file directly from the commandline. If
### you need the ability to continue a build, make and a simple
### Makefile would be a better tool, although it's not clear to me why
### we need to stop and continue (documenting this would be nice).
### 
### Having commands like 'replacetext' is helpful, but those could be
### broken out into independent scripts, so they can just run from
### bash. This would be much easier to work with, since we could 
### run portions of the script by hand 

import os
import os.path
import sys
import time
import subprocess
from xml.dom import minidom

### What is the purpose of these three lines? They appear to do nothing
python = "python"
if sys.version_info >= (3, 0):
    python = python + "3"

working_dir = os.getcwd()
### Same for these three lines. They appear to check the current directory, 
### and then change to the current directory.... A one-line comment with 
### high-level intent would be helpful
dir_descriptor = os.open(working_dir, os.O_RDONLY)
os.fchdir(dir_descriptor)
os.close(dir_descriptor)

### It would be helpful to document what is in reboot.txt. 

### On a high level, my understanding was that this is running on the
### PC and not on the CubieTruck. Why do we ever need to reboot?

reboot = []
try:
    reboot_file = open(working_dir + "/reboot.txt", "r")
    reboot = reboot_file.read().split()
    reboot_file.close()
    if os.path.isfile(working_dir + "/reboot.txt"):
        os.remove(working_dir + "/reboot.txt")
except Exception:
    pass

command_file = 1

### You'd be much better off using argparse. See: 
###    https://docs.python.org/dev/library/argparse.html
### This would be shorter, more readable, and more usable
max_files = len(sys.argv)
current_line = 0
params = sys.argv
if len(sys.argv) == 1 and len(reboot) > 5:
    # I am completely confused by these lines. I have no idea what they mean. I don't know what
    # reboot is, or what reboot[0] is, etc. 
    # Clear variable names would help.  E.g. 
    # start_of_some_data_structure = int(reboot[0])
    # some_data_structure = reboot[start_of_some_data_structure:end_of_some_data_structure]
    # Etc. 
    # In practice, you'd almost certainly be better off using a dictionary with names, rather than file offsets, and pyyaml or json. 
    # http://pyyaml.org/wiki/PyYAMLDocumentation
    command_file = int(reboot[int(reboot[0]) + 1])
    current_line = int(reboot[int(reboot[0]) + 2])
    max_files = int(reboot[0]) + 1
    params = ["execute"] + reboot[1:max_files]

#if len(sys.argv) < 2:
    #sys.exit()

# Why do we have an error parameter, rather than exceptions? 
error = False
file_idx = command_file
line_idx = current_line

# This loop is unreadable. It is over 200 lines of code. Would it be possible
# to break this up into functions, with clear names and docstrings? 
# Step 1, if we went this way, would be to break out special commands 
# into seperate functions, and have those be mapped. E.g. 
# 
# def cd(line):
#   ''' Changes a directory... '''
#   os.fchdir...
#
# def replacetext(line)
#   ...
#
# At that point, you'd dispatch to the appropriate function. 
#
# keywords = {'cd' : cd, 'replacetext': replacetext}
# command = words[0]
# if command in keywords: 
#    keyword[command](words)
#
# If you wanted to be fancy, you could even populate the keywords
# dictionary with a Python decorator
#
# I would propose we don't want to do this, but rather we want to
# break these up into independent scripts.

while file_idx < max_files:
    file_idx_add = 1
    current_file_name = params[file_idx]
    print("")
    print("******************************************************")
    print("*    " + current_file_name + "   STARTED")
    print("******************************************************")
    sys.stdout.flush()
    textFile_commands_to_execute = open(current_file_name, "r")
    lines_commands_to_execute = textFile_commands_to_execute.read().splitlines()
    textFile_commands_to_execute.close()
    variables = {}
    dev = ""
    while line_idx < len(lines_commands_to_execute):
        line_command = lines_commands_to_execute[line_idx]

        if (len(line_command) != 0):
            if (line_command[0] != '#'):
                print("")
                print(line_command)
                sys.stdout.flush()
                words = line_command.split("=")
                if len(words) > 1 and words[0].find("\"") == -1 and words[0].find("'") == -1:
                    word_stripped = words[0].strip()
                    word_parts = word_stripped.split()
                    if len(word_parts) == 1:
                        if not (word_stripped == "card" and variables.get("card", None) != None):
                            variables[word_stripped] = line_command[len(words[0])+1:].strip()
                str_aux = line_command
                if dev == "":
                    if variables.get("card", None) != None:
                        if max_files <= file_idx + 1:
                            print("ERROR! This script needs the SD Card device as a parameter!")
                            sys.stdout.flush()
                            sys.exit()
                        dev = params[file_idx + 1]
                        if dev[:len(dev)-1] != "/dev/sd":
                            print("command-line input for sd card:  " + dev)
                            print("ERROR! Wrong SD Card device!")
                            sys.stdout.flush()
                            sys.exit()
                        file_idx_add = 2
                        variables["card"] = dev
                
                for v in variables:
                    line_command = line_command.replace("${" + v + "}", variables[v])
                if line_command != str_aux:
                    print(line_command)
                    sys.stdout.flush()
                words = line_command.split()
                retvalue = 2

                rebooting = False
                kbinterrupt = False               
                if len(words) == 2 and words[1] == "reboot" or len(words) == 1 and words[0] == "reboot":
                    try:
                        if os.path.isfile(working_dir + "/reboot.txt"):
                            os.remove(working_dir + "/reboot.txt")
                        if (line_idx + 1 < len(lines_commands_to_execute) or file_idx + 1 < max_files):
                            reboot_file = open(working_dir + "/reboot.txt", "w")
                            reboot_file.write(str(len(params[1:])) + "\n")
                            reboot_file.write(" ".join(params[1:]) + "\n")
                            file_idx_aux = file_idx + 1
                            line_idx_aux = 0
                            if line_idx + 1 < len(lines_commands_to_execute):
                                file_idx_aux = file_idx
                                line_idx_aux = line_idx + 1
                            reboot_file.write(str(file_idx_aux) + "\n")
                            reboot_file.write(str(line_idx_aux) + "\n")
                            reboot_file.close()
                        #retvalue = check_call("sudo reboot", shell=True)
                        try:
                            time.sleep(3)
                            proc = subprocess.Popen(line_command, shell=True)
                            retvalue = proc.wait()
                            retvalue = 0
                        except:
                            retvalue = 1
                        if retvalue == 0:
                            rebooting = True
                    except Exception:
                        retvalue = 1

                if len(words) == 2 and words[0] == "cd":
                    dir_descriptor = os.open(words[1], os.O_RDONLY)
                    os.fchdir(dir_descriptor)
                    os.close(dir_descriptor)
                    if os.getcwd() == os.path.abspath(words[1]):
                        retvalue = 0
                    else:
                        retvalue = 1
                elif len(words) == 4 and words[1] == "replacetext" or len(words) == 3 and words[0] == "replacetext":
                    try:
                        replaceTexts = False
                        file_reference = []
                        text_indexes = []
                        for v in variables:
                            if v == "replacementsFile":
                                replaceTexts = True
                        if replaceTexts:
                            xmldoc = minidom.parse(variables["replacementsFile"])
                            fileItemList = xmldoc.getElementsByTagName("file")
                            if len(words) == 4:
                                k = 2
                            else:
                                k = 1
                            file_reference = words[k].split(":")
                            text_indexes = file_reference[1].split(",")
                            for fileItem in fileItemList:
                                if fileItem.getAttribute("name") == file_reference[0]:
                                    replacementItemList = fileItem.getElementsByTagName("replacement")
                                    for i in range(len(text_indexes)):
                                        for replacementItem in replacementItemList:
                                            if text_indexes[i] == replacementItem.getAttribute("id"):
                                                oldItem = replacementItem.getElementsByTagName("old")[0]
                                                newItem = replacementItem.getElementsByTagName("new")[0]
                                                txt_to_repl = ""
                                                if len(oldItem.childNodes) > 0:
                                                    txt_to_repl = oldItem.childNodes[0].nodeValue
                                                txt_repl = ""
                                                if len(newItem.childNodes) > 0:
                                                    txt_repl = newItem.childNodes[0].nodeValue
                                                with open(words[k + 1], "r+") as f:
                                                    file_text = f.read()
                                                    file_text = file_text.replace(txt_to_repl, txt_repl)
                                                    f.seek(0)
                                                    f.write(file_text)
                                                    f.truncate()
                                                print("REPLACED : -----------------------")
                                                print(txt_to_repl)
                                                print("WITH : ---------------------------")
                                                print(txt_repl)
                                                print("----------------------------------")
                            retvalue = 0
                        else:
                            retvalue = 1
                    except KeyboardInterrupt:
                        kbinterrupt = True
                        retvalue = 1
                    except:
                        retvalue = 1
                else:
                    try:
                        proc = subprocess.Popen(line_command, shell=True)
                        retvalue = proc.wait()
                    except KeyboardInterrupt:
                        kbinterrupt = True
                        retvalue = 1
                    except:
                        retvalue = 1
                if retvalue == 0:
                    print("OK!")
                    sys.stdout.flush()
                    if rebooting:
                        sys.exit()
                else:
                    print("ERROR!")
                    sys.stdout.flush()

                    if not kbinterrupt:
                        try:
                            if os.path.isfile(working_dir + "/reboot.txt"):
                                os.system("sudo rm " + working_dir + "/reboot.txt")
                            reboot_file = open(working_dir + "/reboot.txt", "w")
                            reboot_file.write(str(len(params[1:])) + "\n")
                            reboot_file.write(" ".join(params[1:]) + "\n")
                            file_idx_aux = file_idx
                            line_idx_aux = line_idx
                            if "RETRY" in params[file_idx].upper():
                                file_idx_aux = file_idx
                                line_idx_aux = 0
                            if file_idx + 1 < max_files:
                                if "RETRY" in params[file_idx + 1].upper():
                                    file_idx_aux = file_idx + 1
                                    line_idx_aux = 0
                            reboot_file.write(str(file_idx_aux) + "\n")
                            reboot_file.write(str(line_idx_aux) + "\n")
                            reboot_file.close()
                            if file_idx + 1 < max_files:
                                if "RETRY" in params[file_idx + 1].upper():
                                    time.sleep(3)
                                    proc = subprocess.Popen("sudo reboot", shell=True)
                                    proc.wait()
                        except Exception:
                            pass

                    error = True
                    break
        line_idx += 1
    print("")
    sys.stdout.flush()
    dir_descriptor = os.open(working_dir, os.O_RDONLY)
    os.fchdir(dir_descriptor)
    os.close(dir_descriptor)

    if error == True:
        break

    file_idx += file_idx_add
    line_idx = 0

    if file_idx < max_files:
        while "retry" in params[file_idx]:
            file_idx += 1
            if file_idx == max_files - 1:
                break

    print("******************************************************")
    print("*    " + current_file_name + "   FINISHED")
    print("******************************************************")
    print("")
    sys.stdout.flush()
