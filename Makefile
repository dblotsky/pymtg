# variables
CACHED_DB = "http://dmitryblotsky.com/mtgdata/AllSets.json"

# rules
usage help:
	@echo ""
	@echo "Usage:"
	@echo ""
	@echo "    make install   - installs pymtg, invokable via 'mtg.py' (requires root privileges)"
	@echo "    make develop   - same as 'make install', but uses the existing source as the install source"
	@echo "    make uninstall - undoes the actions of 'make install'"
	@echo "    make reinstall - uninstalls and then reinstalls"
	@echo ""
	@echo "    make databank  - downloads the Magic: The Gathering card database found on http://mtgjson.com/ (cached at $(CACHED_DB))"
	@echo ""
	@echo "    make clean     - clean up some generated files"
	@echo ""

databank: pymtg/data/AllSets.json pymtg/data/AllSets-x.json

pymtg/data/AllSets.json pymtg/data/AllSets-x.json:
	curl $(CACHED_DB) -f -o $@
	./bin/format_json.py $@

install: databank
	python setup.py install

develop: databank
	python setup.py develop

uninstall:
	yes | pip uninstall pymtg

reinstall: uninstall install

clean:
	$(RM) *.pyc
	$(RM) -r build
	$(RM) -r dist
	$(RM) -r *.egg-info

.PHONY: clean uninstall develop reinstall install databank
