from app.models.destination import Destination
from app.models.user_preference import UserPreference
from app.services.weather_service import WeatherService
from flask import current_app

class RecommendationService:
    def __init__(self):
        pass

    def get_recommendations(self, user_id):
        self.weather_service = WeatherService()
        """
        Get travel recommendations for a user based on their preferences.
        """
        user_preferences = UserPreference.query.filter_by(user_id=user_id).first()

        if not user_preferences:
            # If no preferences, return a default list of popular destinations
            return Destination.query.limit(10).all()

        # Build a query based on user preferences
        query = self._build_recommendation_query(user_preferences)

        # Execute the query and get the top recommendations
        recommendations = query.limit(10).all()

        return recommendations

    def _build_recommendation_query(self, preferences):
        """
        Build a SQLAlchemy query to filter destinations based on preferences.
        """
        query = Destination.query

        if preferences.preferred_climate:
            query = query.filter(Destination.climate_zone == preferences.preferred_climate)

        # Add more complex filtering logic here based on other preferences
        # For example, filter by continent, activities, etc.

        return query
