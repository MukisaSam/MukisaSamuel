# Student Information — a FastAPI Demo

A small FastAPI project built to **introduce FastAPI**, using the same
**professional folder structure** a real production project would use.

A student has three fields: **name, email, reg number**. The app gives you:
- a single web page listing all students, and
- a full JSON API (create / read / update / delete) with **automatic,
  interactive documentation**.

---

## What is FastAPI?

FastAPI is a modern Python framework for building **web APIs** (and small
web pages). Its selling points:

- **Fast to write** — you describe your data once with Python type hints.
- **Automatic validation** — bad input is rejected for you.
- **Free interactive docs** — a `/docs` page is generated automatically.
- **Fast to run** — one of the quickest Python frameworks available.

---

## Folder & file structure — what each part is for

```
FastApi/
├── app/                          ← all application code
│   ├── __init__.py               → marks "app" as a Python package
│   ├── main.py                   → ENTRY POINT: builds the app, wires it together
│   │
│   ├── core/                     → app-wide configuration
│   │   ├── config.py             → settings (DB url, project name) from .env
│   │   └── __init__.py
│   │
│   ├── db/                       → database plumbing
│   │   ├── base_class.py         → Base class every model inherits from
│   │   ├── session.py            → the engine + SessionLocal (DB connection)
│   │   └── base.py               → imports all models in one place
│   │
│   ├── models/                   → SQLAlchemy models = database TABLES
│   │   └── student.py            → the "students" table
│   │
│   ├── schemas/                  → Pydantic schemas = request/response SHAPES
│   │   └── student.py            → StudentCreate / StudentUpdate / StudentRead
│   │
│   ├── crud/                     → database QUERIES (Create/Read/Update/Delete)
│   │   └── student.py
│   │
│   ├── services/                 → business logic that isn't a plain DB call
│   │   └── reporting.py          → builds a small summary of students
│   │
│   └── api/                      → the HTTP layer (the URLs)
│       ├── deps.py               → shared dependencies (get_db)
│       └── v1/                   → version 1 of the API
│           ├── router.py         → combines all endpoint files into one router
│           └── endpoints/
│               ├── students.py   → /students endpoints (the CRUD)
│               └── reports.py    → /reports endpoint (uses the service)
│
├── templates/
│   └── index.html                → the ONE web page (Jinja2)
├── static/
│   └── style.css                 → page styling
│
├── alembic/                      → database migrations (how the tables are
│   ├── env.py                      actually created & evolved over time)
│   └── versions/                 → the numbered migration files
├── alembic.ini
│
├── scripts/                      → helper scripts you run BY HAND
│   └── seed_data.py              → inserts the demo students
│
├── tests/                        → automated tests
│   ├── conftest.py               → test fixtures (throwaway test DB + client)
│   └── test_students.py
│
├── .env.example                  → template for environment variables
├── .gitignore
├── requirements.txt              → the libraries to install
└── README.md                     → this file
```

### The one big idea: separation of concerns

Each folder has **one job**. A request flows through them like a
production line:

```
HTTP request
   → api/ (endpoint)      "what URL was called?"
   → schemas/ (validate)  "is the incoming data valid?"
   → crud/ (database)     "read/write the students table"
   → models/ (tables)     "how a student is stored"
   → schemas/ (serialize) "shape the response"
HTTP response
```

For an app this small you *could* put everything in one file. We split it
so students see how **real** projects stay organised — and so each concept
(config, database, validation, queries, routes) can be pointed at
individually during the demo.

---

## How to run it

Open a terminal **in this folder** and run:

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 2. Install the libraries
pip install -r requirements.txt

# 3. Create the database tables (Alembic runs the migrations)
alembic upgrade head

# 4. Add the demo students (a script you run by hand)
python -m scripts.seed_data

# 5. Start the server
uvicorn app.main:app --reload
```

`uvicorn app.main:app --reload` means:
- `app.main` → the file `app/main.py`
- `:app`     → the `app = FastAPI()` variable inside it
- `--reload` → auto-restart when you save a file (handy during a demo)

Steps 3 and 4 are only needed **once** (or again after you reset the
database). The app itself no longer touches the schema — creating tables is
Alembic's job, and loading demo data is the seed script's job.

---

## What to open in the browser (great for your demo!)

| URL                                        | What it shows                              |
| ------------------------------------------ | ------------------------------------------ |
| http://127.0.0.1:8000/                     | The student information **web page**       |
| http://127.0.0.1:8000/api/v1/students/     | The raw **JSON** list of students (the API)|
| http://127.0.0.1:8000/api/v1/students/1    | A single student by id                     |
| http://127.0.0.1:8000/api/v1/reports/summary | A summary produced by the services layer |
| http://127.0.0.1:8000/docs                 | **Interactive API docs** (Swagger)         |
| http://127.0.0.1:8000/redoc                | Alternative auto-generated docs            |

The `/docs` page is the "wow" moment — you can create, edit, and delete a
student live from the browser (click an endpoint → **Try it out**).

---

## Running the tests

```bash
pytest
```

The tests use a separate throwaway database, so they never touch your
real data — made easy by the `get_db` dependency (see `tests/conftest.py`).

---

## About Alembic (migrations)

This project uses **Alembic** to manage the database schema — the same way
a real team would. A *migration* is a versioned, ordered script that
describes a change to the database (create a table, add a column, …), so
every database (yours, a teammate's, the live server) can be brought to the
exact same state by running the same migrations.

The workflow:

```bash
# 1. You change or add a MODEL in app/models/ ...
# 2. Ask Alembic to write a migration by comparing models vs. the database:
alembic revision --autogenerate -m "describe your change"

# 3. Apply the migration(s) to actually change the database:
alembic upgrade head

# (to undo the most recent migration)
alembic downgrade -1
```

The first migration — creating the `students` table — already lives in
[`alembic/versions/`](alembic/versions/). Alembic reads your models via
`target_metadata = Base.metadata` in [`alembic/env.py`](alembic/env.py),
which is how `--autogenerate` knows what changed.

> Tip for the demo: change `app/models/student.py` (e.g. add a
> `phone_number` column), run the two commands above, and show the class the
> new migration file Alembic generated. That's the "aha" moment for
> migrations.
