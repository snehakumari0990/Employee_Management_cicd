import pytest
from app import create_app, db
from app.models import Employee

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_employee(app):
    with app.app_context():
        emp = Employee(
            name='Test Employee',
            email='test@example.com',
            department='Engineering',
            position='Developer',
            salary=50000.0
        )
        db.session.add(emp)
        db.session.commit()
        return emp.id

def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_employee_page_loads(client):
    response = client.get('/add')
    assert response.status_code == 200

def test_add_employee(client, app):
    response = client.post('/add', data={
        'name': 'Sneha Sharma',
        'email': 'sneha@example.com',
        'department': 'DevOps',
        'position': 'Pipeline Engineer',
        'salary': '60000'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with app.app_context():
        emp = Employee.query.filter_by(email='sneha@example.com').first()
        assert emp is not None
        assert emp.name == 'Sneha Sharma'

def test_employee_appears_in_list(client, app):
    with app.app_context():
        emp = Employee(
            name='Raj Kumar',
            email='raj@example.com',
            department='HR',
            position='Manager',
            salary=70000.0
        )
        db.session.add(emp)
        db.session.commit()
    
    response = client.get('/')
    assert b'Raj Kumar' in response.data

def test_edit_employee(client, app, sample_employee):
    response = client.post(f'/edit/{sample_employee}', data={
        'name': 'Updated Name',
        'email': 'test@example.com',
        'department': 'Updated Department',
        'position': 'Senior Developer',
        'salary': '75000'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with app.app_context():
        emp = Employee.query.get(sample_employee)
        assert emp.name == 'Updated Name'
        assert emp.salary == 75000.0

def test_delete_employee(client, app, sample_employee):
    response = client.post(f'/delete/{sample_employee}', follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        emp = Employee.query.get(sample_employee)
        assert emp is None

def test_search_employee(client, app):
    with app.app_context():
        emp = Employee(
            name='Arjun Patel',
            email='arjun@example.com',
            department='Finance',
            position='Analyst',
            salary=45000.0
        )
        db.session.add(emp)
        db.session.commit()
    
    response = client.get('/search?query=Arjun')
    assert b'Arjun Patel' in response.data

def test_duplicate_email_rejected(client, app, sample_employee):
    response = client.post('/add', data={
        'name': 'Another Person',
        'email': 'test@example.com',
        'department': 'Sales',
        'position': 'Rep',
        'salary': '30000'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with app.app_context():
        count = Employee.query.filter_by(email='test@example.com').count()
        assert count == 1