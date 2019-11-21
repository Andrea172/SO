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
         self.fname = None
         self.sectorsxClusters = 0
         self.rootEntries = 0
         self.reservedSectors = 0
         self.totalSectors = 0
         self.numFats = 0
         self.sectorsPerFat = 0
         self.bytesRead=0
         self.bytesPerSector=0
         self.numberTracks = 0
         
         self.title("Visor File System FAT") 
         root = tk.Tk()
         self.width = 540
         self.height = 1000000
         self.frame=tk.Frame(self,width=300,height=300)
         self.frame.grid(row=5,column=0)
         
         self.canvas = tk.Canvas( self.frame,width=480, height=480, bg="white")
         vbar = tk.Scrollbar(self.frame, orient = tk.VERTICAL)
         vbar.pack(side=tk.RIGHT,fill=tk.Y)
         vbar.config(command=self.canvas.yview)


         btn_file = tk.Button(self, text="Choose file system image",command=self.choose_file)         
         btn_showBoot = tk.Button(self, text="Boot Sector",command=self.show_bootsector)
         btn_showFat = tk.Button(self, text="File Allocation Table",command=self.show_fat)
         btn_showRootDir = tk.Button(self, text="Root directory",command=self.show_rootdir)                  
         btn_file.grid(row=0, column=0, columnspan=2, padx=60,pady=20 )                 
         btn_showBoot.grid(row=1, column=0)
         btn_showFat.grid(row=1, column=1)
         btn_showRootDir.grid(row=2, column=0, columnspan=2,padx=60,pady=20,sticky='nswe')

         ##self.canvas.grid(row=3, column=0,rowspan=3, columnspan=2)
         self.canvas.config( yscrollcommand=vbar.set)
         self.canvas.pack(side = tk.LEFT, expand=True, fill=tk.BOTH)
         ##self.canvas.config(highlightthickness=0)  


         
           
     def choose_file(self):
         filetypes = (("File sistem images", "*.img"),("All files", "*"))
         filename = fd.askopenfilename(title="Open file", initialdir="/home/alejandro/SourceCode/Python", filetypes=filetypes)
         self.fname = filename
         with open(self.fname,mode='rb') as file:
         	file.seek(54,1)
         	volumen=file.read(8)
         	texto=volumen.decode('utf-8')
         	if 'FAT' not in texto:
         		self.show_error1()
         		self.fname= None



               
               
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
                  self.bytesPerSector= i
                  
                  sectorespc=file.read(1)
                  i=int.from_bytes(sectorespc,byteorder='little')
                  self.canvas.create_text(30,100, text='Sectors per Cluster: '+str(i),anchor=tk.W)
                  self.sectorsxClusters = i
                  
                  sectoresr = file.read(2)
                  i=int.from_bytes(sectoresr,byteorder='little')
                  self.canvas.create_text(30,120, text='Reserved sectors: '+str(i),anchor=tk.W)
                  self.reservedSectors = i
                  
                  nfats=file.read(1)
                  i=int.from_bytes(nfats,byteorder='little')   
                  self.canvas.create_text(30,140, text='Number of FAT copies: '+str(i),anchor=tk.W)
                  self.numFats =  i
                  
                  entradasRaizdir = file.read(2)
                  i=int.from_bytes(entradasRaizdir,byteorder='little')
                  self.canvas.create_text(30,160, text='Number of possible root entries: '+str(i),anchor=tk.W)
                  self.rootEntries = i
                  
                  sectorest=file.read(2)
                  i=int.from_bytes(sectorest,byteorder='little')                  
                  self.canvas.create_text(30,180, text='Small number of sectors: '+str(i),anchor=tk.W)
                  self.totalSectors += i 
                                    
                  descriptorm=file.read(1)
                  i=int.from_bytes(descriptorm,byteorder='little')
                  self.canvas.create_text(30,200, text='Media Descriptor: '+format(i,'X'),anchor=tk.W)
                                    
                  sectorespf=file.read(2)
                  i=int.from_bytes(sectorespf,byteorder='little')
                  self.canvas.create_text(30,220, text='Sectors per FAT: '+str(i),anchor=tk.W)
                  self.sectorsPerFat = i
                  
                  sectorespt=file.read(2)
                  i=int.from_bytes(sectorespt,byteorder='little')
                  self.canvas.create_text(30,240, text='Sectors per Track: '+str(i),anchor=tk.W)
                  self.numberTracks = i
                 
                  numerodec=file.read(2)
                  i=int.from_bytes(numerodec,byteorder='little')
                  self.canvas.create_text(30,260, text='Number of Heads: '+str(i),anchor=tk.W)
                  
                  sectoreso=file.read(4)
                  i=int.from_bytes(sectoreso,byteorder='little')
                  self.canvas.create_text(30,280, text='Hidden Sectors: '+str(i),anchor=tk.W)
                  
                  sectorestl=file.read(4)
                  i=int.from_bytes(sectorestl,byteorder='little')
                  self.canvas.create_text(30,300, text='Large number of sectors: '+str(i),anchor=tk.W)
                  self.totalSectors += i 
                  
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
                  if ("FAT32" in texto):	
                     self.bytesRead=4
                  else:
                      self.bytesRead=2

                  
                  file.seek(448,1)
                  signaturabs=file.read(4)
                  i=int.from_bytes(signaturabs,byteorder='little')
                  self.canvas.create_text(30,440, text='Boot Sector signature: '+format(i,'X'),anchor=tk.W)
                  
     def show_fat(self):
         
         if self.fname == None:
             self.show_error1()
         else:
             self.canvas.delete("all")
             #w = self.canvas.winfo_width() 
             #h = self.canvas.winfo_height()
             w=self.width
             h=self.height
             self.canvas.delete(tk.ALL)
             q = self.rootEntries * self.sectorsxClusters
             #c = math.floor((self.totalSectors-self.reservedSectors-self.numFats*self.sectorsPerFat)/self.sectorsxClusters)            
             c= int((self.sectorsPerFat*self.bytesPerSector )/self.bytesRead)

             with open(self.fname,mode='rb') as file:              
                  file.seek(q)
                  ## Lee solo las primeras 512 entradas de la FAT
                  fat = []
                  for i in range(c):
                      byte=file.read(self.bytesRead)
                      i=int.from_bytes(byte,byteorder='little',signed=True)
                      fat.append(i)                  
                  cont = 0
                  for j in range(0,h,40):
                      for i in range(0,w,40):
                          if fat[cont] != 0:
                              if cont == 0 or cont == 1: 
                                  self.canvas.create_rectangle(i,j,i+40,j+40,fill="red", outline = 'black')
                              else:
                                  self.canvas.create_rectangle(i,j,i+40,j+40,fill="yellow", outline = 'black')
                                  self.canvas.create_text(i+20,j+20,text=str(fat[cont]))
                          else: 
                              self.canvas.create_rectangle(i,j,i+40,j+40,fill="white", outline = 'black') 
                          cont += 1
                          if cont == c:
                              return
                        
     def show_rootdir(self):
     	if self.fname == None:
     		self.show_error1()
     	else:
     		self.canvas.delete("all")
     	q = (self.reservedSectors+self.numFats*self.sectorsPerFat)*self.bytesPerSector

     	with open(self.fname,mode='rb') as file:   
     		file.seek(q)
     		desplaza = 20
     		for j in range(self.numberTracks): 
     		#byte= file.read(1)
     		#i=int.from_bytes(byte,byteorder='little',signed=True)
     		#if (format(i,'X')== format(0,'X')):pass

     		    name=file.read(8).decode('latin_1')
     		    ext = file.read(3).decode('latin_1')
     		    byte=file.read(15)
     		    byte=file.read(2)
     		    firstCluster=int.from_bytes(byte,byteorder='little',signed=True)
     		    byte = file.read(4)
     		    sizeFile = int.from_bytes(byte,byteorder='little',signed=True)

     		    if (firstCluster>0):
     		    	self.canvas.create_text(30,desplaza, text='File name: '+name +'.'+ext,anchor=tk.W)
     		    	desplaza=desplaza+20
     		    	self.canvas.create_text(30,desplaza, text='Inicio de cluster: '+str(firstCluster),anchor=tk.W)
     		    	desplaza=desplaza+20
     		    	self.canvas.create_text(30,desplaza, text='Size: '+str(sizeFile),anchor=tk.W)
     		    	desplaza = desplaza + 20


            
                       
     def show_error1(self):
            msg = "No se ha elegido la imagen del sistema de archivos"
            mb.showerror("Error", msg)
            
     def show_error2(self):
            msg = "El archivo no contiene imagen de sistema de archivos Ext2"
            mb.showerror("Error", msg)
            
if __name__ == "__main__":
       app = App()
       app.mainloop()