import time

class TSL2591(object): # https://github.com/maxlklaxl/python-tsl2591/

	__VISIBLE					= 2  # channel 0 - channel 1
	__INFRARED					= 1  # channel 1
	__FULLSPECTRUM				= 0  # channel 0

	__ADDR						= 0x29
	__READBIT					= 0x01
	__COMMAND_BIT				= 0xA0  # bits 7 and 5 for 'command normal'
	__CLEAR_BIT					= 0x40  # Clears any pending interrupt (write 1 to clear)
	__WORD_BIT					= 0x20  # 1 = read/write word (rather than byte)
	__BLOCK_BIT					= 0x10  # 1 = using block read/write
	__ENABLE_POWERON			= 0x01
	__ENABLE_POWEROFF			= 0x00
	__ENABLE_AEN				= 0x02
	__ENABLE_AIEN				= 0x10
	__CONTROL_RESET				= 0x80
	__LUX_DF					= 408.0
	__LUX_COEFB					= 1.64  # CH0 coefficient
	__LUX_COEFC					= 0.59  # CH1 coefficient A
	__LUX_COEFD					= 0.86  # CH2 coefficient B

	__REGISTER_ENABLE			= 0x00
	__REGISTER_CONTROL			= 0x01
	__REGISTER_THRESHHOLDL_LOW	= 0x02
	__REGISTER_THRESHHOLDL_HIGH	= 0x03
	__REGISTER_THRESHHOLDH_LOW	= 0x04
	__REGISTER_THRESHHOLDH_HIGH	= 0x05
	__REGISTER_INTERRUPT		= 0x06
	__REGISTER_CRC				= 0x08
	__REGISTER_ID				= 0x0A
	__REGISTER_CHAN0_LOW		= 0x14
	__REGISTER_CHAN0_HIGH		= 0x15
	__REGISTER_CHAN1_LOW		= 0x16
	__REGISTER_CHAN1_HIGH		= 0x17
	__INTEGRATIONTIME_100MS		= 0x00
	__INTEGRATIONTIME_200MS		= 0x01
	__INTEGRATIONTIME_300MS		= 0x02
	__INTEGRATIONTIME_400MS		= 0x03
	__INTEGRATIONTIME_500MS		= 0x04
	__INTEGRATIONTIME_600MS		= 0x05

	__GAIN_LOW					= 0x00  # low gain (1x)
	__GAIN_MED					= 0x10  # medium gain (25x)
	__GAIN_HIGH					= 0x20  # medium gain (428x)
	__GAIN_MAX					= 0x30  # max gain (9876x)

	def __init__(self, bus, address=0x29, integration=__INTEGRATIONTIME_100MS, gain=__GAIN_LOW):
		self.__bus = bus
		self.__address = address
		self.integration_time = integration
		self.gain = gain
		self.__set_timing(self.integration_time)
		self.__set_gain(self.gain)
		self.__disable() # to be sure

	def __set_timing(self, integration):
		self.__enable()
		self.integration_time = integration
		self.__bus.write_byte_data(self.__address, self.__COMMAND_BIT | self.__REGISTER_CONTROL, self.integration_time | self.gain)
		self.__disable()

	def __get_timing(self):
		return self.integration_time

	def __set_gain(self, gain):
		self.__enable()
		self.gain = gain
		self.__bus.write_byte_data(self.__address, self.__COMMAND_BIT | self.__REGISTER_CONTROL, self.integration_time | self.gain)
		self.__disable()

	def __get_gain(self):
		return self.gain

	def read(self) -> int:
		full, ir = self.readRaw()
		# Check for overflow conditions first
		if (full == 0xFFFF) | (ir == 0xFFFF):
			return 0
			
		case_integ = {
			self.__INTEGRATIONTIME_100MS: 100.,
			self.__INTEGRATIONTIME_200MS: 200.,
			self.__INTEGRATIONTIME_300MS: 300.,
			self.__INTEGRATIONTIME_400MS: 400.,
			self.__INTEGRATIONTIME_500MS: 500.,
			self.__INTEGRATIONTIME_600MS: 600.,
		}

		if self.integration_time in case_integ.keys():
			atime = case_integ[self.integration_time]
		else:
			atime = 100.

		case_gain = {
			self.__GAIN_LOW: 1.,
			self.__GAIN_MED: 25.,
			self.__GAIN_HIGH: 428.,
			self.__GAIN_MAX: 9876.,
		}

		if self.gain in case_gain.keys():
			again = case_gain[self.gain]
		else:
			again = 1.

		# cpl = (ATIME * AGAIN) / DF
		cpl = (atime * again) / self.__LUX_DF
		lux1 = (full - (self.__LUX_COEFB * ir)) / cpl

		lux2 = ((self.__LUX_COEFC * full) - (self.__LUX_COEFD * ir)) / cpl

		# The highest value is the approximate lux equivalent
		return max([lux1, lux2])

	def __enable(self):
		self.__bus.write_byte_data(self.__address, self.__COMMAND_BIT | self.__REGISTER_ENABLE, self.__ENABLE_POWERON | self.__ENABLE_AEN | self.__ENABLE_AIEN) # Enable

	def __disable(self):
		self.__bus.write_byte_data(self.__address, self.__COMMAND_BIT | self.__REGISTER_ENABLE, self.__ENABLE_POWEROFF)

	def readRaw(self) -> tuple:
		self.__enable()
		time.sleep(0.120*self.integration_time+1) # not sure if we need it "// Wait x ms for ADC to complete"
		full = self.__bus.read_word_data(self.__address, self.__COMMAND_BIT | self.__REGISTER_CHAN0_LOW)
		ir = self.__bus.read_word_data(self.__address, self.__COMMAND_BIT | self.__REGISTER_CHAN1_LOW)
		self.__disable()
		return (full, ir)

	def get_luminosity(self, channel) -> tuple:
		full, ir = self.read()
		if channel == self.__FULLSPECTRUM:
			# Reads two byte value from channel 0 (visible + infrared)
			return full
		elif channel == self.__INFRARED:
			# Reads two byte value from channel 1 (infrared)
			return ir
		elif channel == self.__VISIBLE:
			# Reads all and subtracts out ir to give just the visible!
			return full - ir
		else: # unknown channel!
			return 0