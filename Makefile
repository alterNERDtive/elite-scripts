all: docs

docs:
	bash generate_docs.sh

# requires a windows box
exe:
	pyinstaller.exe -y edsm-getnearest.py
	pyinstaller.exe -y explorationtools.py
