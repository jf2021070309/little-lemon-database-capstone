# Little Lemon Database Design Documentation

## Database Engineer Capstone Project
**Fecha:** 10 de Julio, 2025

---

## 1. Introducción

Este documento describe el diseño de la base de datos para el sistema de gestión de reservas y ventas del restaurante Little Lemon. El sistema está diseñado para manejar las operaciones diarias del restaurante, incluyendo gestión de clientes, reservas, pedidos, inventario y análisis de datos.

## 2. Objetivos del Sistema

### 2.1 Objetivos Principales
- Gestionar eficientemente las reservas de mesas
- Procesar y rastrear pedidos de clientes
- Mantener información actualizada del inventario
- Generar reportes y análisis de ventas
- Proporcionar una base sólida para análisis de datos

### 2.2 Objetivos Específicos
- Implementar procedimientos almacenados para operaciones complejas
- Optimizar consultas mediante índices apropiados
- Asegurar integridad referencial
- Facilitar análisis de datos con Tableau
- Proporcionar interfaz Python para operaciones

## 3. Arquitectura de la Base de Datos

### 3.1 Modelo Conceptual
El sistema utiliza un modelo relacional normalizado con las siguientes entidades principales:

- **Customers**: Información de clientes
- **Employees**: Información del personal
- **Tables**: Mesas del restaurante
- **Menu Categories**: Categorías del menú
- **Menu Items**: Elementos del menú
- **Bookings**: Reservas de mesas
- **Orders**: Pedidos de clientes
- **Order Details**: Detalles de los pedidos
- **Suppliers**: Proveedores
- **Inventory**: Inventario de ingredientes

### 3.2 Relaciones Principales
- Un cliente puede tener múltiples reservas (1:N)
- Una reserva puede generar una orden (1:1)
- Una orden puede tener múltiples detalles (1:N)
- Un elemento del menú puede aparecer en múltiples detalles (N:M)
- Una mesa puede tener múltiples reservas (1:N)
- Un empleado puede atender múltiples reservas (1:N)

## 4. Diseño Detallado de Tablas

### 4.1 Tabla: customers
```sql
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
```

**Propósito:** Almacenar información de clientes del restaurante.

**Campos clave:**
- `customer_id`: Identificador único del cliente
- `email`: Email único para identificación
- `created_at/updated_at`: Auditoría de cambios

### 4.2 Tabla: employees
```sql
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
```

**Propósito:** Gestionar información del personal del restaurante.

**Campos clave:**
- `employee_id`: Identificador único del empleado
- `position`: Posición en el restaurante
- `hire_date`: Fecha de contratación

### 4.3 Tabla: tables
```sql
CREATE TABLE tables (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT UNIQUE NOT NULL,
    seating_capacity INT NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    location VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Propósito:** Administrar las mesas del restaurante.

**Campos clave:**
- `table_number`: Número visible de la mesa
- `seating_capacity`: Capacidad de asientos
- `is_available`: Estado de disponibilidad

### 4.4 Tabla: bookings
```sql
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
```

**Propósito:** Gestionar reservas de mesas.

**Campos clave:**
- `booking_date/booking_time`: Fecha y hora de la reserva
- `status`: Estado de la reserva (confirmada, cancelada, completada, no show)
- `special_requests`: Solicitudes especiales del cliente

### 4.5 Tabla: orders
```sql
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
```

**Propósito:** Rastrear pedidos de clientes.

**Campos clave:**
- `order_status`: Estado del pedido en cocina
- `payment_status`: Estado del pago
- `booking_id`: Vinculación opcional con reserva

## 5. Procedimientos Almacenados

### 5.1 GetMaxQuantity()
```sql
PROCEDURE GetMaxQuantity(
    IN menu_item_name VARCHAR(100),
    OUT max_quantity INT
)
```
**Propósito:** Obtiene la cantidad máxima de un elemento del menú pedido en una sola orden.

### 5.2 ManageBooking()
```sql
PROCEDURE ManageBooking(
    IN booking_date DATE,
    IN table_number INT,
    OUT booking_status VARCHAR(255)
)
```
**Propósito:** Verifica la disponibilidad de una mesa para una fecha específica.

### 5.3 AddBooking()
```sql
PROCEDURE AddBooking(
    IN customer_id_param INT,
    IN table_id_param INT,
    IN booking_date_param DATE,
    IN booking_time_param TIME,
    IN number_of_guests_param INT,
    IN special_requests_param TEXT,
    OUT booking_status VARCHAR(255)
)
```
**Propósito:** Añade una nueva reserva con validaciones completas.

### 5.4 UpdateBooking()
```sql
PROCEDURE UpdateBooking(
    IN booking_id_param INT,
    IN new_booking_date DATE,
    IN new_booking_time TIME,
    IN new_number_of_guests INT,
    OUT update_status VARCHAR(255)
)
```
**Propósito:** Actualiza una reserva existente.

### 5.5 CancelBooking()
```sql
PROCEDURE CancelBooking(
    IN booking_id_param INT,
    OUT cancellation_status VARCHAR(255)
)
```
**Propósito:** Cancela una reserva existente.

## 6. Índices y Optimización

### 6.1 Índices Principales
```sql
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_bookings_date ON bookings(booking_date);
CREATE INDEX idx_bookings_customer ON bookings(customer_id);
CREATE INDEX idx_bookings_table ON bookings(table_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_menu_items_category ON menu_items(category_id);
CREATE INDEX idx_order_details_order ON order_details(order_id);
CREATE INDEX idx_order_details_menu_item ON order_details(menu_item_id);
```

### 6.2 Estrategia de Optimización
- **Índices compuestos** para consultas frecuentes
- **Índices en claves foráneas** para joins eficientes
- **Índices en fechas** para consultas temporales
- **Índices únicos** para mantener integridad

## 7. Vistas para Análisis

### 7.1 booking_details
```sql
CREATE VIEW booking_details AS
SELECT 
    b.booking_id,
    b.booking_date,
    b.booking_time,
    b.number_of_guests,
    b.status,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email AS customer_email,
    t.table_number,
    t.seating_capacity,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN tables t ON b.table_id = t.table_id
LEFT JOIN employees e ON b.employee_id = e.employee_id;
```

### 7.2 sales_analysis
```sql
CREATE VIEW sales_analysis AS
SELECT 
    o.order_id,
    o.order_date,
    o.order_time,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    mi.item_name,
    mc.category_name,
    od.quantity,
    od.unit_price,
    od.subtotal,
    o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_details od ON o.order_id = od.order_id
JOIN menu_items mi ON od.menu_item_id = mi.menu_item_id
JOIN menu_categories mc ON mi.category_id = mc.category_id;
```

## 8. Seguridad y Permisos

### 8.1 Usuarios de Base de Datos
- **root**: Administrador completo
- **app_user**: Usuario para aplicación Python
- **analista**: Usuario para análisis de datos

### 8.2 Permisos por Rol
- **Administrador**: Todos los permisos
- **Aplicación**: SELECT, INSERT, UPDATE, DELETE en tablas operativas
- **Analista**: SELECT en todas las tablas y vistas

## 9. Backup y Recuperación

### 9.1 Estrategia de Backup
- **Backup completo**: Diario a las 2:00 AM
- **Backup incremental**: Cada 4 horas
- **Backup de transacciones**: Cada 15 minutos

### 9.2 Política de Retención
- Backups diarios: 30 días
- Backups semanales: 12 semanas
- Backups mensuales: 12 meses

## 10. Monitoreo y Mantenimiento

### 10.1 Métricas Clave
- Tiempo de respuesta de consultas
- Uso de índices
- Fragmentación de tablas
- Crecimiento de datos

### 10.2 Mantenimiento Programado
- **Actualización de estadísticas**: Semanal
- **Reindexación**: Mensual
- **Limpieza de logs**: Diario
- **Análisis de rendimiento**: Mensual

## 11. Integración con Herramientas

### 11.1 Python Integration
- **mysql-connector-python**: Conexión a base de datos
- **pandas**: Análisis de datos
- **Pool de conexiones**: Optimización de rendimiento

### 11.2 Tableau Integration
- **Conexión directa**: Para análisis en tiempo real
- **Exportación CSV**: Para análisis histórico
- **Vistas optimizadas**: Para dashboards específicos

## 12. Consideraciones de Escalabilidad

### 12.1 Crecimiento Esperado
- 1000 clientes nuevos por mes
- 500 reservas diarias
- 200 pedidos diarios
- 50 GB de datos por año

### 12.2 Estrategias de Escalamiento
- **Particionamiento horizontal**: Por fecha
- **Archivado**: Datos antiguos
- **Replicación**: Para alta disponibilidad
- **Sharding**: Para distribución de carga

## 13. Conclusiones

El diseño de la base de datos Little Lemon proporciona:

1. **Estructura normalizada** que elimina redundancia
2. **Integridad referencial** mediante claves foráneas
3. **Flexibilidad** para agregar nuevas funcionalidades
4. **Optimización** mediante índices estratégicos
5. **Escalabilidad** para crecimiento futuro
6. **Seguridad** a través de roles y permisos
7. **Integración** con herramientas de análisis

Este diseño cumple con todos los requisitos del capstone project y proporciona una base sólida para las operaciones del restaurante Little Lemon.

---

**Autor:** [Tu Nombre]  
**Proyecto:** Database Engineer Capstone - Meta/Coursera  
**Fecha:** 10 de Julio, 2025
