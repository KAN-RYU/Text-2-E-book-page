import configparser

class Text2EbookConfig():
    configFilePath = './config.ini'
    
    #default config
    
    #font
    font_Name = "KoPubWorld Dotum_Pro Medium.otf"
    font_Size = 36
    
    #page
    page_Width = 750
    page_Height = 1060
    margin = 40
    min_Character = 22
    
    #color
    font_Color = '#000000'
    page_Color = '#FFFFFF'
    
    #directory
    text_Directory = './Processing/'
    result_Directory = './Result/'
    
    #Debug
    num_core = 2
    verbos = False
    
    def __init__(self):
        self.loadConfig()
        
    def loadConfig(self):
        print('Reading', self.configFilePath, '...')
        
        config = configparser.RawConfigParser()
        
        try:
            with open(self.configFilePath, 'r') as configFile:
                config.read_file(configFile)
                
                self.font_Name = config.get('Font', 'font_Name')
                self.font_Size = config.getint('Font', 'font_Size')
                            
                self.page_Width = config.getint('Page', 'page_Width')
                self.page_Height = config.getint('Page', 'page_Height')
                self.margin = config.getint('Page', 'margin')
                self.min_Character = config.getint('Page', 'min_Character')
                
                self.font_Color = config.get('Color', 'font_Color')
                self.page_Color = config.get('Color', 'page_Color')
                
                self.text_Directory = config.get('Directory', 'text_Directory')
                self.result_Directory = config.get('Directory', 'result_Directory')
                
                self.num_core = config.getint('Debug', 'num_core')
                
                try:
                    self.verbos = config.getboolean('Debug', 'verbos')
                except ValueError:
                    self.verbos = False
                    print("verbos = False")
            
        except BaseException:
            print('Fail to load config file. Fixing config file...')
            self.writeConfig()
            
        print('Reading done.')
    
    def writeConfig(self):
        print('Writing config file...')
        config = configparser.RawConfigParser()
        
        config.add_section('Font')
        config.set('Font', 'font_Name', self.font_Name)
        config.set('Font', 'font_Size', self.font_Size)
        
        config.add_section('Page')
        config.set('Page', 'page_Width', self.page_Width)
        config.set('Page', 'page_Height', self.page_Height)
        config.set('Page', 'margin', self.margin)
        config.set('Page', 'min_Character', self.min_Character)
        
        config.add_section('Color')
        config.set('Color', 'font_Color', self.font_Color)
        config.set('Color', 'page_Color', self.page_Color)
        
        config.add_section('Directory')
        config.set('Directory', 'text_Directory', self.text_Directory)
        config.set('Directory', 'result_Directory', self.result_Directory)
        
        config.add_section('Debug')
        config.set('Debug', 'num_core', self.num_core)
        config.set('Debug', 'verbos', self.verbos)
        
        try:
            with open(self.configFilePath, 'w') as configFile:
                config.write(configFile)
                configFile.close()
        except:
            raise
        
        print('Writing done.')
    
    def printConfig(self):
        print('\n')
        print('[Font]')
        print('-font_name =', self.font_Name)
        print('-font_size =', self.font_Size)
        print('[Page]')
        print('-page_width =', self.page_Width)
        print('-page_height =', self.page_Height)
        print('-margin =', self.margin)
        print('-min_character', self.min_Character)
        print('[Color]')
        print('-font_color =', self.font_Color)
        print('-page_color =', self.page_Color)
        print('[Directory]')
        print('-text_directory =', self.text_Directory)
        print('-result_driectory =', self.result_Directory)
        print('[Debug]')
        print('-num_core =', self.num_core)
        print('-verbos =', self.verbos)