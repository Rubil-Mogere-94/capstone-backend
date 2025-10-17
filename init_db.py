from app import create_app, db
from app.models.destination import Destination

def init_database():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add sample destinations
        sample_destinations = [
            {
                'name': 'Barcelona',
                'country': 'Spain',
                'latitude': 41.3851,
                'longitude': 2.1734,
                'climate_zone': 'Mediterranean'
            },
            {
                'name': 'Cape Town',
                'country': 'South Africa',
                'latitude': -33.9249,
                'longitude': 18.4241,
                'climate_zone': 'Mediterranean'
            },
            {
                'name': 'Sydney',
                'country': 'Australia',
                'latitude': -33.8688,
                'longitude': 151.2093,
                'climate_zone': 'Temperate'
            },
            {
                'name': 'Tokyo',
                'country': 'Japan',
                'latitude': 35.6762,
                'longitude': 139.6503,
                'climate_zone': 'Temperate'
            },
            {
                'name': 'Rio de Janeiro',
                'country': 'Brazil',
                'latitude': -22.9068,
                'longitude': -43.1729,
                'climate_zone': 'Tropical'
            },
            {
                'name': 'Paris',
                'country': 'France',
                'latitude': 48.8566,
                'longitude': 2.3522,
                'climate_zone': 'Temperate'
            },
            {
                'name': 'New York',
                'country': 'USA',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'climate_zone': 'Temperate'
            },
            {
                'name': 'Bangkok',
                'country': 'Thailand',
                'latitude': 13.7563,
                'longitude': 100.5018,
                'climate_zone': 'Tropical'
            }
        ]
        
        for dest_data in sample_destinations:
            if not Destination.query.filter_by(name=dest_data['name'], country=dest_data['country']).first():
                destination = Destination(**dest_data)
                db.session.add(destination)
        
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_database()
