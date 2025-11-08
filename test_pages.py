from app import app
c = app.test_client()
print('GET /clientes/edit/1 ->', c.get('/clientes/edit/1').status_code)
print('GET /clientes/delete/1 ->', c.get('/clientes/delete/1').status_code)
