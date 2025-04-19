from flask import Blueprint, request, jsonify
from db import db
from models import User, PoliceStation, CaseReport, LostItem, TrackingLog, EscalatedCase

routes = Blueprint('routes', __name__)

# -------------------- USER CRUD --------------------
@routes.route('/')
def index():
    return jsonify({"message": "Welcome to the kenya police tracker API!"}), 200


@routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id, "name": u.name, "email": u.email,
        "role": u.role, "station_id": u.station_id
    } for u in users])

@routes.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        "id": user.id, "name": user.name, "email": user.email,
        "role": user.role, "station_id": user.station_id
    })

@routes.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        name=data['name'], email=data['email'],
        role=data['role'], station_id=data.get('station_id')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "id": user.id}), 201

@routes.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.station_id = data.get('station_id', user.station_id)
    db.session.commit()
    return jsonify({"message": "User updated"})

@routes.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

# -------------------- STATION CRUD --------------------

@routes.route('/stations', methods=['GET'])
def get_stations():
    stations = PoliceStation.query.all()
    return jsonify([{
        "id": s.id, "name": s.name, "location": s.location
    } for s in stations])

@routes.route('/stations/<int:id>', methods=['GET'])
def get_station(id):
    station = PoliceStation.query.get_or_404(id)
    return jsonify({"id": station.id, "name": station.name, "location": station.location})

@routes.route('/stations', methods=['POST'])
def create_station():
    data = request.get_json()
    station = PoliceStation(name=data['name'], location=data['location'])
    db.session.add(station)
    db.session.commit()
    return jsonify({"message": "Station created", "id": station.id}), 201

@routes.route('/stations/<int:id>', methods=['PUT'])
def update_station(id):
    station = PoliceStation.query.get_or_404(id)
    data = request.get_json()
    station.name = data.get('name', station.name)
    station.location = data.get('location', station.location)
    db.session.commit()
    return jsonify({"message": "Station updated"})

@routes.route('/stations/<int:id>', methods=['DELETE'])
def delete_station(id):
    station = PoliceStation.query.get_or_404(id)
    db.session.delete(station)
    db.session.commit()
    return jsonify({"message": "Station deleted"})

# -------------------- CASE REPORT CRUD --------------------

@routes.route('/cases', methods=['GET'])
def get_cases():
    cases = CaseReport.query.all()
    return jsonify([{
        "id": c.id, "case_type": c.case_type, "description": c.description,
        "location": c.location, "status": c.status,
        "escalated_to_dci": c.escalated_to_dci,
        "assigned_officer_id": c.assigned_officer_id,
        "user_id": c.user_id, "created_at": c.created_at.isoformat()
    } for c in cases])

@routes.route('/cases/<int:id>', methods=['GET'])
def get_case(id):
    c = CaseReport.query.get_or_404(id)
    return jsonify({
        "id": c.id, "case_type": c.case_type, "description": c.description,
        "location": c.location, "status": c.status,
        "escalated_to_dci": c.escalated_to_dci,
        "assigned_officer_id": c.assigned_officer_id,
        "user_id": c.user_id, "created_at": c.created_at.isoformat()
    })

@routes.route('/cases', methods=['POST'])
def create_case():
    data = request.get_json()
    case = CaseReport(
        user_id=data['user_id'], case_type=data['case_type'],
        description=data['description'], location=data['location'],
        assigned_officer_id=data.get('assigned_officer_id')
    )
    db.session.add(case)
    db.session.commit()
    return jsonify({"message": "Case created", "id": case.id}), 201

@routes.route('/cases/<int:id>', methods=['PUT'])
def update_case(id):
    c = CaseReport.query.get_or_404(id)
    data = request.get_json()
    c.case_type = data.get('case_type', c.case_type)
    c.description = data.get('description', c.description)
    c.location = data.get('location', c.location)
    c.status = data.get('status', c.status)
    c.escalated_to_dci = data.get('escalated_to_dci', c.escalated_to_dci)
    c.assigned_officer_id = data.get('assigned_officer_id', c.assigned_officer_id)
    db.session.commit()
    return jsonify({"message": "Case updated"})

@routes.route('/cases/<int:id>', methods=['DELETE'])
def delete_case(id):
    c = CaseReport.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Case deleted"})

# -------------------- LOST ITEM CRUD --------------------

@routes.route('/lost-items', methods=['GET'])
def get_lost_items():
    items = LostItem.query.all()
    return jsonify([{
        "id": i.id, "item_type": i.item_type, "identifier": i.identifier,
        "last_known_location": i.last_known_location,
        "status": i.status, "is_tracked": i.is_tracked,
        "assigned_traffic_id": i.assigned_traffic_id,
        "user_id": i.user_id, "created_at": i.created_at.isoformat()
    } for i in items])

@routes.route('/lost-items/<int:id>', methods=['GET'])
def get_lost_item(id):
    i = LostItem.query.get_or_404(id)
    return jsonify({
        "id": i.id, "item_type": i.item_type, "identifier": i.identifier,
        "last_known_location": i.last_known_location,
        "status": i.status, "is_tracked": i.is_tracked,
        "assigned_traffic_id": i.assigned_traffic_id,
        "user_id": i.user_id, "created_at": i.created_at.isoformat()
    })

@routes.route('/lost-items', methods=['POST'])
def create_lost_item():
    data = request.get_json()
    item = LostItem(
        user_id=data['user_id'], item_type=data['item_type'],
        identifier=data['identifier'], last_known_location=data['last_known_location'],
        status=data.get('status', 'missing'),
        is_tracked=data.get('is_tracked', True),
        assigned_traffic_id=data.get('assigned_traffic_id')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Lost item created", "id": item.id}), 201

@routes.route('/lost-items/<int:id>', methods=['PUT'])
def update_lost_item(id):
    i = LostItem.query.get_or_404(id)
    data = request.get_json()
    i.item_type = data.get('item_type', i.item_type)
    i.identifier = data.get('identifier', i.identifier)
    i.last_known_location = data.get('last_known_location', i.last_known_location)
    i.status = data.get('status', i.status)
    i.is_tracked = data.get('is_tracked', i.is_tracked)
    i.assigned_traffic_id = data.get('assigned_traffic_id', i.assigned_traffic_id)
    db.session.commit()
    return jsonify({"message": "Lost item updated"})

@routes.route('/lost-items/<int:id>', methods=['DELETE'])
def delete_lost_item(id):
    i = LostItem.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({"message": "Lost item deleted"})

# -------------------- ESCALATED CASE CRUD --------------------

@routes.route('/escalated-cases', methods=['GET'])
def get_escalated_cases():
    cases = EscalatedCase.query.all()
    return jsonify([{
        "id": e.id, "case_id": e.case_id,
        "escalated_by_id": e.escalated_by_id,
        "reason": e.reason, "status": e.status,
        "dci_officer_id": e.dci_officer_id
    } for e in cases])

@routes.route('/escalated-cases/<int:id>', methods=['GET'])
def get_escalated_case(id):
    e = EscalatedCase.query.get_or_404(id)
    return jsonify({
        "id": e.id, "case_id": e.case_id,
        "escalated_by_id": e.escalated_by_id,
        "reason": e.reason, "status": e.status,
        "dci_officer_id": e.dci_officer_id
    })

@routes.route('/escalated-cases', methods=['POST'])
def create_escalated_case():
    data = request.get_json()
    e = EscalatedCase(
        case_id=data['case_id'], escalated_by_id=data['escalated_by_id'],
        reason=data['reason'], status=data.get('status', 'review'),
        dci_officer_id=data.get('dci_officer_id')
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({"message": "Escalated case created", "id": e.id}), 201

@routes.route('/escalated-cases/<int:id>', methods=['PUT'])
def update_escalated_case(id):
    e = EscalatedCase.query.get_or_404(id)
    data = request.get_json()
    e.reason = data.get('reason', e.reason)
    e.status = data.get('status', e.status)
    e.dci_officer_id = data.get('dci_officer_id', e.dci_officer_id)
    db.session.commit()
    return jsonify({"message": "Escalated case updated"})

@routes.route('/escalated-cases/<int:id>', methods=['DELETE'])
def delete_escalated_case(id):
    e = EscalatedCase.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return jsonify({"message": "Escalated case deleted"})
