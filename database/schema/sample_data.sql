-- Little Lemon Sample Data
-- Database Engineer Capstone Project
-- Fecha: 10 de Julio, 2025

USE little_lemon_db;

-- Insertar datos de ejemplo en la tabla customers
INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES
('María', 'González', 'maria.gonzalez@email.com', '555-0101', '123 Main St', 'Chicago', 'IL', '60601'),
('Carlos', 'Rodríguez', 'carlos.rodriguez@email.com', '555-0102', '456 Oak Ave', 'Chicago', 'IL', '60602'),
('Ana', 'López', 'ana.lopez@email.com', '555-0103', '789 Pine Rd', 'Chicago', 'IL', '60603'),
('Juan', 'Martínez', 'juan.martinez@email.com', '555-0104', '321 Elm St', 'Chicago', 'IL', '60604'),
('Sofia', 'García', 'sofia.garcia@email.com', '555-0105', '654 Maple Dr', 'Chicago', 'IL', '60605'),
('Diego', 'Hernández', 'diego.hernandez@email.com', '555-0106', '987 Cedar Ln', 'Chicago', 'IL', '60606'),
('Isabella', 'Jiménez', 'isabella.jimenez@email.com', '555-0107', '147 Birch Ave', 'Chicago', 'IL', '60607'),
('Miguel', 'Ruiz', 'miguel.ruiz@email.com', '555-0108', '258 Spruce St', 'Chicago', 'IL', '60608'),
('Camila', 'Torres', 'camila.torres@email.com', '555-0109', '369 Willow Rd', 'Chicago', 'IL', '60609'),
('Alejandro', 'Flores', 'alejandro.flores@email.com', '555-0110', '741 Poplar Dr', 'Chicago', 'IL', '60610');

-- Insertar datos de ejemplo en la tabla employees
INSERT INTO employees (first_name, last_name, email, phone, position, hire_date, salary) VALUES
('Roberto', 'Valdez', 'roberto.valdez@littlelemon.com', '555-0201', 'Manager', '2023-01-15', 55000.00),
('Patricia', 'Morales', 'patricia.morales@littlelemon.com', '555-0202', 'Head Chef', '2023-02-01', 50000.00),
('Fernando', 'Castro', 'fernando.castro@littlelemon.com', '555-0203', 'Sous Chef', '2023-02-15', 40000.00),
('Elena', 'Vargas', 'elena.vargas@littlelemon.com', '555-0204', 'Server', '2023-03-01', 35000.00),
('Ricardo', 'Mendoza', 'ricardo.mendoza@littlelemon.com', '555-0205', 'Server', '2023-03-15', 35000.00),
('Lucia', 'Romero', 'lucia.romero@littlelemon.com', '555-0206', 'Bartender', '2023-04-01', 38000.00),
('Andrés', 'Gutiérrez', 'andres.gutierrez@littlelemon.com', '555-0207', 'Host', '2023-04-15', 32000.00),
('Valeria', 'Ortiz', 'valeria.ortiz@littlelemon.com', '555-0208', 'Server', '2023-05-01', 35000.00);

-- Insertar datos de ejemplo en la tabla menu_categories
INSERT INTO menu_categories (category_name, description) VALUES
('Appetizers', 'Delicious starters to begin your meal'),
('Main Courses', 'Hearty and satisfying main dishes'),
('Desserts', 'Sweet treats to end your meal'),
('Beverages', 'Refreshing drinks and cocktails'),
('Salads', 'Fresh and healthy salad options'),
('Pasta', 'Traditional Italian pasta dishes'),
('Seafood', 'Fresh seafood specialties'),
('Vegetarian', 'Plant-based delicious options');

-- Insertar datos de ejemplo en la tabla menu_items
INSERT INTO menu_items (item_name, description, category_id, price, cost, quantity_in_stock) VALUES
('Bruschetta', 'Toasted bread with tomatoes, basil, and garlic', 1, 8.95, 3.50, 50),
('Calamari Rings', 'Crispy fried squid rings with marinara sauce', 1, 12.95, 5.00, 30),
('Caesar Salad', 'Classic romaine lettuce with Caesar dressing', 5, 11.95, 4.50, 40),
('Chicken Parmigiana', 'Breaded chicken breast with marinara and mozzarella', 2, 18.95, 8.00, 25),
('Spaghetti Carbonara', 'Creamy pasta with bacon, eggs, and parmesan', 6, 16.95, 6.50, 35),
('Grilled Salmon', 'Fresh Atlantic salmon with lemon herb butter', 7, 22.95, 12.00, 20),
('Margherita Pizza', 'Traditional pizza with tomato, mozzarella, and basil', 2, 15.95, 6.00, 30),
('Tiramisu', 'Classic Italian dessert with coffee and mascarpone', 3, 7.95, 3.00, 25),
('Chocolate Lava Cake', 'Warm chocolate cake with molten center', 3, 8.95, 3.50, 20),
('House Wine Red', 'Chianti Classico - House selection', 4, 6.95, 2.50, 100),
('House Wine White', 'Pinot Grigio - House selection', 4, 6.95, 2.50, 100),
('Lemonade', 'Fresh squeezed lemonade', 4, 3.95, 1.00, 80),
('Vegetable Lasagna', 'Layers of pasta with seasonal vegetables', 8, 17.95, 7.00, 15),
('Mediterranean Salad', 'Mixed greens with olives, feta, and vinaigrette', 5, 13.95, 5.50, 25),
('Seafood Risotto', 'Creamy arborio rice with mixed seafood', 7, 24.95, 11.00, 18);

-- Insertar datos de ejemplo en la tabla tables
INSERT INTO tables (table_number, seating_capacity, location) VALUES
(1, 2, 'Window Side'),
(2, 2, 'Window Side'),
(3, 4, 'Main Dining'),
(4, 4, 'Main Dining'),
(5, 6, 'Main Dining'),
(6, 6, 'Main Dining'),
(7, 8, 'Private Section'),
(8, 8, 'Private Section'),
(9, 2, 'Bar Area'),
(10, 2, 'Bar Area'),
(11, 4, 'Patio'),
(12, 4, 'Patio');

-- Insertar datos de ejemplo en la tabla bookings
INSERT INTO bookings (customer_id, table_id, employee_id, booking_date, booking_time, number_of_guests, special_requests, status) VALUES
(1, 1, 7, '2025-07-15', '19:00:00', 2, 'Anniversary dinner', 'confirmed'),
(2, 3, 7, '2025-07-15', '19:30:00', 4, 'Birthday celebration', 'confirmed'),
(3, 5, 7, '2025-07-16', '18:00:00', 6, 'Business dinner', 'confirmed'),
(4, 2, 7, '2025-07-16', '20:00:00', 2, NULL, 'confirmed'),
(5, 4, 7, '2025-07-17', '19:00:00', 4, 'Vegetarian options needed', 'confirmed'),
(6, 7, 7, '2025-07-17', '18:30:00', 8, 'Family reunion', 'confirmed'),
(7, 9, 7, '2025-07-18', '17:30:00', 2, 'Quiet table please', 'confirmed'),
(8, 6, 7, '2025-07-18', '19:00:00', 6, NULL, 'confirmed'),
(9, 11, 7, '2025-07-19', '18:00:00', 4, 'Outdoor seating', 'confirmed'),
(10, 12, 7, '2025-07-19', '19:30:00', 4, 'Wine pairing', 'confirmed'),
(1, 2, 7, '2025-07-12', '19:00:00', 2, NULL, 'completed'),
(3, 4, 7, '2025-07-13', '18:30:00', 4, NULL, 'completed'),
(5, 6, 7, '2025-07-14', '20:00:00', 6, NULL, 'completed');

-- Insertar datos de ejemplo en la tabla orders
INSERT INTO orders (customer_id, booking_id, employee_id, order_date, order_time, total_amount, order_status, payment_status) VALUES
(1, 11, 4, '2025-07-12', '19:15:00', 89.85, 'served', 'paid'),
(3, 12, 4, '2025-07-13', '18:45:00', 145.50, 'served', 'paid'),
(5, 13, 5, '2025-07-14', '20:15:00', 178.90, 'served', 'paid'),
(2, 2, 4, '2025-07-15', '19:45:00', 95.75, 'preparing', 'pending'),
(4, 4, 5, '2025-07-16', '20:15:00', 67.40, 'pending', 'pending');

-- Insertar datos de ejemplo en la tabla order_details
INSERT INTO order_details (order_id, menu_item_id, quantity, unit_price, subtotal) VALUES
-- Orden 1 (Customer 1)
(1, 1, 2, 8.95, 17.90),
(1, 6, 1, 22.95, 22.95),
(1, 8, 2, 7.95, 15.90),
(1, 10, 2, 6.95, 13.90),
(1, 12, 2, 3.95, 7.90),
-- Orden 2 (Customer 3)
(2, 2, 1, 12.95, 12.95),
(2, 4, 2, 18.95, 37.90),
(2, 5, 2, 16.95, 33.90),
(2, 9, 2, 8.95, 17.90),
(2, 11, 4, 6.95, 27.80),
-- Orden 3 (Customer 5)
(3, 3, 2, 11.95, 23.90),
(3, 13, 3, 17.95, 53.85),
(3, 14, 2, 13.95, 27.90),
(3, 8, 3, 7.95, 23.85),
(3, 10, 6, 6.95, 41.70),
-- Orden 4 (Customer 2)
(4, 7, 1, 15.95, 15.95),
(4, 3, 2, 11.95, 23.90),
(4, 9, 2, 8.95, 17.90),
(4, 12, 3, 3.95, 11.85),
-- Orden 5 (Customer 4)
(5, 15, 1, 24.95, 24.95),
(5, 14, 1, 13.95, 13.95),
(5, 8, 1, 7.95, 7.95),
(5, 11, 2, 6.95, 13.90);

-- Insertar datos de ejemplo en la tabla suppliers
INSERT INTO suppliers (supplier_name, contact_name, email, phone, address, city, state, zip_code) VALUES
('Fresh Seafood Co.', 'Michael Johnson', 'michael@freshseafood.com', '555-0301', '1000 Harbor Dr', 'Chicago', 'IL', '60611'),
('Organic Vegetables Inc.', 'Sarah Davis', 'sarah@organicveg.com', '555-0302', '2000 Farm Rd', 'Chicago', 'IL', '60612'),
('Premium Meats LLC', 'Robert Wilson', 'robert@premiummeats.com', '555-0303', '3000 Butcher Ave', 'Chicago', 'IL', '60613'),
('Italian Imports', 'Giuseppe Rossi', 'giuseppe@italianImports.com', '555-0304', '4000 Pasta St', 'Chicago', 'IL', '60614'),
('Wine & Spirits Co.', 'Jennifer Brown', 'jennifer@winespirits.com', '555-0305', '5000 Vineyard Ln', 'Chicago', 'IL', '60615');

-- Insertar datos de ejemplo en la tabla inventory
INSERT INTO inventory (item_name, supplier_id, current_stock, minimum_stock, unit_cost, last_restocked) VALUES
('Atlantic Salmon', 1, 50, 20, 8.50, '2025-07-10'),
('Chicken Breast', 3, 100, 30, 4.25, '2025-07-09'),
('Ground Beef', 3, 75, 25, 5.50, '2025-07-08'),
('Fresh Basil', 2, 20, 5, 2.00, '2025-07-10'),
('Tomatoes', 2, 150, 50, 1.50, '2025-07-09'),
('Mozzarella Cheese', 4, 40, 15, 3.75, '2025-07-08'),
('Pasta (Spaghetti)', 4, 200, 50, 0.85, '2025-07-07'),
('Olive Oil', 4, 25, 10, 12.00, '2025-07-06'),
('Chianti Wine', 5, 60, 20, 8.00, '2025-07-05'),
('Pinot Grigio', 5, 55, 20, 7.50, '2025-07-05'),
('Lemons', 2, 100, 30, 0.75, '2025-07-10'),
('Mixed Greens', 2, 80, 25, 2.25, '2025-07-09');

-- Actualizar las cantidades totales en las órdenes
UPDATE orders SET total_amount = (
    SELECT SUM(od.subtotal) 
    FROM order_details od 
    WHERE od.order_id = orders.order_id
);

-- Crear algunos datos adicionales para pruebas
-- Reservas para fechas futuras
INSERT INTO bookings (customer_id, table_id, employee_id, booking_date, booking_time, number_of_guests, special_requests, status) VALUES
(1, 3, 7, '2025-07-20', '19:00:00', 4, 'Window table preferred', 'confirmed'),
(2, 5, 7, '2025-07-21', '18:30:00', 6, 'Birthday cake needed', 'confirmed'),
(4, 1, 7, '2025-07-22', '20:00:00', 2, 'Quiet romantic dinner', 'confirmed'),
(6, 7, 7, '2025-07-23', '19:00:00', 8, 'Corporate event', 'confirmed'),
(8, 9, 7, '2025-07-24', '18:00:00', 2, 'Bar seating', 'confirmed');

-- Mostrar resumen de datos insertados
SELECT 'Datos de ejemplo insertados exitosamente!' AS Status;

SELECT 'Resumen de datos:' AS Info;
SELECT 'Customers' AS Table_Name, COUNT(*) AS Records FROM customers
UNION ALL
SELECT 'Employees', COUNT(*) FROM employees
UNION ALL
SELECT 'Menu Categories', COUNT(*) FROM menu_categories
UNION ALL
SELECT 'Menu Items', COUNT(*) FROM menu_items
UNION ALL
SELECT 'Tables', COUNT(*) FROM tables
UNION ALL
SELECT 'Bookings', COUNT(*) FROM bookings
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Details', COUNT(*) FROM order_details
UNION ALL
SELECT 'Suppliers', COUNT(*) FROM suppliers
UNION ALL
SELECT 'Inventory', COUNT(*) FROM inventory;
