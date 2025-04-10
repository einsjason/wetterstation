import time

class ADS1015: # https://github.com/ncdcommunity/Raspberry_Pi_ADS1115_16Bit_4Channel_ADC_Python_Library/

	# ADS1115 Register Map
	__ADS1115_REG_POINTER_CONVERT		= 0x00 # Conversion register
	__ADS1115_REG_POINTER_CONFIG		= 0x01 # Configuration register
	__ADS1115_REG_POINTER_LOWTHRESH		= 0x02 # Lo_thresh register
	__ADS1115_REG_POINTER_HITHRESH		= 0x03 # Hi_thresh register

	# ADS1115 Configuration Register
	__ADS1115_REG_CONFIG_OS_NOEFFECT	= 0x00 # No effect
	__ADS1115_REG_CONFIG_OS_SINGLE		= 0x80 # Begin a single conversion
	__ADS1115_REG_CONFIG_MUX_DIFF_0_1	= 0x00 # Differential P = AIN0, N = AIN1 (default)
	__ADS1115_REG_CONFIG_MUX_DIFF_0_3	= 0x10 # Differential P = AIN0, N = AIN3
	__ADS1115_REG_CONFIG_MUX_DIFF_1_3	= 0x20 # Differential P = AIN1, N = AIN3
	__ADS1115_REG_CONFIG_MUX_DIFF_2_3	= 0x30 # Differential P = AIN2, N = AIN3
	__ADS1115_REG_CONFIG_MUX_SINGLE_0	= 0x40 # Single-ended P = AIN0, N = GND
	__ADS1115_REG_CONFIG_MUX_SINGLE_1	= 0x50 # Single-ended P = AIN1, N = GND
	__ADS1115_REG_CONFIG_MUX_SINGLE_2	= 0x60 # Single-ended P = AIN2, N = GND
	__ADS1115_REG_CONFIG_MUX_SINGLE_3	= 0x70 # Single-ended P = AIN3, N = GND
	__ADS1115_REG_CONFIG_PGA_6_144V		= 0x00 # +/-6.144V range = Gain 2/3
	__ADS1115_REG_CONFIG_PGA_4_096V		= 0x02 # +/-4.096V range = Gain 1
	__ADS1115_REG_CONFIG_PGA_2_048V		= 0x04 # +/-2.048V range = Gain 2 (default)
	__ADS1115_REG_CONFIG_PGA_1_024V		= 0x06 # +/-1.024V range = Gain 4
	__ADS1115_REG_CONFIG_PGA_0_512V		= 0x08 # +/-0.512V range = Gain 8
	__ADS1115_REG_CONFIG_PGA_0_256V		= 0x0A # +/-0.256V range = Gain 16
	__ADS1115_REG_CONFIG_MODE_CONTIN	= 0x00 # Continuous conversion mode
	__ADS1115_REG_CONFIG_MODE_SINGLE	= 0x01 # Power-down single-shot mode (default)
	__ADS1115_REG_CONFIG_DR_8SPS		= 0x00 # 8 samples per second
	__ADS1115_REG_CONFIG_DR_16SPS		= 0x20 # 16 samples per second
	__ADS1115_REG_CONFIG_DR_32SPS		= 0x40 # 32 samples per second
	__ADS1115_REG_CONFIG_DR_64SPS		= 0x60 # 64 samples per second
	__ADS1115_REG_CONFIG_DR_128SPS		= 0x80 # 128 samples per second (default)
	__ADS1115_REG_CONFIG_DR_250SPS		= 0xA0 # 250 samples per second
	__ADS1115_REG_CONFIG_DR_475SPS		= 0xC0 # 475 samples per second
	__ADS1115_REG_CONFIG_DR_860SPS		= 0xE0 # 860 samples per second
	__ADS1115_REG_CONFIG_CMODE_TRAD		= 0x00 # Traditional comparator with hysteresis (default)
	__ADS1115_REG_CONFIG_CMODE_WINDOW	= 0x10 # Window comparator
	__ADS1115_REG_CONFIG_CPOL_ACTVLOW	= 0x00 # ALERT/RDY pin is low when active (default)
	__ADS1115_REG_CONFIG_CPOL_ACTVHI	= 0x08 # ALERT/RDY pin is high when active
	__ADS1115_REG_CONFIG_CLAT_NONLAT	= 0x00 # Non-latching comparator (default)
	__ADS1115_REG_CONFIG_CLAT_LATCH		= 0x04 # Latching comparator
	__ADS1115_REG_CONFIG_CQUE_1CONV		= 0x00 # Assert ALERT/RDY after one conversions
	__ADS1115_REG_CONFIG_CQUE_2CONV		= 0x01 # Assert ALERT/RDY after two conversions
	__ADS1115_REG_CONFIG_CQUE_4CONV		= 0x02 # Assert ALERT/RDY after four conversions
	__ADS1115_REG_CONFIG_CQUE_NONE		= 0x03 # Disable the comparator and put ALERT/RDY in high state (default)

	def __init__(self, bus, address:int=0x48):
		self.__bus = bus
		self.__address = address

	def __config_single_ended(self, channel:int=0):
		"""Select the Configuration Register data from the given provided value above"""
		if channel == 0:
			CONFIG_REG = [self.__ADS1115_REG_CONFIG_OS_SINGLE | self.__ADS1115_REG_CONFIG_MUX_SINGLE_0 | self.__ADS1115_REG_CONFIG_PGA_4_096V | self.__ADS1115_REG_CONFIG_MODE_CONTIN, self.__ADS1115_REG_CONFIG_DR_128SPS | self.__ADS1115_REG_CONFIG_CQUE_NONE]
		elif channel == 1:
			CONFIG_REG = [self.__ADS1115_REG_CONFIG_OS_SINGLE | self.__ADS1115_REG_CONFIG_MUX_SINGLE_1 | self.__ADS1115_REG_CONFIG_PGA_4_096V | self.__ADS1115_REG_CONFIG_MODE_CONTIN, self.__ADS1115_REG_CONFIG_DR_128SPS | self.__ADS1115_REG_CONFIG_CQUE_NONE]
		elif channel == 2:
			CONFIG_REG = [self.__ADS1115_REG_CONFIG_OS_SINGLE | self.__ADS1115_REG_CONFIG_MUX_SINGLE_2 | self.__ADS1115_REG_CONFIG_PGA_4_096V | self.__ADS1115_REG_CONFIG_MODE_CONTIN, self.__ADS1115_REG_CONFIG_DR_128SPS | self.__ADS1115_REG_CONFIG_CQUE_NONE]
		elif channel == 3:
			CONFIG_REG = [self.__ADS1115_REG_CONFIG_OS_SINGLE | self.__ADS1115_REG_CONFIG_MUX_SINGLE_3 | self.__ADS1115_REG_CONFIG_PGA_4_096V | self.__ADS1115_REG_CONFIG_MODE_CONTIN, self.__ADS1115_REG_CONFIG_DR_128SPS | self.__ADS1115_REG_CONFIG_CQUE_NONE]
		
		self.__bus.write_i2c_block_data(self.__address, self.__ADS1115_REG_POINTER_CONFIG, CONFIG_REG)
	
	def __config_differential(self, channel:int=0):
		"""Select the Configuration Register data from the given provided value above"""
		if channel == 0:
			CONFIG_REG = [self.__ADS1115_REG_CONFIG_OS_SINGLE | self.__ADS1115_REG_CONFIG_MUX_DIFF_0_1 | self.__ADS1115_REG_CONFIG_PGA_4_096V | self.__ADS1115_REG_CONFIG_MODE_CONTIN, self.__ADS1115_REG_CONFIG_DR_128SPS | self.__ADS1115_REG_CONFIG_CQUE_NONE]
		elif channel == 1:
			CONFIG_REG = [self.__ADS1115_REG_CONFIG_OS_SINGLE | self.__ADS1115_REG_CONFIG_MUX_DIFF_0_3 | self.__ADS1115_REG_CONFIG_PGA_4_096V | self.__ADS1115_REG_CONFIG_MODE_CONTIN, self.__ADS1115_REG_CONFIG_DR_128SPS | self.__ADS1115_REG_CONFIG_CQUE_NONE]
		elif channel == 2:
			CONFIG_REG = [self.__ADS1115_REG_CONFIG_OS_SINGLE | self.__ADS1115_REG_CONFIG_MUX_DIFF_1_3 | self.__ADS1115_REG_CONFIG_PGA_4_096V | self.__ADS1115_REG_CONFIG_MODE_CONTIN, self.__ADS1115_REG_CONFIG_DR_128SPS | self.__ADS1115_REG_CONFIG_CQUE_NONE]
		elif channel == 3:
			CONFIG_REG = [self.__ADS1115_REG_CONFIG_OS_SINGLE | self.__ADS1115_REG_CONFIG_MUX_DIFF_2_3 | self.__ADS1115_REG_CONFIG_PGA_4_096V | self.__ADS1115_REG_CONFIG_MODE_CONTIN, self.__ADS1115_REG_CONFIG_DR_128SPS | self.__ADS1115_REG_CONFIG_CQUE_NONE]
		
		self.__bus.write_i2c_block_data(self.__address, self.__ADS1115_REG_POINTER_CONFIG, CONFIG_REG)
	
	def read(self, channel:int=0) -> int:
		self.__config_single_ended(channel)

		time.sleep(0.1)

		data = self.__bus.read_i2c_block_data(self.__address, self.__ADS1115_REG_POINTER_CONVERT, 2)
		
		# Convert the data
		raw_adc = data[0] * 256 + data[1]
		
		if raw_adc > 32767:
			raw_adc -= 65535
		
		return raw_adc >> 4 # >> 4 for ADS1015
	
	def readAll(self) -> tuple:
		return (self.read(0), self.read(1), self.read(2), self.read(3))
