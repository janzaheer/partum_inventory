# Inventory Management System

Inventory Management System is a web based Application developed in Python/Django. The Software is designed for small businesses to maintain their records, customer ledger, sales, and more.

Designed by [Partum Solutions](http://partumsolutions.com) (Startup in Quetta, Pakistan. Provides Services and Solutions).

## Features

- Retailers (Multi Tenancy)
- Customers and Ledgers
- Stock Management
- Low Stock Notification
- Sales & Invoicing
- Employees
- Expenses
- Suppliers
- Feedback
- Sales Reports (Daily, Weekly, Monthly)
- Stock Logs (Daily, Monthly)

## Tech Stack

- **Python**: 3.12
- **Django**: 5.1
- **Database**: SQLite (dev) / PostgreSQL (Docker)
- **Frontend**: Django Templates + jQuery

---

## Getting Started

### Option 1: Docker (Recommended)

1. Clone the repository:

```bash
git clone git@github.com:janzaheer/partum_inventory.git
cd partum_inventory
```

2. Copy the environment file:

```bash
cp .env.example .env
```

3. Build and run with Docker Compose:

```bash
docker compose up --build
```

4. In a separate terminal, run migrations and create superuser:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

5. Access the application at `http://localhost:8010`

### Option 2: Local Development

1. Clone the repository:

```bash
git clone git@github.com:janzaheer/partum_inventory.git
cd partum_inventory
```

2. Create and activate a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the application at `http://localhost:8000`

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run tests for a specific app
pytest pis_com/tests.py
pytest pis_product/tests.py
pytest pis_sales/tests.py
```

---

## Docker Configuration

| Service | Container Name | Host Port | Internal Port |
|---------|---------------|-----------|---------------|
| Web App | partum_inventory_web | 8010 | 8010 |
| PostgreSQL | partum_inventory_db | 5434 | 5432 |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | (dev key) | Django secret key |
| `DJANGO_DEBUG` | `True` | Enable debug mode |
| `DJANGO_ALLOWED_HOSTS` | `*` | Comma-separated allowed hosts |
| `DB_ENGINE` | `sqlite3` | Database engine |
| `DB_NAME` | `db.sqlite3` | Database name |
| `DB_USER` | | Database user |
| `DB_PASSWORD` | | Database password |
| `DB_HOST` | | Database host |
| `DB_PORT` | | Database port |

---

## Project Structure

```
partum_inventory/
├── partum_inventory/     # Django project settings
├── pis_com/              # Core: auth, customers, feedback
├── pis_product/          # Products & stock management
├── pis_retailer/         # Retailer/tenant management
├── pis_sales/            # Sales & invoicing
├── pis_ledger/           # Customer ledgers
├── pis_expense/          # Expense tracking
├── pis_employees/        # Employee management
├── pis_supplier/         # Supplier management
├── templates/            # HTML templates
├── app_static/           # Static assets (CSS/JS)
├── tests/                # Shared test utilities
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Need Help?

- Email: zaheerjanbadini@gmail.com
- Please use GitHub issues to report issues.

## Contribute

As an open source project with a strong focus on the user community, we welcome contributions as GitHub pull requests.
