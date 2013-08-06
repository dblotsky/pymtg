usage help:
	@echo ""
	@echo "Usage:"
	@echo ""
	@echo "    make install   - adds the program to the system path (requires root privileges)"
	@echo "    make uninstall - undoes the actions of 'make install'"
	@echo "    make reinstall - uninstalls and then reinstalls"
	@echo ""
	@echo "    make download  - downloads the Magic: The Gathering card database found on http://mtgjson.com/"
	@echo ""
	@echo "    make clean     - clean up some generated files"
	@echo ""

download: data/AllSets.json data/AllSets-x.json

data/AllSets.json data/AllSets-x.json:
	curl http://dmitryblotsky.com/mtgdata/AllSets.json -f -o $@
	./format_json.py $@

install: download default-collection
	sudo ln -f -s $(PWD)/mtg.py /usr/bin/mtg

uninstall:
	sudo $(RM) /usr/bin/mtg

reinstall: uninstall install

default-collection: data/collections/sample.mtgcollection
	ln -s -f `pwd`/data/collections/sample.mtgcollection data/collections/default.mtgcollection

clean:
	$(RM) *.pyc

.PHONY: clean uninstall reinstall install download
