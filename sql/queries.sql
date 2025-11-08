-- tablas
CREATE TABLE evento (
  id_evento INTEGER PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  fecha DATE NOT NULL,
  sala VARCHAR(100),
  cupo INTEGER NOT NULL,
  entradas_emitidas INTEGER DEFAULT 0
);

CREATE TABLE cliente (
  id_cliente INTEGER PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  email VARCHAR(255) NOT NULL
);

CREATE TABLE entrada (
  id_entrada INTEGER PRIMARY KEY AUTOINCREMENT,
  id_evento INTEGER NOT NULL,
  id_cliente INTEGER NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  estado VARCHAR(20) NOT NULL,
  FOREIGN KEY (id_evento) REFERENCES evento(id_evento),
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  UNIQUE (id_evento, id_cliente) -- evita duplicado
);

INSERT INTO Evento (nombre, fecha, sala, cupo_maximo) VALUES
('Concierto Rock Local', '2025-11-15 21:00:00', 'Sala Principal', 150), 
('Obra Teatro Clásico', '2025-12-01 19:30:00', 'Teatro Menor', 50),
('Stand-up Comedy Show', '2026-01-20 20:00:00', 'Bar Cultural', 80),
('Charla: Ciencia Ficción', '2025-10-25 18:00:00', 'Auditorio', 30),
('Festival de Jazz', '2026-03-05 22:00:00', 'Sala Principal', 200);

INSERT INTO Cliente (nombre, email) VALUES
('Ana Gómez', 'ana.gomez@mail.com'),
('Benito Pérez', 'benito.perez@mail.com'),
('Carla Díaz', 'carla.diaz@mail.com'),
('Darío Castro', 'dario.castro@mail.com'),
('Elena Ruiz', 'elena.ruiz@mail.com');

-- Entradas de Prueba (Algunas emitidas, una anulada)
-- Ana compra para Concierto Rock (id_evento 1)
INSERT INTO Entrada (id_evento, id_cliente, precio, estado) VALUES (1, 1, 15.50, 'emitida');
-- Benito compra para Obra Teatro (id_evento 2)
INSERT INTO Entrada (id_evento, id_cliente, precio, estado) VALUES (2, 2, 25.00, 'emitida');
-- Carla compra para Stand-up (id_evento 3)
INSERT INTO Entrada (id_evento, id_cliente, precio, estado) VALUES (3, 3, 10.00, 'emitida');
-- Darío compra para Concierto Rock (id_evento 1) INSERT INTO Entrada (id_evento, id_cliente, precio, estado) VALUES (1, 4, 15.50, 'emitida');
-- Elena compra para Charla (id_evento 4) y luego es anulada
INSERT INTO Entrada (id_evento, id_cliente, precio, estado) VALUES (4, 5, 5.00, 'anulada');
-- Actualizar cupo de eventos (simulando que se actualizaría tras cada emisión) UPDATE Evento SET cupo_actual = 2 WHERE id_evento = 1; -- 2 entradas emitidas UPDATE Evento SET cupo_actual = 1 WHERE id_evento = 2; 
UPDATE Evento SET cupo_actual = 1 WHERE id_evento = 3;
-- El evento 4 tiene 1 entrada 'anulada', por lo que cupo_actual = 0
SELECT (Reportes)
-- 1. Listado de todos los Eventos con cupo disponible 
SELECT nombre, fecha, sala, cupo_maximo - cupo_actual AS cupo_disponible
FROM Evento
WHERE cupo_actual < cupo_maximo;
-- 2. Entradas por evento (Reporte: Entradas por evento)
SELECT
E.nombre AS Evento,
C.nombre AS Cliente,
T.precio,
T.estado
FROM Entrada AS T 
JOIN Evento AS E ON T.id_evento = E.id_evento
JOIN Cliente AS C ON T.id_cliente = C.id_cliente 
WHERE E.nombre = 'Concierto Rock Local' AND T.estado = 'emitida'; 

-- 3. Recaudación por evento (Reporte: Recaudación por evento) 
SELECT 
E.nombre AS Evento,
SUM(T.precio) AS Recaudacion_Total 
FROM Entrada AS T 
JOIN Evento AS E ON T.id_evento = E.id_evento
WHERE T.estado = 'emitida'
GROUP BY E.nombre;

-- UPDATE relevante: Anular una entrada (simulando la anulación de la entrada con ID 1)
-- IMPORTANTE: Después de este UPDATE, el cupo_actual del Evento 1 debería decrementar en el sistema. UPDATE Entrada 
SET estado = 'anulada' 
WHERE id_entrada = 1;

-- UPDATE relevante: Actualizar el precio de un evento futuro (ej. Evento 5)
UPDATE Entrada
SET precio = 30.00
WHERE id_evento = 5;

-- DELETE relevante: Eliminar un Cliente (se recomienda tener ON DELETE CASCADE en FKs o asegurarse de que no tenga entradas emitidas)
DELETE FROM Cliente
WHERE id_cliente = 5;

-- Reportes
-- Entradas por evento
SELECT * FROM entrada WHERE id_evento = :id_evento;

-- Recaudación por evento
SELECT SUM(precio) AS recaudacion FROM entrada WHERE id_evento = :id_evento AND estado = 'emitida';