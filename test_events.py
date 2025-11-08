from app import app
c = app.test_client()
print('GET /eventos ->', c.get('/eventos').status_code)
print('GET /eventos/create ->', c.get('/eventos/create').status_code)
print('GET /eventos/edit/1 ->', c.get('/eventos/edit/1').status_code)
print('GET /eventos/delete/1 ->', c.get('/eventos/delete/1').status_code)
