from typing import Dict, List, Optional
from .irepos import IEventoRepo, IClienteRepo, IEntradaRepo
from ..domain.evento import Evento
from ..domain.cliente import Cliente
from ..domain.entrada import Entrada

class EventoRepoInMemory(IEventoRepo):
    def __init__(self):
        self._data: Dict[int, Evento] = {}

    def delete(self, id_evento: int) -> None:
        if id_evento in self._data:
            del self._data[id_evento]
        else:
            raise KeyError('Evento no existe')

    def add(self, evento: Evento) -> None:
        self._data[evento.id_evento] = evento

    def get(self, id_evento: int) -> Optional[Evento]:
        return self._data.get(id_evento)

    def list_all(self) -> List[Evento]:
        return list(self._data.values())

    def update(self, evento: Evento) -> None:
        self._data[evento.id_evento] = evento

class ClienteRepoInMemory(IClienteRepo):
    def __init__(self):
        self._data: Dict[int, Cliente] = {}

    def update(self, cliente: Cliente) -> None:
        if cliente.id_cliente in self._data:
            self._data[cliente.id_cliente] = cliente
        else:
            raise KeyError('Cliente no existe')

    def delete(self, id_cliente: int) -> None:
        if id_cliente in self._data:
            del self._data[id_cliente]
        else:
            raise KeyError('Cliente no existe')

    def add(self, cliente: Cliente) -> None:
        self._data[cliente.id_cliente] = cliente

    def get(self, id_cliente: int) -> Optional[Cliente]:
        return self._data.get(id_cliente)

    def list_all(self) -> List[Cliente]:
        return list(self._data.values())

class EntradaRepoInMemory(IEntradaRepo):
    def __init__(self):
        self._data: Dict[int, Entrada] = {}
        self._auto = 1

    def add(self, entrada: Entrada) -> None:
        # assign id if 0
        if entrada.id_entrada == 0:
            entrada.id_entrada = self._auto
            self._auto += 1
        self._data[entrada.id_entrada] = entrada

    def get(self, id_entrada: int) -> Optional[Entrada]:
        return self._data.get(id_entrada)

    def find_by_evento_cliente(self, id_evento: int, id_cliente: int) -> Optional[Entrada]:
        for e in self._data.values():
            if e.id_evento == id_evento and e.id_cliente == id_cliente and e.estado == 'emitida':
                return e
        return None

    def list_by_evento(self, id_evento: int):
        return [e for e in self._data.values() if e.id_evento == id_evento]

    def update(self, entrada: Entrada) -> None:
        self._data[entrada.id_entrada] = entrada