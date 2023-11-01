from app.core import settings


# endpoints
USER_URL = f"{settings.API_STR}/users"
USER_ME_URL = f"{USER_URL}/me"
USER_CREATE_OPEN_URL = f"{USER_URL}/open"
LOGIN_URL = f"{settings.API_STR}/login/access-token"

# test data
SAMPLE_USER_DATA = (
    {
        "email": "deadpool@example.com",
        "first_name": "john",
        "last_name": "doe",
        "password": "chimichangas4life",
    },
    {
        "email": "super-email@example.net",
        "first_name": "mike",
        "last_name": "testified",
        "password": "bigchungus123",
    },
    {
        "email": "jeffthekiller@o2.com",
        "first_name": "jeff",
        "last_name": "the killer",
        "password": "ilikecreepypasta123",
    },
)

SAMPLE_CATEGORY_DATA = (
    {"name": "chest"},
    {"name": "back"},
    {"name": "legs"},
    {"name": "shoulders"},
    {"name": "arms"},
    {"name": "abs"},
)

SAMPLE_EXERCISE_DATA = (
    {
        "name": "bench press",
        "description": "bench press description",
        "category_id": 1,
    },
    {
        "name": "pull ups",
        "description": "pull ups description",
        "category_id": 2,
    },
    {
        "name": "squats",
        "description": "squats description",
        "category_id": 3,
    },
)
