import pdfplumber       #Mierda de pdf
import pandas           #Mierda de pdf2
import os.path          #Para abrir archivos con el open
import requests         #Para descargar el pdf
#import re               #Regex
####Toda esta mierda es para lo del Ctrl+C
from termcolor import colored
import sys
import signal
####
#######Sin uso actualmente
#import time
#import json             #Esto para importal el json
#######

file = '1702992623948ListadoProvisionalPersonasAdmitidas.pdf'
ficherosalida = 'test7.json'
ficherosalidacsv = 'test7.csv'

jsonfinal = 'json.json'
csvfinal = 'csv.csv'

campos = ''

#####Esto es para darle a Ctrl+C y que no te salgan errores#####
def def_handler(sig, frame):
    print(colored(f"\n[!] Abortando\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)
################################################################

def convertir_a_csv():
    #Esto se supone que es para quitar el output
    #import contextlib
    #with contextlib.redirect_stdout(None):
    
    columnas = ["Solicitud","DNI","Nombre","Apellidos","Puesto","Lugar","OrdenPrefer","Autobaremo"]
    listadeDataFrames = []

    with pdfplumber.open(file) as pdf:
        for i,page in enumerate(pdf.pages):
            if i == 0:
                primerapagina = pdf.pages[0]    #Esto es para las cabeceras de mierda 
                table = primerapagina.extract_table()
                DataFrame = pandas.DataFrame(table[1:1], columns=columnas)
                listadeDataFrames.append(DataFrame) #Apendo la primera pagina pa que tenga cabeceras y despues me meto en todas las demas
                #print(listadeDataFrames)
            table = page.extract_table()
            DataFrame = pandas.DataFrame(table[1:], columns=columnas)
            listadeDataFrames.append(DataFrame)
            #print(listadeDataFrames)
            #print(listadeDataFrames) 
        todo = pandas.concat(listadeDataFrames)
        #print(todo)
        todo.reset_index(drop=True, inplace=True)
        
        #todo.to_json(ficherosalida)
        #todo.to_csv(ficherosalidacsv)
        
        return(todo)

def dnisordenados():        #Buscar el dni y sacar los 8 digitos
    DataFrame = convertir_a_csv()
    dnis = []
    anteriornombre = ''
    anteriorapellidos = ''
    columnarepite = 0
    
    for columna in DataFrame.index:
        #print(DataFrame.loc[columna,"DNI"])     #Tengo que pillar el dni de la gente que se llame igual, medio hecho de antes
        ####
        #'''
        if (DataFrame.loc[columna,"Nombre"] == anteriornombre) and (DataFrame.loc[columna,"Apellidos"] == anteriorapellidos):
            dnis[columnarepite].append(DataFrame.loc[columna,"DNI"])
        else:
            if columna == 0:
                pass
            else:
                columnarepite = columnarepite + 1
            #print(DataFrame.loc[columna,"DNI"]+" "+DataFrame.loc[columna,"Nombre"]+" "+DataFrame.loc[columna,"Apellidos"])
            dnis.append([DataFrame.loc[columna,"Nombre"]+" "+DataFrame.loc[columna,"Apellidos"]])
            
            if (dnis[columnarepite][0]):
                dnis[columnarepite].append(DataFrame.loc[columna,"DNI"])
            else:
                columnarepite = columnarepite + 1
        anteriornombre = DataFrame.loc[columna,"Nombre"]
        anteriorapellidos = DataFrame.loc[columna,"Apellidos"]
        #'''
    #print(dnis)     #Aqui tengo la lista de DNIs enascarados y sus usuarios
    dnis = pandas.DataFrame(dnis)
    #dnis.dropna(axis=1, how='any')     #Se supone que quita las columnas que tengan el valor none o valores nulos y eso
    #print(dnis)     #Dataframeado?
    dnis.to_json(ficherosalida)
    

def dni8digitos():
    arrayfinal = []
    
    DataFrame = pandas.read_json(ficherosalida)
    '''#Ejemplo de el output de DataFrame
                                            0          1          2          3          4          5          6          7   ...    22    23    24    25    26    27    28    29
    0               SUSANA ABELLA DUARTE  27*1*0***  2*3**03**  ***1*031*       None       None       None       None  ...  None  None  None  None  None  None  None  None
    1               RAFAEL ADAMUZ SANTOS  *46*2*7**  *4*52**9*  *4**2*79*  *46***79*  *4*5**79*  7**5*37**  ***5237**  ...  None  None  None  None  None  None  None  None
    2    FRANCISCO JAVIER AGUILAR GARCIA  28**5*9**       None       None       None       None       None       None  ...  None  None  None  None  None  None  None  None
    3     ENCARNACION AGUILERA MALDONADO  *2533****  ***33*13*  *2**31*3*  5**33*1**  *253***3*  *2**31*3*  *25*3*1**  ...  None  None  None  None  None  None  None  None
    4             NOELIA ALCANTARA RUEDA  53*80****  5***08*8*  5*68*8***       None       None       None       None  ...  None  None  None  None  None  None  None  None
    ..                               ...        ...        ...        ...        ...        ...        ...        ...  ...   ...   ...   ...   ...   ...   ...   ...   ...
    389             PATRICIA WANG ROMERO  *4*259***  *4*259***  *4**59*3*  4**2**93*  4*02***3*  4*025****  4*02***3*  ...  None  None  None  None  None  None  None  None
    390                JORGE YAÑEZ PADRO  1*6**60**       None       None       None       None       None       None  ...  None  None  None  None  None  None  None  None
    391    MARIA CRISTINA ZAJARA CORONEL  2***14*2*  *863**1**       None       None       None       None       None  ...  None  None  None  None  None  None  None  None
    392           PABLO ZAMORANO FELIZON  28**8*6**  2**488***  2**488***  2***886**  *88***69*       None       None  ...  None  None  None  None  None  None  None  None
    393         VICTOR ZARANDIETA LOPERA  ***064*7*  *8*0*44**       None       None       None       None       None  ...  None  None  None  None  None  None  None  None
    '''
    #print(DataFrame.index) #Numero de filas
    #print(DataFrame.columns)    #Numero de columnas

    filas = DataFrame.index       #Con esto saco la primera fila, osea la de susana
    nombres = DataFrame[0][filas]
    oldDataFrame = pandas.DataFrame(DataFrame)  #Dejo el antiguo sin stripear por si acaso lo necestio
    DataFrame.drop(columns=DataFrame.columns[0], axis=1, inplace=True) #Dropeo la primera columna que tiene el nombre
    DataFrame.columns = range(len(DataFrame.columns))
    columnas = DataFrame.columns    #Con esto saco la columna nombres, y si cambio por el 1 sale la segunda columna, osea el primer dni
    #Tengo que recorrer un bucle dentro de otro, en un vario la fila y en el de dentro la columna
    for f,fila in enumerate(nombres):   #Recorro 393 nombres
        #Inicializo la variable cada vez que recorro un dni
        dniformado = ''
        dni = ''
        letrasdni = ['','','','','','','','','']
        #print(colored(f'[!] Nombre: {fila}', 'green'))
        arrayfinal.append([f'{fila}'])   #Añado el nombre al array que voy a enseñar y meter en un csv... o un json ya veremos pedazo de chupapollas
        for columna in columnas:
            dni = DataFrame[columna][f]
            if str(dni) != 'None':
                #Recorro cada registro de dni
                for l,letra in enumerate(dni):
                    #Si l es mas de 9 es porque el pdf esta hehco como una mierda
                    if l <= 8:
                        #Comrpuebo si antes ya hay un numero
                        #Si no es un numero, ya que es un asterisco o es un campo vacio, entonces hago el proceso de añadirlo a la lista
                        if not letrasdni[l].isnumeric():
                            #Si es un numero y no un asterisco lo meto en la lista
                            if str(letra).isnumeric():
                                letrasdni[l] = letra
                                #print(f'De nuevo la lista cuando ha habido un cambio: {letrasdni}')
                                #Convierto la lista a string
                                dniformado = ''.join(str(e) for e in letrasdni)
                                #Termino de recorrer un dni
        #Habra que comprobar si el string dniformado tiene 8 digitos
        if (dniformado.isnumeric()) and (len(dniformado) == 8):
            #print(colored(f'[!] DNI Formado: {dniformado}','blue'))
            arrayletrasdni = 'TRWAGMYFPDXBNJZSQVHLCKE'
            letradni = arrayletrasdni[int(dniformado)%23]
            #print(colored(f'[!] DNI Completo del colega: {dniformado+letradni}','blue'))
            arrayfinal[f].append(dniformado+letradni)
        else:
            #print(colored(f'[X] No se ha podido formar el dni completo :(','red'))
            arrayfinal[f].append("No se ha podido formar el dni")
    arrayfinal = pandas.DataFrame(arrayfinal, columns=["Nombre","DNI"])
    #print(arrayfinal)   #Hay muchos registros, asi que no te los va a enseñar todos, la verdad es que es un putadon
    
    print(colored(f'Descargando ransomware en /usr/share.... \n....\n....\nes broma, mira la carpeta desde donde estas ejecutando el programa, se han creado dos ficheros, {csvfinal} y {jsonfinal}, se han creado un par mas pero bueno, luego lo modifico','green'))
    #Lo exporto a json y csv
    arrayfinal.to_json(jsonfinal)
    arrayfinal.to_csv(csvfinal)

if __name__ == "__main__":
    url = 'https://www.canalsur.es/resources/archivos_offline/2023/12/19/1702992623948ListadoProvisionalPersonasAdmitidas.pdf'
    if(os.path.exists(file) == False): #No existe el virus.pdf
        descargar = input(f'No existe el pdf, ¿quieres descargartelo de: {url}? \nContesta con Y o con N: \n')
        if(descargar == "Y"):
            response = requests.get(url)
            with open(file, 'wb') as f:
                f.write(response.content)
            if(os.path.exists(ficherosalida) == True):
                print(f"Existe el fichero {ficherosalida} asi que llamo a la funcion de sacar los 8 digitos")
                dni8digitos()
            else:
                print("Sé, que mi suerte no depende del color de un gato, que si metes la pata pagas el pato, \nsé que cuanto mas los quiero peor los trato, y que donde falta plata siempre sobra un plato")
                convertir_a_csv()   #LLamo a la funcion
                dnisordenados()     #me la chupas tonto, a ver como coño hago yo esto
                if(os.path.exists(ficherosalida) == True):
                    print(f"Existe el fichero {ficherosalida} asi que llamo a la funcion de sacar los 8 digitos")
                    dni8digitos()
        elif(descargar == "N"):
            print(f'Si no te fias vete a {url} y te lo descargas tu mismo, dejalo en la misma ruta desde la que estas ejecutando el script y lo inicias otra vez')
        else:
            print("Tu que eres ¿gracioso?, pon Y o N")
    elif(os.path.exists(file) == True): #Si ya existe
        if(os.path.exists(ficherosalida) == True):
            print(f"Existe el fichero {ficherosalida} asi que llamo a la funcion de sacar los 8 digitos")
            dni8digitos()
        else:
            print("Sé, que mi suerte no depende del color de un gato, que si metes la pata pagas el pato, \n sé que cuanto mas los quiero peor los trato, y que donde falta plata siempre sobra un plato")
            convertir_a_csv()   #LLamo a la funcion
            dnisordenados()     #me la chupas tonto, a ver como coño hago yo esto
            if(os.path.exists(ficherosalida) == True):
                print(f"Existe el fichero {ficherosalida} asi que llamo a la funcion de sacar los 8 digitos")
                dni8digitos()