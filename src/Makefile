.PHONY: prod
prod: up-prod

.PHONY: dev
dev:
	docker compose -f ./compose.dev.yml down; \
	docker compose -f ./compose.dev.yml up --build -d; \
	docker compose -f ./compose.supabase.yml up --build -d; \
	docker compose -f ./supabase/docker/compose.supabase.yml up --build -d; \
	chmod +x ./start.sh; \
	./start.sh

.PHONY: off dev
dev: down-dev up-dev start

.PHONY: dev-streamlit
dev-streamlit:
	docker compose -f ./compose.dev.yml up streamlit --build

.PHONY: off
off:
	npx kill-port 5500; \
	npx kill-port 8501; \
	docker compose -f ./compose.dev.yml down; \
	docker compose -f ./compose.prod.yml down; \
	docker compose -f ./supabase/docker/compose.supabase.yml down; \
	pip freeze > requirements.txt
	docker compose -f ./compose.prod.yml down;

.PHONY: test
test: off up-dev
	python3 -m venv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt; \
	PYTHONPATH=./api/src pytest -v -s

.PHONY: up-prod
up-prod:
	docker compose -f ./compose.prod.yml up --build

.PHONY: up-dev
up-dev:
	docker compose -f ./compose.dev.yml up --build -d

.PHONY: down-dev
down-dev:
	docker compose -f ./compose.dev.yml down

.PHONY: start
start:
	chmod +x ./start.sh; \
	./start.sh
