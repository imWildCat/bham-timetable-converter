default:
	docker-compose up

rebuild:
	docker-compose stop && docker-compose rm -f && docker-compose build

clean:
	docker-compose stop && docker-compose rm -f

start:
	docker-compose up -d

upgrade:
	make rebuild && make start