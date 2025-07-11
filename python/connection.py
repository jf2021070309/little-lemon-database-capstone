"""
Little Lemon Database Connection Module
Database Engineer Capstone Project
Fecha: 10 de Julio, 2025
"""

import mysql.connector
from mysql.connector import pooling, Error
import logging
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('little_lemon.log'),
        logging.StreamHandler()
    ]
)

class LittleLemonConnection:
    """Clase para manejar la conexión a la base de datos Little Lemon"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa la conexión con pool de conexiones
        
        Args:
            config: Diccionario con configuración de la base de datos
        """
        self.config = config
        self.pool = None
        self.create_connection_pool()
    
    def create_connection_pool(self):
        """Crea un pool de conexiones para optimizar el rendimiento"""
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="little_lemon_pool",
                pool_size=5,
                pool_reset_session=True,
                **self.config
            )
            logging.info("Pool de conexiones creado exitosamente")
        except Error as e:
            logging.error(f"Error al crear pool de conexiones: {e}")
            raise
    
    def get_connection(self):
        """
        Obtiene una conexión del pool
        
        Returns:
            Connection: Conexión MySQL
        """
        try:
            return self.pool.get_connection()
        except Error as e:
            logging.error(f"Error al obtener conexión: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """
        Ejecuta una consulta SQL
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta
            fetch: Si debe retornar resultados
            
        Returns:
            Resultados de la consulta si fetch=True, sino None
        """
        connection = None
        cursor = None
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                results = cursor.fetchall()
                return results
            else:
                connection.commit()
                return cursor.rowcount
                
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error ejecutando consulta: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def execute_procedure(self, procedure_name: str, params: list = None):
        """
        Ejecuta un procedimiento almacenado
        
        Args:
            procedure_name: Nombre del procedimiento
            params: Lista de parámetros para el procedimiento
            
        Returns:
            Resultados del procedimiento
        """
        connection = None
        cursor = None
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.callproc(procedure_name, params)
            else:
                cursor.callproc(procedure_name)
            
            # Obtener resultados
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            
            # Obtener parámetros de salida si existen
            cursor.execute("SELECT @_" + procedure_name + "_0, @_" + procedure_name + "_1, @_" + procedure_name + "_2")
            out_params = cursor.fetchone()
            
            connection.commit()
            return results, out_params
            
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error ejecutando procedimiento {procedure_name}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def test_connection(self):
        """
        Prueba la conexión a la base de datos
        
        Returns:
            bool: True si la conexión es exitosa
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            logging.info("Conexión a la base de datos exitosa")
            return True
        except Error as e:
            logging.error(f"Error de conexión: {e}")
            return False
    
    def close_pool(self):
        """Cierra el pool de conexiones"""
        if self.pool:
            self.pool.close()
            logging.info("Pool de conexiones cerrado")


def get_database_config(environment: str = "local") -> Dict[str, Any]:
    """
    Obtiene la configuración de la base de datos según el entorno
    
    Args:
        environment: Entorno de trabajo (local, development, production)
        
    Returns:
        Dict con configuración de la base de datos
    """
    configurations = {
        "local": {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "LittleLemon2024!",
            "database": "little_lemon_db",
            "charset": "utf8mb4",
            "use_unicode": True,
            "autocommit": False
        },
        "development": {
            "host": "localhost",
            "port": 3306,
            "user": "app_user",
            "password": "app_secure_pass",
            "database": "little_lemon_db",
            "charset": "utf8mb4",
            "use_unicode": True,
            "autocommit": False
        },
        "production": {
            "host": "localhost",
            "port": 3306,
            "user": "app_user",
            "password": "app_secure_pass",
            "database": "little_lemon_db",
            "charset": "utf8mb4",
            "use_unicode": True,
            "autocommit": False,
            "ssl_disabled": False
        }
    }
    
    return configurations.get(environment, configurations["local"])


def create_database_connection(environment: str = "local") -> LittleLemonConnection:
    """
    Crea una instancia de conexión a la base de datos
    
    Args:
        environment: Entorno de trabajo
        
    Returns:
        LittleLemonConnection: Instancia de conexión
    """
    config = get_database_config(environment)
    return LittleLemonConnection(config)


if __name__ == "__main__":
    # Test de la conexión
    print("Probando conexión a la base de datos Little Lemon...")
    
    try:
        # Crear conexión
        db_connection = create_database_connection("local")
        
        # Probar conexión
        if db_connection.test_connection():
            print("✅ Conexión exitosa a la base de datos")
            
            # Prueba básica de consulta
            result = db_connection.execute_query(
                "SELECT COUNT(*) as total_customers FROM customers", 
                fetch=True
            )
            print(f"Total de clientes en la base de datos: {result[0]['total_customers']}")
            
            # Prueba de procedimiento almacenado
            try:
                results, out_params = db_connection.execute_procedure("GetMaxQuantity", ["Chicken Parmigiana"])
                print(f"Procedimiento GetMaxQuantity ejecutado exitosamente")
            except Exception as e:
                print(f"Error ejecutando procedimiento: {e}")
            
        else:
            print("❌ Error en la conexión a la base de datos")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cerrar conexión
        if 'db_connection' in locals():
            db_connection.close_pool()
            print("Conexión cerrada")
