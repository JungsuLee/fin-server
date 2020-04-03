from app import db
from ...models import Finance
from sqlalchemy.sql import func, extract


def get_analytics(year):
    data = []
    for fin in db.session.query(
        extract('month', Finance.date),
        func.sum(Finance.amount),
        Finance.category,
        Finance.type,
    ).filter(
        extract('year', Finance.date) == year
    ).group_by(
        extract('month', Finance.date),
        Finance.category,
        Finance.type,
    ).order_by(extract('month', Finance.date)).all():
        data.append({
            'month': fin[0],
            'amount': fin[1],
            'category': fin[2],
            'type': fin[3],
        })
    return data
    