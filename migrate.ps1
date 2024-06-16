flask --app migrate:application db init
flask --app migrate:application db migrate -m "Custom message."
flask --app migrate:application db upgrade