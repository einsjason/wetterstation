class PMSA003I(): 

	def __init__(self, bus, address:int=0x12): # ChatGPT 4
		self.__bus = bus
		self.__address = address

	def read(self) -> tuple:
		data = self.__bus.read_i2c_block_data(self.__address, 0x01, 32)

		pm1_cf = (data[4] << 8) + data[5]
		pm2_5_cf = (data[6] << 8) + data[7]
		pm10_cf = (data[8] << 8) + data[9]
		pm1_atm = (data[10] << 8) + data[11]
		pm2_5_atm = (data[12] << 8) + data[13]
		pm10_atm = (data[14] << 8) + data[15]
		particles_0_3 = (data[16] << 8) + data[17]
		particles_0_5 = (data[18] << 8) + data[19]
		particles_1 = (data[20] << 8) + data[21]
		particles_2_5 = (data[22] << 8) + data[23]
		particles_5 = (data[24] << 8) + data[25]
		particles_10 = (data[26] << 8) + data[27]
		
		return (pm1_cf, pm2_5_cf, pm10_cf, pm1_atm, pm2_5_atm, pm10_atm, particles_0_3, particles_0_5, particles_1, particles_2_5, particles_5, particles_10)