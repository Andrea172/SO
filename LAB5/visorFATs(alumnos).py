# Autor: Prof. Alejandro T. Bello Ruiz
# Curso: INF239 Sistemas Operativos
# Laboratorio 5

import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import math

class App(tk.Tk):
     def __init__(self):
         super().__init__()
         self.fname = None#
         self.sectorsXclusters=0#
         self.rootEntries=0#
         self.nSectors=0#
         self.rSectors=0#
         self.bytesXSector=0#
         self.numFats=0#
         self.sectorsXFAT=0#

         
         self.title("Visor File System FAT")   
         root=TK()
         self.scrollbar=tk.Scrollbar(root)      
         self.canvas = tk.Canvas(self, width=450, height=480, bg="white")         
         btn_file = tk.Button(self, text="Choose file system image",command=self.choose_file)         
         btn_showBoot = tk.Button(self, text="Boot Sector",command=self.show_bootsector)
         btn_showFat = tk.Button(self, text="File Allocation Table",command=self.show_fat)
         btn_showRootDir = tk.Button(self, text="Root directory",command=self.show_rootdir)                  
         btn_file.grid(row=0, column=0, columnspan=2, padx=60,pady=20 )                 
         btn_showBoot.grid(row=1, column=0)
         btn_showFat.grid(row=1, column=1)
         btn_showRootDir.grid(row=2, column=0, columnspan=2,padx=60,pady=20,sticky='nswe')
         self.canvas.grid(row=3, column=0,rowspan=3, columnspan=2)
         self.canvas.config(scrollregion=(0,0,450,1000))
         self.canvas.config(highlightthickness=0)         
         
           
     def choose_file(self):
         filetypes = (("File sistem images", "*.img"),("All files", "*"))
         filename = fd.askopenfilename(title="Open file", initialdir="/home/alejandro/SourceCode/Python", filetypes=filetypes)
         self.fname = filename
               
               
     def show_bootsector(self):
         if self.fname == None:
             self.show_error1()
         else:    
             with open(self.fname,mode='rb') as file:
                  self.canvas.delete("all")
                  self.canvas.create_text(180,20, text="Boot Sector",anchor=tk.W)
                  j1=file.read(1)
                  i1=int.from_bytes(j1,byteorder='little')
                  j2=file.read(1)
                  i2=int.from_bytes(j2,byteorder='little')
                  j3=file.read(1)
                  i3=int.from_bytes(j3,byteorder='little')
                  self.canvas.create_text(30,40, text="Code to jump the bootstrap code: "+format(i1,'X')+" "+format(i2,'X')+" "+format(i3,'X'),anchor=tk.W)
                  
                  fabricante=file.read(8)
                  texto=fabricante.decode('utf-8')
                  self.canvas.create_text(30,60, text='Oem ID - Name of the formatting OS: '+texto,anchor=tk.W)
                  
                  bytesps=file.read(2)
                  i=int.from_bytes(bytesps,byteorder='little')
                  self.canvas.create_text(30,80, text='Bytes per Sector: '+str(i),anchor=tk.W)
                  self.bytesXSector=bytesps
                  
                  sectorespc=file.read(1)
                  i=int.from_bytes(sectorespc,byteorder='little')
                  self.canvas.create_text(30,100, text='Sectors per Cluster: '+str(i),anchor=tk.W)
                  self.sectorsXclusters=sectorespc


                  sectoresr = file.read(2)
                  i=int.from_bytes(sectoresr,byteorder='little')
                  self.canvas.create_text(30,120, text='Reserved sectors: '+str(i),anchor=tk.W)
                  self.rSectors=sectoresr
                  
                  nfats=file.read(1)
                  i=int.from_bytes(nfats,byteorder='little')
                  self.canvas.create_text(30,140, text='Number of FAT copies: '+str(i),anchor=tk.W)
                  self.numFats=i
                  
                  entradasRaizdir = file.read(2)
                  i=int.from_bytes(entradasRaizdir,byteorder='little')
                  self.canvas.create_text(30,160, text='Number of possible root entries: '+str(i),anchor=tk.W)
                  self.rootEntries=entradasRaizdir

                  sectorest=file.read(2)
                  i=int.from_bytes(sectorest,byteorder='little')                  
                  self.canvas.create_text(30,180, text='Small number of sectors: '+str(i),anchor=tk.W)
                  self.nSectors+=sectorest

                  descriptorm=file.read(1)
                  i=int.from_bytes(descriptorm,byteorder='little')
                  self.canvas.create_text(30,200, text='Media Descriptor: '+format(i,'X'),anchor=tk.W)
                                    
                  sectorespf=file.read(2)
                  i=int.from_bytes(sectorespf,byteorder='little')
                  self.canvas.create_text(30,220, text='Sectors per FAT: '+str(i),anchor=tk.W)
                  self.sectorsXFAT=sectorespf
                  
                  sectorespt=file.read(2)
                  i=int.from_bytes(sectorespt,byteorder='little')
                  self.canvas.create_text(30,240, text='Sectors per Track: '+str(i),anchor=tk.W)
                 
                  numerodec=file.read(2)
                  i=int.from_bytes(numerodec,byteorder='little')
                  self.canvas.create_text(30,260, text='Number of Heads: '+str(i),anchor=tk.W)
                  
                  sectoreso=file.read(4)
                  i=int.from_bytes(sectoreso,byteorder='little')
                  self.canvas.create_text(30,280, text='Hidden Sectors: '+str(i),anchor=tk.W)
                  
                  sectorestl=file.read(4)
                  i=int.from_bytes(sectorestl,byteorder='little')
                  self.canvas.create_text(30,300, text='Large number of sectors: '+str(i),anchor=tk.W)
                  self.nSectors+=sectorestl


                  drive=file.read(1)
                  i=int.from_bytes(drive,byteorder='little')
                  self.canvas.create_text(30,320, text='Drive Number: '+str(i),anchor=tk.W)
                  
                  reservado=file.read(1)
                  i=int.from_bytes(reservado,byteorder='little')
                  self.canvas.create_text(30,340, text='Reserved: '+str(i),anchor=tk.W)
                  
                  signaturae=file.read(1)
                  i=int.from_bytes(signaturae,byteorder='little')
                  self.canvas.create_text(30,360, text='Extended Boot Signature: '+str(i),anchor=tk.W)
                  
                  volumensn=file.read(4)
                  i=int.from_bytes(volumensn,byteorder='little')
                  self.canvas.create_text(30,380, text='Volume Serial Number: '+str(i),anchor=tk.W)
                  
                  volumen=file.read(11)
                  texto=volumen.decode('utf-8')
                  self.canvas.create_text(30,400, text='Volume Label: '+texto,anchor=tk.W)
                  
                  volumen=file.read(8)
                  texto=volumen.decode('utf-8')
                  self.canvas.create_text(30,420, text='File System Type: '+texto,anchor=tk.W)
                  
                  file.seek(448,1)
                  signaturabs=file.read(4)
                  i=int.from_bytes(signaturabs,byteorder='little')
                  self.canvas.create_text(30,440, text='Boot Sector signature: '+format(i,'X'),anchor=tk.W)
                  
     def show_fat(self):
         
         if self.fname == None:
             self.show_error1()
         else:
             self.canvas.delete("all")
             w = self.canvas.winfo_width() 
             h = self.canvas.winfo_height()
             nData=math.floor((self.nSectors-self.rSectors-self.numFats*self.sectorsXFAT)/self.sectorsXclusters) #se
             self.canvas.delete(tk.ALL)
             with open(self.fname,mode='rb') as file:              
                  file.seek(self.sectorsXclusters * self.rootEntries)
                  ## Lee solo las primeras 512 entradas de la FAT
                  fat = []
                  for i in range(nData):
                      byte=file.read(2)
                      i=int.from_bytes(byte,byteorder='little',signed=True)
                      fat.append(i)                  
                  cont = 0
                  for j in range(0,h,30):
                      for i in range(0,w,30):
                          if fat[cont] != 0:
                              if cont == 0 or cont == 1: 
                                  self.canvas.create_rectangle(i,j,i+30,j+30,fill="red", outline = 'black')
                              else:
                                  self.canvas.create_rectangle(i,j,i+30,j+30,fill="yellow", outline = 'black')
                                  self.canvas.create_text(i+15,j+15,text=str(fat[cont]))
                          else: 
                              self.canvas.create_rectangle(i,j,i+30,j+30,fill="white", outline = 'black') 
                          cont += 1
                          if cont == self.sectorsXclusters * self.rootEntries:
                              return
                        
     def show_rootdir(self):
            pass
                       
     def show_error1(self):
            msg = "No se ha elegido la imagen del sistema de archivos"
            mb.showerror("Error", msg)
            
     def show_error2(self):
            msg = "El archivo no contiene imagen de sistema de archivos Ext2"
            mb.showerror("Error", msg)
            
if __name__ == "__main__":
       app = App()
       app.mainloop()
