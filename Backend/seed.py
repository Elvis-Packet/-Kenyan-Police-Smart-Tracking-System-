from app import app
from db import db
from models import User, PoliceStation, CaseReport, LostItem, TrackingLog, EscalatedCase

with app.app_context():
    print("Seeding database...")

    # Clear all existing data
    EscalatedCase.query.delete()
    TrackingLog.query.delete()
    LostItem.query.delete()
    CaseReport.query.delete()
    User.query.delete()
    PoliceStation.query.delete()

    # Create police stations
    station1 = PoliceStation(name="Central Police Station", location="Nairobi CBD")
    station2 = PoliceStation(name="Westlands Police Station", location="Westlands, Nairobi")
    db.session.add_all([station1, station2])
    db.session.commit()

    # Create users
    officer1 = User(name="Alice Wanjiku", email="alice@police.go.ke", role="officer", station=station1)
    officer2 = User(name="David Otieno", email="david@police.go.ke", role="officer", station=station2)
    dci_officer = User(name="DCI Officer Mike", email="mike@dci.go.ke", role="dci", station=station1)
    db.session.add_all([officer1, officer2, dci_officer])
    db.session.commit()

    # Create a case report
    case1 = CaseReport(
        user_id=officer1.id,
        case_type="Robbery",
        description="Reported robbery on Kenyatta Avenue.",
        location="Kenyatta Avenue",
        status="pending",
        assigned_officer_id=officer2.id
    )
    db.session.add(case1)
    db.session.commit()

    # Create a lost item
    item1 = LostItem(
        user_id=officer2.id,
        item_type="Phone",
        identifier="iPhone 13, black, IMEI 123456789",
        last_known_location="Sarit Centre",
        assigned_traffic_id=officer1.id
    )
    db.session.add(item1)
    db.session.commit()

    # Create tracking log
    log1 = TrackingLog(
        item_id=item1.id,
        station_id=station2.id,
        updated_location="Parklands Police Station"
    )
    db.session.add(log1)
    db.session.commit()

    # Escalated case
    escalation = EscalatedCase(
        case_id=case1.id,
        escalated_by_id=officer1.id,
        reason="Suspected organized crime",
        dci_officer_id=dci_officer.id
    )
    db.session.add(escalation)
    db.session.commit()

    print("Database seeded successfully!")
