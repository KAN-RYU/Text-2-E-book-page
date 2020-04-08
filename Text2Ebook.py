from PIL import ImageFont, Image, ImageDraw
import curses

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

def insertString(origin, that, index):
    return origin[:index] + that + origin[index:]

def makePages():
    input_Text_File = open("./679화 수도로.txt", "r", encoding = 'utf-8')
    input_Text = input_Text_File.read()
    start = 0
    end = 1
    current_Page = 1

    while(start < len(input_Text)):
        page = Image.new("RGB", image_Size)
        page_draw = ImageDraw.Draw(page)
        page_draw.rectangle([(0,0), image_Size], fill = page_Color)

        while(True):
            w, h = page_draw.textsize(input_Text[start:end], font = font_Object, spacing = line_Space)
            
            if h > height_Limit or end > len(input_Text):
                #PageEnd
                end -= 2
                page_draw.text((margin, margin), 
                            text = input_Text[start:end], 
                            font = font_Object, 
                            spacing = line_Space, 
                            fill = font_Color, 
                            align = "left")
                start = end + 1
                end = start + 1
                if not end > len(input_Text):
                    while(input_Text[start] == '\n'):
                        start += 1
                        end += 1
                break
            
            if w > width_Limit:
                input_Text = insertString(input_Text, "\n", end - 1)
                end += 2
            else:
                end += 1
            
        page.save(result_Directory + "test/" + str(current_Page) + ".png", "PNG")
        current_Page += 1


if __name__ == "__main__":
    makePages()