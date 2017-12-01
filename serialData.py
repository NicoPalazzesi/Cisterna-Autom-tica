import serial
import serial.tools.list_ports


porcentajeTanqueArriba=0
porcentajeTanqueAbajo=0
estado="reposo"

if __name__ == "__main__":
	tanqueLeido='arriba';	#Se define una variable para controla de cual tanque se leyo el ultimo dato

	#Detecta el puerto serie donde se encuentra conectado el Arduino
	ports = list(serial.tools.list_ports.comports())
	for p in ports:
		if "Arduino" in p[1]:
			portArduinoConnect=p[0]

	with serial.Serial(portArduinoConnect,9600) as port, open('history.txt','ab') as output, open('datos.txt', 'ab') as dataout:	#Se establece la conexion serie a 9600 baudios y se abre el archivo en modo de escritura
		while(1):	
			x = port.readline()		#Se lee un dato. Size = 10 indica la cantidad maxima de bytes a leer.
			x = x.rstrip('\r\n')
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
					x = x.rstrip('\r\n')
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

					#Guardo los valores en el archivo
					print porcentajeTanqueArriba
					dataout.write("{0}/{1}/{2}\n".format(porcentajeTanqueArriba,porcentajeTanqueAbajo,estado))
					dataout.flush()