from flask import Blueprint, request, jsonify
from app import db
from app.models.destination import Destination
from app.models.favorite import Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.weather_service import WeatherService

destinations_bp = Blueprint('destinations', __name__)

@destinations_bp.route('/search', methods=['GET'])
def search_destinations():
    try:
        query = request.args.get('q', '')
        country = request.args.get('country', '')
        climate_zone = request.args.get('climate_zone', '')
        
        # Build query
        destinations_query = Destination.query
        
        if query:
            destinations_query = destinations_query.filter(
                Destination.name.ilike(f'%{query}%')
            )
        
        if country:
            destinations_query = destinations_query.filter(
                Destination.country.ilike(f'%{country}%')
            )
        
        if climate_zone:
            destinations_query = destinations_query.filter(
                Destination.climate_zone == climate_zone
            )
        
        destinations = destinations_query.limit(50).all()
        
        return jsonify({
            'destinations': [dest.to_dict() for dest in destinations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@destinations_bp.route('/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    try:
        weather_service = WeatherService()
        destination = Destination.query.get(destination_id)
        
        if not destination:
            return jsonify({'error': 'Destination not found'}), 404
        
        # Get weather data
        weather_data = weather_service.get_current_weather(
            f"{destination.name}, {destination.country}"
        )
        
        response_data = destination.to_dict()
        if weather_data:
            response_data['current_weather'] = weather_data
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@destinations_bp.route('/<int:destination_id>/weather', methods=['GET'])
def get_destination_weather(destination_id):
    try:
        weather_service = WeatherService()
        destination = Destination.query.get(destination_id)
        
        if not destination:
            return jsonify({'error': 'Destination not found'}), 404
        
        days = request.args.get('days', 7, type=int)
        weather_data = weather_service.get_forecast(
            f"{destination.name}, {destination.country}",
            days=days
        )
        
        if not weather_data:
            return jsonify({'error': 'Weather data not available'}), 404
        
        return jsonify(weather_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@destinations_bp.route('/<int:destination_id>/climate', methods=['GET'])
def get_destination_climate(destination_id):
    try:
        weather_service = WeatherService()
        destination = Destination.query.get(destination_id)
        
        if not destination:
            return jsonify({'error': 'Destination not found'}), 404
        
        climate_data = weather_service.get_climate_data(
            f"{destination.name}, {destination.country}"
        )
        
        if not climate_data:
            return jsonify({'error': 'Climate data not available'}), 404
        
        return jsonify(climate_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
