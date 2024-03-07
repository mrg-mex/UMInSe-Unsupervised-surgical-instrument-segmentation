# -*- coding: utf-8 -*-
"""
Autores:
    Rodrigo Eduardo Arevalo Ancona
    Daniel Haro Mendoza
    Manuel Cedillo Hernández
    Víctor Javier Gonzalez Villela
    
Instituto Politécnico Nacional ESIME SEPI-Culhucán
Universidad Nacional Autónoma de México

Enero 2024

Software para la segmentación de instrumentos quirúrgicos
"""



import os
import cv2
import time
import segmentacion
import tkinter as tk
import numpy as np
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


# Función para crear una carpeta si no existe
def create_folder(nombre):
    try:
        os.stat(nombre)
    except:
        os.mkdir(nombre)

class DualVideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Software para la Segmentación de Instrumentos Quirúrgicos No Superivsado")
        self.root.geometry("1200x800")

        # Variables para el primer video
        self.video_source_1 = None
        self.cap_1 = None
        self.paused_1 = False
        self.photo_1 = None

        # Variables para el segundo video
        self.video_source_2 = None
        self.cap_2 = None
        self.paused_2 = False
        self.photo_2 = None

        # Canvas para mostrar video 1
        self.video_canvas_1 = tk.Canvas(root, width=500, height=500, bg='#333')
        self.video_canvas_1.pack()
        self.video_canvas_1.place(x=20, y=20)

        # Canvas para mostrar video 2
        self.video_canvas_2 = tk.Canvas(root, width=500, height=500, bg='#333')
        self.video_canvas_2.pack()
        self.video_canvas_2.place(x=550, y=20)

        # Label mostrar ruta del video 1
        self.lbl_video_path_1 = tk.Label(root, text="Ruta del Video: No seleccionado")
        self.lbl_video_path_1.pack(pady=5)
        self.lbl_video_path_1.place(x=20, y=530)

        # Botones para el primer video
        self.btn_open_1 = tk.Button(root, text="Abrir Video 1", command=self.open_video_1, width=15, height=2)
        self.btn_open_1.pack(pady=10)
        self.btn_open_1.place(x=20, y=570)
        
        # Botón para reproducir el video original
        self.btn_play_1 = tk.Button(root, text="Reproducir 1", command=self.play_video_1, width=15, height=2)
        self.btn_play_1.pack(pady=5)
        self.btn_play_1['state'] = 'disabled'
        self.btn_play_1.place(x=150, y=570)
        
        # Botón para pausar o continuar la reproducción del video original
        self.btn_pause_1 = tk.Button(root, text="Pausar/Continuar 1", command=self.pause_video_1, width=15, height=2)
        self.btn_pause_1.pack(pady=5)
        self.btn_pause_1['state'] = 'disabled'
        self.btn_pause_1.place(x=280, y=570)
        
        # Botón para detener la reproducción del video original
        self.btn_stop_1 = tk.Button(root, text="Detener 1", command=self.stop_video_1, width=15, height=2)
        self.btn_stop_1.pack(pady=5)
        self.btn_stop_1['state'] = 'disabled'
        self.btn_stop_1.place(x=410, y=570)

        # Label mostrar ruta del video 2
        self.lbl_video_path_2 = tk.Label(root, text="Ruta del Video Segmentado: No seleccionado")
        self.lbl_video_path_2.pack(pady=5)
        self.lbl_video_path_2.place(x=550, y=530)

        # Botón para reproducir el video segmentado
        self.btn_play_2 = tk.Button(root, text="Reproducir 2", command=self.play_video_2, width=15, height=2)
        self.btn_play_2.pack(pady=5)
        self.btn_play_2['state'] = 'disabled'
        self.btn_play_2.place(x=630, y=570)
        
        # Botón para pausar o continuar reproduciendo el video segmentado 
        self.btn_pause_2 = tk.Button(root, text="Pausar/Continuar 2", command=self.pause_video_2, width=15, height=2)
        self.btn_pause_2.pack(pady=5)
        self.btn_pause_2['state'] = 'disabled'
        self.btn_pause_2.place(x=770, y=570)
        
        # Botón para Detener el video Segmentado
        self.btn_stop_2 = tk.Button(root, text="Detener 2", command=self.stop_video_2, width=15, height=2)
        self.btn_stop_2.pack(pady=5)
        self.btn_stop_2['state'] = 'disabled'
        self.btn_stop_2.place(x=910, y=570)

        # Botón para salir de la aplicación
        self.btn_exit = tk.Button(root, text="Salir", command=self.exit_app, width=15, height=2)
        self.btn_exit.pack(pady=10)
        self.btn_exit.place(x=1070, y=710)
        
        # Botón Para realizar el proceso de segmetnación de los intrumentos quirúrgicos
        self.btn_show_path = tk.Button(root, text="Detección de los de los instrumentos quirúrgicos", 
                                       command=self.segmentar_video, width=40, height=2)
        self.btn_show_path.pack(pady=5)
        self.btn_show_path.place(x=20, y=630)
        self.btn_show_path['state'] = 'disabled'
        self.btn_show_path.bind("<Enter>", self.on_enter)
        self.btn_show_path.bind("<Leave>", self.on_leave)
     
    def on_enter(self, event):
        event.widget.config(relief="raised")
        event.widget.config(bg='gray80')

    def on_leave(self, event):
        event.widget.config(relief="raised")
        event.widget.config(bg='gray90')
    
    # Segmentación de instrumentos quirúrgicos
    def segmentar_video(self):
       if self.video_source_1:
           
            # Ruta del archivo de video de entrada
            video_path = self.video_source_1
            # Abre el archivo de video
            cap = cv2.VideoCapture(video_path)

            # Verifica si el video se abrió correctamente
            if not cap.isOpened():
               print("Error al abrir el video.")
               exit()

            # Obtén las propiedades del video original
            fps = cap.get(cv2.CAP_PROP_FPS)
            ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
           
            create_folder('Segmentado/')
            # Crea un objeto VideoWriter para el video de salida en formato AVI
            output_video_path = 'Segmentado/video_segm.mp4'
            fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
            video_salida = cv2.VideoWriter(output_video_path, fourcc, fps, (ancho, altura))
            
            cont = 1
            
            # Itera sobre los frames del video
            while True:
                
                
                tstart = time.time()
                
                # Lectura de los frames para su segmentación
                frame2 = np.empty((altura, ancho, 3))
                ret, frame = cap.read()
                 
                # Verifica si el video ha llegado al final
                if not ret:
                    break
                
                frame2 = frame.copy()
                
                # Selecciona la zona donde se enfoca la segmentación de los instrumentos quirúrgicos     
                frame2[0::, 0:110, :] = 255
                frame2[0::, 580::, :] = 255
                frame2[0:120, :, :] = 255
                
                # Segmentación de los intrumentos quirúrgicos referente a cada frame
                img_seg = segmentacion.segmentacion(frame2)

                #Escalar los valores de píxeles en el rango [0, 1]
                frame = frame.astype(np.float32) / 255.0
                
                # Definir los parámetros de la transformada gamma
                gamma = 0.5  # Puedes ajustar este valor según tus necesidades
                
                # Aplicar la transformada gamma
                frame = np.power(frame, gamma)
                
                
                # Escalar nuevamente los valores de píxeles al rango [0, 255]
                frame = (frame * 255).astype(np.uint8)
                
                img_seg[0::, 0:110, :] = frame[0::, 0:110, :]
                img_seg[0::, 580::, :] = frame[0::, 580::, :]
                img_seg[0:120, :, :] = frame[0:120, :, :]
                
                # Escribe el frame manipulado en el video de salida
                video_salida.write(img_seg)
                tend = time.time()
                tt = tend-tstart
               
                # Muestra el tiempo aproximado de procesamiento 
                if cont == 1:
                    
                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    tts = tt * total_frames
                    tts = tts / 60
                    mensaje = f"Total de frames a procesar: {total_frames}, Tiempo esperado de procesamiento: {tts} minutos"
                    tk.messagebox.showinfo("Número de Frames", mensaje)
    
    
                print(f'Frame procesado: {cont}')
                cont = cont + 1
            
            # Libera los recursos
            cap.release()
            video_salida.release()
            
            # Muestra el fin del procesamiento
            mensaje = "Proceso de Segmentación Finalizado"
            tk.messagebox.showinfo("Sementación Finalizada", mensaje)
            
            # Asigna el video al label para poder mostrar la segmentación realizada
            file_path = output_video_path
            self.cap_2 = cv2.VideoCapture(file_path)
            self.lbl_video_path_2.config(text="Ruta del Video Segmentado: " + file_path)
            self.btn_play_2['state'] = 'normal'
            self.btn_pause_2['state'] = 'normal'
            self.btn_stop_2['state'] = 'normal'

    # Función para cerrar la interfaz
    def exit_app(self):
        self.root.destroy()
        
    # Función para abrir el video
    def open_video_1(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4;*.avi;*.mkv")])
        if file_path:
            self.video_source_1 = file_path
            self.cap_1 = cv2.VideoCapture(file_path)
            self.lbl_video_path_1.config(text="Ruta del Video 1: " + file_path)
            self.btn_play_1['state'] = 'normal'
            self.btn_pause_1['state'] = 'normal'
            self.btn_stop_1['state'] = 'normal'
            self.btn_show_path['state'] = 'normal'

    # Funciones para reproducir el video
    def play_video_1(self):
        if self.cap_1 is not None and not self.paused_1:
            ret, frame = self.cap_1.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (500, 500))
                self.photo_1 = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video_canvas_1.config(width=500, height=500, bg='#333')
                self.video_canvas_1.create_image(0, 0, anchor=tk.NW, image=self.photo_1)
                self.root.after(10, self.play_video_1)

    def play_video_2(self):
        if self.cap_2 is not None and not self.paused_2:
            ret, frame = self.cap_2.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (500, 500))
                self.photo_2 = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video_canvas_2.config(width=500, height=500, bg='#333')
                self.video_canvas_2.create_image(0, 0, anchor=tk.NW, image=self.photo_2)
                self.root.after(10, self.play_video_2)
                
    # Funciones para pausar los videos y continuar su reproduccción 
    def pause_video_1(self):
        self.paused_1 = not self.paused_1
        if self.paused_1:
            self.btn_play_1['state'] = 'normal'
        else:
            self.btn_play_1['state'] = 'disabled'
            self.play_video_1()

    def pause_video_2(self):
        self.paused_2 = not self.paused_2
        if self.paused_2:
            self.btn_play_2['state'] = 'normal'
        else:
            self.btn_play_2['state'] = 'disabled'
            self.play_video_2()
    
    
    # Funciones para detener los videos
    def stop_video_1(self):
        if self.cap_1 is not None:
            self.cap_1.release()
            self.video_canvas_1.delete("all")
            self.btn_play_1['state'] = 'disabled'
            self.btn_pause_1['state'] = 'disabled'
            self.btn_stop_1['state'] = 'disabled'
            self.paused_1 = False

    def stop_video_2(self):
        if self.cap_2 is not None:
            self.cap_2.release()
            self.video_canvas_2.delete("all")
            self.btn_play_2['state'] = 'disabled'
            self.btn_pause_2['state'] = 'disabled'
            self.btn_stop_2['state'] = 'disabled'
            self.paused_2 = False

if __name__ == "__main__":
    root = tk.Tk()
    app = DualVideoPlayer(root)
    root.mainloop()
