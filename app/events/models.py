from app import db

class EventCategory(db.Model):
    __tablename__ = 'event_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<EventCategory {self.name}>"

class SportEvent(db.Model):
    __tablename__ = 'sport_events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('event_categories.id'), nullable=False)

    owner = db.relationship('User', backref='sport_events', lazy=True)
    category = db.relationship('EventCategory', backref='sport_events', lazy=True)

    def __repr__(self):
        return f"<SportEvent {self.name}>"
