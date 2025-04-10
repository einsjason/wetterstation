from time import sleep

class MLX90614(): # https://github.com/CRImier/python-MLX90614

	__MLX90614_RAWIR1 = 0x04
	__MLX90614_RAWIR2 = 0x05
	__MLX90614_TA = 0x06
	__MLX90614_TOBJ1 = 0x07
	__MLX90614_TOBJ2 = 0x08

	__MLX90614_TOMAX = 0x20
	__MLX90614_TOMIN = 0x21
	__MLX90614_PWMCTRL = 0x22
	__MLX90614_TARANGE = 0x23
	__MLX90614_EMISS = 0x24
	__MLX90614_CONFIG = 0x25
	__MLX90614_ADDR = 0x0E
	__MLX90614_ID1 = 0x3C
	__MLX90614_ID2 = 0x3D
	__MLX90614_ID3 = 0x3E
	__MLX90614_ID4 = 0x3F

	__comm_retries = 5
	__comm_sleep_amount = 0.1

	def __init__(self, bus, address:int=0x5a):
		self.__address = address
		self.__bus = bus

	def __read_reg(self, reg_addr:int) -> int:
		err = None
		for i in range(self.__comm_retries):
			try:
				return self.__bus.read_word_data(self.__address, reg_addr)
			except IOError as e:
				err = e
				# "Rate limiting" - sleeping to prevent problems with sensor
				# when requesting data too quickly
				sleep(self.__comm_sleep_amount)
		# By this time, we made a couple requests and the sensor didn't respond
		# (judging by the fact we haven't returned from this function yet)
		# So let's just re-raise the last IOError we got
		raise err

	def __data_to_temp(self, data:int) -> float:
		temp = (data*0.02) - 273.15
		return temp
	
	def read(self) -> tuple:
		data_ta = self.__read_reg(self.__MLX90614_TA)
		data_to = self.__read_reg(self.__MLX90614_TOBJ1)
		return (self.__data_to_temp(data_ta), self.__data_to_temp(data_to))
