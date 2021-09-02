from tkinter import*
from threading import Thread
from tkinter import filedialog
import requests
import wget, os
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from time import sleep 
import shutil, PyPDF2
from zipfile import ZipFile
#import pm_app_fxn as pm
output1 = ['']*1
class main_App(Thread):
    def __init__(self):
        Thread.__init__(self)

    def browse_button(self):
        filename = filedialog.askdirectory()
        self.filename1[0]=filename
        #print(filename)
        self.entry_1.insert(0,filename)
        return filename

    def output(self, value):
        #value = sample_text.get(1.0, "end-1c")
        self.entry_2.insert(END, value+'\n')

    def output_screen(self):
        #value = sample_text.get(1.0, "end-1c")
        value = output1[0]
        self.output(value)
        #self.entry_2.insert(1.0, value+'\n')

    def jpg_to_pdf(self):
        filename = self.filename1[0]
        to_be_excute = "jpg_to_pdf"
        ch = ConvertHandler( filename, to_be_excute )
        ch.start()    

    def merge_pdf(self):
        filename = self.filename1[0]
        to_be_excute = "merge_pdf"
        ch = ConvertHandler( filename, to_be_excute )
        ch.start()
           
    def split_pdf(self):
        filename = self.filename1[0]
        to_be_excute = "split_pdf"
        ch = ConvertHandler( filename, to_be_excute )
        ch.start()
    
    def run(self):
        self.filename1 = ['']*1
        self.data1 = ['']*1
        self.root = Tk()
        self.entry_0 = Text(self.root, height = 10, width = 90)
        self.entry_1 = Entry(self.root, width=82)
        self.entry_2 = Text(self.root, height = 10, width = 90)
        
        #self.root = Tk()
        self.root.geometry('900x500')
        self.root.title("PDF Project - Play with your PDF as you like")
        # File path selector
        Button(self.root, text='Choose path of folder where file available',command = self.browse_button, width=35,bg='brown',fg='white').place(x=90,y=50)
        self.entry_1 = Entry(self.root, width=76)
        self.entry_1.place(x=350,y=50)
        # Action using button
        Button(self.root, text='JPG TO PDF',command = self.jpg_to_pdf, width=20,bg='green',fg='white').place(x=90,y=90)
        Button(self.root, text='Merge PDF',command = self.merge_pdf, width=20,bg='green',fg='white').place(x=280,y=90)
        Button(self.root, text='SPLIT PDF',command = self.split_pdf, width=20,bg='green',fg='white').place(x=470,y=90)
        Button(self.root, text='EXIT ',command = self.root.quit, width=20,bg='red',fg='white').place(x=660,y=90)
        # Display Logs
        # Action to download
        self.entry_2 = Text(self.root, height = 16, width = 90)
        self.entry_2.place(x=90,y=140)
        self.root.mainloop()
        print("\n\nProgram Exit")


class Converter():
    def __init__(self):
        pass
        #Thread.__init__(self)
        #self.path = path
    def jpg_to_pdf(self,path):
        #print("Path Value = ",path)
        list = os.listdir(path)
        for f1 in list:
            if f1[-5:] == ".jpeg":
                image_file = Image.open(path+"\\"+f1)
                im1 = image_file.convert('RGB')
                pdf_path = path+"\\"+f1[0:-5]+".pdf"
                #print(f"{f1} converted to {f1[0:-5]}.pdf")
                main_App.output(pm,f"{f1} converted to {f1[0:-5]}.pdf")
                im1.save(pdf_path)
            elif f1[-4:] == ".jpg":
                image_file = Image.open(path+"\\"+f1)
                im1 = image_file.convert('RGB')
                pdf_path = path+"\\"+f1[0:-4]+".pdf"
                main_App.output(pm,f"{f1} converted to {f1[0:-4]}.pdf")
                im1.save(pdf_path)
            
    def merge_pdf(self,path):
        p1 = path.split('/')
        sep = '\\'
        source_folder = sep.join(p1)
        merged_file_name = "Combined_file.pdf"
        if os.path.exists(source_folder+'\\'+merged_file_name):
            os.remove(source_folder+'\\'+merged_file_name)
        list_of_all_files = os.listdir(source_folder)
        list_of_only_pdf = []
        for f in list_of_all_files:
            if f[-4:] == ".pdf":
                list_of_only_pdf.append(f)
        pdfWriter = PyPDF2.PdfFileWriter()
        no_of_files = len(list_of_only_pdf)
        i = 1
        output_string= ""
        for each_pdf_file in list_of_only_pdf:
            pdf_files = open(source_folder+'//'+each_pdf_file , 'rb' )
            pdf_reader = PyPDF2.PdfFileReader(pdf_files)
            
            if i < no_of_files:
                output_string = output_string+each_pdf_file+" + "
            else: 
                output_string = output_string+each_pdf_file+" = "
            i+=1
            
            for pageNum in range(pdf_reader.numPages):
                pageObj = pdf_reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
        pdfOutputFile = open(source_folder+'//'+merged_file_name, 'wb')
        pdfWriter.write(pdfOutputFile)
        output_string = output_string+merged_file_name
        main_App.output(pm,output_string)
        pdfOutputFile.close()
        pdf_files.close()

    def split_pdf(self,path):
        p1 = path.split('/')
        sep = '\\'
        source_folder = sep.join(p1)
        Source_file_names = os.listdir(source_folder)
        #print(Source_file_names)
        for source_files in Source_file_names:
            in_pdf = source_folder+'\\'+source_files
            #print(in_pdf)
            #self.split_pdf(in_pdf)
            if source_files[-4:] == ".pdf":
                step = 1
                splitted_files = []
                try:
                    with open(in_pdf, 'rb') as in_file:
                        input_pdf = PdfFileReader(in_file)
                        num_pages = input_pdf.numPages
                        input_dir, filename = os.path.split(in_pdf)
                        filename = os.path.splitext(filename)[0]
                        output_dir = input_dir + "/" + filename + "_splitted/"
                        os.mkdir(output_dir)
                        intervals = range(0, num_pages, step)
                        intervals = dict(enumerate(intervals, 1))
                        naming = f'{filename}_p'
                        
                        count = 0
                        for key, val in intervals.items():
                            output_pdf = PdfFileWriter()
                            if key == len(intervals):
                                for i in range(val, num_pages):
                                    output_pdf.addPage(input_pdf.getPage(i))
                                nums = f'{val + 1}' if step == 1 else f'{val + 1}-{val + step}'
                                with open(f'{output_dir}{naming}{nums}.pdf', 'wb') as outfile:
                                    output_pdf.write(outfile)
                                #print(f'{naming}{nums}.pdf written to {output_dir}')
                                splitted_files.append(f'{naming}{nums}.pdf')
                                count += 1
                            else:
                                for i in range(val, intervals[key + 1]):
                                    output_pdf.addPage(input_pdf.getPage(i))
                                nums = f'{val + 1}' if step == 1 else f'{val + 1}-{val + step}'
                                with open(f'{output_dir}{naming}{nums}.pdf', 'wb') as outfile:
                                    output_pdf.write(outfile)
                                #print(f'{naming}{nums}.pdf written to {output_dir}')
                                splitted_files.append(f'{naming}{nums}.pdf')
                                count += 1
                except FileExistsError as err:
                    #print('Cannot find the specified file. Check your input:')
                    main_App.output(pm,'Cannot find the specified file. Check your input:')
                #print(f'{count} pdf files written to {output_dir}')
                #print("\n\n" )
                out = "\n"
                #print(source_files, end =" " )
                out = out+source_files+" "+"Splitted as"+" "
                #print("Splitted as", end=" ")
                m = len(splitted_files)
                n = 1
                for f in splitted_files:
                    if n < m:
                        #print(f, end=", ")
                        out = out+f+", "
                    else:
                        #print(f, end="")
                        out = out+f+" "
                    n+=1
                main_App.output(pm,out)

     

class ConvertHandler(Thread):
    def __init__(self, path, action ):
        Thread.__init__(self)
        self.path = path
        self.action = action
        
    def run(self):
        if self.action == "jpg_to_pdf":
            #print('Action Value - ',self.path)
            Converter.jpg_to_pdf(cn,self.path)
        elif self.action == "merge_pdf":
            Converter.merge_pdf(cn, self.path)
        else:
            Converter.split_pdf(cn, self.path)
 
pm = main_App()
cn = Converter()
pm.start()
