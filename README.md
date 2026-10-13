# Personal To-Do
It is a multi-user to-do app where you can sort your tasks into categories and set due dates and times.

**Live demo:** https://todo-app-theta-two-31.vercel.app/

![Screenshot of the app](docs/screenshot.png)

## Features

- Sign up and log in (each user only sees their own data)
- Create, edit and delete tasks and categories
- Due dates with time
- See how many tasks are due in each category
- Light and dark mode (todo)

## Tech stack

- Python 3.12, Flask
- SQLAlchemy / Flask-SQLAlchemy
- Flask-Login, Flask-WTF
- Bootstrap 5 (Bootstrap-Flask) and Jinja templates
- PostgreSQL (Neon) in production, SQLite locally

Requires [uv](https://docs.astral.sh/uv/).

    git clone https://github.com/Kylekibet/todo_app.git
    cd todo_app
    uv sync
    cp .env.example .env     # then edit to your own values SEE BELOW
    uv run python app.py

Open http://localhost:PORT_NUMBER

For live edits change debug=True

## Environment variables

| Name | Purpose |
|------|---------|
| `FLASK_KEY` | Secret key for sessions and forms |
| `DATABASE_URL` | Postgres connection string (optional locally, SQLite is used if unset) |

## Deployment

Deployed on Vercel with a Neon Postgres database. Set `FLASK_KEY` and
`DATABASE_URL` in the Vercel project settings.

## Roadmap

- [ ] Search and filter tasks
- [ ] Email reminders
- [ ] Light and dark mode 
- [ ] Notifications
- [ ] Move task to other category