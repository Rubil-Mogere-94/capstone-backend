from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.recommendation_service import RecommendationService

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get travel recommendations for the current user."""
    try:
        recommendation_service = RecommendationService()
        user_id = get_jwt_identity()
        
        recommendations = recommendation_service.get_recommendations(user_id)
        
        return jsonify({
            'recommendations': [dest.to_dict() for dest in recommendations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
