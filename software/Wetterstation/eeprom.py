import struct
from i2c.lib_24c32 import CAT24C32

class EEPROM:

	class __TYPE:
		INT = 0x01
		FLOAT = 0x02
		UINT = 0x03
		BOOL = 0x04
	
	def __init__(self, bus, address:int=0x50, physical_length:int=4096):
		self.__eeprom = CAT24C32(bus, address)
		self.__length = physical_length # Größe des EEPROM'S
		self.__bytes_per_value = 5 # Bytes, die für die Speicherung einer Variable (Datentyp + Wert) benötigt werden (1 Byte Datentyp + 4 Bytes Wert)
	
	@property
	def length(self) -> int:
		return self.__length // self.__bytes_per_value
	
	@property
	def bytes_per_value(self) -> int:
		return self.__bytes_per_value
	
	def isAddressValid(self, address:int) -> bool:
		return address < self.__length // self.__bytes_per_value
	
	def get(self, address:int, raw:bool=False) -> any:
		if(self.isAddressValid(address)):
			address *= self.__bytes_per_value

			data = []
			addr = 0
			while(len(data) < self.__bytes_per_value):
				data.append(self.__eeprom.read(address + addr)[0])
				addr += 1

			if(raw):
				return data
			else:
				return self.__convertFromBytes(data)
		else:
			raise ValueError("invalid address")

	def put(self, address:int, value:any, raw:bool=False):
		if(self.isAddressValid(address)):
			address *= self.__bytes_per_value

			if(not raw):
				data = self.__convertToBytes(value)
			else:
				data = value

			addr = 0
			while(len(data) > 0):
				self.__eeprom.write(address + addr, [data[0]])
				data.pop(0)
				addr += 1
		else:
			raise ValueError("invalid address")

	def update(self, address:int, value:any) -> any:
		stored_data = self.get(address, True)
		data = self.__convertToBytes(value)

		if(stored_data != data):
			self.put(address, data, True)
			return self.__convertFromBytes(stored_data)
		else:
			return False
		
	def clear(self, address:int):
		self.update(address, None)
		
	def __convertToBytes(self, value:any) -> list:
		if(isinstance(value, bool)):
			return [self.__TYPE.BOOL] + self.boolToBytes(value)
		elif(isinstance(value, int)):
			if(value < 0):
				return [self.__TYPE.INT] + self.intToBytes(value, True)
			else:
				return [self.__TYPE.UINT] + self.intToBytes(value, False)
		elif(isinstance(value, float)):
			return [self.__TYPE.FLOAT] + self.floatToBytes(value)
		elif(value == None):
			return [0x00]*5
		else:
			raise TypeError("invalid data type " + str(type(value)))
		
	def __convertFromBytes(self, data:list) -> any:
		data_type = data[0]
		data.pop(0)

		if(data_type == self.__TYPE.INT):
			return self.bytesToInt(data, True)
		elif(data_type == self.__TYPE.UINT):
			return self.bytesToInt(data, False)
		elif(data_type == self.__TYPE.FLOAT):
			return self.bytesToFloat(data)
		elif(data_type == self.__TYPE.BOOL):
			return self.bytesToBool(data)
		else:
			return None
		
	@staticmethod
	def intToBytes(val:int, signed:bool=True) -> list:
		return list(val.to_bytes(4, 'big', signed=signed))

	@staticmethod
	def bytesToInt(val:list, signed:bool=True) -> int:
		return int.from_bytes(bytes(val), 'big', signed=signed)

	@staticmethod
	def floatToBytes(val:float) -> list:
		return list(struct.pack('!f', val))

	@staticmethod
	def bytesToFloat(val:list) -> float:
		return struct.unpack('!f', bytes(val))[0]

	@staticmethod
	def boolToBytes(val:bool) -> list:
		return [0xff if val else 0x00]*4

	@staticmethod
	def bytesToBool(val:list) -> bool:
		return val == [0xff]*4