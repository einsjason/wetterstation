import math
from time import sleep

class TLV493D: # https://github.com/Infineon/RaspberryPi_TLV/
	
	"""Class of 3D Magnetic Sensor TLV493D.
	"""
	
	__bx = 0
	__by = 0
	__bz = 0 
	__temp = 0
	__data =[]
	
	def __init__(self, bus, address:int = 0x5e):
		self.__address = address
		self.__bus = bus

	def __update_data(self):
		""" Read data from register
		"""
		self.__bus.write_byte_data(self.__address, 0x11,0x01)
		self.__data = self.__bus.read_i2c_block_data(self.__address, 0x00, 10)

		self.__get_x()
		self.__get_y()
		self.__get_z()
		 
	def __get_x(self):
		self.__bx = (self.__data[0] << 4) or ((self.__data[4] >> 4) & 0x0f)
		
		if self.__bx > 2047:	
			self.__bx -= 4096
		self.__bx *=0.098
   
	def __get_y(self):
		self.__by = self.__data[1] << 4 or self.__data[4] & 0x0f

		if self.__by > 2047:
			self.__by -= 4096
		self.__by *=0.098

	def __get_z(self):
		self.__bz = self.__data[2] << 4 or self.__data[5] & 0x0f
		
		if self.__bz > 2047:
			self.__bz -= 4096
		self.__bz *=0.098
	
	def read(self) -> tuple:
		self.__update_data()

		return (self.__bx, self.__by, self.__bz)

	def readRadial(self) -> float:
		self.__update_data()
		
		return math.sqrt(self.__bx*self.__bx+self.__by*self.__by+self.__bz*self.__bz)
	
	def readPolar(self) -> float:
		self.__update_data()
		
		return math.cos(math.atan2(self.__bz,math.sqrt(self.__bx*self.__bx+self.__by*self.__by)))
	
	def readAzimuth(self) -> float:
		self.__update_data()
		
		return math.atan2(self.__by,self.__bx)
  