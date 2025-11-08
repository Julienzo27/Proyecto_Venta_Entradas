from app import app

client = app.test_client()
resp = client.get('/clientes')
print('GET /clientes ->', resp.status_code)
print(resp.data.decode('utf-8')[:600])
