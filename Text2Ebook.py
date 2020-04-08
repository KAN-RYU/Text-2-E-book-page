from PIL import ImageFont, Image, ImageDraw
import sys
import os

#Global Variable
font_Name = "KoPubWorld Dotum_Pro Medium.otf"
font_Size = 36
font_Object = ImageFont.truetype(font = font_Name, size = font_Size)

font_Color = "black"
page_Color = "white"

text_Directory = "./Processing/"
result_Directory = "./Result/"

image_Size = (750, 1060)
margin = 40
width_Limit = image_Size[0] - margin * 2
height_Limit = image_Size[1] - margin * 2
line_Space = font_Size // 2 #Change

verbos_line = ""

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
    fileNameRaw = fileName[:-5]

    while(end < len(input_Text)):
        sys.stdout.write(verbos_line + fileNameRaw + " " + str(current_Page) + " Pages.")
        sys.stdout.flush()
        while(True):
            w, h = page_draw.textsize(input_Text[start:end], font = font_Object, spacing = line_Space)
            if h > height_Limit or end > len(input_Text):
                #PageEnd
                end -= 1
                page_Queue.append((start, end))
                start = end + 1
                end = start + 2
                if not end > len(input_Text):
                    while(input_Text[start] == '\n' and end < len(input_Text)):
                        start += 1
                        end += 1
                break
            if w > width_Limit:
                input_Text = insertString(input_Text, "\n", end - 1)
            else:
                end += 1
        current_Page += 1
        
    current_Page = 1
    for i, pair in enumerate(page_Queue):
        page_draw.rectangle([(0,0), image_Size], fill = page_Color)
        page_draw.text((margin, margin), 
                            text = input_Text[pair[0]:pair[1]], 
                            font = font_Object, 
                            spacing = line_Space, 
                            fill = font_Color, 
                            align = "left")

        try:
            os.mkdir(result_Directory + folderName + fileNameRaw)
        except FileExistsError:
            pass

        page.save(result_Directory + folderName + fileNameRaw + '/' + str(i + 1) + ".png", "PNG")
    
    input_Text_File.close()

def makeBook(folderName):
    if(folderName[-1] != '/'):
        folderName = folderName + '/'
    file_List = os.listdir(text_Directory + folderName)

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