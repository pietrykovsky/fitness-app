#! /usr/bin/env sh

# Let the DB start
python wait_for_db.py

# Run migrations
alembic upgrade head

# Run uvicorn server
if [ "$DEV" = "true" ]; then
    uvicorn app.main:app --host $HOST --port 8000 --reload
else
    uvicorn app.main:app --host $HOST --port 8000
fi
