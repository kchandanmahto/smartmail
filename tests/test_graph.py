
from app.schemas import EmailRequest


def test_email_request_defaults():

    request = EmailRequest(
        email="Please send me the project update."
    )

    assert request.tone == "professional"
    assert request.length == "medium"


def test_invalid_tone():

    try:
        EmailRequest(
            email="Please send me an update.",
            tone="angry"
        )
        assert False, "Invalid tone should be rejected"

    except ValueError:
        assert True
