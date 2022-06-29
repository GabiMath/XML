# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 08:55:37 2021

@author: Gabriela
"""


import xml.etree.ElementTree as ET

posicion = [0, 1, 8, 2, 5, 9, 12, 3, 4, 6, 7, 10, 11, 12, 13, 14]

width, height = 150, 120

def datosXML(archivoXML):
    
    try:
        arbol = ET.parse(archivoXML)
        
    except IOError:
        print ('No se encuentra el archivo ', archivoXML)
        exit()
        
    except ET.ParseError:
        print("Error procesando en el archivo XML = ", archivoXML)
        exit()
       
    raiz = arbol.getroot()
    
    raiz = arbol.getroot()
    data1=[]
    for persona in raiz.iter('{http://www.uniovi.es}persona'):
        lugN = persona[0].find('{http://www.uniovi.es}lugarNacimiento').text
        fNac = persona[0].find('{http://www.uniovi.es}fechaNacimiento').text
        coorN = persona[0].find('{http://www.uniovi.es}coordenadasNacimiento')
        lugF = persona[0].find('{http://www.uniovi.es}lugarFallecimiento')
        fFac = persona[0].find('{http://www.uniovi.es}fechaFallecimiento')
        coorF = persona[0].find('{http://www.uniovi.es}coordenadasFallecimiento')
        desc = persona[0].find('{http://www.uniovi.es}comentario')
        foto = persona[0].find('{http://www.uniovi.es}fotografia').text
        video = persona[0].find('{http://www.uniovi.es}video')
        datos = persona.attrib
        datos['nombre'] = datos.get('nombre')+" "+datos.get('apellido')
        del datos['apellido']
        datos['descripcion']=desc.text
        datos['foto']=foto
        if (coorN and lugN and fNac) is not None:
            latN, lonN, altN = coorN[0].text, coorN[1].text, coorN[2].text
            datos['lugN']=lugN
            datos['fNac']=fNac
            datos['latN']=latN
            datos['lonN']=lonN
            datos['altN']=altN
        if (coorF and lugF and fFac) is not None:
            latF, lonF, altF = coorF[0].text, coorF[1].text, coorF[2].text
            datos['lugF']=lugF.text
            datos['fFac']=fFac.text
            datos['latF']=latF
            datos['lonF']=lonF
            datos['altF']=altF
        else:
            datos['lugF']="NA"
            datos['fFac']="NA"
            datos['latF']="NA"
            datos['lonF']="NA"
            datos['altF']="NA"
        if video is not None:
            datos['video']=video.text
        else:
            datos['video']='NA'
        data1.append(datos)
        
    data = [{}]*15
    for i in range(len(data)):
        data[i] = data1[posicion[0]]
        posicion.pop(0)
        
    return data

def prologoSVG(archivo):
    archivo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    archivo.write('<svg width="1500" height="5270" style="overflow:visible " version="1.1" xmlns="http://www.w3.org/2000/svg">\n')

    
def escribirElemento(archivo, elemento, x, y):
    archivo.write('<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(width)+'" height="'+str(height)+'" style="fill:white;stroke:black;stroke-width:1" />\n')
    archivo.write('<text x="'+str(x+5)+'" y="'+str(y+10)+'" font-size="10" style="fill:black">'+elemento['nombre']+'</text>\n')
    archivo.write('<text x="'+str(x+5)+'" y="'+str(y+22)+'" font-size="10" style="fill:purple">'+elemento['descripcion'][:33]+'</text>\n')
    y += 15
    archivo.write('<text x="'+str(x+10)+'" y="'+str(y+20)+'" font-size="8" style="fill:purple">Datos Nacimiento</text>\n')
    y += 10
    archivo.write('<text x="'+str(x+15)+'" y="'+str(y+20)+'" font-size="8" style="fill:purple">Fecha: '+elemento['fNac']+'</text>\n')
    y += 10
    archivo.write('<text x="'+str(x+15)+'" y="'+str(y+20)+'" font-size="8" style="fill:purple">Lugar: '+elemento['lugN']+'</text>\n')
    y += 10
    archivo.write('<text x="'+str(x+15)+'" y="'+str(y+20)+'" font-size="8" style="fill:purple">Coordenadas: '+elemento['latN']+', '+elemento['lonN']+', '+elemento['altN']+'</text>\n')
    y += 10
    archivo.write('<text x="'+str(x+10)+'" y="'+str(y+20)+'" font-size="8" style="fill:purple">Datos Fallecimiento</text>\n')
    y += 10
    archivo.write('<text x="'+str(x+15)+'" y="'+str(y+20)+'" font-size="8" style="fill:purple">Fecha: '+elemento['fFac']+'</text>\n')
    y += 10
    archivo.write('<text x="'+str(x+15)+'" y="'+str(y+20)+'" font-size="8" style="fill:purple">Lugar: '+elemento['lugF']+'</text>\n')
    y += 10
    archivo.write('<text x="'+str(x+15)+'" y="'+str(y+20)+'" font-size="8" style="fill:purple">Coordenadas: '+elemento['latF']+', '+elemento['lonF']+', '+elemento['altF']+'</text>\n')
    y += 10
    x += width + 20
    #archivo.write('<path d="M'+str(width)+' -40 C'+str(x)+' 40 '+str(y)+' -40 '+str(x)+' 40" style="fill:transparent;stroke:black" />')

    
def añadirContenido(archivo, datos):
    x1, y = 650, 20
    k=0
    escribirElemento(archivo, datos[0], x1, y)
    y += 150
    x = (1/(2))*x1
    for i in range(1,4):
        for j in range(2**i):
            k += 1
            escribirElemento(archivo, datos[k], x, y)
            x += 200*(15/(i+1)**2.1)
        x = (1/(i+1))*(x1-100*(i+1))
        y += 150
        
def añadirRelaciones(archivo):
    
    archivo.write('<path d="M730 140 L1100 170" stroke="purple" stroke-width="2" fill="none" />\n')
    archivo.write('<path d="M730 140 L400 170" stroke="purple" stroke-width="2" fill="none" />\n')
    
    archivo.write('<path d="M395 290 L600 320" stroke="purple" stroke-width="2" fill="none" />\n')
    archivo.write('<path d="M395 290 L300 320" stroke="purple" stroke-width="2" fill="none" />\n')
    
    archivo.write('<path d="M1095 290 L1200 320" stroke="purple" stroke-width="2" fill="none" />\n')
    archivo.write('<path d="M1095 290 L900 320" stroke="purple" stroke-width="2" fill="none" />\n')
    
    archivo.write('<path d="M296 440 L350 470" stroke="purple" stroke-width="2" fill="none" />\n')
    archivo.write('<path d="M296 440 L190 470" stroke="purple" stroke-width="2" fill="none" />\n')
    archivo.write('<path d="M1196 440 L1350 470" stroke="purple" stroke-width="2" fill="none" />\n')
    archivo.write('<path d="M1196 440 L1150 470" stroke="purple" stroke-width="2" fill="none" />\n')
    
    archivo.write('<path d="M596 440 L500 470" stroke="purple" stroke-width="2" fill="none" />\n')
    archivo.write('<path d="M596 440 L690 470" stroke="purple" stroke-width="2" fill="none" />\n')
    archivo.write('<path d="M900 440 L850 470" stroke="purple" stroke-width="2" fill="none" />\n')
    archivo.write('<path d="M900 440 L1000 470" stroke="purple" stroke-width="2" fill="none" />\n')
    
        

def main():
    
    
    archivo = 'arbolGenealogico.xml'
    
    #print(datosXML(archivo))
    
    try:
        arbol = ET.parse(archivo)
        
    except IOError:
        print ('No se encuentra el archivo ', archivo)
        exit()
        
    except ET.ParseError:
        print("Error procesando en el archivo XML = ", archivo)
        exit()
       
    raiz = arbol.getroot()
    
    #nombreSalida  = input("Introduzca el nombre del archivo generado (*.svg) = ")
    nombreSalida = 'arbolGenealogico'
    try:
        salida = open(nombreSalida + ".svg",'w',encoding='utf-8')
    except IOError:
        print ('No se puede crear el archivo ', nombreSalida + ".svg")
        exit()
    
    prologoSVG(salida)
    #añadirContenidoHTML(salida, datosXML(archivo))
    #epilogoHTML(salida)
    añadirContenido(salida, datosXML(archivo))
    añadirRelaciones(salida)
    salida.write('</svg>')
    salida.close()
    print('Documento '+nombreSalida+'.svg creado exitosamente')
    
if __name__ == "__main__":
    main()  
