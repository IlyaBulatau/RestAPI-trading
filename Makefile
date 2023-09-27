up:
	docker compose up

logs: 
	docker compose logs -f $(container)

psql:
	docker compose exec -u ${user} ${container} psql
