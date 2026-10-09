SHELL := /bin/bash

# 1. Catch-all rule handles direct inventory names (e.g., make lab_test ...)
%:
	@set -- $(MAKECMDGOALS); \
	case "$$1" in \
		lab|prep|install|configure|graph) exit 0 ;; \
	esac; \
	INV="$$1"; \
	shift; \
	CONFIG_FILE=""; \
	ANSIBLE_ARGS=""; \
	while [ "$$#" -gt 0 ]; do \
		case "$$1" in \
			config:*) CONFIG_FILE="$${1#config:}" ;; \
			--) ;; \
			*) ANSIBLE_ARGS="$$ANSIBLE_ARGS $$1" ;; \
		esac; \
		shift; \
	done; \
	if [ -z "$$INV" ]; then \
		echo "Error: Missing inventory file."; \
		echo "Usage: make <inventory_name> [config:name] [-- ansible options]"; \
		exit 1; \
	fi; \
	EXTRA_ARG=""; \
	if [ -n "$$CONFIG_FILE" ]; then \
		EXTRA_ARG="-e mainvars=$$CONFIG_FILE.yml"; \
	fi; \
	ansible-playbook main.yml -i inventories/$$INV.yml $$EXTRA_ARG $$ANSIBLE_ARGS

.PHONY: configure
configure:
	@mkdir -p vars; \
	set -- $(MAKECMDGOALS); \
	shift; \
	NAME="$${1:-main}"; \
	nano vars/$$NAME.yml

.PHONY: install
install: 
	@ansible-playbook install-requirements.yml

.PHONY: lab
lab:
	@set -- $(MAKECMDGOALS); \
	shift; \
	INV="$$1"; \
	shift; \
	CONFIG_FILE=""; \
	ANSIBLE_ARGS=""; \
	while [ "$$#" -gt 0 ]; do \
		case "$$1" in \
			config:*) CONFIG_FILE="$${1#config:}" ;; \
			--) ;; \
			*) ANSIBLE_ARGS="$$ANSIBLE_ARGS $$1" ;; \
		esac; \
		shift; \
	done; \
	if [ -z "$$INV" ]; then \
		echo "Error: Missing inventory file."; \
		echo "Usage: make lab <inventory_name> [config:name] [-- ansible options]"; \
		exit 1; \
	fi; \
	EXTRA_ARG=""; \
	if [ -n "$$CONFIG_FILE" ]; then \
		EXTRA_ARG="-e mainvars=$$CONFIG_FILE.yml"; \
	fi; \
	ansible-playbook main.yml -i inventories/$$INV.yml $$EXTRA_ARG $$ANSIBLE_ARGS

.PHONY: prep
prep:
	@set -- $(MAKECMDGOALS); \
	shift; \
	INV="$$1"; \
	shift; \
	CONFIG_FILE=""; \
	ANSIBLE_ARGS=""; \
	while [ "$$#" -gt 0 ]; do \
		case "$$1" in \
			config:*) CONFIG_FILE="$${1#config:}" ;; \
			--) ;; \
			*) ANSIBLE_ARGS="$$ANSIBLE_ARGS $$1" ;; \
		esac; \
		shift; \
	done; \
	if [ -z "$$INV" ]; then \
		echo "Error: Missing inventory file."; \
		echo "Usage: make prep <inventory_name> [config:name] [-- ansible options]"; \
		exit 1; \
	fi; \
	EXTRA_ARG=""; \
	if [ -n "$$CONFIG_FILE" ]; then \
		EXTRA_ARG="-e mainvars=$$CONFIG_FILE.yml"; \
	fi; \
	ansible-playbook prep.yml -i inventories/$$INV.yml $$EXTRA_ARG $$ANSIBLE_ARGS


.PHONY: graph
graph:
	@set -- $(MAKECMDGOALS); \
	shift; \
	INV="$$1"; \
	shift; \
	CONFIG_FILE=""; \
	ANSIBLE_ARGS=""; \
	while [ "$$#" -gt 0 ]; do \
		case "$$1" in \
			config:*) CONFIG_FILE="$${1#config:}" ;; \
			--) ;; \
			*) ANSIBLE_ARGS="$$ANSIBLE_ARGS $$1" ;; \
		esac; \
		shift; \
	done; \
	if [ -z "$$INV" ]; then \
		echo "Error: Missing inventory file."; \
		echo "Usage: make lab <inventory_name> [config:name] [-- ansible options]"; \
		exit 1; \
	fi; \
	EXTRA_ARG=""; \
	if [ -n "$$CONFIG_FILE" ]; then \
		EXTRA_ARG="-e mainvars=$$CONFIG_FILE.yml"; \
	fi; \
	ansible-inventory --graph -i inventories/$$INV.yml $$EXTRA_ARG $$ANSIBLE_ARGS
