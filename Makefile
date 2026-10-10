SHELL := /bin/bash

# Prevent make from throwing errors on unknown targets/inventories
%::
	@:

.PHONY: configure install lab prep graph

configure:
	@mkdir -p vars; \
	NAME="$${config:-main}"; \
	nano vars/$$NAME.yml

install:
	@ansible-playbook install-requirements.yml

lab:
	@INV="$(word 2, $(MAKECMDGOALS))"; \
	[ -z "$$INV" ] && INV="$(firstword $(MAKECMDGOALS))"; \
	[ "$$INV" = "lab" ] && INV="$(word 2, $(MAKECMDGOALS))"; \
	EXTRA_ARGS=""; \
	if [ -n "$(config)" ]; then \
		EXTRA_ARGS="$$EXTRA_ARGS -e mainvars=$(config).yml"; \
	fi; \
	if [ -n "$(datastore)" ]; then \
		EXTRA_ARGS="$$EXTRA_ARGS -e lab_vm_datastore=$(datastore)"; \
	fi; \
	if [ -n "$(limit)" ]; then \
		EXTRA_ARGS="$$EXTRA_ARGS -l $(limit)"; \
	fi; \
	ansible-playbook main.yml -i inventories/$$INV.yml $$EXTRA_ARGS

prep:
	@INV="$(word 2, $(MAKECMDGOALS))"; \
	[ -z "$$INV" ] && INV="$(firstword $(MAKECMDGOALS))"; \
	[ "$$INV" = "prep" ] && INV="$(word 2, $(MAKECMDGOALS))"; \
	EXTRA_ARGS=""; \
	if [ -n "$(config)" ]; then \
		EXTRA_ARGS="$$EXTRA_ARGS -e mainvars=$(config).yml"; \
	fi; \
	if [ -n "$(datastore)" ]; then \
		EXTRA_ARGS="$$EXTRA_ARGS -e lab_vm_datastore=$(datastore)"; \
	fi; \
	if [ -n "$(limit)" ]; then \
		EXTRA_ARGS="$$EXTRA_ARGS -l $(limit)"; \
	fi; \
	ansible-playbook prep.yml -i inventories/$$INV.yml $$EXTRA_ARGS

graph:
	@INV="$(word 2, $(MAKECMDGOALS))"; \
	[ -z "$$INV" ] && INV="$(firstword $(MAKECMDGOALS))"; \
	[ "$$INV" = "graph" ] && INV="$(word 2, $(MAKECMDGOALS))"; \
	EXTRA_ARGS=""; \
	if [ -n "$(limit)" ]; then \
		EXTRA_ARGS="$$EXTRA_ARGS -l $(limit)"; \
	fi; \
	ansible-inventory --graph -i inventories/$$INV.yml $$EXTRA_ARGS