import tkinter as tk
from tkinter import filedialog as fd
import datetime
import os
import shutil

from tkinter import messagebox as msb


class Application:
    fileName = datetime.datetime.today().strftime('%Y-%m-%d')
    directory = ""
    pathDestination = ""
    mainFilePath = ""
    nameNewFile = ""
    listLocalizationsToBackup = ""
    listCopiedFiles = []

    def __init__(self):
        self.window = tk.Tk()
        self.window.bind("<Button-1>", self.click_ppm_lpm_controller)
        self.window.bind("<Button-3>", self.click_ppm_lpm_controller)
        textInfo =  "Witaj, \n kliknij w to okno aby wybrać lokalizację pliku z listą katalogów\n "
        self.displayInfo(textInfo)

        self.window.mainloop()

    def displayInfo(self, textInfo):
        text = tk.StringVar()
        label = tk.Label(self.window, textvariable=text, padx=100, pady=20)
        label.pack()
        text.set(textInfo)

    def click_ppm_lpm_controller (self, event):

        self.listLocalizationsToBackup = self.openFile()

        if msb.askokcancel("Wybór folderu do zapisu backapu", "Wybierz folder w ktorym zostanie zapisana kopia zapasowa"):
            self.createDirectoryToBackup()
        if msb.askokcancel("Czy rozpoczać backup?", "Czy rozpocząć tworzenie kopii zapasowej?"):
            self.runBackup(self.listLocalizationsToBackup)

        print("Backup gotowy")
        newTextInfo = " Zostały skopiowane pliki:"
        self.displayInfo(newTextInfo)
        for file in self.listCopiedFiles:
            newTextInfo = file
            self.displayInfo(newTextInfo)




    def createDirectoryToBackup(self):

        self.directory = fd.askdirectory()  # wskazanie ścieżki do folderu docelowego
        if self.directory:
            msb.showinfo("Info", "Wybrano taki folder {folder} do zapisu plików.".format(folder=self.directory))
            directoryName = str(self.getDateToDirectoryName())

        if directoryName:
            print ("Nazwa katalogu to %s"%directoryName)
            fullPathAndName = self.createDirectoryPath(directoryName)
            if os.path.isdir(fullPathAndName):
                fullPathAndName = fullPathAndName + datetime.datetime.today().strftime("_%H-%M-%S")
                os.mkdir(fullPathAndName)
                self.pathDestination = fullPathAndName
                if os.path.exists(fullPathAndName):
                    print("Pełna ścieżka i nazwa katalogu: %s"%fullPathAndName)

            else:
                os.mkdir(fullPathAndName)
                if os.path.exists(fullPathAndName):
                    print("Pełna ścieżka i nazwa katalogu: %s"%fullPathAndName)

    def getDateToDirectoryName(self):
        self.fileName = datetime.datetime.today().strftime('%Y-%m-%d')
        return self.fileName

    def createDirectoryPath(self, directoryName):
        path = os.path.join(self.directory, directoryName)
        self.pathDestination = path
        return path

    def openFile(self):
        filename = fd.askopenfilename(filetypes=[("Plik tekstowy","*.txt")]) # wywołanie okna dialogowego open file
        if filename:
            readFiles = open(filename, "r")
            contetnReadFiles= readFiles.readlines()
            readFiles.close()
        return  contetnReadFiles

    def runBackup(self,srcBackup):
        for src in srcBackup:
            self.createBackup(src, self.pathDestination)

    def walidacjaSciezki(self,path):
        newPath = path.replace('\n', '')
        newPath = newPath.replace("/[/]+", "/")
        newPath = newPath.replace("\[\]+", "\\")
        if (newPath[len(newPath)-1]!="\\" or newPath[len(newPath)-1]!="/"):
            newPath = newPath+"/"

        return newPath

    def createBackup(self,src,dst):
        dir_src = self.walidacjaSciezki(src)
        dir_dst = self.walidacjaSciezki(dst)

        for fileName in os.listdir(dir_src):
            if fileName.endswith(".txt"):
                shutil.copy(dir_src + fileName, dir_dst)
            print("skopiowano %s" % fileName)
            self.listCopiedFiles.append(fileName)






apl = Application()