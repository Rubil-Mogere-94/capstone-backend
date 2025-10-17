from app import db

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    preferred_climate = db.Column(db.String(50))
    # Add other preferences here, e.g.:
    # preferred_continent = db.Column(db.String(50))
    # preferred_activities = db.Column(db.String(255)) # Could be a comma-separated list

    user = db.relationship('User', back_populates='preferences')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'preferred_climate': self.preferred_climate,
        }
