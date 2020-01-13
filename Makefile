all: docs

zipfile = elite-scripts.zip

clean:
	rm -f $(zipfile)

docs:
	bash generate_docs.sh

# requires a windows box
exe:
	pip install --user -r requirements.txt
	pip install --user -r pyEDSM\requirements.txt
	pyinstaller.exe -y edsm-getnearest.py
	pyinstaller.exe -y explorationtools.py

# probably won’t work unless you’re me :)
release: clean
	rsync -avz gezocks:/mnt/d/git/elite-scripts/dist/ build/
	cd build && zip -r ../$(zipfile) *
