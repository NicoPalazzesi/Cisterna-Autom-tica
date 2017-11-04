import serial
import time

tanqueLeido='arriba';

with serial.Serial('COM5',9600) as port, open('history.txt','ab') as output:
	while(1):	
		x = port.read(size=10)
		if(x == "completado") or (x == "fallo"):
			#Guardo el estado Final
			x=x+"\r\n"
			output.write(x)
			output.flush()
			#Guardo la fecha
			fecha=time.strftime("%d/%m/%Y")
			fecha=fecha+"\r\n"
			output.write(fecha)
			output.flush()
			#Guardo la hora
			hora=time.strftime("%H:%M")
			hora=hora+"\r\n"
			output.write(hora)
			output.flush()
			#Guardo el porcentaje final de los tanques
			for i in range(2):
				x = port.read(size=6)
				if(i==1):
					x=x+"\r\n"
				output.write(x)
				output.flush()
			#Dejar de mostrar que la bomba esta prendida
		elif(x == "cargando"):
			#Mostrar en pantalla que la bomba esta prendida
			print "bomba prendida"
		else:
			if(tanqueLeido == 'arriba'):
				tanqueLeido = 'abajo'
				#Actualizar el valor del tanque de arriba
			else:
				tanqueLeido = 'arriba'
				#Actualizar el valor del tanque de abajo
