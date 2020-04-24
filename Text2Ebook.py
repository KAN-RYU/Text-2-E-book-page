from PIL import ImageFont, Image, ImageDraw
import sys
import os
import re
import ConfigParser

#Global Variable
font_Name = "KoPubWorld Dotum_Pro Medium.otf"
font_Size = 36
font_Object = ImageFont.truetype(font = font_Name, size = font_Size)
font_Offset = font_Size // 12

font_Color = "black"
page_Color = "white"

text_Directory = "./Processing/"
result_Directory = "./Result/"

image_Size = (750, 1060)
margin = 40
width_Limit = image_Size[0] - margin * 2
height_Limit = image_Size[1] - margin * 2
line_Space = font_Size // 2 #Change
max_Line = (image_Size[1] - margin * 2 + line_Space) // (font_Size + line_Space + font_Offset)
min_Character = 22

verbos_line = ""
verbos_Length = 0

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def insertString(origin, that, index):
    return origin[:index] + that + origin[index:]

def makePages(fileName, folderName):
    input_Text_File = open(text_Directory +  folderName + fileName, "r", encoding = 'utf-8')
    input_Text = input_Text_File.read()
    start = 0
    end = 1
    current_Page = 1
    page_Queue = []
    page = Image.new("RGB", image_Size)
    page_draw = ImageDraw.Draw(page)
    global verbos_Length
    spin_Bar = '-\\|/'
    spin_Index = 0
    fileNameRaw = fileName[:-4]
    while fileNameRaw.endswith(' '):
        fileNameRaw = fileNameRaw[:-1]
    fileNameRaw = fileNameRaw.replace(".", "．")

    nLFlag = False

    sys.stdout.write("\r" + " " * verbos_Length)
    verbos_M = verbos_line + fileNameRaw + " "
    sys.stdout.write(verbos_M)
    sys.stdout.flush()

    if not os.path.exists(result_Directory + folderName + fileNameRaw):
        while(end < len(input_Text)):
            w, h = font_Object.getsize_multiline(input_Text[start:end], spacing = line_Space)
            if w > width_Limit:
                sys.stdout.write("\b" + spin_Bar[spin_Index])
                sys.stdout.flush()
                spin_Index = (spin_Index + 1) % 4
                input_Text = insertString(input_Text, "\n", end - 1)
                start = end
                end += min_Character
            else:
                end += 1

        start = 0
        end = 1
        cnt = 0
        while(end < len(input_Text)):
            if input_Text[end] == '\n':
                cnt += 1
                if(cnt == max_Line):
                    page_Queue.append((start, end))
                    start = end + 1
                    end = start
                    if(start < len(input_Text)):
                        cnt = 1 if input_Text[start] == '\n' else 0
                    current_Page += 1
            end += 1
        page_Queue.append((start, end))

        try:
            os.mkdir(result_Directory + folderName + fileNameRaw)
        except FileExistsError:
            pass

        for i, pair in enumerate(page_Queue):
            sys.stdout.write("\r" + " " * verbos_Length)
            verbos_M = verbos_line + fileNameRaw + " " + str(i+1) + "/" + str(current_Page) + " Pages. "
            sys.stdout.write(verbos_M)
            sys.stdout.flush()
            verbos_Length = min(170, len(verbos_M.encode()))
            page_draw.rectangle([(0,0), image_Size], fill = page_Color)
            page_draw.text((margin, margin), 
                                text = input_Text[pair[0]:pair[1]], 
                                font = font_Object, 
                                spacing = line_Space, 
                                fill = font_Color, 
                                align = "left")

            page.save(result_Directory + folderName + fileNameRaw + '/' + str(i + 1) + ".png", "PNG")
    else:
        sys.stdout.write("\r" + " " * verbos_Length)
        verbos_M = verbos_line + fileNameRaw + " Skip. "
        sys.stdout.write(verbos_M)
        sys.stdout.flush()
        verbos_Length = min(170, len(verbos_M.encode()))

    input_Text_File.close()

def makeBook(folderName):
    if(folderName[-1] != '/'):
        folderName = folderName + '/'
    file_List = os.listdir(text_Directory + folderName)
    file_List = sorted_alphanumeric(file_List)

    try:
        os.mkdir(result_Directory + folderName)
    except FileExistsError:
        pass

    
    for i, name in enumerate(file_List):
        global verbos_line
        verbos_line = "\r" + folderName[:-1] + " " + str(i + 1) + "/" + str(len(file_List)) + " Total Chapters. "
        makePages(name, folderName)
    print()
 
if __name__ == "__main__":
    makeBook(input())