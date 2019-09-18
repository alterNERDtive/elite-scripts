all: exe

# requires a windows box
exe:
	pyinstaller.exe -y edsm-getnearest.py
