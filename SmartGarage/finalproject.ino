/*int pin11Buzzer = 11;
int sensorPin2 = A1; // Cambia el pin del sensor a un pin analógico (por ejemplo, A0)
int lecturaPin2 = 0;

int threshold = 500; // Establece un umbral de sensibilidad

void setup() {
  Serial.begin(9600);
  pinMode(pin11Buzzer, OUTPUT);
  pinMode(sensorPin2, INPUT);
}

void loop() {
  lecturaPin2 = analogRead(sensorPin2); // Lee el valor analógico del sensor
  Serial.println(lecturaPin2);

  if (lecturaPin2 < 1010) { // Compara el valor leído con el umbral
    digitalWrite(pin11Buzzer, HIGH);
    delay(1000);
    digitalWrite(pin11Buzzer, LOW);
  }
}
*/


#include <Servo.h>

const int sensorPiezo = A0; // Pin analógico donde está conectado el sensor piezoeléctrico
const int sensorKY031 = A1; // Pin analógico donde está conectado el sensor KY-031
const int sensorPin = A2; // Pin analógico donde está conectado el sensor KY-028
const int ledPin = 2; // Pin del LED incorporado en la placa Arduino
const int servoPin = 9; // Pin del servo motor
const int pin11Buzzer = 11;
Servo myServo;
int pos = 0;          // Variable para almacenar la posición actual del servo
int increment = 1;    // Valor de incremento para mover el servo lentamente


int thresholdPiezo = 50; // Umbral de sensibilidad para el sensor piezoeléctrico
int thresholdKY031 = 500; // Umbral de sensibilidad para el sensor KY-031

// Parámetros de calibración del sensor NTC
const float A = 0.001129148;
const float B = 0.000234125;
const float C = 0.0000000876741;

void setup() {
  myServo.attach(servoPin); // Inicializa el servo motor
  pinMode(ledPin, OUTPUT);
  pinMode(sensorPiezo, INPUT);
  pinMode(sensorKY031, INPUT);
  pinMode(pin11Buzzer, OUTPUT);
  
  Serial.begin(9600); // Inicia la comunicación serial a 9600 baudios
}

void loop() {
  int sensorValuePiezo = analogRead(sensorPiezo); // Lee el valor del sensor piezoeléctrico
  int sensorValueKY031 = analogRead(sensorKY031); // Lee el valor del sensor KY-031
  
  Serial.println("Valor del sensor piezoeléctrico: " + String(sensorValuePiezo));
  Serial.println("Valor del sensor KY-031: " + String(sensorValueKY031));

  if (sensorValuePiezo > thresholdPiezo) {
    digitalWrite(ledPin, HIGH); // Enciende el LED si se detecta una vibración con el sensor piezoeléctrico
    for (pos = 0; pos <= 90; pos += increment) {
      myServo.write(pos);
      delay(15); // Pequeña pausa para controlar la velocidad (ajusta según sea necesario)
    }
    delay(4000); // Mantén el servo en posición durante 4 segundos
    for (pos = 90; pos >= 0; pos -= increment) {
      myServo.write(pos);
      delay(15); // Pequeña pausa para controlar la velocidad (ajusta según sea necesario)
    }
    digitalWrite(ledPin, LOW); // Apaga el LED
  }
  
  if (sensorValueKY031 < 1020) {
    // Compara el valor leído con el umbral
    digitalWrite(pin11Buzzer, HIGH);
    delay(1000);
    digitalWrite(pin11Buzzer, LOW);
  }

   int sensorValue = analogRead(sensorPin);

  // Invertimos las lecturas para obtener valores positivos
  sensorValue = 1023 - sensorValue;

  // Convertimos el valor analógico en resistencia
  float resistance = (1023.0 / sensorValue - 1.0) * 10000.0;

  // Calculamos la temperatura utilizando la ecuación de Steinhart-Hart
  float temperaturaKelvin = 1.0 / (A + B * log(resistance) + C * pow(log(resistance), 3));
  float temperaturaCelsius = temperaturaKelvin - 273.15;

  // Si la temperatura es menor que cero, ajustamos a cero para evitar valores negativos
  if (temperaturaCelsius < 0) {
    temperaturaCelsius = 0;
  }

  // Envia la temperatura a través de la comunicación serial
  Serial.print(temperaturaCelsius);
  Serial.println();
}
