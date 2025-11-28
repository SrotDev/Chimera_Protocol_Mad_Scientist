.PHONY: help setup install migrate run test clean

help:
	@echo "Chimera Protocol - Backend Commands"
	@echo ""
	@echo "  make setup      - Initial project setup"
	@echo "  make install    - Install dependencies"
	@echo "  make migrate    - Run database migrations"
	@echo "  make run        - Start development server"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean temporary files"
	@echo "  make superuser  - Create Django superuser"
	@echo ""

setup:
	@echo "🧪 Setting up Chimera Protocol..."
	python -m venv .venv
	@echo "✅ Virtual environment created"
	@echo "Run: source .venv/bin/activate (or .venv\\Scripts\\activate on Windows)"

install:
	@echo "📥 Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

migrate:
	@echo "🗄️  Running migrations..."
	python manage.py makemigrations
	python manage.py migrate
	@echo "✅ Migrations complete"

run:
	@echo "🚀 Starting development server..."
	python manage.py runserver

test:
	@echo "🧪 Running tests..."
	python manage.py test

clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	@echo "✅ Cleanup complete"

superuser:
	@echo "👤 Creating superuser..."
	python manage.py createsuperuser

shell:
	@echo "🐚 Opening Django shell..."
	python manage.py shell
