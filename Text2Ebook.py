from PIL import ImageFont, Image, ImageDraw
from Text2EbookHelper import sorted_alphanumeric, insertString
import configparser
import sys
import os
import multiprocessing
from tqdm import tqdm
from itertools import repeat

class Text2Ebook():
    def __init__(self, __config):
        self.font_Name = __config.font_Name
        self.font_Size = __config.font_Size
        self.font_Offset = self.font_Size // 12

        self.font_Color = __config.font_Color
        self.page_Color = __config.page_Color

        self.text_Directory = __config.text_Directory
        self.result_Directory = __config.result_Directory

        self.image_Size = (__config.page_Width, __config.page_Height)
        self.margin = __config.margin
        self.width_Limit = self.image_Size[0] - self.margin * 2
        self.height_Limit = self.image_Size[1] - self.margin * 2
        self.line_Space = self.font_Size // 2 #Change
        self.max_Line = (self.image_Size[1] - self.margin * 2 + self.line_Space) // (self.font_Size + self.line_Space + self.font_Offset)
        self.min_Character = __config.min_Character
        
        self.num_core = __config.num_core

        self.verbos_line = ""
        self.verbos_Length = 0

    def makePages(self, fileName, folderName):
        font_Object = ImageFont.truetype(font = self.font_Name, size = self.font_Size)
        input_Text_File = open(self.text_Directory +  folderName + fileName, "r", encoding = 'utf-8')
        input_Text = input_Text_File.read()
        start = 0
        end = 1
        current_Page = 1
        page_Queue = []
        page = Image.new("RGB", self.image_Size)
        page_draw = ImageDraw.Draw(page)
        spin_Bar = '-\\|/'
        spin_Index = 0
        fileNameRaw = fileName[:-4]
        while fileNameRaw.endswith(' '):
            fileNameRaw = fileNameRaw[:-1]
        fileNameRaw = fileNameRaw.replace(".", "．")

        nLFlag = False

        while(end < len(input_Text)):
            w, h = font_Object.getsize_multiline(input_Text[start:end], spacing = self.line_Space)
            if w > self.width_Limit:
                input_Text = insertString(input_Text, "\n", end - 1)
                start = end
                end += self.min_Character
            else:
                end += 1

        start = 0
        end = 1
        cnt = 0
        while(end < len(input_Text)):
            if input_Text[end] == '\n':
                cnt += 1
                if(cnt == self.max_Line):
                    page_Queue.append((start, end))
                    start = end + 1
                    end = start
                    if(start < len(input_Text)):
                        cnt = 1 if input_Text[start] == '\n' else 0
                    current_Page += 1
            end += 1
        page_Queue.append((start, end))

        try:
            os.mkdir(self.result_Directory + folderName + fileNameRaw)
        except FileExistsError:
            pass

        for i, pair in enumerate(page_Queue):
            page_draw.rectangle([(0,0), self.image_Size], fill = self.page_Color)
            page_draw.text((self.margin, self.margin), 
                                text = input_Text[pair[0]:pair[1]], 
                                font = font_Object, 
                                spacing = self.line_Space, 
                                fill = self.font_Color, 
                                align = "left")

            page.save(self.result_Directory + folderName + fileNameRaw + '/' + str(i + 1) + ".png", "PNG")

        input_Text_File.close()
        return 1

    def makeBook(self, folderName, skipProcessed = True):
        if(folderName[-1] != '/'):
            folderName = folderName + '/'
        file_List = os.listdir(self.text_Directory + folderName)
        file_List = sorted_alphanumeric(file_List)

        try:
            os.mkdir(self.result_Directory + folderName)
        except FileExistsError:
            pass

        file_List_tmp = []
        if skipProcessed:
            for name in file_List:
                fileNameRaw = name[:-4]
                while fileNameRaw.endswith(' '):
                    fileNameRaw = fileNameRaw[:-1]
                fileNameRaw = fileNameRaw.replace(".", "．")

                if not os.path.exists(self.result_Directory + folderName + fileNameRaw):
                    file_List_tmp.append(name)
            file_List = file_List_tmp
        
        if len(file_List) == 0:
            print(folderName[:-1], 'skip.')
            return
        print(folderName[:-1], str(len(file_List)), 'chapters.')
        
        #Multi
        num_cores = min(multiprocessing.cpu_count(), self.num_core)
        pool = multiprocessing.Pool(num_cores)
        total = len(file_List)
        with tqdm(total = total) as pbar:
            def update(*a):
                pbar.update()
            for i in range(total):
                pool.apply_async(self.makePages, args=(file_List[i], folderName), callback=update)
            pool.close()
            pool.join()
        print()
        return