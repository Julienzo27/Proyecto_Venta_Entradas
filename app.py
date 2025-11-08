import os
from flask import Flask, render_template, request, redirect, url_for, flash
from repositorios.sqlite_repos import SqliteEventoRepo, SqliteClienteRepo, SqliteEntradaRepo
from servicios.servicio_entradas import ServicioEntradas
from exceptions.custom_error import CupoAgotadoError, EntradaDuplicadaError, DatoInvalidoError

app = Flask(__name__)
# Use SESSION_SECRET from Replit environment or fallback to dev key
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret')

db_path = 'db.sqlite3'
evento_repo = SqliteEventoRepo(db_path)
cliente_repo = SqliteClienteRepo(db_path)
entrada_repo = SqliteEntradaRepo(db_path)
serv = ServicioEntradas(evento_repo, cliente_repo, entrada_repo)

# Ensure DB exists (useful on first deployment)
try:
    from create_db import init_db
    if not os.path.exists(db_path):
        init_db(db_path)
except Exception:
    # if DB init fails, continue; errors will appear in logs
    pass

@app.route('/')
def root():
    return redirect(url_for('lista_eventos'))

@app.route('/eventos')
def lista_eventos():
    eventos = evento_repo.list_all()
    return render_template('eventos.html', eventos=eventos)


@app.route('/eventos/create', methods=['GET'])
def evento_create_form():
    return render_template('eventos_create.html')


@app.route('/eventos/create', methods=['POST'])
def evento_create():
    nombre = request.form.get('nombre', '').strip()
    fecha = request.form.get('fecha', '').strip()
    sala = request.form.get('sala', '').strip()
    try:
        cupo = int(request.form.get('cupo'))
    except Exception:
        cupo = 0
    from domain.evento.evento import Evento
    evento = Evento(id_evento=0, nombre=nombre, fecha=fecha, sala=sala, cupo=cupo)
    try:
        serv.crear_evento(evento)
        flash('Evento creado con éxito', 'success')
    except DatoInvalidoError as e:
        flash(str(e), 'danger')
    return redirect(url_for('lista_eventos'))


@app.route('/eventos/edit/<int:id>', methods=['GET'])
def evento_edit_form(id):
    evento = evento_repo.get(id)
    if not evento:
        flash('Evento no encontrado', 'danger')
        return redirect(url_for('lista_eventos'))
    return render_template('eventos_edit.html', evento=evento)


@app.route('/eventos/edit/<int:id>', methods=['POST'])
def evento_edit(id):
    nombre = request.form.get('nombre', '').strip()
    fecha = request.form.get('fecha', '').strip()
    sala = request.form.get('sala', '').strip()
    try:
        cupo = int(request.form.get('cupo'))
    except Exception:
        cupo = 0
    from domain.evento.evento import Evento
    evento = Evento(id_evento=id, nombre=nombre, fecha=fecha, sala=sala, cupo=cupo)
    try:
        serv.actualizar_evento(evento)
        flash('Evento actualizado con éxito', 'success')
    except DatoInvalidoError as e:
        flash(str(e), 'danger')
    return redirect(url_for('lista_eventos'))


@app.route('/eventos/delete/<int:id>', methods=['GET'])
def evento_delete_confirm(id):
    evento = evento_repo.get(id)
    if not evento:
        flash('Evento no encontrado', 'danger')
        return redirect(url_for('lista_eventos'))
    return render_template('eventos_delete.html', evento=evento)


@app.route('/eventos/delete/<int:id>', methods=['POST'])
def evento_delete(id):
    try:
        serv.eliminar_evento(id)
        flash('Evento eliminado', 'success')
    except DatoInvalidoError as e:
        flash(str(e), 'danger')
    return redirect(url_for('lista_eventos'))

@app.route('/clientes')
def lista_clientes():
    clientes = cliente_repo.list_all()
    return render_template('clientes.html', clientes=clientes)


@app.route('/clientes/edit/<int:id>', methods=['GET'])
def cliente_edit_form(id):
    cliente = cliente_repo.get(id)
    if not cliente:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('lista_clientes'))
    return render_template('clientes_edit.html', cliente=cliente)


@app.route('/clientes/edit/<int:id>', methods=['POST'])
def cliente_edit(id):
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip()
    from domain.cliente.cliente import Cliente
    cliente = Cliente(id_cliente=id, nombre=nombre, email=email)
    try:
        serv.actualizar_cliente(cliente)
        flash('Cliente actualizado con éxito', 'success')
    except DatoInvalidoError as e:
        flash(str(e), 'danger')
    return redirect(url_for('lista_clientes'))


@app.route('/clientes/delete/<int:id>', methods=['GET'])
def cliente_delete_confirm(id):
    cliente = cliente_repo.get(id)
    if not cliente:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('lista_clientes'))
    return render_template('clientes_delete.html', cliente=cliente)


@app.route('/clientes/delete/<int:id>', methods=['POST'])
def cliente_delete(id):
    try:
        serv.eliminar_cliente(id)
        flash('Cliente eliminado', 'success')
    except DatoInvalidoError as e:
        flash(str(e), 'danger')
    return redirect(url_for('lista_clientes'))

@app.route('/entradas')
def lista_entradas():
    # listar todas las entradas de ejemplo
    # para simplicidad, mostramos entradas por evento 1..n
    # fetch todos eventos y entradas
    eventos = evento_repo.list_all()
    entradas_por_evento = {e.id_evento: entrada_repo.list_by_evento(e.id_evento) for e in eventos}
    return render_template('entradas.html', eventos=eventos, entradas_por_evento=entradas_por_evento)

@app.route('/clientes/create', methods=['POST'])
def crear_cliente():
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip()
    from domain.cliente.cliente import Cliente
    # usa id_cliente=0 para que el repo asigne id autoincremental
    cliente = Cliente(id_cliente=0, nombre=nombre, email=email)
    try:
        serv.crear_cliente(cliente)
        flash('Cliente creado', 'success')
    except DatoInvalidoError as e:
        flash(str(e), 'danger')
    return redirect(url_for('lista_clientes'))

@app.route('/entradas/emitir', methods=['POST'])
def emitir():
    try:
        id_evento = int(request.form.get('id_evento'))
        id_cliente = int(request.form.get('id_cliente'))
        precio = float(request.form.get('precio'))
        serv.emitir_entrada(id_evento, id_cliente, precio)
        flash('Entrada emitida', 'success')
    except (EntradaDuplicadaError, CupoAgotadoError, DatoInvalidoError) as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash('Error inesperado: ' + str(e), 'danger')
    return redirect(url_for('lista_entradas'))

if __name__ == '__main__':
    # Bind to 0.0.0.0 and use the PORT env var provided by Replit (or 5000 locally)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
