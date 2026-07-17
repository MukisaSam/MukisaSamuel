"""
db/base.py
----------
The single place that "knows about" every model.

Its only job is to import Base AND every model class, so that anything
importing this file (Alembic migrations, or startup table creation) sees
the complete list of tables in one go.

If you add a new model, import it here too.
"""

from app.db.base_class import Base

# Import all the models so they get registered on Base.metadata.
from app.models.student import Student
