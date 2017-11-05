import serial
import time
import app as a

<<<<<<< HEAD
tanqueLeido='arriba';	#Se define una variable para controla de cual tanque se leyo el ultimo dato
=======
tanqueLeido='arriba'
>>>>>>> table-history

with serial.Serial('COM5',9600) as port, open('history.txt','ab') as output:	#Se establece la conexión serie a 9600 baudios y se abre el archivo en modo de escritura
	while(1):	
<<<<<<< HEAD
		x = port.read(size=10)		#Se lee un dato. Size = 10 indica la cantidad máxima de bytes a leer.
		if(x == "completado") or (x == "fallo"):	#Si el dato leido es completado o fallo, se debe almacenar en el archivo
=======
		x = port.read(size=10)
		a.porcentajeTanqueArriba=50;
		if(x == "completado") or (x == "fallo"):
>>>>>>> table-history
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
				x = port.read(size=6)				# 	Los siguientes dos datos leídos 
				if(i==1):							#		indican el valor sensado
					x=x+"\r\n"						#			de los tanques
				output.write(x)
				output.flush()
			
			#Dejar de mostrar que la bomba esta prendida
		elif(x == "cargando"):			# Si el dato leido es cargando, se indica en la página principal de la web que la bomba esta encendida
			#Mostrar en pantalla que la bomba esta prendida
			print "bomba prendida"
<<<<<<< HEAD
		else:							#Significa que lo que se leyó fue un valor numérico
			if(tanqueLeido == 'arriba'):	#	Si el valor leído corresponde al tanque de arriba
				tanqueLeido = 'abajo'		#		el proximo valor a leer será del de abajo
				#Actualizar el valor del tanque de arriba
			else:
				tanqueLeido = 'arriba'		#	El proximo valor leido corresponderá al tanque de arriba
				#Actualizar el valor del tanque de abajo
=======
		else:
			if(tanqueLeido == 'arriba'):
				tanqueLeido = 'abajo'
				#porcentajeTanqueArriba=50
			else:
				tanqueLeido = 'arriba'
				#porcentajeTanqueAbajo=x
>>>>>>> table-history
