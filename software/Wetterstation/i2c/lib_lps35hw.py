class LPS35HW(): #https://github.com/OlivierdenOuden/LPS33HW

	__LPS33HW_CHECK			= 0x0F
	__LPS33HW_CTRL_REG_1	= 0x10
	__LPS33HW_P_OUT_XL		= 0x28
	__LPS33HW_P_OUT_L		= 0x29
	__LPS33HW_P_OUT_H		= 0x2A
	__LPS33HW_T_OUT_L		= 0x2B
	__LPS33HW_T_OUT_H		= 0x2C

	def __init__(self, bus, address:int=0x5d):
		self.__bus = bus
		self.__address = address
		self.__bus.write_byte_data(self.__address, self.__LPS33HW_CTRL_REG_1, 0b00011100)

	def read(self) -> tuple:
		# Read Pressure
		p = self.__bus.read_i2c_block_data(self.__address, self.__LPS33HW_P_OUT_XL, 3) # [__LPS33HW_P_OUT_XL, __LPS33HW_P_OUT_L, __LPS33HW_P_OUT_H]
		
		p_data = p[2] << 16 | p[1] << 8 | p[0]
		pressure = p_data / 4096.0

		# Read Temperature
		t = self.__bus.read_i2c_block_data(self.__address, self.__LPS33HW_T_OUT_L, 2) # [__LPS33HW_P_OUT_L, __LPS33HW_P_OUT_H]

		t_data = t[1] << 8 | t[0]
		temperature = t_data / 100.0

		return (temperature, pressure)
