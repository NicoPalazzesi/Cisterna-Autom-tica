from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/history')
def history():
	i=0
	tamano=0
	estado=[]
	fecha=[]
	hora=[]
	tanqueArriba=[]
	tanqueAbajo=[]
	with open('history.txt', 'r') as file:
		for line in file:
			if(i==0):
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

	return render_template('history.html',estado=estado,fecha=fecha,hora=hora,tanqueArriba=tanqueArriba,tanqueAbajo=tanqueAbajo,tamano=tamano)

@app.route('/pruebas')
def pruebas():
	return render_template('pruebas.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=True)