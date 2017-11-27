from flask import Flask, render_template		#Se importan los modulos necesarios de Flask para poder levantar la web
import threading
import serial
import time

porcentajeTanqueArriba=0
porcentajeTanqueAbajo=0
estado="reposo"

def seriaDataThreadFunction():
	global porcentajeTanqueArriba
	global porcentajeTanqueAbajo
	global estado
	tanqueLeido='arriba';	#Se define una variable para controla de cual tanque se leyo el ultimo dato

	with serial.Serial('COM5',9600) as port, open('history.txt','ab') as output:	#Se establece la conexion serie a 9600 baudios y se abre el archivo en modo de escritura
		while(1):	
			x = port.read(size=10)		#Se lee un dato. Size = 10 indica la cantidad maxima de bytes a leer.
			#print porcentajeTanqueArriba
			if(x == "completado") or (x == "fallo"):	#Si el dato leido es completado o fallo, se debe almacenar en el archivo
				#Guardo el estado Final
				x=x+"\r\n"								#Se agrega un salto de linea al final del dato
				output.write(x)							#Se escribe el dato en el archivo
				output.flush()
				#Guardo la fecha
				fecha=time.strftime("%d/%m/%Y")			#
				fecha=fecha+"\r\n"						#	 Se escribe la fecha actual
				output.write(fecha)						#		en el archivo
				output.flush()							#
				#Guardo la hora
				hora=time.strftime("%H:%M")				#
				hora=hora+"\r\n"						# 	Se escribe la hora actual
				output.write(hora)						#		en el archivo
				output.flush()							#
				
				#Guardo el porcentaje final de los tanques
				for i in range(2):						#	
					x = port.read(size=6)				# 	Los siguientes dos datos leidos 
					if(i==1):							#		indican el valor sensado
						x=x+"\r\n"						#			de los tanques
					output.write(x)
					output.flush()
					estado="reposo"				#Dejar de mostrar que la bomba esta prendida
			elif(x == "cargando"):				# Si el dato leido es cargando, se indica en la pagina principal de la web que la bomba esta encendida
				estado="funcionando"			#Mostrar en pantalla que la bomba esta prendida
			else:								#	Significa que lo que se leyo fue un valor numerico
				if(tanqueLeido == 'arriba'):	#	Si el valor leido corresponde al tanque de arriba
					tanqueLeido = 'abajo'		#		el proximo valor a leer sera del de abajo
					porcentajeTanqueArriba = x	#	Actualizar el valor del tanque de arriba
				else:
					tanqueLeido = 'arriba'		#	El proximo valor leido correspondera al tanque de arriba
					porcentajeTanqueAbajo = x	#	Actualizar el valor del tanque de abajo

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', tanqueArriba=porcentajeTanqueArriba, tanqueAbajo=20, estado="reposo")

@app.route('/history')
def history():
	i=0				#Se define una variable para controlar que dato se leyo
	tamano=0		#En la variable tamano se cuentan cuantas filas completas de datos se leyeron
	estado=[]		# Se definen cinco arreglos en los que se almacenan todos los datos leidos
	fecha=[]		
	hora=[]
	tanqueArriba=[]
	tanqueAbajo=[]
	with open('history.txt', 'r') as file:		#Se abre el archivo en modo lectura
		for line in file:						#Se lee una linea y para cada una se anade al final
			if(i==0):							#del arreglo correspondiente 
				estado.append(line[:-1])
			elif(i==1):
				fecha.append(line[:-1])
			elif(i==2):
				hora.append(line[:-1])
			elif(i==3):
				tanqueArriba.append(line[:-4])
			elif(i==4):
				tanqueAbajo.append(line[:-4])
			i=i+1
			if(i==5):
				i=0
				tamano=tamano+1
	return render_template('history.html',estado=estado,fecha=fecha,hora=hora,tanqueArriba=tanqueArriba,tanqueAbajo=tanqueAbajo,tamano=tamano) #Se renderiza la pagina del historial de la web

@app.route('/pruebas')
def pruebas():
	return render_template('pruebas.html')

if __name__ == '__main__':		#Esta linea controla que se haya corrido el script desde la linea de comandos y no desde otro script
	seriaDataThread = threading.Thread(target = seriaDataThreadFunction)
	#seriaDataThread.start()
	#seriaDataThread.join()
	app.run(debug=True, host='0.0.0.0', use_reloader=True) #Levanta el servidor