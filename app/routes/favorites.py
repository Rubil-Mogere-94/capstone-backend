from flask import Blueprint, request, jsonify
from app import db
from app.models.favorite import Favorite
from app.models.destination import Destination
from flask_jwt_extended import jwt_required, get_jwt_identity

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('', methods=['GET'])
@jwt_required()
def get_favorites():
    try:
        user_id = get_jwt_identity()
        
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'favorites': [fav.to_dict() for fav in favorites]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@favorites_bp.route('', methods=['POST'])
@jwt_required()
def add_favorite():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('destination_id'):
            return jsonify({'error': 'Destination ID is required'}), 400
        
        destination_id = data['destination_id']
        
        # Check if destination exists
        destination = Destination.query.get(destination_id)
        if not destination:
            return jsonify({'error': 'Destination not found'}), 404
        
        # Check if already favorited
        existing_favorite = Favorite.query.filter_by(
            user_id=user_id, 
            destination_id=destination_id
        ).first()
        
        if existing_favorite:
            return jsonify({'error': 'Destination already in favorites'}), 409
        
        # Create favorite
        favorite = Favorite(
            user_id=user_id,
            destination_id=destination_id,
            notes=data.get('notes')
        )
        
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Destination added to favorites',
            'favorite': favorite.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@favorites_bp.route('/<int:favorite_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(favorite_id):
    try:
        user_id = get_jwt_identity()
        
        favorite = Favorite.query.filter_by(
            id=favorite_id, 
            user_id=user_id
        ).first()
        
        if not favorite:
            return jsonify({'error': 'Favorite not found'}), 404
        
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Favorite removed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@favorites_bp.route('/<int:favorite_id>', methods=['PUT'])
@jwt_required()
def update_favorite(favorite_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        favorite = Favorite.query.filter_by(
            id=favorite_id, 
            user_id=user_id
        ).first()
        
        if not favorite:
            return jsonify({'error': 'Favorite not found'}), 404
        
        if 'notes' in data:
            favorite.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Favorite updated successfully',
            'favorite': favorite.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
