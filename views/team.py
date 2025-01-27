from flask import request, jsonify
from models import db, Team, TeamMember, User  # Ensure TeamMember is imported
from . import team_bp
from flask_jwt_extended import jwt_required, get_jwt_identity

# Get all teams (Read)
@team_bp.route('/', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([{
        'team_id': team.team_id,
        'name': team.name,
        'description': team.description
    } for team in teams])

# Create a new team (Create)
@team_bp.route('/', methods=['POST'])
@jwt_required()  
def create_team():
    data = request.json

    # Validate input
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'message': 'Name and description are required'}), 422

    name = data['name']
    description = data['description']

   
    existing_team = Team.query.filter_by(name=name).first()
    if existing_team:
        return jsonify({'message': 'A team with this name already exists'}), 400

    # Create and add the new team
    new_team = Team(name=name, description=description)

    try:
        db.session.add(new_team)
        db.session.commit()

        # Automatically add the creator to the team
        current_user_id = get_jwt_identity()
        team_member = TeamMember(team_id=new_team.team_id, user_id=current_user_id)
        db.session.add(team_member)
        db.session.commit()

        return jsonify({'message': 'Team created and you have joined it'}), 201
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Failed to create team', 'error': str(e)}), 500

# Update an existing team (Update)
@team_bp.route('/<int:team_id>', methods=['PUT'])
@jwt_required()  
def update_team(team_id):
    data = request.json
    team = Team.query.get(team_id)

    if not team:
        return jsonify({'message': 'Team not found'}), 404

    # Validate input
    if not data or ('name' not in data and 'description' not in data):
        return jsonify({'message': 'At least one of name or description is required'}), 422

    if 'name' in data:
        team.name = data['name']

    if 'description' in data:
        team.description = data['description']

    try:
        db.session.commit()
        return jsonify({'message': 'Team updated successfully'}), 200
    except Exception as e:
        db.session.rollback() 
        return jsonify({'message': 'Failed to update team', 'error': str(e)}), 500

# Delete a team (Delete)
@team_bp.route('/<int:team_id>', methods=['DELETE'])
@jwt_required()  
def delete_team(team_id):
    team = Team.query.get(team_id)

    if not team:
        return jsonify({'message': 'Team not found'}), 404

    try:
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'Team deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Failed to delete team', 'error': str(e)}), 500

# Add a member to a team
@team_bp.route('/<int:team_id>/add-member', methods=['POST'])
@jwt_required()  
def add_team_member(team_id):
    data = request.json
    
    # Validate input
    if not data or 'user_id' not in data:
        return jsonify({'message': 'User ID is required'}), 422
    
    user_id = data['user_id']
    
    
    user = User.query.get(user_id)  
    team = Team.query.get(team_id)

    if not team or not user:
        return jsonify({'message': 'Team or user not found'}), 404
    
    # Check if the user is already a member of the team
    existing_member = TeamMember.query.filter_by(team_id=team.team_id, user_id=user.user_id).first()
    
    if existing_member:
        return jsonify({'message': 'User is already a member of this team'}), 400
    
    new_member = TeamMember(team_id=team.team_id, user_id=user.user_id)

    try:
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'User added to the team successfully'}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': 'Failed to add user to the team', 'error': str(e)}), 500

# Remove a member from a team
@team_bp.route('/<int:team_id>/remove-member', methods=['POST'])
@jwt_required() 
def remove_team_member(team_id):
   data = request.json
   
   # Validate input
   if not data or 'user_id' not in data:
       return jsonify({'message': 'User ID is required'}), 422
   
   user_id = data['user_id']

   user = User.query.get(user_id)  
   team = Team.query.get(team_id)

   if not team or not user:
       return jsonify({'message': 'Team or user not found'}), 404
   
   member_to_remove = TeamMember.query.filter_by(team_id=team.team_id, user_id=user.user_id).first()

   if not member_to_remove:
       return jsonify({'message': 'User is not a member of this team'}), 400
   
   try:
       db.session.delete(member_to_remove)  
       db.session.commit()  
       return jsonify({'message':'User removed from the team successfully'}),200 
   except Exception as e:  
       db.session.rollback()  
       return jsonify({'message':'Failed to remove user from the team','error':str(e)}),500 
