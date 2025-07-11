-- Little Lemon Database Schema
-- Database Engineer Capstone Project
-- Fecha: 10 de Julio, 2025

-- Crear base de datos
DROP DATABASE IF EXISTS little_lemon_db;
CREATE DATABASE little_lemon_db;
USE little_lemon_db;

-- Tabla de Clientes
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Empleados
CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    position VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Categorías de Menú
CREATE TABLE menu_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Elementos del Menú
CREATE TABLE menu_items (
    menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    category_id INT,
    price DECIMAL(8, 2) NOT NULL,
    cost DECIMAL(8, 2),
    quantity_in_stock INT DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES menu_categories(category_id)
);

-- Tabla de Mesas
CREATE TABLE tables (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT UNIQUE NOT NULL,
    seating_capacity INT NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    location VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Reservas
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    table_id INT NOT NULL,
    employee_id INT,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    number_of_guests INT NOT NULL,
    special_requests TEXT,
    status ENUM('confirmed', 'cancelled', 'completed', 'no_show') DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (table_id) REFERENCES tables(table_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Tabla de Órdenes
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    booking_id INT,
    employee_id INT,
    order_date DATE NOT NULL,
    order_time TIME NOT NULL,
    total_amount DECIMAL(10, 2),
    order_status ENUM('pending', 'preparing', 'ready', 'served', 'cancelled') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'refunded') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Tabla de Detalles de Órdenes
CREATE TABLE order_details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(8, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id)
);

-- Tabla de Proveedores
CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Inventario
CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    supplier_id INT,
    current_stock INT DEFAULT 0,
    minimum_stock INT DEFAULT 0,
    unit_cost DECIMAL(8, 2),
    last_restocked DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- Crear índices para optimizar consultas
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_bookings_date ON bookings(booking_date);
CREATE INDEX idx_bookings_customer ON bookings(customer_id);
CREATE INDEX idx_bookings_table ON bookings(table_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_menu_items_category ON menu_items(category_id);
CREATE INDEX idx_order_details_order ON order_details(order_id);
CREATE INDEX idx_order_details_menu_item ON order_details(menu_item_id);

-- Crear vista para información completa de reservas
CREATE VIEW booking_details AS
SELECT 
    b.booking_id,
    b.booking_date,
    b.booking_time,
    b.number_of_guests,
    b.status,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email AS customer_email,
    c.phone AS customer_phone,
    t.table_number,
    t.seating_capacity,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    b.special_requests,
    b.created_at,
    b.updated_at
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN tables t ON b.table_id = t.table_id
LEFT JOIN employees e ON b.employee_id = e.employee_id;

-- Crear vista para análisis de ventas
CREATE VIEW sales_analysis AS
SELECT 
    o.order_id,
    o.order_date,
    o.order_time,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    mi.item_name,
    mi.category_id,
    mc.category_name,
    od.quantity,
    od.unit_price,
    od.subtotal,
    o.total_amount,
    o.order_status,
    o.payment_status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_details od ON o.order_id = od.order_id
JOIN menu_items mi ON od.menu_item_id = mi.menu_item_id
JOIN menu_categories mc ON mi.category_id = mc.category_id;

-- Crear vista para disponibilidad de mesas
CREATE VIEW table_availability AS
SELECT 
    t.table_id,
    t.table_number,
    t.seating_capacity,
    t.location,
    t.is_available,
    COUNT(b.booking_id) as total_bookings,
    MAX(b.booking_date) as last_booking_date
FROM tables t
LEFT JOIN bookings b ON t.table_id = b.table_id AND b.status = 'confirmed'
GROUP BY t.table_id, t.table_number, t.seating_capacity, t.location, t.is_available;

-- Mostrar estructura de tablas creadas
SHOW TABLES;

-- Mostrar información sobre las tablas principales
DESCRIBE customers;
DESCRIBE bookings;
DESCRIBE orders;
DESCRIBE menu_items;

PRINT 'Little Lemon Database Schema creado exitosamente!';
