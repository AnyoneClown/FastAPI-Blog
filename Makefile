## help: Show this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

## clean: Run ruff linter
.PHONY: clean
clean:
	ruff check --fix backend/
	ruff format backend/
