@startuml
class Evento {
  - id_evento: int
  - nombre: String
  - fecha: Date
  - sala: String
  - cupo: int
  - entradas_emitidas: int
  + hay_cupo()
  + reservar_butaca()
}
class Cliente {
  - id_cliente: int
  - nombre: String
  - email: String
}
class Entrada {
  - id_entrada: int
  - id_evento: int
  - id_cliente: int
  - precio: float
  - estado: string
  + anular()
}
class ServicioEntradas
interface IEventoRepo
interface IClienteRepo
interface IEntradaRepo

Evento "1" -- "*" Entrada : tiene >
Cliente "1" -- "*" Entrada : compra >
ServicioEntradas ..> IEventoRepo
ServicioEntradas ..> IClienteRepo
ServicioEntradas ..> IEntradaRepo
@enduml
