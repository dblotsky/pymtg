usage help:
	@echo ""
	@echo "Usage:"
	@echo ""
	@echo "    make install   - adds the program to the system path (requires root privileges)"
	@echo "    make uninstall - undoes the actions of 'make install'"
	@echo "    make reinstall - uninstalls and then reinstalls"
	@echo ""
	@echo "    make databank  - downloads the Magic: The Gathering card database found on http://mtgjson.com/"
	@echo ""
	@echo "    make clean     - clean up some generated files"
	@echo ""

databank: pymtg/data/AllSets.json pymtg/data/AllSets-x.json

PRIVILEGED:
	@echo "requiring root privileges ..."
	@sudo -v

pymtg/data/AllSets.json pymtg/data/AllSets-x.json:
	sudo ls > /dev/null
	curl http://dmitryblotsky.com/mtgdata/AllSets.json -f -o $@
	./bin/format_json.py $@

install: PRIVILEGED databank
	sudo python setup.py install

uninstall: PRIVILEGED
	yes | sudo pip uninstall pymtg

reinstall: uninstall install

clean:
	$(RM) *.pyc

.PHONY: clean uninstall reinstall install download PRIVILEGED
