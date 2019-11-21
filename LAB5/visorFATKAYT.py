# Autor: Prof. Alejandro T. Bello Ruiz
# Curso: INF239 Sistemas Operativos
# Laboratorio 5
#hexdump -C FAT16.img | less
from tkinter import ttk
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.fname = None
        self.title("Visor File System FAT") 

        self.width = 540
        self.height = 100000
        self.frame = tk.Frame(self,width=self.width, height=self.height)
        self.frame.grid(row=5, column=0)  

        self.canvas = tk.Canvas(self.frame, width=560, height=480, bg="white")
        hbar=tk.Scrollbar(self.frame,orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM,fill=tk.X)
        hbar.config(command=self.canvas.xview)
        vbar=tk.Scrollbar(self.frame,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=self.canvas.yview)
        
        self.canvas.config(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        self.canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        self.frame2 = tk.Frame(self, width=500, height=250)
        self.frame2.grid(row=1, column=0)
        self.canvas2 = tk.Canvas(self.frame2,width=500, height=250, bg="white")
        
        btn_file = tk.Button(self.frame2, text="Choose file system image",command=self.choose_file)         
        btn_showBoot = tk.Button(self.frame2, text="Boot Sector",command=self.show_bootsector)
        btn_showFat = tk.Button(self.frame2, text="File Allocation Table",command=self.show_fat)
        btn_showRootDir = tk.Button(self.frame2, text="Root directory",command=self.show_rootdir)                  
        #self.canvas.grid(row=3, column=0,rowspan=3, columnspan=2)

        self.bytesLeer = None
        self.bytesInSector = None
        self.nroFat = None 
        self.sectorInFat  = None
        self.sectoresReservados = None
        self.entradasDirectory = None
        self.sectoresPerTrack = None
        self.clustersRoot = []
        self.fat = []
        self.initCluster = None
        self.comboBox = tk.ttk.Combobox(self.frame2, values=self.clustersRoot)
        self.comboBox.bind("<<ComboboxSelected>>",self.pintarCluster)
        self.comboBox.grid(row=3,column=0, columnspan=2)
        btn_file.grid(row=0, column=0, columnspan=2, padx=60,pady=20 )
        btn_showBoot.grid(row=1, column=0)
        btn_showFat.grid(row=1, column=1)
        btn_showRootDir.grid(row=2, column=0, columnspan=2,padx=60,pady=20,sticky='nswe')
         
    def choose_file(self):
        filetypes = (("File sistem images", "*.img"),("All files", "*"))
        filename = fd.askopenfilename(title="Open file", initialdir="/home/alejandro/SourceCode/Python", filetypes=filetypes)
        self.fname = filename
        with open(self.fname,mode='rb') as file:
            file.seek(54)
            name = str(file.read(8))
            #print(name)
            if 'FAT' not in name:
                self.show_error2()
        
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
                self.bytesInSector = i
                self.canvas.create_text(30,80, text='Bytes per Sector: '+str(i),anchor=tk.W)
                
                sectorespc=file.read(1)
                i=int.from_bytes(sectorespc,byteorder='little')
                self.canvas.create_text(30,100, text='Sectors per Cluster: '+str(i),anchor=tk.W)
                
                sectoresr = file.read(2)
                i=int.from_bytes(sectoresr,byteorder='little')
                self.sectoresReservados = i
                self.canvas.create_text(30,120, text='Reserved sectors: '+str(i),anchor=tk.W)
                
                nfats=file.read(1)
                i=int.from_bytes(nfats,byteorder='little')
                self.nroFat = i
                self.canvas.create_text(30,140, text='Number of FAT copies: '+str(i),anchor=tk.W)
                
                entradasRaizdir = file.read(2)
                i=int.from_bytes(entradasRaizdir,byteorder='little')
                self.entradasDirectory = i
                self.canvas.create_text(30,160, text='Number of possible root entries: '+str(i),anchor=tk.W)
                
                sectorest=file.read(2)
                i=int.from_bytes(sectorest,byteorder='little')                  
                self.canvas.create_text(30,180, text='Small number of sectors: '+str(i),anchor=tk.W)
                                
                descriptorm=file.read(1)
                i=int.from_bytes(descriptorm,byteorder='little')
                self.canvas.create_text(30,200, text='Media Descriptor: '+format(i,'X'),anchor=tk.W)
                                
                sectorespf=file.read(2)
                i=int.from_bytes(sectorespf,byteorder='little')
                self.sectorInFat  = i
                self.canvas.create_text(30,220, text='Sectors per FAT: '+str(i),anchor=tk.W)
                
                sectorespt=file.read(2)
                i=int.from_bytes(sectorespt,byteorder='little')
                self.sectoresPerTrack = i
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
                if("FAT16" in texto):
                    self.bytesLeer=2
                elif("FAT32" in texto):
                    self.bytesLeer=4
                self.canvas.create_text(30,420, text='File System Type: '+texto,anchor=tk.W)
                
                file.seek(448,1)
                signaturabs=file.read(4)
                i=int.from_bytes(signaturabs,byteorder='little')
                self.canvas.create_text(30,440, text='Boot Sector signature: '+format(i,'X'),anchor=tk.W)

    def pintarCluster(self,event=None):
        # print(self.comboBox.get())
        self.canvas.delete("all")
        if event:
            self.initCluster = int(event.widget.get())
            print(event.widget.get())

            #w = self.canvas.winfo_width() 
            #h = self.canvas.winfo_height()
            w = self.width 
            h = self.height
            self.canvas.delete(tk.ALL)
            cont = 0
            cadenaCluster = []
            pos = int(self.initCluster)
            cadenaCluster.append(pos)
            while True:
                if self.fat[pos] == -1:
                    break
                pos = self.fat[pos]    
                cadenaCluster.append(pos)
            self.comboBox['values'] = self.clustersRoot
            self.comboBox.current(0)
            for j in range(0,h,40):
                for i in range(0,w,40):
                    if self.fat[cont] != 0:
                        if cont == 0 or cont == 1: 
                            self.canvas.create_rectangle(i,j,i+40,j+40,fill="red", outline = 'black')
                        elif cont in cadenaCluster:
                            self.canvas.create_rectangle(i,j,i+40,j+40,fill="blue", outline = 'black')
                        else:
                            self.canvas.create_rectangle(i,j,i+40,j+40,fill="yellow", outline = 'black')
                            self.canvas.create_text(i+20,j+20,text=str(self.fat[cont]))
                    else: 
                        self.canvas.create_rectangle(i,j,i+40,j+40,fill="white", outline = 'black') 
                    cont += 1
                    if cont == self.sectorInFat*self.bytesInSector/self.bytesLeer:
                        return
            

    def show_fat(self):
        
        if self.fname == None:
            self.show_error1()
        else:
            self.canvas.delete("all")
            #w = self.canvas.winfo_width() 
            #h = self.canvas.winfo_height()
            w = self.width 
            h = self.height
            self.canvas.delete(tk.ALL)
            
            self.comboBox['values'] = self.clustersRoot
            self.comboBox.current(0)
            
            with open(self.fname,mode='rb') as file:              
                file.seek(self.sectoresReservados * self.bytesInSector)
                ## Lee solo las primeras 512 entradas de la FAT
                for i in range(int(self.sectorInFat*self.bytesInSector/self.bytesLeer)):
                    byte=file.read(self.bytesLeer)
                    i=int.from_bytes(byte,byteorder='little',signed=True)
                    self.fat.append(i)
                cadenaCluster = []
                pos = int(self.initCluster)
                cadenaCluster.append(pos)
                while True:
                    if self.fat[pos] == -1:
                        break
                    pos = self.fat[pos]    
                    cadenaCluster.append(pos)
                
                cont = 0
                for j in range(0,h,40):
                    for i in range(0,w,40):
                        if self.fat[cont] != 0:
                            if cont == 0 or cont == 1: 
                                self.canvas.create_rectangle(i,j,i+40,j+40,fill="red", outline = 'black')
                            elif cont in cadenaCluster:
                                self.canvas.create_rectangle(i,j,i+40,j+40,fill="blue", outline = 'black')
                            else:
                                self.canvas.create_rectangle(i,j,i+40,j+40,fill="yellow", outline = 'black')
                                self.canvas.create_text(i+20,j+20,text=str(self.fat[cont]))
                        else: 
                            self.canvas.create_rectangle(i,j,i+40,j+40,fill="white", outline = 'black') 
                        cont += 1
                        if cont == self.sectorInFat*self.bytesInSector/self.bytesLeer:
                            return

    def show_rootdir(self):
        self.canvas.delete(tk.ALL)

        with open(self.fname,mode='rb') as file:
            inicioRootDir = self.nroFat*self.sectorInFat*self.bytesInSector + self.sectoresReservados * self.bytesInSector
            file.seek(inicioRootDir)
            desplaza=20 

            for i in range(self.sectoresPerTrack):
                # cada entrada es de 32 bytes dice google 
                name = file.read(8).decode('latin_1')
                exte = file.read(3).decode('latin_1')
                filename = name+"."+exte
                file.read(15)

                startCluster = file.read(2)
                startCluster = int.from_bytes(startCluster,byteorder='little')
                filesize = int.from_bytes(file.read(4),byteorder='little')
                
                if (startCluster > 0):
                    self.canvas.create_text(20 , desplaza, text="filename: " + str(filename),anchor=tk.W)
                    desplaza += 20
                    self.canvas.create_text(20 , desplaza, text="inicio del cluster: " + str(startCluster),anchor=tk.W)
                    if startCluster not in self.clustersRoot:
                        self.clustersRoot.append(startCluster)
                    desplaza += 20
                    self.canvas.create_text(20 , desplaza, text="tamannho: " + str(filesize),anchor=tk.W)
                    desplaza += 20

    def show_error1(self):
        msg = "No se ha elegido la imagen del sistema de archivos"
        mb.showerror("Error", msg)
        
    def show_error2(self):
        msg = "El archivo no contiene imagen de sistema de archivos FAT"
        mb.showerror("Error", msg)
            
if __name__ == "__main__":
    app = App()
    app.mainloop()