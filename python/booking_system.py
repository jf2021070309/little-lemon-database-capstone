"""
Little Lemon Booking System
Database Engineer Capstone Project
Fecha: 10 de Julio, 2025
"""

import sys
import os
from datetime import datetime, date, time
from typing import Optional, Dict, List, Any, Tuple
import logging

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from connection import create_database_connection, LittleLemonConnection

class LittleLemonBookingSystem:
    """Sistema de gestión de reservas para Little Lemon Restaurant"""
    
    def __init__(self, environment: str = "local"):
        """
        Inicializa el sistema de reservas
        
        Args:
            environment: Entorno de trabajo (local, development, production)
        """
        self.db_connection = create_database_connection(environment)
        self.logger = logging.getLogger(__name__)
        
        # Verificar conexión
        if not self.db_connection.test_connection():
            raise Exception("No se pudo conectar a la base de datos")
    
    def get_max_quantity(self, menu_item_name: str) -> int:
        """
        Obtiene la cantidad máxima de un elemento del menú
        
        Args:
            menu_item_name: Nombre del elemento del menú
            
        Returns:
            int: Cantidad máxima pedida
        """
        try:
            # Ejecutar procedimiento almacenado
            query = "CALL GetMaxQuantity(%s, @max_quantity)"
            self.db_connection.execute_query(query, (menu_item_name,))
            
            # Obtener el resultado
            result = self.db_connection.execute_query(
                "SELECT @max_quantity AS max_quantity", 
                fetch=True
            )
            
            max_quantity = result[0]['max_quantity'] if result else 0
            self.logger.info(f"Cantidad máxima para {menu_item_name}: {max_quantity}")
            return max_quantity
            
        except Exception as e:
            self.logger.error(f"Error en get_max_quantity: {e}")
            return 0
    
    def manage_booking(self, booking_date: date, table_number: int) -> str:
        """
        Gestiona la disponibilidad de una reserva
        
        Args:
            booking_date: Fecha de la reserva
            table_number: Número de mesa
            
        Returns:
            str: Estado de la reserva
        """
        try:
            # Ejecutar procedimiento almacenado
            query = "CALL ManageBooking(%s, %s, @booking_status)"
            self.db_connection.execute_query(query, (booking_date, table_number))
            
            # Obtener el resultado
            result = self.db_connection.execute_query(
                "SELECT @booking_status AS booking_status", 
                fetch=True
            )
            
            status = result[0]['booking_status'] if result else "Error"
            self.logger.info(f"Estado de reserva para mesa {table_number} el {booking_date}: {status}")
            return status
            
        except Exception as e:
            self.logger.error(f"Error en manage_booking: {e}")
            return f"Error: {str(e)}"
    
    def update_booking(self, booking_id: int, new_booking_date: date, 
                      new_booking_time: time, new_number_of_guests: int) -> str:
        """
        Actualiza una reserva existente
        
        Args:
            booking_id: ID de la reserva
            new_booking_date: Nueva fecha
            new_booking_time: Nueva hora
            new_number_of_guests: Nuevo número de huéspedes
            
        Returns:
            str: Estado de la actualización
        """
        try:
            # Ejecutar procedimiento almacenado
            query = "CALL UpdateBooking(%s, %s, %s, %s, @update_status)"
            self.db_connection.execute_query(
                query, 
                (booking_id, new_booking_date, new_booking_time, new_number_of_guests)
            )
            
            # Obtener el resultado
            result = self.db_connection.execute_query(
                "SELECT @update_status AS update_status", 
                fetch=True
            )
            
            status = result[0]['update_status'] if result else "Error"
            self.logger.info(f"Actualización de reserva {booking_id}: {status}")
            return status
            
        except Exception as e:
            self.logger.error(f"Error en update_booking: {e}")
            return f"Error: {str(e)}"
    
    def add_booking(self, customer_id: int, table_id: int, booking_date: date,
                   booking_time: time, number_of_guests: int, 
                   special_requests: Optional[str] = None) -> str:
        """
        Añade una nueva reserva
        
        Args:
            customer_id: ID del cliente
            table_id: ID de la mesa
            booking_date: Fecha de la reserva
            booking_time: Hora de la reserva
            number_of_guests: Número de huéspedes
            special_requests: Solicitudes especiales
            
        Returns:
            str: Estado de la reserva
        """
        try:
            # Ejecutar procedimiento almacenado
            query = "CALL AddBooking(%s, %s, %s, %s, %s, %s, @booking_status)"
            self.db_connection.execute_query(
                query, 
                (customer_id, table_id, booking_date, booking_time, 
                 number_of_guests, special_requests)
            )
            
            # Obtener el resultado
            result = self.db_connection.execute_query(
                "SELECT @booking_status AS booking_status", 
                fetch=True
            )
            
            status = result[0]['booking_status'] if result else "Error"
            self.logger.info(f"Nueva reserva: {status}")
            return status
            
        except Exception as e:
            self.logger.error(f"Error en add_booking: {e}")
            return f"Error: {str(e)}"
    
    def cancel_booking(self, booking_id: int) -> str:
        """
        Cancela una reserva existente
        
        Args:
            booking_id: ID de la reserva a cancelar
            
        Returns:
            str: Estado de la cancelación
        """
        try:
            # Ejecutar procedimiento almacenado
            query = "CALL CancelBooking(%s, @cancellation_status)"
            self.db_connection.execute_query(query, (booking_id,))
            
            # Obtener el resultado
            result = self.db_connection.execute_query(
                "SELECT @cancellation_status AS cancellation_status", 
                fetch=True
            )
            
            status = result[0]['cancellation_status'] if result else "Error"
            self.logger.info(f"Cancelación de reserva {booking_id}: {status}")
            return status
            
        except Exception as e:
            self.logger.error(f"Error en cancel_booking: {e}")
            return f"Error: {str(e)}"
    
    def check_booking_availability(self, check_date: date, check_time: time, 
                                 required_capacity: int) -> List[Dict]:
        """
        Verifica la disponibilidad de mesas
        
        Args:
            check_date: Fecha a verificar
            check_time: Hora a verificar
            required_capacity: Capacidad requerida
            
        Returns:
            List[Dict]: Lista de mesas disponibles
        """
        try:
            # Ejecutar procedimiento almacenado
            query = "CALL CheckBookingAvailability(%s, %s, %s)"
            result = self.db_connection.execute_query(
                query, 
                (check_date, check_time, required_capacity), 
                fetch=True
            )
            
            self.logger.info(f"Verificación de disponibilidad para {check_date} {check_time}: {len(result)} mesas")
            return result
            
        except Exception as e:
            self.logger.error(f"Error en check_booking_availability: {e}")
            return []
    
    def get_bookings_by_date(self, search_date: date) -> List[Dict]:
        """
        Obtiene todas las reservas para una fecha específica
        
        Args:
            search_date: Fecha a buscar
            
        Returns:
            List[Dict]: Lista de reservas
        """
        try:
            # Ejecutar procedimiento almacenado
            query = "CALL GetBookingsByDate(%s)"
            result = self.db_connection.execute_query(
                query, 
                (search_date,), 
                fetch=True
            )
            
            self.logger.info(f"Reservas para {search_date}: {len(result)} encontradas")
            return result
            
        except Exception as e:
            self.logger.error(f"Error en get_bookings_by_date: {e}")
            return []
    
    def get_customer_info(self, customer_id: int) -> Optional[Dict]:
        """
        Obtiene información de un cliente
        
        Args:
            customer_id: ID del cliente
            
        Returns:
            Dict: Información del cliente
        """
        try:
            query = """
            SELECT customer_id, first_name, last_name, email, phone, 
                   address, city, state, zip_code, created_at
            FROM customers 
            WHERE customer_id = %s
            """
            result = self.db_connection.execute_query(query, (customer_id,), fetch=True)
            
            if result:
                return result[0]
            return None
            
        except Exception as e:
            self.logger.error(f"Error en get_customer_info: {e}")
            return None
    
    def get_menu_items(self) -> List[Dict]:
        """
        Obtiene todos los elementos del menú
        
        Returns:
            List[Dict]: Lista de elementos del menú
        """
        try:
            query = """
            SELECT mi.menu_item_id, mi.item_name, mi.description, 
                   mi.price, mi.quantity_in_stock, mi.is_available,
                   mc.category_name
            FROM menu_items mi
            JOIN menu_categories mc ON mi.category_id = mc.category_id
            WHERE mi.is_available = TRUE
            ORDER BY mc.category_name, mi.item_name
            """
            result = self.db_connection.execute_query(query, fetch=True)
            return result
            
        except Exception as e:
            self.logger.error(f"Error en get_menu_items: {e}")
            return []
    
    def get_tables_info(self) -> List[Dict]:
        """
        Obtiene información de todas las mesas
        
        Returns:
            List[Dict]: Lista de mesas
        """
        try:
            query = """
            SELECT table_id, table_number, seating_capacity, 
                   location, is_available
            FROM tables
            ORDER BY table_number
            """
            result = self.db_connection.execute_query(query, fetch=True)
            return result
            
        except Exception as e:
            self.logger.error(f"Error en get_tables_info: {e}")
            return []
    
    def generate_daily_report(self, report_date: date) -> Dict[str, Any]:
        """
        Genera un reporte diario de reservas
        
        Args:
            report_date: Fecha del reporte
            
        Returns:
            Dict: Reporte con estadísticas
        """
        try:
            # Obtener reservas del día
            bookings = self.get_bookings_by_date(report_date)
            
            # Calcular estadísticas
            total_bookings = len(bookings)
            confirmed_bookings = len([b for b in bookings if b['status'] == 'confirmed'])
            cancelled_bookings = len([b for b in bookings if b['status'] == 'cancelled'])
            completed_bookings = len([b for b in bookings if b['status'] == 'completed'])
            
            # Obtener información de mesas
            tables_info = self.get_tables_info()
            total_tables = len(tables_info)
            tables_booked = len(set([b['table_number'] for b in bookings if b['status'] == 'confirmed']))
            
            report = {
                'date': report_date,
                'total_bookings': total_bookings,
                'confirmed_bookings': confirmed_bookings,
                'cancelled_bookings': cancelled_bookings,
                'completed_bookings': completed_bookings,
                'total_tables': total_tables,
                'tables_booked': tables_booked,
                'occupancy_rate': (tables_booked / total_tables * 100) if total_tables > 0 else 0,
                'bookings_detail': bookings
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error en generate_daily_report: {e}")
            return {}
    
    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self.db_connection:
            self.db_connection.close_pool()


def main():
    """Función principal para demostrar el uso del sistema"""
    print("=== Little Lemon Booking System ===")
    print("Database Engineer Capstone Project")
    print("=====================================\n")
    
    try:
        # Crear sistema de reservas
        booking_system = LittleLemonBookingSystem("local")
        print("✅ Sistema de reservas inicializado correctamente\n")
        
        # Demostrar funcionalidades
        
        # 1. GetMaxQuantity
        print("1. Prueba GetMaxQuantity:")
        max_qty = booking_system.get_max_quantity("Chicken Parmigiana")
        print(f"   Cantidad máxima de Chicken Parmigiana: {max_qty}\n")
        
        # 2. ManageBooking
        print("2. Prueba ManageBooking:")
        status = booking_system.manage_booking(date(2025, 7, 25), 1)
        print(f"   Estado de reserva mesa 1 para 2025-07-25: {status}\n")
        
        # 3. CheckBookingAvailability
        print("3. Verificar disponibilidad:")
        availability = booking_system.check_booking_availability(
            date(2025, 7, 25), time(19, 0), 4
        )
        print(f"   Mesas disponibles para 4 personas: {len(availability)}")
        for table in availability[:3]:  # Mostrar solo las primeras 3
            print(f"   - Mesa {table['table_number']}: {table['availability_status']}")
        print()
        
        # 4. AddBooking
        print("4. Prueba AddBooking:")
        new_booking_status = booking_system.add_booking(
            customer_id=1,
            table_id=1,
            booking_date=date(2025, 7, 25),
            booking_time=time(19, 0),
            number_of_guests=2,
            special_requests="Mesa junto a la ventana"
        )
        print(f"   Nueva reserva: {new_booking_status}\n")
        
        # 5. GetBookingsByDate
        print("5. Reservas para una fecha:")
        bookings_today = booking_system.get_bookings_by_date(date(2025, 7, 15))
        print(f"   Total reservas para 2025-07-15: {len(bookings_today)}")
        for booking in bookings_today[:2]:  # Mostrar solo las primeras 2
            print(f"   - {booking['customer_name']} - Mesa {booking['table_number']} a las {booking['booking_time']}")
        print()
        
        # 6. Reporte diario
        print("6. Reporte diario:")
        report = booking_system.generate_daily_report(date(2025, 7, 15))
        print(f"   Fecha: {report['date']}")
        print(f"   Total reservas: {report['total_bookings']}")
        print(f"   Reservas confirmadas: {report['confirmed_bookings']}")
        print(f"   Tasa de ocupación: {report['occupancy_rate']:.1f}%\n")
        
        # 7. Información del menú
        print("7. Elementos del menú:")
        menu_items = booking_system.get_menu_items()
        print(f"   Total elementos en el menú: {len(menu_items)}")
        for item in menu_items[:5]:  # Mostrar solo los primeros 5
            print(f"   - {item['item_name']}: ${item['price']:.2f} ({item['category_name']})")
        print()
        
        print("✅ Todas las funcionalidades probadas exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cerrar conexión
        if 'booking_system' in locals():
            booking_system.close_connection()
            print("\n🔒 Conexión cerrada correctamente")


if __name__ == "__main__":
    main()
