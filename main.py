from domain.evento import Evento
from domain.cliente import Cliente
from repositorios.in_memory_repos import EventoRepoInMemory, ClienteRepoInMemory, EntradaRepoInMemory
from servicios.servicio_entradas import ServicioEntradas
from exceptions.custom_error import CupoAgotadoError, EntradaDuplicadaError, DatoInvalidoError

# inicializar repos y servicio
er = EventoRepoInMemory()
cr = ClienteRepoInMemory()
erp = EntradaRepoInMemory()
serv = ServicioEntradas(er, cr, erp)

# crear datos
evento = Evento(id_evento=1, nombre='Concierto', fecha='2025-12-01', sala='Sala A', cupo=2)
cliente = Cliente(id_cliente=1, nombre='Ana', email='ana@mail.com')
serv.crear_evento(evento)
serv.crear_cliente(cliente)

# emitir entrada con try/except
try:
    entrada = serv.emitir_entrada(1, 1, 150.0)
    print('Entrada emitida:', entrada)
except EntradaDuplicadaError as e:
    print('Duplicada:', e)
except CupoAgotadoError as e:
    print('Cupo agotado:', e)
except DatoInvalidoError as e:
    print('Dato inválido:', e)
except Exception as e:
    print('Error inesperado:', e)