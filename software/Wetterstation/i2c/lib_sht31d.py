import time

class SHT31D():
	
	def __init__(self, bus, address:int=0x44): # https://github.com/ncdcommunity/Raspberry_Pi_SHT31_Humidity_Temperature_Sensor_Python_library/blob/master/SHT31.py
		self.__bus = bus
		self.__address = address

	def getHeater(self) -> bool:
		self.__bus.write_i2c_block_data(self.__address, 0xF3, [0x2D])
		time.sleep(0.5)
		data = self.__bus.read_i2c_block_data(self.__address, 0x00, 3)
		state = ((data[0] << 8) | data[1]) & 0x2000 # isoliere das 14. Bit von rechts
		return bool(state)
	
	def setHeater(self, state:bool):
		if(state):
			self.__bus.write_i2c_block_data(self.__address, 0x30, [0x6D])
		else:
			self.__bus.write_i2c_block_data(self.__address, 0x30, [0x66])
		time.sleep(0.5)
	
	def read(self) -> tuple:
		self.__bus.write_i2c_block_data(self.__address, 0x2C, [0x06])
		time.sleep(0.5)
		data = self.__bus.read_i2c_block_data(self.__address, 0x00, 6)
		
		# Convert the data
		temp = (data[0] << 8) | data[1]
		cTemp = -45 + (175 * temp / 65535.0)
		#fTemp = -49 + (315 * temp / 65535.0)
		humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
		
		return (cTemp, humidity)