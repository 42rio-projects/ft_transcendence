COMPOSE = cd src && docker-compose -f docker-compose.yml

VOLUMES = ../postgres_data

all: up

up: volumes
	$(COMPOSE) up -d --build

start:
	$(COMPOSE) start

down:
	$(COMPOSE) down

stop:
	$(COMPOSE) stop

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f

volumes:
	mkdir -p $(VOLUMES)

clean: down
	docker rm -f $$(docker ps -aq) & docker rmi -f $$(docker images -q)

.PHONY: all up start down stop restart logs volumes clean
