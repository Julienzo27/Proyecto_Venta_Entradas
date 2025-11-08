from app import app
c = app.test_client()
resp = c.post('/clientes/delete/1', follow_redirects=True)
print('POST delete client 1 ->', resp.status_code)
text = resp.data.decode('utf-8')
print('Contains error message?', 'No se puede eliminar un cliente con entradas emitidas' in text)
