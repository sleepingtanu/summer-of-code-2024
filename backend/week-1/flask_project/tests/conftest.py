import pytest
from app import create_app, db

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres1:tanvi12345@localhost:5432/dsoc_db'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()
