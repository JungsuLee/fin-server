from app import db


class Offering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    description = db.Column(db.Text)
    name = db.Column(db.Text)
    category = db.Column(db.String(15))
    moneyType = db.Column(db.String(15))

    def to_json2(self):
        return {
            'date': str(self.date),
            'amount': self.amount,
            'description': self.description,
            'name': self.name,
            'category': self.category,
            'moneyType': self.moneyType,
        }


class Revenue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    description = db.Column(db.Text)
    # ministry = db.Column(db.String(15))
    team = db.Column(db.String(15))
    reference = db.Column(db.String(15))


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    description = db.Column(db.Text)
    # ministry = db.Column(db.String(15))
    team = db.Column(db.String(15))
    status = db.Column(db.String(15))
    reference = db.Column(db.String(15))
