/**************************************************************************/
/*! 
    @file     readMifare.pde
    @author   Adafruit Industries
    @license  BSD (see license.txt)

    This example will wait for any ISO14443A card or tag, and
    depending on the size of the UID will attempt to read from it.
   
    If the card has a 4-byte UID it is probably a Mifare
    Classic card, and the following steps are taken:
   
    - Authenticate block 4 (the first block of Sector 1) using
      the default KEYA of 0XFF 0XFF 0XFF 0XFF 0XFF 0XFF
    - If authentication succeeds, we can then read any of the
      4 blocks in that sector (though only block 4 is read here)
   
    If the card has a 7-byte UID it is probably a Mifare
    Ultralight card, and the 4 byte pages can be read directly.
    Page 4 is read by default since this is the first 'general-
    purpose' page on the tags.


    This is an example sketch for the Adafruit PN532 NFC/RFID breakout boards
    This library works with the Adafruit NFC breakout 
      ----> https://www.adafruit.com/products/364
 
    Check out the links above for our tutorials and wiring diagrams 
    These chips use I2C to communicate

    Adafruit invests time and resources providing this open source code, 
    please support Adafruit and open-source hardware by purchasing 
    products from Adafruit!
*/
/**************************************************************************/
#include <Wire.h>
#include <Adafruit_NFCShield_I2C.h>

#define IRQ   (2)
#define RESET (3)  // Not connected by default on the NFC Shield

Adafruit_NFCShield_I2C nfc(IRQ, RESET);

int led13 = 13;
int led11 = 11;

boolean occupied = false;
boolean isInputComplete = false;
boolean readNFC = false;
byte fromFrontBuffer[0];

uint8_t currUid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned U

void setup(void) {
  pinMode(led13, OUTPUT);
  pinMode(led11, OUTPUT);
  Serial.begin(115200);
  readNFC = false;
  isInputComplete = false;
  //  Serial.println("Hello!");

  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    Serial.print("Didn't find PN53x board");
    while (1); // halt
  }
  // Got ok data, print it out!
//  Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX); 
//  Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC); 
//  Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);
  
  // configure board to read RFID tags
  nfc.SAMConfig();
  
//  Serial.println("Waiting for an ISO14443A Card ...");
}


void loop(void) {
  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
    
  // Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
  // 'uid' will be populated with the UID, and uidLength will indicate
  // if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
  if(!readNFC)
  {
//    Serial.println("DEBUG: waiting for NFC");
    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);
    if (success) {
      // Display some basic information about the card
  //    Serial.println("Found an ISO14443A card");
  //    Serial.print("  UID Length: ");Serial.print(uidLength, DEC);Serial.println(" bytes");
  //    Serial.print("  UID Value: ");
  //    nfc.PrintHex(uid, uidLength);
  //    Serial.println("");
      
      if (uidLength == 4)
      {
        uint8_t keya[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };
        success = true;
      
        if (success)
        {
  //        Serial.println("Sector 1 (Blocks 4..7) has been authenticated");
          uint8_t data[16];
          // Try to read the contents of block 4
  //        success = nfc.mifareclassic_ReadDataBlock(4, data);
    
          if (success)
          {
            /* 2 for invalid card
               0 for valid card and locking bike
               1 for valid card and unlocking bike
            */
            authenticateUid(uid, uidLength);
          }
          else
          {
  //          Serial.println("Ooops ... unable to read the requested block.  Try another key?");
          }
        }
        else
        {
          Serial.println("Ooops ... authentication failed: Try another key?");
        }
      }
    }
  }
  else
  {
    if(isInputComplete)
    {
      
      if (fromFrontBuffer[0] != -1)
      {
        if (fromFrontBuffer[0] == 0)
        {
          digitalWrite(led11, HIGH); // turn on occupied FLAG
//          Serial.println("You have successfully locked your bike!");
        }
        if (fromFrontBuffer[0] == 1)
        {
          digitalWrite(led13, HIGH);   // turn the LED on (HIGH is the voltage level)
          delay(250);               // wait for a second
          digitalWrite(led13, LOW); 
          
          digitalWrite(led11, LOW);  // turn off occupied FLAG
        }    
      }
      // Wait a bit before reading the card again
      delay(1000);
      readNFC = false;
      isInputComplete = false;
    }
     
  }
}

void authenticateUid(uint8_t uid[], uint8_t uidLength){
    nfc.PrintHex(uid, uidLength);
    readNFC = true;
}

void serialEvent()
{
  char command[0];
  char validInput[3] = {'0', '1', '2'};
  boolean isValid = false;
//  readByteArrayFromSerial(fromFrontBuffer, 10);
  command[0] = Serial.read();
  
  for (int i=0; i<3; i++) { 
    if (command[0] == validInput[i])
      isValid = true;
  }
  
  if(isValid) { 
    fromFrontBuffer[0] = charNumToByteNum(char(command[0]));
    isInputComplete = true;
  }
  
}

byte charNumToByteNum(char c){
  if (c >=48 && c <= 57){
     return (c - 48); 
  } 
}
