import smbus
from smbus2 import SMBus, i2c_msg
from liquidcrystal_i2c import LCD
import time
from time import sleep
import struct
import sys


#For all the Addresses & Registers of the BNO055:
class BNO055:

	BNO055_ADDR = 0x28
	BNO055_ID = 0xA0
	
	
	#Power modes
	PW_NORMAL = 0x00
	PW_LOW = 0x01
	
	
	#Operation Modes
	OP_CONFIG = 0x00
	OP_COMPASS = 0x09
	OP_ACCEL = 0x01
	OP_MAG = 0x02
	OP_GYRO = 0x03
	
	
	#Accelerometer Data Registers. Scale by 1.
	ACCEL_X_LSB = 0x08
	ACCEL_X_MSB = 0x09
	ACCEL_Y_LSB = 0x0A
	ACCEL_Y_MSB = 0x0B
	ACCEL_Z_LSB = 0x0C
	ACCEL_Z_MSB = 0x0D
	
	#Magnetometer Data Registers. Scale by 1/16.
	MAG_X_LSB = 0x0E
	MAG_X_MSB = 0x0F
	MAG_Y_LSB = 0x10
	MAG_Y_MSB = 0x11
	MAG_Z_LSB = 0x12
	MAG_Z_MSG = 0x13
	
	#Gyro Data Registers. Scale by 1/900.
	GYRO_X_LSB = 0x14
	GYRO_X_MSB = 0x15
	GYRO_Y_LSB = 0x16
	GYRO_Y_MSB = 0x17
	GYRO_Z_LSB = 0x18
	GYRO_Z_MSB = 0x19
	
	
	#Euler Vector Data Registers. Heading, Pitch, Roll. Scale 1/16 to read.
	EULER_H_LSB = 0x1A
	EULER_H_MSB = 0x1B
	EULER_P_LSB = 0x1C
	EULER_P_MSB = 0x1D
	EULER_R_LSB = 0x1E
	EULER_R_MSB = 0x1F
	
	
	#Temperature Data Register
	BNO055_TEMP = 0x34
	
	
	#Status Registers
	BNO055_CALIBRATE = 0x35
	BNO055_SELFTEST_RESULT = 0x36
	BNO055_SYS_STAT = 0x39
	BNO055_SYS_ERR = 0x3A
	
	
	
	#Mode Registers
	BNO055_OP_MODE = 0x3D
	BNO055_PW_MODE = 0x3E
	BNO055_TEMP_SRC = 0x40
	
	










#I2C Bus 0: SDA on pin 27, SCL on pin 28.
#I2C Bus 1: SDA on pin 3, SCL on pin 5.


#BNO055 on bus 0, LCD on bus 1. Subject to Change.
def initI2C():

	try:
		BNOBus = SMBus(0)

		lcd = LCD(bus=1, addr=0x27, cols=16, rows=2)
		lcd.clear()
		lcd.home()
	except:
		return None,None

	return BNOBus, lcd



#Helper fxn for writing to the LCD. "stSm" will make the line Stay Same ( no update )
def LCDWrite(lcd, line1, line2):

	try:
		
		if(line1 != "stSm"):
			lcd.setCursor(0,0)
			lcd.print(line1)
		
		
		if(line2 != "stSm"):
			lcd.setCursor(0,1)
			lcd.print(line2)
			
		lcd.home()

	except:
		return -1

	return 0


#Helper Fxns for BNO055:

#Set Mode sets powermode and operationmode. Use -1 to leave a mode unchanged.
def setMode(bus, powMode, opMode):

	try:
		#PowerMode:
		if(powMode > -1):
			bus.write_byte_data( BNO055.BNO055_ADDR, BNO055.BNO055_PW_MODE, powMode )
		
		#OperationMode:
		if(opMode > -1):
			bus.write_byte_data( BNO055.BNO055_ADDR, BNO055.BNO055_OP_MODE, opMode )
		
	except:
		return -1
		
	return 0



#Reads, Concatenates, Converts 16 bit values ( vectors )
def read16Data(bus, LSBreg):
	
	retnVal = -1
	
	try:
		retnVal = bus.read_byte_data( BNO055.BNO055_ADDR, LSBreg, 0 ) | bus.read_byte_data( BNO055.BNO055_ADDR, LSBreg + 0x01, 0 ) << 8
		
		#Accelerometer
		if(LSBreg < 0x0C and LSBreg > 0x07):
			return retnVal
			
		#Gyro
		if(LSBreg < 0x1A and LSBreg > 0x13):
			return retnVal/900
		
		#Magnetometer or Euler
		else:
			return retnVal/16

	except:
		return retnVal

	
#Reads 8 bit values.
def read8Data(bus, reg):

	try:
		return bus.read_byte_data( BNO055.BNO055_ADDR, reg, 0)
	except:
		return -1




def sendData(BNO):

	return(read8Data(BNO, BNO055.BNO055_TEMP), read16Data(BNO, BNO055.EULER_H_LSB)) 







BNO, LCD = initI2C()

LCDWrite(LCD, "SD Drone2Cell", "")

if(BNO is None or LCD is None):
	sys.exit()



'''
while True:


	temp = read8Data(BNO, BNO055.BNO055_TEMP )
	
	heading = read16Data(BNO,BNO055.EULER_H_LSB)

	LCDWrite(LCD, "stSm", "Temp:" + str(temp) + "C" + " H:" + str(heading))
	
	sendData(BNO)
	
	
	sleep(1)
'''	
	
		
	

	
	
