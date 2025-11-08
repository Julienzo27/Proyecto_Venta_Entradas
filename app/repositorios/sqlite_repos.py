import sqlite3
from typing import List, Optional
from app.domain.evento.evento import Evento
from app.domain.cliente.cliente import Cliente
from app.domain.entrada.entrada import Entrada
from repositorios.irepos import IEventoRepo, IClienteRepo, IEntradaRepo


def _row_to_evento(row) -> Evento:
    return Evento(id_evento=row[0], nombre=row[1], fecha=row[2], sala=row[3], cupo=row[4], entradas_emitidas=row[5])


def _row_to_cliente(row) -> Cliente:
    return Cliente(id_cliente=row[0], nombre=row[1], email=row[2])


def _row_to_entrada(row) -> Entrada:
    return Entrada(id_entrada=row[0], id_evento=row[1], id_cliente=row[2], precio=row[3], estado=row[4])


class SqliteEventoRepo(IEventoRepo):
    def __init__(self, db_path='db.sqlite3'):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = None
        return conn

    def add(self, evento: Evento) -> None:
        conn = self._conn()
        cur = conn.cursor()
        if getattr(evento, 'id_evento', 0):
            cur.execute("INSERT OR REPLACE INTO evento (id_evento, nombre, fecha, sala, cupo, entradas_emitidas) VALUES (?, ?, ?, ?, ?, ?)",
                        (evento.id_evento, evento.nombre, evento.fecha, evento.sala, evento.cupo, evento.entradas_emitidas))
        else:
            cur.execute("INSERT INTO evento (nombre, fecha, sala, cupo, entradas_emitidas) VALUES (?, ?, ?, ?, ?)",
                        (evento.nombre, evento.fecha, evento.sala, evento.cupo, evento.entradas_emitidas))
            evento.id_evento = cur.lastrowid
        conn.commit()
        conn.close()

    def get(self, id_evento: int) -> Optional[Evento]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT id_evento, nombre, fecha, sala, cupo, entradas_emitidas FROM evento WHERE id_evento = ?", (id_evento,))
        row = cur.fetchone()
        conn.close()
        return _row_to_evento(row) if row else None

    def list_all(self) -> List[Evento]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT id_evento, nombre, fecha, sala, cupo, entradas_emitidas FROM evento")
        rows = cur.fetchall()
        conn.close()
        return [_row_to_evento(r) for r in rows]

    def update(self, evento: Evento) -> None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("UPDATE evento SET nombre=?, fecha=?, sala=?, cupo=?, entradas_emitidas=? WHERE id_evento=?",
                    (evento.nombre, evento.fecha, evento.sala, evento.cupo, evento.entradas_emitidas, evento.id_evento))
        conn.commit()
        conn.close()

    def delete(self, id_evento: int) -> None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM evento WHERE id_evento = ?", (id_evento,))
        conn.commit()
        conn.close()


class SqliteClienteRepo(IClienteRepo):
    def __init__(self, db_path='db.sqlite3'):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = None
        return conn

    def add(self, cliente: Cliente) -> None:
        conn = self._conn()
        cur = conn.cursor()
        if getattr(cliente, 'id_cliente', 0):
            cur.execute("INSERT OR REPLACE INTO cliente (id_cliente, nombre, email) VALUES (?, ?, ?)",
                        (cliente.id_cliente, cliente.nombre, cliente.email))
        else:
            cur.execute("INSERT INTO cliente (nombre, email) VALUES (?, ?)",
                        (cliente.nombre, cliente.email))
            cliente.id_cliente = cur.lastrowid
        conn.commit()
        conn.close()

    def update(self, cliente: Cliente) -> None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("UPDATE cliente SET nombre=?, email=? WHERE id_cliente=?",
                    (cliente.nombre, cliente.email, cliente.id_cliente))
        conn.commit()
        conn.close()

    def delete(self, id_cliente: int) -> None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente,))
        conn.commit()
        conn.close()

    def get(self, id_cliente: int) -> Optional[Cliente]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT id_cliente, nombre, email FROM cliente WHERE id_cliente = ?", (id_cliente,))
        row = cur.fetchone()
        conn.close()
        return _row_to_cliente(row) if row else None

    def list_all(self) -> List[Cliente]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT id_cliente, nombre, email FROM cliente")
        rows = cur.fetchall()
        conn.close()
        return [_row_to_cliente(r) for r in rows]


class SqliteEntradaRepo(IEntradaRepo):
    def __init__(self, db_path='db.sqlite3'):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = None
        return conn

    def add(self, entrada: Entrada) -> None:
        conn = self._conn()
        cur = conn.cursor()
        if getattr(entrada, 'id_entrada', 0):
            cur.execute("INSERT OR REPLACE INTO entrada (id_entrada, id_evento, id_cliente, precio, estado) VALUES (?, ?, ?, ?, ?)",
                        (entrada.id_entrada, entrada.id_evento, entrada.id_cliente, entrada.precio, entrada.estado))
        else:
            cur.execute("INSERT INTO entrada (id_evento, id_cliente, precio, estado) VALUES (?, ?, ?, ?)",
                        (entrada.id_evento, entrada.id_cliente, entrada.precio, entrada.estado))
            entrada.id_entrada = cur.lastrowid
        conn.commit()
        conn.close()

    def get(self, id_entrada: int) -> Optional[Entrada]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT id_entrada, id_evento, id_cliente, precio, estado FROM entrada WHERE id_entrada = ?", (id_entrada,))
        row = cur.fetchone()
        conn.close()
        return _row_to_entrada(row) if row else None

    def find_by_evento_cliente(self, id_evento: int, id_cliente: int) -> Optional[Entrada]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT id_entrada, id_evento, id_cliente, precio, estado FROM entrada WHERE id_evento = ? AND id_cliente = ? AND estado = 'emitida'",
                    (id_evento, id_cliente))
        row = cur.fetchone()
        conn.close()
        return _row_to_entrada(row) if row else None

    def list_by_evento(self, id_evento: int):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT id_entrada, id_evento, id_cliente, precio, estado FROM entrada WHERE id_evento = ?", (id_evento,))
        rows = cur.fetchall()
        conn.close()
        return [_row_to_entrada(r) for r in rows]

    def update(self, entrada: Entrada) -> None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("UPDATE entrada SET id_evento=?, id_cliente=?, precio=?, estado=? WHERE id_entrada=?",
                    (entrada.id_evento, entrada.id_cliente, entrada.precio, entrada.estado, entrada.id_entrada))
        conn.commit()
        conn.close()
