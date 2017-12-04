from flask import Flask, render_template		#Se importan los modulos necesarios de Flask para poder levantar la web

app = Flask(__name__)

@app.route('/')
def index():
	#Apertura de archivo donde se alojan los ultimos valores leidos desde el arduino

	with open('datos.txt','r') as datain:
		line = datain.readline()			#Lectura de los datos
		data=line.split("/")
		#print("TArriba: {}, TAbajo: {}, Estado: {}".format(data[0],data[1],data[2]))
		porcentajeTanqueArriba = data[0]
		porcentajeTanqueAbajo = data[1]
		estado = data[2].rstrip('\r\n')
		print porcentajeTanqueArriba
	return render_template('index.html', tanqueArriba=porcentajeTanqueArriba, tanqueAbajo=porcentajeTanqueAbajo, estado=estado)

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
				tanqueArriba.append(line[:-1])
			elif(i==4):
				tanqueAbajo.append(line[:-1])
			i=i+1
			if(i==5):
				i=0
				tamano=tamano+1
	return render_template('history.html',estado=estado,fecha=fecha,hora=hora,tanqueArriba=tanqueArriba,tanqueAbajo=tanqueAbajo,tamano=tamano) #Se renderiza la pagina del historial de la web

if __name__ == '__main__':		#Esta linea controla que se haya corrido el script desde la linea de comandos y no desde otro script
	app.run(debug=True, host='0.0.0.0', use_reloader=True) #Levanta el servidor