from app import app
c = app.test_client()
resp = c.post('/eventos/delete/1', follow_redirects=True)
print('POST delete event 1 ->', resp.status_code)
text = resp.data.decode('utf-8')
print('Contains error message?', 'No se puede eliminar un evento con entradas emitidas' in text)
