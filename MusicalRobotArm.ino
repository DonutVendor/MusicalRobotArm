#include <Braccio.h>
#include <Servo.h>
#include <math.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

float a0, a1, a2, a3;
String lastInput;

int xMove, yMove, zMove;
int xJog, yJog, zJog;

int currentCoord = 0;
int inputType = 0;

float thetaBase = 90;
float thetaShoulder = 45;
float thetaElbow = 180;
float thetaWristVertical = 90;
float thetaWristRotation = 90;
float thetaGripper = 73;

float BASE_HGT = 70;
float HUMERUS = 125;
float ULNA = 125;
float GRIPPER = 200;

/* pre-calculations */
float hum_sq;
float uln_sq;

void setup() {

  hum_sq = HUMERUS*HUMERUS;
  uln_sq = ULNA*ULNA;

  Serial.begin(9600);

  pinMode(12, OUTPUT);    //you need to set HIGH the pin 12
  digitalWrite(12, HIGH);
  
  Braccio.begin(SOFT_START_DISABLED);

  //callHome();

  Serial.println("Booted and Ready!");

  //testRun();
}

void restartBraccio(){
  Braccio.begin();
}

void callHome(){
  Braccio.ServoMovement(20, 90, 45, 180, 180, 90, 73);
}

void openClaw(){
  thetaGripper = 10;
  Braccio.ServoMovement(20, thetaBase, thetaShoulder, thetaElbow, thetaWristVertical, thetaWristRotation, thetaGripper);
}

void closeClaw(){
  thetaGripper = 73;
  Braccio.ServoMovement(20, thetaBase, thetaShoulder, thetaElbow, thetaWristVertical, thetaWristRotation, thetaGripper);
}

void rotateClaw1(){
  thetaWristRotation += 90;
  Braccio.ServoMovement(20, thetaBase, thetaShoulder, thetaElbow, thetaWristVertical, thetaWristRotation, thetaGripper);
}

void rotateClaw2(){
  thetaWristRotation -= 90;
  Braccio.ServoMovement(20, thetaBase, thetaShoulder, thetaElbow, thetaWristVertical, thetaWristRotation, thetaGripper);
}

void loop() {
  if (Serial.available())  {
    char c = Serial.read();  //gets one byte from serial buffer
    if(c == 'M'){
      lastInput=""; //clears variable for new input 
      currentCoord = 0;
      inputType = 0;
    }
    else if(c == 'J'){
      lastInput=""; //clears variable for new input ?
      currentCoord = 0;
      inputType = 1;
    }
    else if(c == 'G'){
      lastInput=""; //clears variable for new input ?
      currentCoord = 0;
      inputType = 2;
      Serial.print("Current Pos: "); Serial.print(xMove);Serial.print(", ");Serial.print(yMove);Serial.print(", ");Serial.print(zMove); Serial.println("");
      printAngles();
    }
    else if(c == 'H'){
      lastInput=""; //clears variable for new input ?
      currentCoord = 0;
      inputType = 3;
      callHome();
    }
    else if(c == 'O'){
      lastInput=""; //clears variable for new input ?
      currentCoord = 0;
      inputType = 4;
      openClaw();
    }
    else if(c == 'D'){
      //Strum in currect position 
      lastInput=""; //clears variable for new input ?
      currentCoord = 0;
      inputType = 5;
      moveTo(xMove, yMove + 30, zMove, 10);
      delay(100);
      moveTo(xMove, yMove - 30, zMove, 5);
    }
    else if(c == 'C'){
      lastInput=""; //clears variable for new input ?
      currentCoord = 0;
      inputType = 6;
      closeClaw();
    }else if(c == 'R'){
      lastInput=""; //clears variable for new input ?
      currentCoord = 0;
      inputType = 7;
      restartBraccio();
    }else if(c == 'E'){
      lastInput=""; //clears variable for new input ?
      currentCoord = 0;
      inputType = 6;
      rotateClaw1();
    }else if(c == 'Q'){
      lastInput=""; //clears variable for new input ?
      currentCoord = 0;
      inputType = 6;
      rotateClaw2();
    }
    else if (inputType == 0 && c == ',') {
      if(currentCoord == 0){
        xMove = lastInput.toInt();
      }else if(currentCoord == 1){
        yMove = lastInput.toInt();
      }else if(currentCoord == 2){
        zMove = lastInput.toInt();
        moveTo(xMove, yMove, zMove, 20);
        Serial.print("Moving to: "); Serial.print(xMove);Serial.print(", ");Serial.print(yMove);Serial.print(", ");Serial.print(zMove); Serial.println("");
      }
      currentCoord++;
      
      //Serial.println(lastInput); //prints string to serial port out
      lastInput=""; //clears variable for new input     
    }
    else if(inputType == 1 && c == ','){
      if(currentCoord == 0){
        xJog = lastInput.toInt();
      }else if(currentCoord == 1){
        yJog = lastInput.toInt();
      }else if(currentCoord == 2){
        zJog = lastInput.toInt();
        jog(xJog, yJog, zJog, 20);
        Serial.print("Jogging to: "); Serial.print(xMove);Serial.print(", ");Serial.print(yMove);Serial.print(", ");Serial.print(zMove); Serial.println("");
      }
      currentCoord++;
      
      //Serial.println(lastInput); //prints string to serial port out
      lastInput=""; //clears variable for new input  
    }
    else {     
      lastInput += c; //makes the string readString
    }
  }
}

void moveTo(int x, int y, int z, float moveSpeed){
  
  SetArm(x, y, z);

  printAngles();
 
  /*
    Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
    M1=base degrees. Allowed values from 0 to 180 degrees
    M2=shoulder degrees. Allowed values from 15 to 165 degrees
    M3=elbow degrees. Allowed values from 0 to 180 degrees
    M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
    M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
    M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  */
  Braccio.ServoMovement(moveSpeed, thetaBase, thetaShoulder, thetaElbow, thetaWristVertical, thetaWristRotation, thetaGripper);

  xMove = x; yMove = y; zMove = z;
}

void printAngles(){
  Serial.print("Angles: "); Serial.print(thetaBase);Serial.print(", ");Serial.print(thetaShoulder);Serial.print(", ");Serial.print(thetaElbow); Serial.print(", ");Serial.print(thetaWristVertical); Serial.print(", ");Serial.print(thetaWristRotation);Serial.print(", ");Serial.print(thetaGripper);Serial.println("");
}

void jog(int x, int y, int z, float moveSpeed){
  xMove += x;
  yMove += y;
  zMove += z;
  moveTo(xMove, yMove, zMove, moveSpeed);
}

// Quick conversion from the Braccio angle system to radians
float b2a(float b){
  return b / 180.0 * PI - HALF_PI;
}

// Quick conversion from radians to the Braccio angle system
float a2b(float a) {
  return (a + HALF_PI) * 180 / PI;
}

float rad2deg(float rad){
  return (rad * 4068) / 71;
}

void SetArm(float x, float y, float z) {
    // Base angle
    float bas_angle_r = atan2( x, z );
    float bas_angle_d = rad2deg(bas_angle_r) + 90;

    float wrt_y = y - BASE_HGT; // Wrist relative height to shoulder
    float s_w = x * x + z * z + wrt_y * wrt_y; // Shoulder to wrist distance square
    float s_w_sqrt = sqrt (s_w);

    // Elbow angle: knowing 3 edges of the triangle, get the angle
    float elb_angle_r = acos ((hum_sq + uln_sq - s_w) / (2 * HUMERUS * ULNA));
    float elb_angle_d = 270 - rad2deg(elb_angle_r) - 90;

    // Shoulder angle = a1 + a2
    float a1 = atan2 (wrt_y, sqrt (x * x + z * z));
    float a2 = acos ((hum_sq + s_w - uln_sq) / (2 * HUMERUS * s_w_sqrt));
    float shl_angle_r = a1 + a2;
    float shl_angle_d = 180 - rad2deg(shl_angle_r) - 90;

    ////////
    float end_x = xMove;
    float end_y = yMove;
    float end_z = zMove;

    float end_last_angle = thetaWristVertical;

    float dx = end_x - x;
    float dz = end_z - z;

    float wrt_angle_r = atan2(end_y - y, sqrt(dx * dx + dz * dz));
    float wrt_angle_d = end_last_angle + rad2deg(wrt_angle_r);

    // Update angle
    if (wrt_angle_d >= 0 && wrt_angle_d <= 180)
      thetaWristVertical = wrt_angle_d - 90;

    //////////

    // Update angles
    if (bas_angle_d >= 0 && bas_angle_d <= 180)
      thetaBase = bas_angle_d;
    if (shl_angle_d >= 15 && shl_angle_d <= 165)
      thetaShoulder = shl_angle_d;
    if (elb_angle_d >= 0 && elb_angle_d <=180)
      thetaElbow = elb_angle_d; 
}
