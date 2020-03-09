all: docs

zipfile = elite-scripts.zip

clean:
	rm -f $(zipfile)

docs:
	bash generate_docs.sh

# requires a windows box
exe:
	pip install --user --upgrade -r requirements.txt
	pip install --user --upgrade -r pyEDSM\requirements.txt
	python -OO -m PyInstaller --clean -yF edsm-getnearest.py
	python -OO -m PyInstaller --clean -yF explorationtools.py
	python -OO -m PyInstaller --clean -yF spansh.py

# probably won’t work unless you’re me :)
release: clean
	rsync -avz gezocks:/mnt/d/git/elite-scripts/dist/ build/
	cd build && zip -r ../$(zipfile) *
