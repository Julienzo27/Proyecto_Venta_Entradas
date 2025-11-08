from dataclasses import dataclass

@dataclass
class Cliente:
    id_cliente: int
    nombre: str
    email: str