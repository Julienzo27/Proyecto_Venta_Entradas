from dataclasses import dataclass

@dataclass
class Entrada:
    id_entrada: int
    id_evento: int
    id_cliente: int
    precio: float
    estado: str  # 'emitida' | 'anulada'

    def anular(self):
        self.estado = 'anulada'