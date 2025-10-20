.PHONY: help install-backend install-frontend install format lint type-check test clean

help:
	@echo "Available commands:"
	@echo "  make install          - Install all dependencies (backend + frontend)"
	@echo "  make install-backend  - Install backend Python dependencies"
	@echo "  make install-frontend - Install frontend npm dependencies"
	@echo "  make format           - Format all code (backend + frontend)"
	@echo "  make format-backend   - Format backend Python code"
	@echo "  make format-frontend  - Format frontend TypeScript code"
	@echo "  make lint             - Lint all code (backend + frontend)"
	@echo "  make lint-backend     - Lint backend Python code"
	@echo "  make lint-frontend    - Lint frontend TypeScript code"
	@echo "  make type-check       - Type check all code"
	@echo "  make clean            - Clean build artifacts"
	@echo "  make dev-backend      - Start backend dev server"
	@echo "  make dev-frontend     - Start frontend dev server"

install: install-backend install-frontend

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && python3.10 -m venv venv || true
	cd backend && . venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

format: format-backend format-frontend

format-backend:
	@echo "Formatting backend code..."
	cd backend && . venv/bin/activate && black src/ api_main.py

format-frontend:
	@echo "Formatting frontend code..."
	cd frontend && npm run format

lint: lint-backend lint-frontend

lint-backend:
	@echo "Linting backend code..."
	cd backend && . venv/bin/activate && ruff check src/ api_main.py

lint-backend-fix:
	@echo "Linting and fixing backend code..."
	cd backend && . venv/bin/activate && ruff check --fix src/ api_main.py

lint-frontend:
	@echo "Linting frontend code..."
	cd frontend && npm run lint

type-check: type-check-backend type-check-frontend

type-check-backend:
	@echo "Type checking backend code..."
	cd backend && . venv/bin/activate && mypy src/ api_main.py

type-check-frontend:
	@echo "Type checking frontend code..."
	cd frontend && npm run type-check

clean:
	@echo "Cleaning build artifacts..."
	rm -rf backend/__pycache__ backend/.mypy_cache backend/.pytest_cache backend/.ruff_cache
	rm -rf frontend/.next frontend/node_modules/.cache
	find backend/src -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

dev-backend:
	@echo "Starting backend server..."
	cd backend && . venv/bin/activate && python api_main.py

dev-frontend:
	@echo "Starting frontend server..."
	cd frontend && npm run dev

check-all: format lint type-check
	@echo "✅ All checks passed!"