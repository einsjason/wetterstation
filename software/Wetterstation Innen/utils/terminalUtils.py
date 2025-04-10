class terminalUtils:
	reset = "\u001b[0m"
	bold = "\u001b[1m"
	underline = "\u001b[4m"
	reverse = "\u001b[7m"

	clear = "\u001b[2J"
	clearline = "\u001b[2K"

	nextline = "\u001b[1E"
	prevline = "\u001b[1F"

	top = "\u001b[0;0H"

	colors = {
		"red": "\u001b[38;2;192;0;0m",
		"green": "\u001b[38;2;83;134;44m",
		"yellow": "\u001b[38;2;255;205;47m",
		"blue": "\u001b[38;2;25;95;171m",
		"gray": "\u001b[38;2;122;155;178m",
		"gray2": "\u001b[38;2;120;120;120m"
	}

	def rgb(r:int, g:int, b:int) -> str:
		return f"\u001b[38;2;{r};{g};{b}m"
	
	def link(uri:str, label:str=None) -> str:
		if label == None: 
			label = uri
		parameters = ''

		return f'\033]8;;{uri}\033\\{label}\033]8;;\033\\'