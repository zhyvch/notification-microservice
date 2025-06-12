DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
ENV = --env-file .env
APP_CONTAINER = notification-service

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: strages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: app
app:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: new-migration
new-migration:
	${EXEC} ${APP_CONTAINER} beanie new-migration -n migration -p src/infrastructure/migrations/

.PHONY: migrate-all
migrate-all:
	${EXEC} ${APP_CONTAINER} python -m src.settings.scripts.migrations.run_migrate_all

.PHONY: downgrade-all
downgrade-all:
	${EXEC} ${APP_CONTAINER} python -m src.settings.scripts.migrations.run_downgrade_all

.PHONY: migrate-one
migrate-one:
	${EXEC} ${APP_CONTAINER} python -m src.settings.scripts.migrations.run_migrate_one

.PHONY: downgrade-one
downgrade-one:
	${EXEC} ${APP_CONTAINER} python -m src.settings.scripts.migrations.run_downgrade_one
