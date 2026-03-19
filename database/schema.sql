CREATE TABLE IF NOT EXISTS vehiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    precio REAL NOT NULL,
    cilindraje INTEGER NOT NULL,
    estado TEXT NOT NULL DEFAULT 'disponible' CHECK(estado IN ('disponible', 'vendido')),
    color TEXT,
    anio INTEGER,
    imagen_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    documento TEXT NOT NULL UNIQUE,
    telefono TEXT NOT NULL,
    email TEXT,
    direccion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_vehiculo INTEGER NOT NULL,
    fecha_venta DATE NOT NULL,
    valor REAL NOT NULL,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id)
);

-- Datos de pruebaa
INSERT OR IGNORE INTO vehiculos (marca, modelo, precio, cilindraje, estado, color, anio) VALUES
('Ducati', 'Panigale V4', 28500000, 1103, 'disponible', 'Rojo', 2024),
('BMW', 'S1000RR', 35000000, 999, 'disponible', 'Negro', 2024),
('Kawasaki', 'Ninja ZX-10R', 24900000, 998, 'disponible', 'Verde', 2023),
('Honda', 'CBR1000RR-R', 29800000, 1000, 'disponible', 'Rojo', 2024),
('Yamaha', 'YZF-R1', 27500000, 998, 'disponible', 'Azul', 2023),
('Aprilia', 'RSV4', 26900000, 1099, 'disponible', 'Naranja', 2024),
('Triumph', 'Daytona 765', 19800000, 765, 'disponible', 'Blanco', 2023),
('Suzuki', 'GSX-R1000', 22500000, 999, 'vendido', 'Negro', 2023);

INSERT OR IGNORE INTO clientes (nombre, documento, telefono, email, direccion) VALUES
('Carlos Rodríguez', '1234567890', '3001234567', 'carlos@email.com', 'Bogotá, Chapinero'),
('María González', '0987654321', '3109876543', 'maria@email.com', 'Medellín, El Poblado'),
('Juan Pérez', '1122334455', '3201122334', 'juan@email.com', 'Cali, Granada');

INSERT OR IGNORE INTO ventas (id_cliente, id_vehiculo, fecha_venta, valor, notas) VALUES
(1, 8, '2024-11-15', 22500000, 'Venta al contado');
