from decimal import Decimal
from typing import Dict, Any

from sqlalchemy import text
from app.core.database_pool import db_pool


async def _session():
    if not db_pool.session_factory:
        await db_pool.initialize()
    return await db_pool.get_session()


async def calculate_total_revenue(property_id: str, tenant_id: str) -> Dict[str, Any]:
    async with await _session() as session:
        row = (await session.execute(text("""
            SELECT SUM(total_amount) AS total, COUNT(*) AS count
            FROM reservations
            WHERE property_id = :p AND tenant_id = :t
        """), {"p": property_id, "t": tenant_id})).fetchone()

    total = Decimal(str(row.total)) if row and row.total is not None else Decimal("0")
    return {
        "property_id": property_id,
        "tenant_id": tenant_id,
        "total": str(total),
        "currency": "USD",
        "count": row.count if row else 0,
    }
