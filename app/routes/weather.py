from flask import Blueprint, request, jsonify
from app.services.weather_service import WeatherService

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/current', methods=['GET'])
def get_current_weather():
    try:
        weather_service = WeatherService()
        location = request.args.get('location', '')
        
        if not location:
            return jsonify({'error': 'Location parameter is required'}), 400
        
        weather_data = weather_service.get_current_weather(location)
        
        if not weather_data:
            return jsonify({'error': 'Weather data not available'}), 404
        
        return jsonify(weather_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@weather_bp.route('/forecast', methods=['GET'])
def get_forecast():
    try:
        weather_service = WeatherService()
        location = request.args.get('location', '')
        days = request.args.get('days', 7, type=int)
        
        if not location:
            return jsonify({'error': 'Location parameter is required'}), 400
        
        forecast_data = weather_service.get_forecast(location, days=days)
        
        if not forecast_data:
            return jsonify({'error': 'Forecast data not available'}), 404
        
        return jsonify(forecast_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@weather_bp.route('/search', methods=['GET'])
def search_locations():
    try:
        weather_service = WeatherService()
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        locations = weather_service.search_locations(query)
        
        return jsonify({'locations': locations}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
