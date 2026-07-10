"""
Importing all models here means anywhere that does `from app import models`
(e.g. Alembic's env.py, or main.py) registers ALL three tables with
Base.metadata — not just whichever one happened to be imported directly.
"""
from app.models.doctor import Doctor  # noqa: F401
from app.models.patient import Patient  # noqa: F401
from app.models.staff import Staff  # noqa: F401
