import Text2Ebook
from Text2EbookConfig import Text2EbookConfig
import os
import sys

__config = Text2EbookConfig()

VERBOS = __config.verbos
VERSION = 'ver 0.3'

def makeBooks():
    folder_List = os.listdir(Text2Ebook.text_Directory)
    print("Start processing total " + str(len(folder_List)) + " Books.")
    for name in folder_List:
        Text2Ebook.makeBook(name)
    print("Done!")

def menu():
    print('\n\nText 2 Ebook Page', VERSION)
    print('---------------------------')
    print('1: Process without already processed file. (Noticed by existing folder)')
    print('2: Process in working directory')
    print('3: Process with one folder')
    print('---------------------------')
    print('r: Reload Config File')
    print('p: Print Config File')
    print('x: Exit Program')
    print('---------------------------')

if __name__ == "__main__":
    __config.printConfig()
    while True:
        menu()
        choice = input('Type: ')
        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == 'r':
            __config.loadConfig()
            __config.printConfig()
        elif choice == 'p':
            __config.printConfig()
        elif choice == 'x':
            sys.exit()
    