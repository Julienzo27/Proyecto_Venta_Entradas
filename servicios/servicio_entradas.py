from exceptions.custom_error import CupoAgotadoError, EntradaDuplicadaError, DatoInvalidoError

class ServicioEntradas:
    def __init__(self, evento_repo, cliente_repo, entrada_repo):
        self.evento_repo = evento_repo
        self.cliente_repo = cliente_repo
        self.entrada_repo = entrada_repo

    def crear_evento(self, evento):
        if evento.cupo <= 0:
            raise DatoInvalidoError('El cupo debe ser mayor a 0')
        self.evento_repo.add(evento)

    def actualizar_evento(self, evento):
        if evento.cupo <= 0:
            raise DatoInvalidoError('El cupo debe ser mayor a 0')
        existing = self.evento_repo.get(evento.id_evento)
        if not existing:
            raise DatoInvalidoError('Evento no existe')
        self.evento_repo.update(evento)

    def eliminar_evento(self, id_evento: int):
        existing = self.evento_repo.get(id_evento)
        if not existing:
            raise DatoInvalidoError('Evento no existe')
        # Prevent deletion if there are emitted entradas for the event
        entradas = self.entrada_repo.list_by_evento(id_evento)
        for ent in entradas:
            if ent.estado == 'emitida':
                raise DatoInvalidoError('No se puede eliminar un evento con entradas emitidas')
        self.evento_repo.delete(id_evento)

    def crear_cliente(self, cliente):
        if '@' not in cliente.email:
            raise DatoInvalidoError('Email inválido')
        self.cliente_repo.add(cliente)

    def actualizar_cliente(self, cliente):
        if '@' not in cliente.email:
            raise DatoInvalidoError('Email inválido')
        # ensure exists
        existing = self.cliente_repo.get(cliente.id_cliente)
        if not existing:
            raise DatoInvalidoError('Cliente no existe')
        self.cliente_repo.update(cliente)

    def eliminar_cliente(self, id_cliente: int):
        existing = self.cliente_repo.get(id_cliente)
        if not existing:
            raise DatoInvalidoError('Cliente no existe')
        # business rule: prevent deletion if client has emitted entradas
        # check via entrada_repo
        entradas = self.entrada_repo.list_by_evento(0) if hasattr(self.entrada_repo, 'list_all') else None
        # simpler: ask repo for any entrada with this cliente
        # We implemented find_by_evento_cliente, but it requires evento id; instead iterate all entradas
        has_emitidas = False
        try:
            # try to use a repo method list_all if exists
            if hasattr(self.entrada_repo, 'list_all'):
                all_ent = self.entrada_repo.list_all()
            else:
                # fallback: try event ids from evento_repo
                all_ent = []
                eventos = self.evento_repo.list_all()
                for e in eventos:
                    all_ent.extend(self.entrada_repo.list_by_evento(e.id_evento))
            for ent in all_ent:
                if ent.id_cliente == id_cliente and ent.estado == 'emitida':
                    has_emitidas = True
                    break
        except Exception:
            has_emitidas = False
        if has_emitidas:
            raise DatoInvalidoError('No se puede eliminar un cliente con entradas emitidas')
        self.cliente_repo.delete(id_cliente)

    def emitir_entrada(self, id_evento: int, id_cliente: int, precio: float):
        # Validaciones y excepciones con try/except en el caller
        evento = self.evento_repo.get(id_evento)
        if not evento:
            raise DatoInvalidoError('Evento no existe')
        cliente = self.cliente_repo.get(id_cliente)
        if not cliente:
            raise DatoInvalidoError('Cliente no existe')

        # duplicado
        existente = self.entrada_repo.find_by_evento_cliente(id_evento, id_cliente)
        if existente:
            raise EntradaDuplicadaError('El cliente ya posee una entrada para este evento')

        # cupo
        if not evento.hay_cupo():
            raise CupoAgotadoError('No hay más cupo para el evento')

        # generar entrada
        from ..domain.entrada import Entrada
        entrada = Entrada(id_entrada=0, id_evento=id_evento, id_cliente=id_cliente, precio=precio, estado='emitida')
        # reservar cupo
        evento.reservar_butaca()
        # persistir
        self.evento_repo.update(evento)
        self.entrada_repo.add(entrada)
        return entrada

    def anular_entrada(self, id_entrada: int):
        entrada = self.entrada_repo.get(id_entrada)
        if not entrada:
            raise DatoInvalidoError('Entrada no existe')
        if entrada.estado == 'anulada':
            return entrada
        # liberar cupo
        evento = self.evento_repo.get(entrada.id_evento)
        if evento:
            evento.liberar_butaca()
            self.evento_repo.update(evento)
        entrada.anular()
        self.entrada_repo.update(entrada)
        return entrada

    # Reportes
    def entradas_por_evento(self, id_evento: int):
        return self.entrada_repo.list_by_evento(id_evento)

    def recaudacion_por_evento(self, id_evento: int) -> float:
        entradas = self.entrada_repo.list_by_evento(id_evento)
        return sum(e.precio for e in entradas if e.estado == 'emitida')