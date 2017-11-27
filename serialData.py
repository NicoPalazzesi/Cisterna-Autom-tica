import serial
import time

porcentajeTanqueArriba=0
porcentajeTanqueAbajo=0
estado="reposo"

def getPorcentajeTanqueArriba():
	return porcentajeTanqueArriba

def getPorcentajeTanqueAbajo():
	return porcentajeTanqueAbajo

def getEstado():
	return estado

def setPorcentajeTanqueArriba(valor):
	porcentajeTanqueArriba=valor

def setPorcentajeTanqueAbajo(valor):
	porcentajeTanqueAbajo=valor

def setEstado(valor):
	estado=valor

if __name__ == "__main__":
	tanqueLeido='arriba';	#Se define una variable para controla de cual tanque se leyo el ultimo dato

	with serial.Serial('COM4',9600) as port, open('history.txt','ab') as output:	#Se establece la conexion serie a 9600 baudios y se abre el archivo en modo de escritura
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
					setPorcentajeTanqueArriba(x)	#	Actualizar el valor del tanque de arriba
				else:
					tanqueLeido = 'arriba'		#	El proximo valor leido correspondera al tanque de arriba
					setPorcentajeTanqueAbajo(x)		#	Actualizar el valor del tanque de abajo