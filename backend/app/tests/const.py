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
