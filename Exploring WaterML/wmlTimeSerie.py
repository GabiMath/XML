# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 04:59:39 2021

@author: Gabriela
"""

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from dateutil.parser import parse

def timeSerieWML(file):
    x = []
    y = []
    try:
        tree = ET.parse(file)
        
    except IOError:
        print ('No se encuentra el archivo ', file)
        exit()
        
    except ET.ParseError:
        print("Error procesando en el archivo XML = ", file)
        exit()
    root = tree.getroot()
    url=root.tag.split('}')[0]
    for measurement in root.iter(url+'}MeasurementTVP'):
        date = measurement.find(url+'}time').text
        value = measurement.find(url+'}value').text
        date = parse(date)
        x.append(date)
        y.append(value)
    fig, ax = plt.subplots(figsize=(15, 8), dpi=200)
    ax.plot(x, y)
    fig.autofmt_xdate()
    ax.set_title('Time Serie')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    nombre = file.split('.')[0]
    plt.savefig(nombre+'.svg')

def main():
    
    #measurement-timeseries-discharge.wml
    #KiWIS-WML2-Example.wml
    
    file = input('Ingrese el nombre del archivo wml: ')
    
    #print(datosXML(archivo))
    
    timeSerieWML(file)
    
    print('Archivo SVG creado con éxito')
    
if __name__ == "__main__":
    main()  