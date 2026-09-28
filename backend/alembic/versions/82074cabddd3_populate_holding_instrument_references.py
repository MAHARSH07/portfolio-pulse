"""populate holding instrument references

Revision ID: 82074cabddd3
Revises: 4d6f5801f71c
Create Date: 2026-09-28 23:45:08.467503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82074cabddd3'
down_revision: Union[str, Sequence[str], None] = '4d6f5801f71c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Populate holdings.instrument_id from instruments.trading_symbol."""
    connection = op.get_bind()

    connection.execute(
        sa.text(
            """
            UPDATE holdings AS h
            SET instrument_id = i.id
            FROM instruments AS i
            WHERE h.symbol = i.trading_symbol
              AND h.instrument_id IS NULL
            """
        )
    )


def downgrade() -> None:
    """Clear holding instrument references."""
    connection = op.get_bind()

    connection.execute(
        sa.text(
            """
            UPDATE holdings
            SET instrument_id = NULL
            """
        )
    )
