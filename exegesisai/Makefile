.PHONY: dev lint fmt test migrate seed

dev:
	uvicorn backend.app.main:app --reload --port 8000

lint:
	python -m pip install --quiet ruff || true
	ruff check backend

fmt:
	python -m pip install --quiet black isort || true
	black backend && isort backend

test:
	pytest -q

migrate:
	alembic upgrade head

seed:
	python -m backend.app.scripts.seed_minimal
*** End Patch

