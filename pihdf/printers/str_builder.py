import os
from time import gmtime, strftime

from .. import mylog

class StrBuilder:
    '''|
    | String builder used to generate text files. It supports indentation to facilitate formatting
    |________'''
    def __init__(self, indentation='    '):
        self.indentation = indentation
        self.level       = 0
        self.code        = ''
        self.noindent    = False


    def noIndent(self):
        '''|
        | Switch-off indentation. Auto-enabled when adding a string
        |________'''
        self.noindent = True
        return ''


    def indent(self, levels=1):
        '''|
        | Increase indentation
        |________'''
        self.level += levels
        return ''


    def dedent(self, levels=1):
        '''|
        | Decrease indentation
        |________'''
        if self.level >= levels:
            self.level -= levels
        else:
            self.level = 0
        return ''


    def __add__(self, value):
        '''|
        | Add a string to the code generator. Enables indentation if it was disabled
        |________'''
        tmpIndent = 0 if self.noindent else self.level
        self.code += tmpIndent*self.indentation + str(value)
        self.noindent = False
        return self

 
    def __sub__(self, number):
        '''|
        | Remove the last 'number' of characters from the end of the string
        |________'''
        self.code = self.code[:-number]
        return self   


    def newLine(self, num=1):
        '''|
        | Add 'num' new line characters at the end of the string
        |________'''
        for n in range(num):
            self.code += '\n'
        return ''


    def __str__(self):
        return str(self.code)


    def header_comment(self, str):
        '''|
        | Insert formatted python-commented text
        |________'''
        words = str.split()
        subs = []
        my_sub = []
        n = 68
        for i in range(len(words)):
            if len(' '.join(my_sub)) + len(words[i]) < n:
                my_sub.append(words[i])
            else:    
                subs.append(" ".join(my_sub))    
                my_sub = [words[i]]
        subs.append(" ".join(my_sub))    

        tmpIndent = 0 if self.noindent else self.level
        indent = tmpIndent * self.indentation                         
        s =                             "'''|\n"
        for line in subs: s += indent + '| '  + line + '\n'
        s +=                   indent + "|________'''\n"
        return s

    
    def write(self, filename, overwrite=False):
        '''|
        | Write the built string to a file
        |________'''
        try:
            if overwrite:
                with open(filename) as f: mylog.warn("File '" + filename + "' found. It will be overwritten...")
            else:
                filename_1 = filename+str(strftime(" (%Y-%m-%d %H:%M)", gmtime()))
                with open(filename) as f: mylog.info("File '%s' found. It will be backed-up in file %s." % (filename,filename_1))
                os.rename(filename, filename_1)
        except IOError as e:
            mylog.info("Writing file: " + filename)
            
        tmpFile = open(filename, 'w')
        tmpFile.write(self.code)
        tmpFile.close()
