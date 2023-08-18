PROJECT_NAME=personal_page
PROJECT_LOCALES=pt
export COMPOSE_FILE=local.yml

.PHONY: help up build down start stop prune clear ps restore_db shell manage
default: up

## help	:	Print commands help.
help : Makefile
	@sed -n 's/^##//p' $<

## up	:	Start up containers.
up:
	@echo "Starting up containers for for $(PROJECT_NAME)..."
	# docker-compose pull
	# docker-compose build
	docker-compose up -d --remove-orphans

## build	:	Build python image.
build:
	@echo "Building python image for for $(PROJECT_NAME)..."
	docker-compose build

## down	:	Stop containers.
down: stop

## start	:	Start containers without updating.
start:
	@echo "Starting containers for $(PROJECT_NAME) from where you left off..."
	docker-compose start

## stop	:	Stop containers.
stop:
	@echo "Stopping containers for $(PROJECT_NAME)..."
	docker-compose stop

## prune	:	Remove containers and their volumes.
##		You can optionally pass an argument with the service name to prune single container
##		prune postgres	: Prune `mariadb` container and remove its volumes.
##		prune postgres redis	: Prune `postgres` and `redis` containers and remove their volumes.
prune:
	@echo "Removing containers for $(PROJECT_NAME)..."
	docker-compose down -v $(filter-out rm,$(filter-out $@,$(MAKECMDGOALS)))

## clear       :	Remove images, containers and their volumes. Also prunes docker
##		Use with caution
clear: prune
	@echo "Removing images for $(PROJECT_NAME)..."
	$(eval IMAGES=$(shell docker images -f 'reference=$(PROJECT_NAME)*' -q))
	@if [ -n "$(IMAGES)" ]; then docker rmi $(IMAGES); docker image prune -af; docker builder prune -af; fi

## ps	:	List running containers.
ps:
	docker ps --filter name='$(PROJECT_NAME)*'

## backup_db	:	Restore database backup needs a database dump
##		Example: make backup_db
##		Use with caution, not enough tests made yet
backup_db:
	docker-compose exec postgres backup

## cp_backup	:	copy database backup
##		Example: make cp_backup xxx.sql.gz
##		Use with caution, not enough tests made yet
cp_backup:
	$(eval DB_IMAGE_ID=$(shell docker ps --filter name='$(PROJECT_NAME).*postgres' --format "{{.ID}}"))
	docker cp $(DB_IMAGE_ID):/backups/$(filter-out $@,$(MAKECMDGOALS)) $(subst \,,$(MAKEFLAGS)) .

## restore_db	:	Restore database backup needs a database dump
##		Example: make restore_db xxx.sql.gz
##		Use with caution, not enough tests made yet
restore_db:
	$(eval DB_IMAGE_ID=$(shell docker ps --filter name='$(PROJECT_NAME).*postgres' --format "{{.ID}}"))
	docker cp $(filter-out $@,$(MAKECMDGOALS)) $(DB_IMAGE_ID):/backups
	docker-compose exec postgres restore $(notdir $(filter-out $@,$(MAKECMDGOALS)))

## rsync_media	:	Rsyncs media folder from server
##		Example: make rsync_media
rsync_media:
	rsync -avzrP django@ge.evolutio.pt:/home/django/django/up_events/media/ up_events/media/

## cp_db_production	 :	Get latest db production dump to backups folder
cp_db_production:
	mkdir -p backups
	rsync -azrP django@ge.evolutio.pt:/var/lib/autopostgresqlbackup/latest/up_events_* backups/


## restore_db_production  :  Restore latestes database backup from production
restore_db_production: cp_db_production
	$(MAKE) restore_db $(shell ls -t backups/*.sql.gz | head -1)

## dbshell	:	Access `postgres` dbshell
##		uses exec
##		python manage.py dbshell does not use the correct psql version
##      psql 11(FROM python:3.8) and 12(FROM postgres:12) diverge quite a bit
dbshell:
	docker-compose exec postgres bash -c "psql -U \$$POSTGRES_USER"

# ## rsync_media	:	Rsyncs media folder from server
# ##		Example: make rsync_media
# rsync_media:
# 	rsync -avzrP django@appii.pt:/home/django/django/appii/media appii/
# 	rsync -avzrP django@appii.pt:/home/django/django/locale/ locale/

# This hack allows for exec when an existing container is found, instead of run --rm
CONTAINER=django
RUN=exec
ENTRYPOINT='/entrypoint'
EXEC=$(shell docker-compose -f $(COMPOSE_FILE) $(RUN) $(CONTAINER) ls > /dev/null 2>&1; echo $$?)

ifeq ($(EXEC), 0)
	RUN=exec
	ENTRYPOINT='/entrypoint'
else
	RUN=run --rm
	ENTRYPOINT=
endif

## bash	:	Access `python` container via shell.
##		You can optionally pass an argument with a service name to open a shell on the specified container
bash:
	docker-compose $(RUN) $(CONTAINER) $(ENTRYPOINT) bash $(filter-out $@,$(MAKECMDGOALS))

## More database utilities
## Added on 20/09/2021

## sqlbash : Access `postgres` container via shell.
## alias for bash postgres
sqlbash:
	$(eval DB_IMAGE_ID=$(shell docker ps --filter name='$(PROJECT_NAME).*postgres' --format "{{.ID}}"))
	docker exec -it $(DB_IMAGE_ID) /bin/bash

## psql :   Access postgres client on the default database.
##     make psql
psql:
	$(eval DB_IMAGE_ID=$(shell docker ps --filter name='$(PROJECT_NAME).*postgres' --format "{{.ID}}"))
	$(eval POSTGRES_USER=$(shell docker exec $(DB_IMAGE_ID) env | grep POSTGRES_USER | cut -d'=' -f2))
	$(eval POSTGRES_DB=$(shell docker exec $(DB_IMAGE_ID) env | grep POSTGRES_DB | cut -d'=' -f2))
	docker exec -it $(DB_IMAGE_ID) psql -U $(POSTGRES_USER) $(POSTGRES_DB)

## createdb :   Creates db on Postgres container.
##     make createdb
##     Creates a database with the default name set on envs.
createdb:
	$(eval DB_IMAGE_ID=$(shell docker ps --filter name='$(PROJECT_NAME).*postgres' --format "{{.ID}}"))
	$(eval POSTGRES_USER=$(shell docker exec $(DB_IMAGE_ID) env | grep POSTGRES_USER | cut -d'=' -f2))
	$(eval POSTGRES_DB=$(shell docker exec $(DB_IMAGE_ID) env | grep POSTGRES_DB | cut -d'=' -f2))
	docker exec -it $(DB_IMAGE_ID) createdb -U $(POSTGRES_USER) --owner=$(POSTGRES_USER) $(POSTGRES_DB)

## dropdb :  Drop db on Postgres container.
##     make dropdb
##     Drops the database with the default name on envs.
dropdb:
	$(eval DB_IMAGE_ID=$(shell docker ps --filter name='$(PROJECT_NAME).*postgres' --format "{{.ID}}"))
	$(eval POSTGRES_USER=$(shell docker exec $(DB_IMAGE_ID) env | grep POSTGRES_USER | cut -d'=' -f2))
	$(eval POSTGRES_DB=$(shell docker exec $(DB_IMAGE_ID) env | grep POSTGRES_DB | cut -d'=' -f2))
	docker exec -it $(DB_IMAGE_ID) dropdb -U $(POSTGRES_USER) $(POSTGRES_DB)

## dropdbf : Forces Drop db even if connections are active on Postgres container.
##     make dropdbf
##     Drops the database with the default name on envs.
dropdbf:
	$(eval DB_IMAGE_ID=$(shell docker ps --filter name='$(PROJECT_NAME).*postgres' --format "{{.ID}}"))
	$(eval POSTGRES_USER=$(shell docker exec $(DB_IMAGE_ID) env | grep POSTGRES_USER | cut -d'=' -f2))
	$(eval POSTGRES_DB=$(shell docker exec $(DB_IMAGE_ID) env | grep POSTGRES_DB | cut -d'=' -f2))
	docker exec -it $(DB_IMAGE_ID) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$(POSTGRES_DB)' AND pid <> pg_backend_pid();"
	docker exec -it $(DB_IMAGE_ID) dropdb -U $(POSTGRES_USER) $(POSTGRES_DB)

# Django migrations utils
# Added on 2021, i believe

## makemigrations
##	make makemigrations
##  Makes migrations

makemigrations:
	docker-compose $(RUN) $(CONTAINER) $(ENTRYPOINT) python manage.py makemigrations

## migrate
##	make migrate
##  Makes migrations

migrate:
	docker-compose $(RUN) $(CONTAINER) $(ENTRYPOINT) python manage.py migrate

## makemigrate
##	make makemigrate
##  Makes migrations & migrates.
makemigrate:
	docker-compose $(RUN) $(CONTAINER) $(ENTRYPOINT) python manage.py makemigrations
	docker-compose $(RUN) $(CONTAINER) $(ENTRYPOINT) python manage.py migrate

# i18n/Rosetta Utils
# Added 27/07/2022

## makemessages
##	make makemessages
##  Makes messages on rosetta (LOCALE: define on the top of the file (env))
makemessages:
	docker-compose $(RUN) $(CONTAINER) $(ENTRYPOINT) python manage.py makemessages --locale=$(PROJECT_LOCALES)

## compilemessages
##	make compilemessages
##  Compiles messages on rosetta
compilemessages:
	docker-compose $(RUN) $(CONTAINER) $(ENTRYPOINT) python manage.py compilemessages

## manage	:   python manage command
##		You can optionally pass an argument to manage
##		To use "--flag" arguments include them in quotation marks.
##		For example: make manage "makemessages --locale=pt"
manage:
	docker-compose $(RUN) $(CONTAINER) $(ENTRYPOINT) python manage.py $(filter-out $@,$(MAKECMDGOALS)) $(subst \,,$(MAKEFLAGS))

# https://stackoverflow.com/a/6273809/1826109
%:
	@:
