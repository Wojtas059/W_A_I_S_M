import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from threading import Thread 
import _thread
import time
import ctypes
from tkinter import filedialog
import os
import serial.tools.list_ports as list_ports
from serial.tools.list_ports_common import ListPortInfo
import struct
import proto_file.proto_comm as proto_comm
import sys
import serial
from kivy.clock import Clock, mainthread
import asyncio
from kivy.loader import Loader
import asynckivy as ak
from kivy.uix.popup import Popup
import queue




class MyGrid(Widget):
    com = ObjectProperty(None)
    comm = None
    port = ''
    csvQueue=queue.Queue()
    def __init__(self, **var_args):
        super(MyGrid, self).__init__(**var_args)


        
    trump =False              
    

    def on_press(self):
        self.trump =True
        try:   
            self.comm = proto_comm.ProtobufComm( self.port, 115200)
            self.comm.stm.flush()
            self.comm.stm.read_all()
            self.comm.stm.flushInput()
            self.comm.stm.flushOutput()
            self.comm.start_data_output()
            self.com.text += "\nRozpozęto pomiar\n\n"
            self.com.text = self.comm.start_pom()
            self.csvQueue.put_nowait(self.comm.start_pom())
            while self.trump:
                line_from_stm_output=self.comm.handle_data()
                self.com.text +=   line_from_stm_output
                self.csvQueue.put_nowait(line_from_stm_output)
            self.comm.stm.flush()
            self.comm.stm.flushInput()
            self.comm.stm.read_all()
            self.comm.stm.flushOutput()
            self.comm.stop_data_output()
            self.comm = None
        except serial.serialutil.SerialException:
             Thread(target = self.error_win("Błąd połączenia się z portem ")).start()
        except struct.error:
            Thread(target = self.error_win('Urządzenie zostało odłączone')).start()
            self.comm.stm.flush()
            self.comm.stm.flushInput()
            self.comm.stm.read_all()
            self.comm.stm.flushOutput()
            self.comm.stop_data_output()
        except TypeError:
            Thread(target = self.error_win("Błąd połączenia się z portem ")).start()
        self.trump =False
        

        
    def spinner_clicked(self, value):
        self.port = value



    def save_file(self):
        self.trump =True
        f = open("zapis.csv", "a")
        dataArray1 = []
        print('Przed loop')
        while(self.csvQueue.qsize( )>0 ):
            dataArray1 = self.csvQueue.get_nowait()
            f.write(str(dataArray1))
        print('Po loop')
        f.close()


    def start_thread(self):
        if not(self.trump):
            self.com.text = "Rozpozęto pomiar"
            Thread(target = self.on_press).start()
        else:
            Thread(target = self.error_win("Już uruchomiłeś pomiar")).start()
        

    def error_win(self, error_txt):
        ctypes.windll.user32.MessageBoxW(None, error_txt, "Error", 0)

    def on_press_false(self):
        if (self.trump):
            self.trump = False
            time.sleep(0.2)
            self.com.text += "Pomiar Zastopowano"
        
    def stop(self):
        time.sleep(0.3)
        Thread(target=self.on_press_false).start()
        


    def save_file_(self):
        Thread(target = self.save_file).start()
        
    def file_load(self):
        filedialog.askopenfilename()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.com.text)
