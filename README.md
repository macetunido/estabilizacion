
First time writing a script in python. 
I wanted to automate something and people usually do it in python so this is my take on it. 


## Description
It asks you if you want to download a pdf file from a website and creates 3 files, a "test.json" which i use to read from within the same application (i know i shouldnt even need to create that file to then read it afterwards), a "json.json" and a "csv.csv" file with the output of names on the pdf and their respectives DNI (basically the identification number of the person) fully formed.

They are based on the output of the original pdf file, which shows multiple rows of the same person but the identification number masking is changed around everytime the person shows on the list.

The original pdf can be found somewhere in here as of time of writing: [Canal Sur Estabilizacion](https://www.canalsur.es/transparencia/procedimiento-selectivo-extraordinario-de-estabilizacion/1974317.html)

### How can you get the number?

Example of a bad masked DNI: 


| DNI        | Nombre           | Apellidos |
| ------------- |:-------------:| -----:|
| 1\*\*456\*\*\* | Pepito | Grillo |
| \*\*345\*7\*\* | Pepito | Grillo |
| \*2\*\*\*\*\*8\* | Pepito | Grillo |
| ................ | ............. | .......... |


The only thing missing there is the final character of the DNI, it is in fact a letter and it can be formed based on the leftside numbers, an example of a DNI would be: "12345678Z"

This link shows how you can get the letter: [Ministerio del Interior | Cálculo del Dígito de Control del NIF-NIE](https://www.interior.gob.es/opencms/es/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/)

#### Usage
You need to have pdfplumber, pandas, and termcolor libraries installed to use the script
To install the libraries use pip:
```bash
pip install pdfplumber pandas termcolor
```
To execute the script
```bash
python3 estabilizacion7.py
```

In case they delete the pdf there is a webarchive link to it:

[WebArchive PDF](http://web.archive.org/web/20240224134257/https://www.canalsur.es/resources/archivos_offline/2023/12/19/1702992623948ListadoProvisionalPersonasAdmitidas.pdf)
