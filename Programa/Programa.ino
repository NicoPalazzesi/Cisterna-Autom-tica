//Estados del Arduino
const int reposo = 0;
const int cargando = 1;
const int fallo = 2;
int estadoArduino;

//Estados de los Sensores de Agua
const int sensor_de_agua_arriba = 2;
const int sensor_de_agua_abajo = 1;
const double nivel_minimo_agua = 60.00;
const double nivel_maximo_agua = 80.00;
double nivel_tanque_arriba=0;
double nivel_tanque_abajo=0;

//Estados de la Bomba de Agua
const int rele_control = 9;
const int apagar=0;
const int prender=1;
int estadoBomba;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //inicia la comunicación entre el arduino y la pc por serie a 9600 baudios
  pinMode(rele_control, OUTPUT);//Configuro el pin digital del rele como salida

  //Condiciones Iniciales
  estadoArduino=reposo;
  estadoBomba=apagar;
  bomba(apagar);
}

double sensar_agua(int tanque){
  double valorAgua=0;
   valorAgua = analogRead(tanque);
   valorAgua = valorAgua/728; //728 es el valor analogico maximo registrado al sumerguir completamente el sensor de agua.
   valorAgua = valorAgua*100; //calculo el porcentaje
   Serial.println(valorAgua); //imprimo el porcentaje de agua medido
   return(valorAgua);
}

void bomba(int estado){
  if(estado == 0)
    digitalWrite(rele_control,HIGH);//Apago la bomba
  else
    digitalWrite(rele_control,LOW);//Prendo la bomba
}

void loop() {
  // put your main code here, to run repeatedly:
  nivel_tanque_arriba = sensar_agua(sensor_de_agua_arriba);
  nivel_tanque_abajo = sensar_agua(sensor_de_agua_abajo);
  switch(estadoArduino){
    case reposo:
      if(nivel_tanque_arriba<nivel_minimo_agua)
        if(nivel_tanque_abajo >= nivel_minimo_agua){
          estadoArduino=cargando;
          bomba(prender);
          Serial.print("cargando");
        }else
          estadoArduino=fallo;
      break;
    case cargando:
      if(nivel_tanque_arriba>=nivel_maximo_agua || nivel_tanque_abajo<=nivel_minimo_agua){
        bomba(apagar);
        estadoArduino=reposo;
        if(nivel_tanque_arriba>=nivel_maximo_agua)
          Serial.print("completado");
        else
          Serial.print("fallo");
      }
      break;
    case fallo:
      Serial.print("fallo");
      delay(14000);//Mejora: poder cambiar la frecuencia a la que intenta volver a cargar la bomba
      estadoArduino=reposo;
      break;
  }
  Serial.println(nivel_tanque_arriba);
  Serial.println(nivel_tanque_abajo);
  delay(1000);
}
