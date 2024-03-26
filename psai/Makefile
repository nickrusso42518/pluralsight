# Version: GNU Make 3.81
# Author:  Nick Russo (njrusmc@gmail.com)

.DEFAULT_GOAL := test
.PHONY: test
test:	lint gai gft bf txt

.PHONY: cont
cont:
	@echo "Starting  batfish container"
	sudo docker container prune --force
	sudo docker container run --name batfish \
		--volume batfish-data:/data \
		--publish 8888:8888 --publish 9997:9997 --publish 9996:9996 \
		--detach batfish/allinone:2023.12.16.1270
	# nc -v -n -w 1 127.0.0.1 8888
	# nc -v -n -w 1 127.0.0.1 9997
	# nc -v -n -w 1 127.0.0.1 9996
	nmap localhost -p T:8888,9996,9997 | grep closed ; test $$? -eq 1
	@echo "Completed batfish container"

.PHONY: lint
lint:
	@echo "Starting  lint"
	# find . -name "*.py" -not -path "./.old/*" | xargs black -l 82 --check
	find . -name "*.py" -not -path "./.old/*" | xargs black -l 82
	find . -name "*.py" -not -path "./.old/*" | xargs pylint
	@echo "Completed lint"

.PHONY: gfd
gfd:
	@echo "Starting  GAI foundation conversion"
	python gai/foundation_convert.py \
		--src_os cisco_iosxe --dst_os juniper_junos \
		--src_cfg bf/snapshots/pre/configs/R01.txt --num_choices 2
	head gai/choices/foundation/*.txt
	@echo "Completed GAI foundation conversion"

.PHONY: gft
gft:
	@echo "Starting  GAI fine-tune conversion"
	python gai/finetune_convert.py \
		--src_os cisco_iosxe --dst_os juniper_junos \
		--src_cfg bf/snapshots/pre/configs/R01.txt --num_choices 2 \
		--model ft:gpt-3.5-turbo-0613:personal::8nu4Ddmi
	head gai/choices/finetune/*.txt
	@echo "Completed GAI fine-tune conversion"


.PHONY: mke
mke:
	@echo "Starting  make embeddings"
	python gai/make_embed_cmd_map.py \
		--src_os cisco_iosxe --dst_os juniper_junos \
		--model text-embedding-3-large
	python gai/make_embed_cmd_map.py \
		--src_os juniper_junos --dst_os cisco_iosxe \
		--model text-embedding-3-large
	jq '.["area <address> stub"]' \
		gai/inputs/cisco_iosxe_2_juniper_junos.json
	jq '.["set area <area_id> stub"]' \
		gai/inputs/juniper_junos_2_cisco_iosxe.json
	@echo "Completed make embeddings"

.PHONY: gem
gem:
	@echo "Starting  GAI embedding conversion"
	python gai/embedding_convert.py \
		--src_os cisco_iosxe --dst_os juniper_junos \
		--src_cfg bf/snapshots/pre/configs/R01.txt --num_choices 2
	head gai/choices/embedding/*.txt
	@echo "Completed GAI embedding conversion"

.PHONY: bf
bf:
	@echo "Starting  batfish pytest"
	# pytest --verbose bf/ospf_pytest.py --snapshot_name pre
	pytest --verbose bf/ospf_pytest.py --snapshot_name post
	@echo "Completed batfish pytest"

.PHONY: gns3
gns3:
	@echo "Starting  gns3 deployment"
	# python gns3/deploy_topology.py http://192.168.120.128:80/v2 pre
	python gns3/deploy_topology.py http://192.168.120.128:80/v2 post
	@echo "Completed gns3 deployment"

.PHONY: txt
txt:
	@echo "Starting  textfsm parsing"
	python gns3/textfsm/parse_all.py
	./gns3/textfsm/tabulate.sh
	@echo "Completed textfsm parsing"

.PHONY: aio
aio:
	@echo "Starting  asyncio/scrapli tests"
	# python gns3/ospf_asyncio.py pre
	python gns3/ospf_asyncio.py post
	@echo "Completed asyncio/scrapli tests"

.PHONY: clean
clean:
	@echo "Starting  clean"
	sudo docker container ls --all --quiet | sudo xargs docker stop | sudo xargs docker rm
	sudo service docker restart
	find . -name "*.pyc" | xargs -r rm
	@echo "Completed clean"
