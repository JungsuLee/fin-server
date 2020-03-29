from app import db


class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    description = db.Column(db.Text)
    category = db.Column(db.String(15))
    type = db.Column(db.String(10))

    def to_json2(self):
        return {
            'date': self.date.strftime('%m/%d'),
            'amount': self.amount,
            'description': self.description,
            'category': self.category,
        }
