from db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('police_station.id'), nullable=True)

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"

class PoliceStation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    users = db.relationship('User', backref='station', lazy=True)

    def __repr__(self):
        return f"<PoliceStation {self.name}>"

class CaseReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    case_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='pending')
    escalated_to_dci = db.Column(db.Boolean, default=False)
    assigned_officer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CaseReport {self.id} - {self.case_type}>"

class LostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_type = db.Column(db.String(100), nullable=False)
    identifier = db.Column(db.String(200), nullable=False)
    last_known_location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='missing')
    is_tracked = db.Column(db.Boolean, default=True)
    assigned_traffic_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LostItem {self.id} - {self.item_type}>"

class TrackingLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('lost_item.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('police_station.id'), nullable=False)
    updated_location = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TrackingLog {self.id} - Item {self.item_id}>"

class EscalatedCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case_report.id'), nullable=False)
    escalated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='review')
    dci_officer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"<EscalatedCase {self.id} - Case {self.case_id}>"
