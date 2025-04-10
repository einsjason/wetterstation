import smbus2
import time

class CAT24C32: # https://github.com/bluerobotics/cat24c32-python
	def __init__(self, bus, address:int=0x50):
		self.__bus = bus
		self.__address = address

	def write(self, register_address:int, data:list):
		data = list(register_address.to_bytes(2, "big")) + data
		msg = smbus2.i2c_msg.write(self.__address, data)

		try:
			self.__bus.i2c_rdwr(msg)
			return
		except OSError as e:
			if e.errno == 121: # if e.errno is 121: # Remote I/O error aka slave NAK
				pass

		time.sleep(0.005)
		self.__bus.i2c_rdwr(msg)

	def read(self, register_address:int, length:int=1) -> list:
		self.write(register_address, [])
		msg = smbus2.i2c_msg.read(self.__address, length)
		self.__bus.i2c_rdwr(msg)
		data = list(msg)
		return data
