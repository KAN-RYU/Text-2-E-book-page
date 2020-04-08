import Text2Ebook
import os

VERBOS = True

def makeBooks():
    folder_List = os.listdir(Text2Ebook.text_Directory)
    print("Start processing total " + str(len(folder_List)) + " Books.")
    for name in folder_List:
        Text2Ebook.makeBook(name)
    print("Done!")


if __name__ == "__main__":
    makeBooks()