usage help:
	@echo "Usage:"
	@echo "    make install - adds the program to the system path (requires root privileges)"

install:
	sudo ln -s $(PWD)/mtg.py /usr/bin/mtg
