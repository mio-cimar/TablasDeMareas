"""
**************************************************************
******* Script para generar una Tabla de Mareas *******
**************************************************************
Description: Genera una tabla de mareas
Input: "marea".csv
Output: "marea".pdf
Usage: python generate_tides_table.py
Notes:
    
Authors: Estudiante Alejandro Rodriguez Badilla.
Modifications: M.Sc. Rodney E. Mora
Creation day Aug 1, 2019
"""
#######################################################################
# Load library

# configuración local
import locale
import pprint
locale.setlocale(locale.LC_ALL, '') 
configuracion = locale.localeconv()
imprimir = pprint.PrettyPrinter()
imprimir.pprint(configuracion)

# 
import os
import csv 
import numpy as np

# Biblioteca de Tiempos
from datetime import datetime, timedelta
from pytz import timezone

# Biblioteca PyLatex
from pylatex import Document, Section, MultiColumn,\
    MultiRow, Command, PageStyle, \
    LineBreak, LargeText, NewPage, Tabu, Head, Foot, \
    Figure, MiniPage, StandAloneGraphic, VerticalSpace
from pylatex.utils import bold, NoEscape, italic

# Biblioteca Skyfield
from skyfield import api
from skyfield import almanac
#######################################################################
# Directorio de trabajo
cwd=os.getcwd()
#######################################################################
# Parametros
# Revisar en el archivo la fecha inicial y fecha final. Recordar n-1
# Datoi=(35291) -1
# Datof=(36701)
Datoi=(39529) -1 #ultimo dato archivo 39528
Datof=(40937) # primer dato archivo 40937
# Años bisiestos: 2020, 2024, 2028, 2032, 2036, 2040, 2044, 2048, agregar un día más
DiaJ=365
Input_data= 'IsladelCoco.csv'
File_name='Tabla_Mareas_IsladelCoco-2022'
Anne='2022'
Site='Isla del Coco'
State='Puntarenas'
Lon='-86.98°W'
Lat='5.55°N'
#######################################################################
# Skyfield. Escala de tiempo y Efemérides
ts = api.load.timescale()
e = api.load('de421.bsp')

#hora_local=timezone('America/Costa_Rica')
#ei = hora_local.localize(datetime(2019, 1, 1,6,0,0))
#ef=hora_local.localize(datetime(2020, 1, 1,5,59,59))

t0 = ts.utc(int(Anne), 1, 1,6,0,0)
t1 = ts.utc(int(Anne)+1, 1, 1, 5,59,59)
#Tiempos y Códigos de la Fase Lunar
tm, ym = almanac.find_discrete(t0, t1, almanac.moon_phases(e))

# Para cambiar a hora local la fase lunar
temp1 = []
temp1.append(tm.utc_strftime("%Y-%m-%d %H:%S"))
temp2=[]
for jj in range(49):
    temp2.append(datetime.strptime(temp1[0][jj],"%Y-%m-%d %H:%S")- timedelta(hours=6))
#
moon1 = []
for kk in range(49):
    moon1.append(temp2[kk].strftime("%Y-%m-%d"))
# Nombre de la Fase Lunar
moon2=[]
moon2.append([almanac.MOON_PHASES[yi] for yi in ym])

#######################################################################

image_filename = os.path.join(os.path.dirname(__file__), cwd+'/UCR.png')

#######################################################################
# Lectura de datos de mareas en formato csv
# Los datos están en horas expresadas en UTC
# Cambiar la hora a Hora Local CR
for path, dirs, files in os.walk( cwd +"/mareas_csv"):
    for file in files:        
        filename = os.path.join(path, file)
        name = filename.rstrip(".csv")
		
        if Input_data in file:
            
            rows_data = []
            with open(filename) as datos:
                data_reader = csv.reader(datos, delimiter = ",")
                for row in data_reader:
                    rows_data.append(row)
                                        
            rt = []                    
            for i in range(Datoi,Datof):
                print(i)
                rt.append(datetime.strptime(rows_data[i][0],"%Y-%m-%dT%H:%M:%S+00:00") - timedelta(hours=6) )
            rt = np.flipud(rt)

                      
            rm = []                            
            for i in range(Datoi,Datof):
                rm.append(float(rows_data[i][1]))
            rm = np.flipud(rm)
            
            def daylist(ti,ma):
                dlist = [[] for i in range(DiaJ)]
                vlist = [[] for i in range(DiaJ)]
                for a in range(len(ti)):
                    for b in range(len(ti)):
                        if ti[b].date() == (ti[0] + timedelta(days=a)).date():
                            dlist[a].append(ti[b])
                            vlist[a].append('{: 5.2f}'.format(ma[b]))
                return dlist, vlist
            
            dias = daylist(rt, rm)
            mar = dias[1]
            dias= dias[0]
            
            for i in range(DiaJ):
                for j in range(4-len(dias[i])):
                #if len(dias[i])<4:
                    dias[i].append("")
                    mar[i].append("")
                    
            def monlist(di,ma):
                dlist = [[] for i in range(12)]
                vlist = [[] for i in range(12)]
                for m in range(1,13):
                    for x in range(len(di)):
                        if di[x][0].month == m:
                            dlist[m-1].append(di[x])    
                            vlist[m-1].append(ma[x])   
                return dlist, vlist
                
            meses = monlist(dias, mar)
            mar_m = meses[1]
            meses= meses[0]
            
            re = ["" for i in range(4)]
            for i in range(12):
                if len(meses[i]) == 31:
                    mar_m[i].append(re)
                    meses[i].append(re)
                else:
                    for j in range(32-len(meses[i])):
                        mar_m[i].append(re)
                        meses[i].append(re)

#######################################################################
# Genera el documento en LaTEX
# Call to PyLatex
def generate_table():
    geometry_options = {
        "landscape": False,
        "a4paper": True,
        "margin": "0.275in",
        "headheight": "10pt",
        "headsep": "8pt",
        "includeheadfoot": True
    }
                
    doc = Document(geometry_options=geometry_options)
    header = PageStyle("header")

#######################################################################          
# Encabezado
# Create left header
    with header.create(Head("L")) as header_left:
        with header_left.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                         pos='c')) as logo_wrapper:
            logo_file = os.path.join(os.path.dirname(__file__),cwd + '/MIO.pdf')
            logo_wrapper.append(StandAloneGraphic(image_options="width=80px",
                                filename=logo_file))
# Create center header
    with header.create(Head("C")):
        header.append(LargeText(bold(Site + ", " + State + ", Costa Rica")))
        header.append(LineBreak())
        header.append("Latitud " + Lat +", Longitud " + Lon)
        header.append(LineBreak())
        header.append("Hora y altura de la pleamar y bajamar")
# Create right header
    with header.create(Head("R")):
        header.append(LargeText(bold(Anne)))
        header.append(LineBreak())
        header.append("Hora Local")

    #with header.create(Foot("R")):
     #   header.append(Command('thepage'))

#######################################################################
# Preambulo
    doc.preamble.append(header)

    doc.preamble.append(Command('usepackage','times'))
    doc.preamble.append(Command('usepackage', 'wasysym'))
    doc.preamble.append(Command('usepackage','hyperref'))
    #doc.preamble.append(Command('usepackage','showframe'))
    #doc.preamble.append(Command('usepackage','babel','spanish'))
    #doc.preamble.append(Command('usepackage','datetime','yyyy'))
    #doc.preamble.append(Command('yyyydate'))

#######################################################################
# Rellenado en la tabla con la información de dia, hora, faselunar y altura
    d = [[] for i in range(12)]
    d1 = []
    
    for n in range(12):
        for m in range(32): 
            if type(meses[n][m][0]) == datetime:  
                
                d1.append(MultiRow(2, data=meses[n][m][0].strftime("%d")))
                d1.append(MultiRow(1, data=""))
                d1.append(MultiRow(1, data=meses[n][m][0].strftime("%a")))
                mpf = ""
                ms = meses[n][m][0].strftime("%Y-%m-%d")
                
                if ms in moon1:
                    
                    mi = moon1.index(meses[n][m][0].strftime("%Y-%m-%d"))
                    mph = moon2[0][mi]

                    if mph == "New Moon":
                        mpf = NoEscape(r'\newmoon')
                    if mph == "First Quarter":
                        mpf = NoEscape(r'\rightmoon')
                    if mph == "Full Moon":
                        mpf = NoEscape(r'\fullmoon')
                    if mph == "Last Quarter":
                        mpf = NoEscape(r'\leftmoon')
                        
                d1.append(MultiRow(1, data=mpf))
                d[n].append(d1)  
                
            elif type(meses[n][m][0]) == str: 
                for l in range(4):
                    d1.append(MultiRow(1, data=""))
                    
                d[n].append(d1)
                
            d1 = []
                       
    h = [[] for i in range(12)]
    h1 = []
    
    for n in range(12):
        for m in range(32):
            for l in range(4):
                if type(meses[n][m][l]) == datetime:
                    h1.append(MultiRow(1, data=meses[n][m][l].strftime("%H:%M")))
                else: 
                    h1.append(MultiRow(1, data=""))
                    
            h[n].append(h1)
            h1 = []
            
    mv = [[] for i in range(12)]
    mv1 = []
    
    for n in range(12):
        for m in range(32):
            for l in range(4):
                if type(meses[n][m][l]) == datetime:
                    mv1.append(MultiRow(1, data=mar_m[n][m][l]))
                else: 
                    mv1.append(MultiRow(1, data=""))
                    
            mv[n].append(mv1)
            mv1 = [] 

#######################################################################
# Primera página. Generalidades
    doc.append(Command('thispagestyle{empty}'))
    with doc.create(Section('Aviso Legal.',numbering=False)):
        doc.append(italic('La utilización del servicio brindado por el Módulo de Información Oceanográfica ')) 
        doc.append(italic('(MIO) así como las conclusiones que se extraigan de la información suministrada corren por cuenta ')) 
        doc.append(italic('y riesgo propio del usuario y la Universidad de Costa Rica (UCR) rechaza expresamente toda ')) 
        doc.append(italic('responsabilidad en relación con los servicios de información y, en ningún caso, podrá ser considerada ')) 
        doc.append(italic('responsable frente a terceros por cualquier pérdida o daño que se deriven del uso de los servicios de información. ')) 
        doc.append(italic('La antedicha exclusión de responsabilidad se refiere a cualesquiera de las información ')) 
        doc.append(italic('prestada por la UCR en sus servicios de información.\n\n'))
        
    with doc.create(Section('Información de contacto.',numbering=False)):
        doc.append('Centro de Investigación en Ciencias del Mar y Limnología, Ciudad de la Investigación, Finca 2, ')
        doc.append('Edificio CIMAR.\n\n')
        doc.append('Apdo. 11501-2060, Costa Rica.\n\n')
        doc.append('Tels: (506) 2511-2210 / 2232. \n\n')
        doc.append('Fax: (506) 2511-2206.\n\n')
        doc.append('Correo: ')
        doc.append(Command('href',arguments='mailto:mio.cimar@ucr.ac.cr',extra_arguments='mio.cimar@ucr.ac.cr'))
        doc.append('.\n\n')
    with doc.create(Section('Comentarios generales.',numbering=False)):
        doc.append(Command('textsuperscript'))
        doc.append(Command('textcopyright'))
        doc.append('Derechos reservados de la Universidad de Costa Rica,  ')
        doc.append('Centro de Investigación en Ciencias del Mar y Limnología, ')
        doc.append('Módulo de Información Oceanográfica ' + Anne + '.\n\n')
        #doc.append(Command('today'))
        doc.append('La predicción de marea es con referencia al promedio de las mareas bajas en un registro de al menos 20 años.\n\n')
        doc.append('Las horas están en hora local estándar (UTC -06:00).\n\n')
        doc.append('Simbología: ')
        doc.append(Command('fullmoon'))
        doc.append(' Luna Llena ')
        doc.append(Command('leftmoon'))
        doc.append(' Cuarto Menguante ')
        doc.append(Command('newmoon'))
        doc.append(' Luna Nueva ')
        doc.append(Command('rightmoon'))
        doc.append(' Cuarto Creciente')
        doc.append(Command('vfill'))
        with doc.create(Figure(position='h!')) as mio_pic:
            mio_pic.add_image(image_filename, width='120px')
    
#######################################################################
# Tabla de mareas por meses
# Meses de enero-febrero-marzo

    doc.append(Command('arrayrulewidth=1.2pt'))
    doc.append(NewPage()) 
    doc.append(VerticalSpace("35pt"))
    with doc.create(Tabu("cccccc|cccccc|cccccc", col_space="0.05in", row_height=0.70)) as table1:

        table1.add_row((MultiColumn(6, align="c", data=bold("Enero"))), \
                       (MultiColumn(6, align="c", data=bold("Febrero"))), \
                       (MultiColumn(6, align="c", data=bold("Marzo"))))
        table1.add_empty_row()
        table1.add_row(("","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]"))
        table1.add_empty_row()
                
        for s in range(16):
            for t in range(4):
                table1.add_row((d[0][s][t], h[0][s][t], mv[0][s][t], \
                                d[0][s+16][t], h[0][s+16][t], mv[0][s+16][t], \
                                d[1][s][t], h[1][s][t], mv[1][s][t], \
                                d[1][s+16][t], h[1][s+16][t], mv[1][s+16][t], \
                                d[2][s][t], h[2][s][t], mv[2][s][t], \
                                d[2][s+16][t], h[2][s+16][t], mv[2][s+16][t]))
            table1.add_empty_row()

    doc.change_document_style("header")

# Meses de abril-mayo-junio
    doc.append(NewPage())   
    with doc.create(Tabu("cccccc|cccccc|cccccc", col_space="0.05in", row_height=0.70)) as table2:
        
        table2.add_row((MultiColumn(6, align="c", data=bold("Abril"))), \
                       (MultiColumn(6, align="c", data=bold("Mayo"))), \
                       (MultiColumn(6, align="c", data=bold("Junio"))))
        table2.add_empty_row()
        table2.add_row(("","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]"))
        table2.add_empty_row()      
        
        for s in range(16):
            for t in range(4):
                table2.add_row((d[3][s][t], h[3][s][t], mv[3][s][t], \
                                d[3][s+16][t], h[3][s+16][t], mv[3][s+16][t], \
                                d[4][s][t], h[4][s][t], mv[4][s][t], \
                                d[4][s+16][t], h[4][s+16][t], mv[4][s+16][t], \
                                d[5][s][t], h[5][s][t], mv[5][s][t], \
                                d[5][s+16][t], h[5][s+16][t], mv[5][s+16][t]))
            table2.add_empty_row()


# Meses de julio-agosto-septiembre    
    doc.append(NewPage())    
    with doc.create(Tabu("cccccc|cccccc|cccccc", col_space="0.05in", row_height=0.70)) as table3:
        
        table3.add_row((MultiColumn(6, align="c", data=bold("Julio"))), \
                       (MultiColumn(6, align="c", data=bold("Agosto"))), \
                       (MultiColumn(6, align="c", data=bold("Septiembre"))))
        table3.add_empty_row()
        table3.add_row(("","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]"))
        table3.add_empty_row()      
                
        for s in range(16):
            for t in range(4):
                table3.add_row((d[6][s][t], h[6][s][t], mv[6][s][t], \
                                d[6][s+16][t], h[6][s+16][t], mv[6][s+16][t], \
                                d[7][s][t], h[7][s][t], mv[7][s][t], \
                                d[7][s+16][t], h[7][s+16][t], mv[7][s+16][t], \
                                d[8][s][t], h[8][s][t], mv[8][s][t], \
                                d[8][s+16][t], h[8][s+16][t], mv[8][s+16][t]))
            table3.add_empty_row()
    
  
# Meses de octubre-noviembre-diciembre
    doc.append(NewPage())    
    with doc.create(Tabu("cccccc|cccccc|cccccc", col_space="0.05in", row_height=0.70)) as table4:
        
        table4.add_row((MultiColumn(6, align="c", data=bold("Octubre"))), \
                       (MultiColumn(6, align="c", data=bold("Noviembre"))), \
                       (MultiColumn(6, align="c", data=bold("Diciembre"))))
        table4.add_empty_row()
        table4.add_row(("","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]","","Hora","[m]"))
        table4.add_empty_row()     
                
        for s in range(16):
            for t in range(4):
                table4.add_row((d[9][s][t], h[9][s][t], mv[9][s][t], \
                                d[9][s+16][t], h[9][s+16][t], mv[9][s+16][t], \
                                d[10][s][t], h[10][s][t], mv[10][s][t], \
                                d[10][s+16][t], h[10][s+16][t], mv[10][s+16][t], \
                                d[11][s][t], h[11][s][t], mv[11][s][t], \
                                d[11][s+16][t], h[11][s+16][t], mv[11][s+16][t]))
            table4.add_empty_row()


#######################################################################   
    doc.generate_pdf(cwd +'/Tablas-2022/' + File_name, clean_tex=False)
    
generate_table()
