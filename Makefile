all: clean docs release

zipfile = elite-scripts.zip

clean:
	rm -f $(zipfile)

docs:
	bash generate_docs.sh

# requires a windows box
exe:
	pip install --user --upgrade -r requirements.txt
	pip install --user --upgrade -r pyEDSM\requirements.txt
	pip install --user --upgrade pywin32-ctypes cffi
	pip install --user --upgrade pyinstaller
	python -m PyInstaller --clean -yF edsm-getnearest.py
	python -m PyInstaller --clean -yF edts.py
	python -m PyInstaller --clean -yF explorationtools.py
	python -m PyInstaller --clean -yF spansh.py

release: clean
	pwsh -Command "Compress-Archive -Path .\dist\*.exe elite-scripts.zip"
