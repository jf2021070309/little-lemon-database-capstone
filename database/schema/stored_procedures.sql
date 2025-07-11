-- Little Lemon Stored Procedures
-- Database Engineer Capstone Project
-- Fecha: 10 de Julio, 2025

USE little_lemon_db;

-- Eliminar procedimientos existentes si existen
DROP PROCEDURE IF EXISTS GetMaxQuantity;
DROP PROCEDURE IF EXISTS ManageBooking;
DROP PROCEDURE IF EXISTS UpdateBooking;
DROP PROCEDURE IF EXISTS AddBooking;
DROP PROCEDURE IF EXISTS CancelBooking;
DROP PROCEDURE IF EXISTS CheckBookingAvailability;
DROP PROCEDURE IF EXISTS GetBookingsByDate;

-- Cambiar el delimitador para permitir múltiples declaraciones
DELIMITER //

-- 1. GetMaxQuantity() - Obtiene la cantidad máxima de un elemento específico
CREATE PROCEDURE GetMaxQuantity(
    IN menu_item_name VARCHAR(100),
    OUT max_quantity INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET max_quantity = 0;
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    SELECT MAX(quantity) INTO max_quantity
    FROM order_details od
    JOIN menu_items mi ON od.menu_item_id = mi.menu_item_id
    WHERE mi.item_name = menu_item_name;
    
    -- Si no se encuentra el elemento, devolver 0
    IF max_quantity IS NULL THEN
        SET max_quantity = 0;
    END IF;
    
    COMMIT;
END//

-- 2. ManageBooking() - Gestiona reservas generales con validaciones
CREATE PROCEDURE ManageBooking(
    IN booking_date DATE,
    IN table_number INT,
    OUT booking_status VARCHAR(255)
)
BEGIN
    DECLARE table_exists INT DEFAULT 0;
    DECLARE table_available INT DEFAULT 0;
    DECLARE existing_bookings INT DEFAULT 0;
    DECLARE target_table_id INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET booking_status = 'Error: Transaction failed';
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- Verificar si la mesa existe
    SELECT COUNT(*), table_id INTO table_exists, target_table_id
    FROM tables 
    WHERE table_number = table_number AND is_available = TRUE;
    
    IF table_exists = 0 THEN
        SET booking_status = 'Error: Table not found or not available';
        ROLLBACK;
    ELSE
        -- Verificar si hay reservas existentes para esa fecha y mesa
        SELECT COUNT(*) INTO existing_bookings
        FROM bookings 
        WHERE table_id = target_table_id 
        AND booking_date = booking_date 
        AND status = 'confirmed';
        
        IF existing_bookings > 0 THEN
            SET booking_status = CONCAT('Table ', table_number, ' is already booked for ', booking_date);
        ELSE
            SET booking_status = CONCAT('Table ', table_number, ' is available for booking on ', booking_date);
        END IF;
    END IF;
    
    COMMIT;
END//

-- 3. UpdateBooking() - Actualiza reservas existentes
CREATE PROCEDURE UpdateBooking(
    IN booking_id_param INT,
    IN new_booking_date DATE,
    IN new_booking_time TIME,
    IN new_number_of_guests INT,
    OUT update_status VARCHAR(255)
)
BEGIN
    DECLARE booking_exists INT DEFAULT 0;
    DECLARE current_status VARCHAR(20);
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET update_status = 'Error: Update failed';
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- Verificar si la reserva existe
    SELECT COUNT(*), status INTO booking_exists, current_status
    FROM bookings 
    WHERE booking_id = booking_id_param;
    
    IF booking_exists = 0 THEN
        SET update_status = 'Error: Booking not found';
        ROLLBACK;
    ELSEIF current_status = 'cancelled' THEN
        SET update_status = 'Error: Cannot update cancelled booking';
        ROLLBACK;
    ELSE
        -- Actualizar la reserva
        UPDATE bookings 
        SET 
            booking_date = new_booking_date,
            booking_time = new_booking_time,
            number_of_guests = new_number_of_guests,
            updated_at = CURRENT_TIMESTAMP
        WHERE booking_id = booking_id_param;
        
        SET update_status = CONCAT('Booking ID ', booking_id_param, ' updated successfully');
    END IF;
    
    COMMIT;
END//

-- 4. AddBooking() - Añade nuevas reservas
CREATE PROCEDURE AddBooking(
    IN customer_id_param INT,
    IN table_id_param INT,
    IN booking_date_param DATE,
    IN booking_time_param TIME,
    IN number_of_guests_param INT,
    IN special_requests_param TEXT,
    OUT booking_status VARCHAR(255)
)
BEGIN
    DECLARE customer_exists INT DEFAULT 0;
    DECLARE table_exists INT DEFAULT 0;
    DECLARE table_capacity INT DEFAULT 0;
    DECLARE existing_bookings INT DEFAULT 0;
    DECLARE new_booking_id INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET booking_status = 'Error: Booking creation failed';
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- Verificar si el cliente existe
    SELECT COUNT(*) INTO customer_exists
    FROM customers 
    WHERE customer_id = customer_id_param;
    
    IF customer_exists = 0 THEN
        SET booking_status = 'Error: Customer not found';
        ROLLBACK;
    ELSE
        -- Verificar si la mesa existe y obtener su capacidad
        SELECT COUNT(*), seating_capacity INTO table_exists, table_capacity
        FROM tables 
        WHERE table_id = table_id_param AND is_available = TRUE;
        
        IF table_exists = 0 THEN
            SET booking_status = 'Error: Table not found or not available';
            ROLLBACK;
        ELSEIF number_of_guests_param > table_capacity THEN
            SET booking_status = CONCAT('Error: Number of guests (', number_of_guests_param, ') exceeds table capacity (', table_capacity, ')');
            ROLLBACK;
        ELSE
            -- Verificar disponibilidad para la fecha y hora
            SELECT COUNT(*) INTO existing_bookings
            FROM bookings 
            WHERE table_id = table_id_param 
            AND booking_date = booking_date_param 
            AND booking_time = booking_time_param
            AND status = 'confirmed';
            
            IF existing_bookings > 0 THEN
                SET booking_status = 'Error: Table already booked for this date and time';
                ROLLBACK;
            ELSE
                -- Crear la nueva reserva
                INSERT INTO bookings (
                    customer_id, 
                    table_id, 
                    booking_date, 
                    booking_time, 
                    number_of_guests, 
                    special_requests,
                    status
                ) VALUES (
                    customer_id_param,
                    table_id_param,
                    booking_date_param,
                    booking_time_param,
                    number_of_guests_param,
                    special_requests_param,
                    'confirmed'
                );
                
                SET new_booking_id = LAST_INSERT_ID();
                SET booking_status = CONCAT('Booking confirmed with ID: ', new_booking_id);
            END IF;
        END IF;
    END IF;
    
    COMMIT;
END//

-- 5. CancelBooking() - Cancela reservas existentes
CREATE PROCEDURE CancelBooking(
    IN booking_id_param INT,
    OUT cancellation_status VARCHAR(255)
)
BEGIN
    DECLARE booking_exists INT DEFAULT 0;
    DECLARE current_status VARCHAR(20);
    DECLARE booking_date_val DATE;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET cancellation_status = 'Error: Cancellation failed';
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- Verificar si la reserva existe y obtener su estado
    SELECT COUNT(*), status, booking_date INTO booking_exists, current_status, booking_date_val
    FROM bookings 
    WHERE booking_id = booking_id_param;
    
    IF booking_exists = 0 THEN
        SET cancellation_status = 'Error: Booking not found';
        ROLLBACK;
    ELSEIF current_status = 'cancelled' THEN
        SET cancellation_status = 'Error: Booking already cancelled';
        ROLLBACK;
    ELSEIF current_status = 'completed' THEN
        SET cancellation_status = 'Error: Cannot cancel completed booking';
        ROLLBACK;
    ELSE
        -- Cancelar la reserva
        UPDATE bookings 
        SET 
            status = 'cancelled',
            updated_at = CURRENT_TIMESTAMP
        WHERE booking_id = booking_id_param;
        
        SET cancellation_status = CONCAT('Booking ID ', booking_id_param, ' cancelled successfully');
    END IF;
    
    COMMIT;
END//

-- 6. CheckBookingAvailability() - Verifica disponibilidad de mesas
CREATE PROCEDURE CheckBookingAvailability(
    IN check_date DATE,
    IN check_time TIME,
    IN required_capacity INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error: Query failed' AS status;
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    SELECT 
        t.table_id,
        t.table_number,
        t.seating_capacity,
        t.location,
        CASE 
            WHEN b.booking_id IS NULL THEN 'Available'
            ELSE 'Booked'
        END AS availability_status
    FROM tables t
    LEFT JOIN bookings b ON t.table_id = b.table_id 
        AND b.booking_date = check_date 
        AND b.booking_time = check_time
        AND b.status = 'confirmed'
    WHERE t.is_available = TRUE 
        AND t.seating_capacity >= required_capacity
    ORDER BY t.table_number;
    
    COMMIT;
END//

-- 7. GetBookingsByDate() - Obtiene todas las reservas para una fecha específica
CREATE PROCEDURE GetBookingsByDate(
    IN search_date DATE
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error: Query failed' AS status;
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
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
        b.special_requests,
        b.created_at
    FROM bookings b
    JOIN customers c ON b.customer_id = c.customer_id
    JOIN tables t ON b.table_id = t.table_id
    WHERE b.booking_date = search_date
    ORDER BY b.booking_time;
    
    COMMIT;
END//

-- Restaurar el delimitador
DELIMITER ;

-- Mostrar procedimientos creados
SHOW PROCEDURE STATUS WHERE Db = 'little_lemon_db';

SELECT 'Little Lemon Stored Procedures creados exitosamente!' AS Status;
