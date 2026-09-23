from fastapi import APIRouter, HTTPException
from ..models import placeModel
PLACES_DATABASE = {
    "delhi": [
        placeModel(
            name="India Gate",
            description="War memorial and iconic landmark of Delhi",
            category="Monument",
            rating=4.7,
            estimated_time_hours=2,
            entry_fee=None
        ),
        placeModel(
            name="Red Fort",
            description="Historic Mughal fort and UNESCO World Heritage Site",
            category="Historical",
            rating=4.6,
            estimated_time_hours=3,
            entry_fee=50
        ),
        placeModel(
            name="Qutub Minar",
            description="Tallest brick minaret in the world",
            category="Historical",
            rating=4.6,
            estimated_time_hours=2,
            entry_fee=40
        ),
        placeModel(
            name="Lotus Temple",
            description="Famous Baháʼí House of Worship",
            category="Religious",
            rating=4.7,
            estimated_time_hours=2,
            entry_fee=None
        ),
        placeModel(
            name="Akshardham Temple",
            description="Magnificent Hindu temple complex",
            category="Religious",
            rating=4.8,
            estimated_time_hours=4,
            entry_fee=None
        ),
        placeModel(
            name="Humayun's Tomb",
            description="UNESCO World Heritage Site",
            category="Historical",
            rating=4.6,
            estimated_time_hours=2,
            entry_fee=40
        ),
        placeModel(
            name="Chandni Chowk",
            description="Famous market and food destination",
            category="Market",
            rating=4.5,
            estimated_time_hours=3,
            entry_fee=None
        ),
        placeModel(
            name="Jama Masjid",
            description="One of India's largest mosques",
            category="Religious",
            rating=4.6,
            estimated_time_hours=2,
            entry_fee=None
        ),
        placeModel(
            name="National Museum",
            description="Museum showcasing Indian history and culture",
            category="Museum",
            rating=4.4,
            estimated_time_hours=3,
            entry_fee=20
        ),
        placeModel(
            name="Lodhi Garden",
            description="Beautiful urban park with historic tombs",
            category="Park",
            rating=4.7,
            estimated_time_hours=2,
            entry_fee=None
        ),
    ],

    "mumbai": [
        placeModel(
            name="Gateway of India",
            description="Iconic arch monument overlooking the Arabian Sea",
            category="Monument",
            rating=4.7,
            estimated_time_hours=2,
            entry_fee=None
        ),
        placeModel(
            name="Marine Drive",
            description="Scenic seaside promenade",
            category="Beach",
            rating=4.8,
            estimated_time_hours=2,
            entry_fee=None
        ),
        placeModel(
            name="Elephanta Caves",
            description="UNESCO World Heritage cave temples",
            category="Historical",
            rating=4.5,
            estimated_time_hours=4,
            entry_fee=40
        ),
        placeModel(
            name="Juhu Beach",
            description="Popular beach and street food destination",
            category="Beach",
            rating=4.4,
            estimated_time_hours=3,
            entry_fee=None
        ),
        placeModel(
            name="Siddhivinayak Temple",
            description="Famous Ganesh temple",
            category="Religious",
            rating=4.8,
            estimated_time_hours=2,
            entry_fee=None
        ),
        placeModel(
            name="Chhatrapati Shivaji Maharaj Terminus",
            description="Historic railway station and UNESCO site",
            category="Historical",
            rating=4.7,
            estimated_time_hours=1,
            entry_fee=None
        ),
        placeModel(
            name="Haji Ali Dargah",
            description="Mosque located on an islet",
            category="Religious",
            rating=4.6,
            estimated_time_hours=2,
            entry_fee=None
        ),
        placeModel(
            name="Sanjay Gandhi National Park",
            description="Large protected area with wildlife",
            category="Park",
            rating=4.5,
            estimated_time_hours=5,
            entry_fee=85
        ),
        placeModel(
            name="Bandra-Worli Sea Link",
            description="Modern engineering marvel",
            category="Landmark",
            rating=4.7,
            estimated_time_hours=1,
            entry_fee=None
        ),
        placeModel(
            name="Colaba Causeway",
            description="Popular shopping and dining street",
            category="Market",
            rating=4.5,
            estimated_time_hours=3,
            entry_fee=None
        ),
    ],

    "hyderabad": [
        placeModel(
            name="Charminar",
            description="Historic monument and symbol of Hyderabad",
            category="Historical",
            rating=4.6,
            estimated_time_hours=2,
            entry_fee=25
        ),
        placeModel(
            name="Golconda Fort",
            description="Ancient fort known for its acoustics",
            category="Historical",
            rating=4.7,
            estimated_time_hours=4,
            entry_fee=25
        ),
        placeModel(
            name="Ramoji Film City",
            description="World's largest integrated film studio complex",
            category="Entertainment",
            rating=4.6,
            estimated_time_hours=8,
            entry_fee=1500
        ),
        placeModel(
            name="Hussain Sagar Lake",
            description="Large lake with Buddha statue",
            category="Lake",
            rating=4.5,
            estimated_time_hours=2,
            entry_fee=None
        ),
        placeModel(
            name="Birla Mandir",
            description="White marble Hindu temple",
            category="Religious",
            rating=4.7,
            estimated_time_hours=2,
            entry_fee=None
        ),
        placeModel(
            name="Salar Jung Museum",
            description="One of India's largest museums",
            category="Museum",
            rating=4.6,
            estimated_time_hours=4,
            entry_fee=50
        ),
        placeModel(
            name="Chowmahalla Palace",
            description="Former residence of the Nizams",
            category="Historical",
            rating=4.5,
            estimated_time_hours=3,
            entry_fee=80
        ),
        placeModel(
            name="Nehru Zoological Park",
            description="Popular zoo with diverse wildlife",
            category="Zoo",
            rating=4.4,
            estimated_time_hours=4,
            entry_fee=100
        ),
        placeModel(
            name="Lumbini Park",
            description="Urban park near Hussain Sagar",
            category="Park",
            rating=4.3,
            estimated_time_hours=2,
            entry_fee=20
        ),
        placeModel(
            name="Shilparamam",
            description="Arts and crafts village",
            category="Cultural",
            rating=4.4,
            estimated_time_hours=3,
            entry_fee=60
        ),
    ]
}


async def fetch_places(destination: str) -> list[placeModel]:
    """
    Fetch places of interest for a given destination.
    """

    
    return PLACES_DATABASE.get(destination.lower(),[])