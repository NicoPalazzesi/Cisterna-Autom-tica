from flask import Flask, render_template		#Se importan los modulos necesarios de Flask para poder levantar la web

app = Flask(__name__)
@app.route('/')
def index():
	return render_template('index.html')	#Se renderiza la página principal de la web

@app.route('/history')
def history():
	i=0				#Se define una variable para controlar que dato se leyó
	tamano=0		#En la variable tamaño se cuentan cuantas filas completas de datos se leyeron
	estado=[]		# Se definen cinco arreglos en los que se almacenan todos los datos leídos
	fecha=[]		
	hora=[]
	tanqueArriba=[]
	tanqueAbajo=[]
	with open('history.txt', 'r') as file:		#Se abre el archivo en modo lectura
		for line in file:						#Se lee una linea y para cada una se añade al final
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
	return render_template('history.html',estado=estado,fecha=fecha,hora=hora,tanqueArriba=tanqueArriba,tanqueAbajo=tanqueAbajo,tamano=tamano) #Se renderiza la página del historial de la web

@app.route('/pruebas')
def pruebas():
	return render_template('pruebas.html')

if __name__ == '__main__':		#Esta linea controla que se haya corrido el script desde la linea de comandos y no desde otro script
    app.run(debug=True, host='0.0.0.0', use_reloader=True) #Levanta el servidor