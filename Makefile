default:
	docker-compose up

rebuild:
	docker-compose stop && docker-compose rm -f && docker-compose build

clean:
	docker-compose rm -f