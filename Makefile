usage help:
	@echo "Usage:"
	@echo "    make install  - adds the program to the system path (requires root privileges)"
	@echo "    make download - downloads the Magic: The Gathering card database"

download: data/AllSets.json data/AllSets-x.json

data/AllSets.json data/AllSets-x.json:
	curl http://dmitryblotsky.com/mtgdata/AllSets.json -f -o $@
	./format_json.py $@

install: download
	sudo ln -f -s $(PWD)/mtg.py /usr/bin/mtg

clean:
	$(RM) *.pyc

.PHONY: clean
