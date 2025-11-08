@startuml
actor Usuario
participant ServicioEntradas
participant EventoRepo
participant ClienteRepo
participant EntradaRepo

Usuario -> ServicioEntradas: emitir_entrada(idEvento, idCliente, precio)
activate ServicioEntradas
ServicioEntradas -> EventoRepo: get(idEvento)
EventoRepo --> ServicioEntradas: Evento / None
ServicioEntradas -> ClienteRepo: get(idCliente)
ClienteRepo --> ServicioEntradas: Cliente / None
alt evento o cliente inválido
  ServicioEntradas --> Usuario: DatoInvalidoError
else
  ServicioEntradas -> EntradaRepo: find_by_evento_cliente(...)
  EntradaRepo --> ServicioEntradas: existente / None
  alt existe
    ServicioEntradas --> Usuario: EntradaDuplicadaError
  else
    ServicioEntradas -> Evento: hay_cupo?
    alt sin cupo
      ServicioEntradas --> Usuario: CupoAgotadoError
    else
      ServicioEntradas -> Evento: reservar_butaca()
      ServicioEntradas -> EventoRepo: update(evento)
      ServicioEntradas -> EntradaRepo: add(entrada)
      ServicioEntradas --> Usuario: Entrada creada
    end
  end
end
deactivate ServicioEntradas
@enduml
