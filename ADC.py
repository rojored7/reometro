import time
import Adafruit_ADS1x15
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
import threading

adc = Adafruit_ADS1x15.ADS1115()                #asigna la libreria al adc
gData = []                                      #crea una lista 
gData.append([0])                               #agrega el valor 0 al primer item de la lista
gData.append([0])                               #agrega el valor 0 al segundo item de la lista
GAIN = 1                                        #asigna ganacia 0

#Configuramos la gráfica
fig = plt.figure()
ax = fig.add_subplot(111)
hl, = plt.plot(gData[0], gData[1])
plt.ylim(-1000, 40000)                          #Se configura el alto de la ventana dependiendo el valor maximo y minimo que se puede tener en el canal del i2c
plt.xlim(0,500)

def GetData(out_data):
    while True:
        value = adc.read_adc(0, gain=GAIN)          #lee el valor del adc (selecciona el canal, el valor de la ganancia)
       #print(value)                                #imprime el valor que tiene 
        time.sleep(0.1)                             
        # Añadimos el nuevo valor, si hay más de 500 muestras quitamos la primera
        
        out_data[1].append( float(value) )
        if len(out_data[1]) > 500:
            out_data[1].pop(0)

# Función que actualizará los datos de la gráfica
# Se llama periódicamente desde el 'FuncAnimation'
def update_line(num, hl, data):
    hl.set_data(range(len(data[1])), data[1])
    return hl,

# Configuramos la función que "animará" nuestra gráfica
line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, gData),
    interval=50, blit=False)

# Configuramos y lanzamos el hilo encargado de leer datos del i2c
dataCollector = threading.Thread(target = GetData, args=(gData,))
dataCollector.start()
plt.show()
dataCollector.join()
