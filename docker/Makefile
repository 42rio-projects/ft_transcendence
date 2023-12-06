COMPOSE = cd src && docker-compose -f docker-compose.yml

all: up

up:
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

clean: down
	docker rm -f $$(docker ps -aq) & docker rmi -f $$(docker images -q)

.PHONY: all up start down stop restart logs clean
