.DEFAULT_GOAL := help

run: ## запускаем наш сервер командой make run
	poetry run uvicorn main:app --reload --env-file .local.env
	## poetry run fastapi dev main.py --reload тут --env-file не работает

install: ## устанавливаем зависимости используя poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## удаляем зависимости используя poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove (LIBRARY)

update: ## обновление пакета используя poetry
	@echo "Update dependency $(LIBRARY)"
	poetry update (LIBRARY)

migrate-create:
	 alembic revision --autogenerate -m $(MESSAGE)

migrate-apply:
	alembic upgrade head

