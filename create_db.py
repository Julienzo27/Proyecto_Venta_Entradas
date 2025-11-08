import sqlite3

sql = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS evento (
  id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  fecha TEXT NOT NULL,
  sala TEXT,
  cupo INTEGER NOT NULL,
  entradas_emitidas INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cliente (
  id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS entrada (
  id_entrada INTEGER PRIMARY KEY AUTOINCREMENT,
  id_evento INTEGER NOT NULL,
  id_cliente INTEGER NOT NULL,
  precio REAL NOT NULL,
  estado TEXT NOT NULL,
  FOREIGN KEY (id_evento) REFERENCES evento(id_evento) ON DELETE CASCADE,
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
  UNIQUE (id_evento, id_cliente)
);
"""

def seed(conn):
    cur = conn.cursor()
    # check if there are eventos; if empty, insert sample data
    cur.execute("SELECT count(*) FROM evento")
    if cur.fetchone()[0] == 0:
        eventos = [
            ('Concierto Rock Local', '2025-11-15 21:00:00', 'Sala Principal', 150),
            ('Obra Teatro Clásico', '2025-12-01 19:30:00', 'Teatro Menor', 50),
            ('Stand-up Comedy Show', '2026-01-20 20:00:00', 'Bar Cultural', 80),
            ('Charla: Ciencia Ficción', '2025-10-25 18:00:00', 'Auditorio', 30),
            ('Festival de Jazz', '2026-03-05 22:00:00', 'Sala Principal', 200),
        ]
        cur.executemany("INSERT INTO evento (nombre, fecha, sala, cupo) VALUES (?, ?, ?, ?)", eventos)
    cur.execute("SELECT count(*) FROM cliente")
    if cur.fetchone()[0] == 0:
        clientes = [
            ('Ana Gómez', 'ana.gomez@mail.com'),
            ('Benito Pérez', 'benito.perez@mail.com'),
            ('Carla Díaz', 'carla.diaz@mail.com'),
            ('Darío Castro', 'dario.castro@mail.com'),
            ('Elena Ruiz', 'elena.ruiz@mail.com'),
        ]
        cur.executemany("INSERT INTO cliente (nombre, email) VALUES (?, ?)", clientes)
    cur.execute("SELECT count(*) FROM entrada")
    if cur.fetchone()[0] == 0:
        entradas = [
            (1, 1, 15.50, 'emitida'),
            (2, 2, 25.00, 'emitida'),
            (3, 3, 10.00, 'emitida'),
            (1, 4, 15.50, 'emitida'),
            (4, 5, 5.00, 'anulada'),
        ]
        cur.executemany("INSERT INTO entrada (id_evento, id_cliente, precio, estado) VALUES (?, ?, ?, ?)", entradas)
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    conn.executescript(sql)
    seed(conn)
    conn.close()
    print('db.sqlite3 creada/actualizada y semilla aplicada')


def init_db(db_path='db.sqlite3'):
    """Create or update the sqlite DB and apply seed data. Safe to call multiple times."""
    conn = sqlite3.connect(db_path)
    conn.executescript(sql)
    seed(conn)
    conn.close()


