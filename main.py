from tkinter import Tk, Label, Entry, Button, StringVar
from tkinter.ttk import Progressbar, Style
from pytube import YouTube
from pytube import Playlist
import os
import moviepy.editor as mp
import re
import threading

class YouTubeDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Playlist Downloader")

        largura = 600
        altura = 300
        tela_l = master.winfo_screenwidth()
        tela_a = master.winfo_screenheight()
        x = (tela_l - largura) // 2
        y = (tela_a - altura) // 2
        master.geometry(f"{largura}x{altura}+{x}+{y}")

        self.label = Label(master, text="Digite o link da playlist:")
        self.label.pack(pady=50)

        self.entry = Entry(master, width=60)
        self.entry.pack(pady=10)

        self.download = Button(master, text="Baixar", command=self.download_and_convert)
        self.download.pack()

        self.barra_progresso = Label(master, text="")
        self.barra_progresso.pack()

        self.progress_var = StringVar()
        style = Style()
        style.configure("TProgressbar",
                        thickness=20,
                        troughcolor='gray', 
                        background='green')  

        self.progress = Progressbar(master, orient="horizontal", length=500, mode="determinate",
                                    variable=self.progress_var, style="TProgressbar")
        self.progress.pack(pady=10)

    def download_and_convert(self):
        link = self.entry.get()

        diretorio = os.getcwd() + '/Songs'
        playlist = Playlist(link)

        total = len(playlist)
        cont_arq= 0

        for url in playlist:
            video = YouTube(url)
            video_title = video.title
            self.barra_progresso.config(text=f"Baixando: {video_title}")
            self.master.update()

            video.streams.first().download(diretorio)
            cont_arq+= 1
            porcentagem = (cont_arq/ total) * 100
            self.progress_var.set(porcentagem)
            self.progress.update()

        for arquivo in os.listdir(diretorio):
            if re.search('mp4', arquivo):
                mp4 = os.path.join(diretorio, arquivo)
                mp3 = os.path.join(diretorio, os.path.splitext(arquivo)[0] + '.mp3')
                new = mp.AudioFileClip(mp4)
                new.write_audiofile(mp3)
                os.remove(mp4)

        self.barra_progresso.config(text="Download concluído! :)")

if __name__ == "__main__":
    tk = Tk()
    app = YouTubeDownloaderGUI(tk)
    tk.mainloop()