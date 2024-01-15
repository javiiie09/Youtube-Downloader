from pytube import YouTube
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from threading import Thread

"""
Definición método descarga de Audio
"""
def descargarMp3():
    enlace = videos.get()
    video = YouTube(enlace)
    descargamp3 = video.streams.get_audio_only()
    descargamp3.download(filename_prefix="Audio Only - ")

"""
Definición método descarga de Video y Audio en la máxima calidad posible
"""
def descargarVideo():
    enlace = videos.get()
    video = YouTube(enlace)
    descarga = video.streams.get_highest_resolution()
    descarga.download(filename_prefix="Video + Audio - ")

"""
Definición método con información
"""
def popup1():
    MessageBox.showinfo("Youtube Downloader Version", "Version: 1.0\n"
                                                          "Autor: javiiie09")


root = Tk()                         #Definición Interfaz de la ventana
root.config(bd=60)                  #Tamaño de la ventana
root.title("Youtube Downloader")    #Nombre de la ventana

"""
Barra superior de opciones
"""
menubar = Menu(root)
root.config(menu=menubar)
helpmenu = Menu(menubar, tearoff=0)

"""
Submenú
"""
menubar.add_cascade(label="Archivo", menu=helpmenu)
helpmenu.add_command(label="Versión", command=popup1)
helpmenu.add_command(label="Salir", command=root.destroy)

"""
Cuadro para introducir URL del video y botones de descarga
"""
instrucciones = Label(root, text="Introduce la dirección URL del vídeo")
instrucciones.grid(row=0, column=1)

videos = Entry(root)
videos.grid(row=1, column=1)

boton = Button(root, text="Descargar Solo Audio", command=descargarMp3)
boton.grid(row=2, column=1)
boton2 = Button(root, text="Descargar Video", command=descargarVideo)
boton2.grid(row=3, column=1)


root.mainloop()
