import cmd
from datascience.ui.pathCompletion import pathCompletion
from datascience.computing import *
import os
import glob
import ntpath

class CommandLine(cmd.Cmd):
    intro = "***Data Science project***"
    
    def __init__(self):
        super().__init__()
        self._setPrompt_()
        self.datas = None

    def _setPrompt_(self, text=""):
        self.prompt = f"({text})> "

    def do_exit(self, line):
        """exit :
        Quit the program
        """
        print("Quitting...")
        return True

    do_EOF = do_exit

    def emptyline(self):
        pass

    def default(self, line):
        print(f"Unknown command : {line}")

    def do_load(self, filename):
        """load <pathOfFile> :
        Load a file to work on"""
        try:
            print("Loading datas...")
            self.datas = loadFile(filename)
            print("Datas loaded")
            self._setPrompt_(ntpath.basename(filename))
        except:
            print(f'Cannot load file "{filename}"')

    def do_unload(self, line):
        """unload :
        Unload the file"""
        self.datas = None
        self._setPrompt_()

    def complete_load(self, text, line, begidx, endidx):
        return pathCompletion(text, line, begidx, endidx)

    def do_total_mail(self, line):
        """total_mail (by <time>) :
        Return the total number of mails sent. 
        You can optionnaly filter by HOUR, WEEK, MONTH, YEAR
        """
        args = line.split(' ')
        if self.datas:
            if args[0] == "":
                res = countMail(self.datas)
                print(f"Result : {res}")

            elif len(args) >= 2 and args[0] == "by":
                if args[1] == "WEEK":
                    res = countMail(self.datas, "WEEK")
                    print("Result :")
                    for key in res.keys():
                        print(f"    {key} : {res.get(key)}")

                elif args[1] == "HOUR":
                    res = countMail(self.datas, "HOUR")
                    print("Result :")
                    for key in res.keys():
                        print(f"    {key}h : {res.get(key)}")

                else:
                    print("Wrong arguments")
            
            else:
                print("Wrong arguments")

        else:
            print("No datas loaded")

    def complete_total_mail(self, text, line, begidx, endidx):
        args = line.split(" ")
        if len(args) == 1 or len(args) == 2 and "by ".startswith(text) and not "by " in line:
            return ["by "]

        elif len(args) == 3:
            return [x for x in ["HOUR", "WEEK", "MONTH", "YEAR"] if x.startswith(text.upper())]

        else: return []