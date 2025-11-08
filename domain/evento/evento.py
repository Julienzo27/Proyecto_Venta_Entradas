from dataclasses import dataclass, field
from datetime import date

@dataclass
class Evento:
    id_evento: int
    nombre: str
    fecha: date
    sala: str
    cupo: int
    entradas_emitidas: int = field(default=0)

    def hay_cupo(self) -> bool:
        return self.entradas_emitidas < self.cupo

    def reservar_butaca(self):
        if not self.hay_cupo():
            raise ValueError("Cupo agotado")
        self.entradas_emitidas += 1

    def liberar_butaca(self):
        if self.entradas_emitidas > 0:
            self.entradas_emitidas -= 1