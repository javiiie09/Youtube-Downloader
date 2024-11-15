import concurrent.futures
import multiprocessing
import threading
from concurrent.futures import ThreadPoolExecutor
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox

from pytubefix import YouTube, Playlist
from pytubefix.exceptions import VideoUnavailable, RegexMatchError

executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())


def actualizar_progreso(valor):
    progress_bar["value"] = valor
    progreso_texto.set(f"{int(valor)}%")


def mostrar_mensaje(mensaje):
    estado.set(mensaje)


def toggle_buttons(state):
    boton_mp3["state"] = state
    boton_mp4["state"] = state


def descargar_mp3():
    enlace = videos.get()

    if not enlace:
        mostrar_mensaje("Por favor, introduce una URL.")
        return

    toggle_buttons("disabled")

    def proceso_descarga_mp3():
        try:
            if not var.get():
                video = YouTube(enlace, on_progress_callback=progress_callback)
                mostrar_mensaje(f"Descargando {video.title}...")
                descargar_audio(video)
            else:
                descargar_playlist(enlace, True)

        except VideoUnavailable:
            mostrar_mensaje("El video no está disponible.")
        except RegexMatchError:
            mostrar_mensaje("URL inválida.")
        except Exception as e:
            mostrar_mensaje(f"error: {e}")
        finally:
            toggle_buttons("normal")

    threading.Thread(target=proceso_descarga_mp3).start()


def descargar_mp4():
    enlace = videos.get()

    if not enlace:
        mostrar_mensaje("Por favor, introduce una URL.")
        return
    toggle_buttons("disabled")

    def proceso_descarga_mp4():
        try:
            if not var.get():
                video = YouTube(enlace, on_progress_callback=progress_callback)
                mostrar_mensaje(f"Descargando {video.title}...")
                descargar_video(video)
            else:
                descargar_playlist(enlace, False)

        except VideoUnavailable:
            mostrar_mensaje("El video no está disponible.")
        except RegexMatchError:
            mostrar_mensaje("URL inválida.")
        except Exception as e:
            mostrar_mensaje(f"Error inesperado: {e}")
        finally:
            toggle_buttons("normal")

    threading.Thread(target=proceso_descarga_mp4).start()


def descargar_playlist(enlace, es_audio):
    playlist = Playlist(enlace)

    if playlist.length == 0:
        mostrar_mensaje("No hay videos en la lista.")
        return

    mostrar_mensaje(f"Descargando playlist {playlist.title}...")
    futures = [executor.submit(descargar_audio if es_audio else descargar_video, v) for v in playlist.videos]

    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        future.result()
        actualizar_progreso((i + 1) / playlist.length * 100)

    mostrar_mensaje(f"Playlist descargada correctamente.")


def descargar_audio(video):
    try:
        audio_stream = video.streams.get_audio_only()
        audio_stream.download(filename_prefix="Audio Only - ")
        mostrar_mensaje(f"{video.title} descargado.")

    except Exception as e:
        mostrar_mensaje(f"error: {e}")


def descargar_video(video):
    try:
        video_stream = video.streams.get_highest_resolution()
        video_stream.download(filename_prefix="Video + Audio - ")
        mostrar_mensaje(f"{video.title} descargado.")

    except Exception as e:
        mostrar_mensaje(f"error: {e}")


def progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    downloaded_size = total_size - bytes_remaining
    percent = (downloaded_size / total_size) * 100
    actualizar_progreso(percent)


# Popup con información de la aplicación
def popup1():
    MessageBox.showinfo("Youtube Downloader Version", "Version: 1.2\n"
                                                      "Autor: javiiie09")


root = Tk()  # Definición Interfaz de la ventana
root.config(bd=60)  # Tamaño de la ventana
root.title("Youtube Downloader")  # Nombre de la ventana
root.minsize(400, 300)
root.resizable(False, False)

# Menú barra superior
menubar = Menu(root)
root.config(menu=menubar)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Archivo", menu=helpmenu)
helpmenu.add_command(label="Versión", command=popup1)
helpmenu.add_command(label="Salir", command=root.destroy)

frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

# Cuadro URL
instrucciones = Label(frame, text="Introduce la dirección URL del vídeo o playlist")
instrucciones.grid(row=0, column=0)

videos = ttk.Entry(frame, width=40)
videos.grid(row=1, column=0)

# Casilla selección Playlist
var = IntVar()
check = ttk.Checkbutton(frame, text="Playlist", variable=var, onvalue=1, offvalue=0)
check.grid(row=4, column=0, pady=5)

# Botón descarga mp3
boton_mp3 = ttk.Button(frame, text="Descargar Solo Audio", command=descargar_mp3)
boton_mp3.grid(row=2, column=0, pady=5)

# Botón descarga mp4
boton_mp4 = ttk.Button(frame, text="Descargar Video", command=descargar_mp4)
boton_mp4.grid(row=3, column=0, pady=0)

# Texto de estado
estado = StringVar()
estado.set("Esperando acción...")
label_estado = Label(frame, textvariable=estado, fg="green")
label_estado.grid(row=5, column=0, pady=0)

progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=6, column=0, pady=10)

progreso_texto = StringVar()
progreso_texto.set("0%")
label_progreso = Label(frame, textvariable=progreso_texto, fg="blue")
label_progreso.grid(row=7, column=0, pady=5)

if __name__ == "__main__":
    root.mainloop()
