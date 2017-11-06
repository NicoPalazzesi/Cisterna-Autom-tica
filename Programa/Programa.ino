//Estados del Arduino
const int reposo = 0;
const int cargando = 1;
int estadoArduino;

//Estados de los Sensores de Agua
const int sensor_de_agua_arriba = 2;
const int sensor_de_agua_abajo = 1;
const double nivel_minimo_agua = 60.00;
const double nivel_maximo_agua = 80.00;
double nivel_tanque_arriba;
double nivel_tanque_abajo;

//Estados de la Bomba de Agua
const int rele_control = 9;
const int apagar = 0;
const int prender = 1;
int estadoBomba=apagar;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //inicia la comunicación entre el arduino y la pc por serie a 9600 baudios
  pinMode(rele_control, OUTPUT);//Configuro el pin digital del rele como salida

  //Configuraciones y condiciones iniciales
  estadoArduino=reposo;
  bomba(apagar);
}

double sensar_agua(int tanque){
  double valorAgua=0;
   valorAgua = analogRead(tanque);  //Lee el valor del sensor correspondiente al tanque indicado en la variable 'tanque'
   valorAgua = valorAgua/728; //728 es el valor analogico maximo registrado al sumerguir completamente el sensor de agua.
   valorAgua = valorAgua*100; //calculo el porcentaje
   //Serial.println(valorAgua); //imprimo el porcentaje de agua medido
   return(valorAgua);
}

void bomba(int estado){
  if(estado == 0)   // estado = 0 --> bomba encendida. estado = 1 --> bomba apagada
    digitalWrite(rele_control,HIGH);//Apago la bomba
  else
    digitalWrite(rele_control,LOW);//Prendo la bomba
}

void loop() {
  // put your main code here, to run repeatedly:
  nivel_tanque_arriba = sensar_agua(sensor_de_agua_arriba); //Se sensa el nivel del tanque superior
  nivel_tanque_abajo = sensar_agua(sensor_de_agua_abajo);   //Se sensa el nivel del tanque inferior
  switch(estadoArduino){
    case reposo:                
      if(nivel_tanque_arriba<nivel_minimo_agua)       //Si el nivel del agua del tanque superior es menor al minimo establecido (en este caso, 50.00 o medio tanque)
        if(nivel_tanque_abajo >= nivel_minimo_agua){  //Si el nivel del agua del tanque inferior es mayor al minimo establecido
          estadoArduino=cargando;                     //Cambio de estado
          bomba(prender);                             //Se enciende la bomba
          Serial.print("cargando");                   //Se envia una linea a la PC indicando que comenzo la carga
        }else                                         
          Serial.print("fallo");                      //Se envia una linea a la PC indicando que ocurrió un fallo
      break;
    case cargando:
      if(nivel_tanque_arriba>=nivel_maximo_agua || nivel_tanque_abajo<=nivel_minimo_agua ){ //Si el nivel del agua del tanque superior es mayor al maximo establecido (en este caso, 98.00) o el nivel del agua del tanque inferior es menor al minimo establecido
        bomba(apagar);                    //Se apaga la bomba
        estadoArduino=reposo;             //Cambio de estado
        if(nivel_tanque_arriba>=nivel_maximo_agua)  //Si se cumplió la primera condición, quiere decir que se completó la carga del tanque superior
          Serial.print("completado");               //Se envia una linea a la PC indicando que se completó correctamente la carga
        else                             //El tanque inferior se quedo sin agua suficiente
          Serial.print("fallo");         //Se envia una linea a la PC indicando que comenzo la carga
      }
      break;
  }
  Serial.println(nivel_tanque_arriba);    //Se envia el nivel del tanque superior a la PC
  Serial.println(nivel_tanque_abajo);     //Se envia el nivel del tanque inferior a la PC
  delay(1000);       //Espera 1 segundo antes de volver a ejecutar el loop
}
