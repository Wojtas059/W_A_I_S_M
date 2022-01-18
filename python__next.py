
#  importujemy biblioteke o nazwie: kivy
import kivy
kivy.require('1.0.6') # replace with your current kivy version !

# Importujemy z biblioteki kivy.uix.widget metodę/klasę o nazwie: Widget
from kivy.uix.widget import Widget

# Importujemy z biblioteki kivy.properties metodę/klasę o nazwie: ObjectProperty
from kivy.properties import ObjectProperty

# Importujemy z biblioteki threading metodę/klasę o nazwie: Thread

# Rozpoczynamy definicje nowego wątku
from threading import Thread 

#  importujemy biblioteke o nazwie: _thread
import _thread

#  importujemy biblioteke o nazwie: time
import time

#  importujemy biblioteke o nazwie: ctypes
import ctypes

# Importujemy z biblioteki tkinter metodę/klasę o nazwie: filedialog
from tkinter import filedialog

#  importujemy biblioteke o nazwie: os
import os

#  importujemy biblioteke o nazwie: serial.tools.list_ports
import serial.tools.list_ports as list_ports

# Importujemy z biblioteki serial.tools.list_ports_common metodę/klasę o nazwie: ListPortInfo
from serial.tools.list_ports_common import ListPortInfo

#  importujemy biblioteke o nazwie: struct
import struct

#  importujemy biblioteke o nazwie: proto_file.proto_comm
import proto_file.proto_comm as proto_comm

#  importujemy biblioteke o nazwie: sys
import sys

#  importujemy biblioteke o nazwie: serial
import serial

# Importujemy z biblioteki kivy.clock metodę/klasę o nazwie: Clock,
from kivy.clock import Clock, mainthread

#  importujemy biblioteke o nazwie: asyncio
import asyncio

# Importujemy z biblioteki kivy.loader metodę/klasę o nazwie: Loader
from kivy.loader import Loader

#  importujemy biblioteke o nazwie: asynckivy
import asynckivy as ak

# Importujemy z biblioteki kivy.uix.popup metodę/klasę o nazwie: Popup
from kivy.uix.popup import Popup

#  importujemy biblioteke o nazwie: queue
import queue





# Rozpoczynamy definicje obiektu/klasy
class MyGrid(Widget):
    com = ObjectProperty(None)
    comm = None
    port = ''
    csvQueue=queue.Queue()


# Rozpoczynamy definicje funkcji magicznej
    def __init__(self, **var_args):
        super(MyGrid, self).__init__(**var_args)


        
    trump =False              
    



# Rozpoczynamy definicje funkcji
    def on_press(self):
        self.trump =True

# Rozpoczynamy zagnieżdżenie bloku wyjątku
        try:   
            self.comm = proto_comm.ProtobufComm( self.port, 115200)
            self.comm.stm.flush()
            self.comm.stm.read_all()
            self.comm.stm.flushInput()
            self.comm.stm.flushOutput()
            self.comm.start_data_output()
            self.com.text += "\nRozpozÄ™to pomiar\n\n"
            self.com.text = self.comm.start_pom()
            self.csvQueue.put_nowait(self.comm.start_pom())

# Rozpoczynamy pętle while
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

# Rozpoczynamy zagnieżdżenie wsytąpienie wyjątku: serial.serialutil.SerialException:
        except serial.serialutil.SerialException:

# Rozpoczynamy definicje nowego wątku
             Thread(target = self.error_win("BĹ‚Ä…d poĹ‚Ä…czenia siÄ™ z portem ")).start()

# Rozpoczynamy zagnieżdżenie wsytąpienie wyjątku: struct.error:
        except struct.error:

# Rozpoczynamy definicje nowego wątku
            Thread(target = self.error_win('UrzÄ…dzenie zostaĹ‚o odĹ‚Ä…czone')).start()
            self.comm.stm.flush()
            self.comm.stm.flushInput()
            self.comm.stm.read_all()
            self.comm.stm.flushOutput()
            self.comm.stop_data_output()

# Rozpoczynamy zagnieżdżenie wsytąpienie wyjątku: TypeError:
        except TypeError:

# Rozpoczynamy definicje nowego wątku
            Thread(target = self.error_win("BĹ‚Ä…d poĹ‚Ä…czenia siÄ™ z portem ")).start()
        self.trump =False
        

        


# Rozpoczynamy definicje funkcji
    def spinner_clicked(self, value):
        self.port = value





# Rozpoczynamy definicje funkcji
    def save_file(self):
        self.trump =True
        f = open("zapis.csv", "a")
        dataArray1 = []
        print('Przed loop')

# Rozpoczynamy pętle while
        while(self.csvQueue.qsize( )>0 ):
            dataArray1 = self.csvQueue.get_nowait()
            f.write(str(dataArray1))
        print('Po loop')
        f.close()




# Rozpoczynamy definicje funkcji
    def start_thread(self):

# Rozpoczynamy definicje bloku warunkowego
        if not(self.trump):
            self.com.text = "RozpozÄ™to pomiar"

# Rozpoczynamy definicje nowego wątku
            Thread(target = self.on_press).start()
        else:

# Rozpoczynamy definicje nowego wątku
            Thread(target = self.error_win("JuĹĽ uruchomiĹ‚eĹ› pomiar")).start()
        



# Rozpoczynamy definicje funkcji
    def error_win(self, error_txt):
        ctypes.windll.user32.MessageBoxW(None, error_txt, "Error", 0)



# Rozpoczynamy definicje funkcji
    def on_press_false(self):

# Rozpoczynamy definicje bloku warunkowego
        if (self.trump):
            self.trump = False
            time.sleep(0.2)
            self.com.text += "Pomiar Zastopowano"
        


# Rozpoczynamy definicje funkcji
    def stop(self):
        time.sleep(0.3)

# Rozpoczynamy definicje nowego wątku

# Startujemy nowy wątek
        Thread(target=self.on_press_false).start()
        




# Rozpoczynamy definicje funkcji
    def save_file_(self):

# Rozpoczynamy definicje nowego wątku
        Thread(target = self.save_file).start()
        


# Rozpoczynamy definicje funkcji
    def file_load(self):
        filedialog.askopenfilename()



# Rozpoczynamy definicje funkcji
    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.com.text)
