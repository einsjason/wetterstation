import subprocess

def getTimezoneContinentCity() -> str:
	output = subprocess.getoutput('cat /etc/timezone')
	return(output)