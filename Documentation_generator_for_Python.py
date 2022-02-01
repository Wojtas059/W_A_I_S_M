import queue
from file import Document

import queue
from file import Document

flag = 0
csvQueue=queue.Queue()

file_write=queue.Queue()
q1 = queue.LifoQueue()
def line_queqe():
    file = open("<NAZWA PLIKU DO KTÓREGO CHCEMY DODAĆ KOMENTARZE>.py")
    for line in file:
        csvQueue.put_nowait(str(line))
    file.close

dataarray = []
def spr_tab():
    print('Sprawdzam')
    while(csvQueue.qsize( )>0 ):
        line = csvQueue.get_nowait()
        dataarray = str(line).split()
        if dataarray != []:
            if line.find('from ') != -1 :
                file_write.put_nowait('\n# Importujemy z biblioteki '+dataarray[1]+' metodę/klasę o nazwie: '+dataarray[3]+'\n')
            else:
                if line.find('import') != -1:
                    file_write.put_nowait('\n#  importujemy biblioteke o nazwie: '+dataarray[1]+'\n')

            if dataarray[0] == 'class':
                file_write.put_nowait('\n# Rozpoczynamy definicje obiektu/klasy\n')
                
            if dataarray[0] == 'def':
                str_line = '\n# Rozpoczynamy definicje funkcji'
                i = str(line).count("__")
                if "__" in line:
                    if i == 2:
                        print("licznik: "+str(i))
                        str_line +=' magicznej'
                file_write.put_nowait('\n'+str_line+'\n')
            if dataarray[0] == 'if':
                file_write.put_nowait('\n# Rozpoczynamy definicje bloku warunkowego\n')

            if dataarray[0] == 'try:':
                file_write.put_nowait('\n# Rozpoczynamy zagnieżdżenie bloku wyjątku\n')

            if dataarray[0] == 'except':
                file_write.put_nowait('\n# Rozpoczynamy zagnieżdżenie wsytąpienie wyjątku: '+dataarray[1]+'\n')
            
            if "Thread" in dataarray[0]:
                file_write.put_nowait('\n# Rozpoczynamy definicje nowego wątku\n')

            if "threading" in line:
                file_write.put_nowait('\n# Rozpoczynamy definicje nowego wątku\n')
            
            if "threading.Timer" in line:
                file_write.put_nowait('#  Określenie wątku, który wykona daną metodę w określonym czasie \n')

            if ".start()" in dataarray[0]:
                file_write.put_nowait('\n# Startujemy nowy wątek\n')
            
            if "for" in dataarray[0]:
                file_write.put_nowait('\n# Rozpoczynamy pętle for \n')

            if "while" in dataarray[0] :
                file_write.put_nowait('\n# Rozpoczynamy pętle while\n')

            if "return" in dataarray[0]:
                file_write.put_nowait('\n# Zwracanie z funkcji obiektu\n')
            
            if "#" in dataarray[0]:
                file_write.put_nowait('# Komentarz programisty\n')

            if "logging." in dataarray[0]:
                file_write.put_nowait('\n# Wyświetlenie informacji w konsoli\n')

                
            if "raise" in line:
                file_write.put_nowait('\n# Podniesienie flagi wyjątku '+dataarray[1]+'\n')
        
        file_write.put_nowait(line)
        #print(dataarray)
    print('Zakonczylem sprawdzanie')
    file = open("<NAZWA PLIKU DO KTÓREGO CHCEMY DODAĆ KOMENTARZE>_documentation.py", "w", encoding="utf-8")
    while(file_write.qsize( )>0 ):
        file.write(file_write.get_nowait())
        
    file.close


line_queqe()
spr_tab()



