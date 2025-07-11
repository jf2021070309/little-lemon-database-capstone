"""
Little Lemon Data Analysis Module
Database Engineer Capstone Project
Fecha: 10 de Julio, 2025
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
import logging

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from connection import create_database_connection

class LittleLemonDataAnalyzer:
    """Clase para análisis de datos de Little Lemon Restaurant"""
    
    def __init__(self, environment: str = "local"):
        """
        Inicializa el analizador de datos
        
        Args:
            environment: Entorno de trabajo
        """
        self.db_connection = create_database_connection(environment)
        self.logger = logging.getLogger(__name__)
        
        # Configurar estilo de gráficos
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Verificar conexión
        if not self.db_connection.test_connection():
            raise Exception("No se pudo conectar a la base de datos")
    
    def get_sales_data(self, start_date: Optional[date] = None, 
                      end_date: Optional[date] = None) -> pd.DataFrame:
        """
        Obtiene datos de ventas para análisis
        
        Args:
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)
            
        Returns:
            pd.DataFrame: DataFrame con datos de ventas
        """
        try:
            # Construir consulta base
            query = """
            SELECT 
                o.order_id,
                o.order_date,
                o.order_time,
                o.total_amount,
                o.order_status,
                o.payment_status,
                c.customer_id,
                CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                c.email AS customer_email,
                c.city AS customer_city,
                c.state AS customer_state,
                od.order_detail_id,
                od.quantity,
                od.unit_price,
                od.subtotal,
                mi.menu_item_id,
                mi.item_name,
                mi.description AS item_description,
                mi.cost AS item_cost,
                mc.category_id,
                mc.category_name,
                b.booking_id,
                b.table_id,
                t.table_number,
                t.seating_capacity,
                t.location AS table_location
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN order_details od ON o.order_id = od.order_id
            JOIN menu_items mi ON od.menu_item_id = mi.menu_item_id
            JOIN menu_categories mc ON mi.category_id = mc.category_id
            LEFT JOIN bookings b ON o.booking_id = b.booking_id
            LEFT JOIN tables t ON b.table_id = t.table_id
            """
            
            # Agregar filtros de fecha si se proporcionan
            params = []
            if start_date or end_date:
                query += " WHERE "
                conditions = []
                
                if start_date:
                    conditions.append("o.order_date >= %s")
                    params.append(start_date)
                
                if end_date:
                    conditions.append("o.order_date <= %s")
                    params.append(end_date)
                
                query += " AND ".join(conditions)
            
            query += " ORDER BY o.order_date DESC, o.order_time DESC"
            
            # Ejecutar consulta
            result = self.db_connection.execute_query(query, tuple(params), fetch=True)
            
            # Convertir a DataFrame
            df = pd.DataFrame(result)
            
            if not df.empty:
                # Convertir tipos de datos
                df['order_date'] = pd.to_datetime(df['order_date'])
                df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S').dt.time
                df['total_amount'] = pd.to_numeric(df['total_amount'])
                df['subtotal'] = pd.to_numeric(df['subtotal'])
                df['unit_price'] = pd.to_numeric(df['unit_price'])
                df['item_cost'] = pd.to_numeric(df['item_cost'])
                df['quantity'] = pd.to_numeric(df['quantity'])
                
                # Calcular métricas adicionales
                df['profit'] = df['subtotal'] - (df['item_cost'] * df['quantity'])
                df['hour'] = df['order_time'].apply(lambda x: x.hour)
                df['day_of_week'] = df['order_date'].dt.day_name()
                df['month'] = df['order_date'].dt.month
                df['month_name'] = df['order_date'].dt.month_name()
            
            self.logger.info(f"Datos de ventas obtenidos: {len(df)} registros")
            return df
            
        except Exception as e:
            self.logger.error(f"Error obteniendo datos de ventas: {e}")
            return pd.DataFrame()
    
    def get_booking_data(self, start_date: Optional[date] = None, 
                        end_date: Optional[date] = None) -> pd.DataFrame:
        """
        Obtiene datos de reservas para análisis
        
        Args:
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)
            
        Returns:
            pd.DataFrame: DataFrame con datos de reservas
        """
        try:
            query = """
            SELECT 
                b.booking_id,
                b.booking_date,
                b.booking_time,
                b.number_of_guests,
                b.status,
                b.special_requests,
                b.created_at,
                b.updated_at,
                c.customer_id,
                CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                c.email AS customer_email,
                c.city AS customer_city,
                c.state AS customer_state,
                t.table_id,
                t.table_number,
                t.seating_capacity,
                t.location AS table_location,
                e.employee_id,
                CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
                e.position AS employee_position
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN tables t ON b.table_id = t.table_id
            LEFT JOIN employees e ON b.employee_id = e.employee_id
            """
            
            # Agregar filtros de fecha si se proporcionan
            params = []
            if start_date or end_date:
                query += " WHERE "
                conditions = []
                
                if start_date:
                    conditions.append("b.booking_date >= %s")
                    params.append(start_date)
                
                if end_date:
                    conditions.append("b.booking_date <= %s")
                    params.append(end_date)
                
                query += " AND ".join(conditions)
            
            query += " ORDER BY b.booking_date DESC, b.booking_time DESC"
            
            # Ejecutar consulta
            result = self.db_connection.execute_query(query, tuple(params), fetch=True)
            
            # Convertir a DataFrame
            df = pd.DataFrame(result)
            
            if not df.empty:
                # Convertir tipos de datos
                df['booking_date'] = pd.to_datetime(df['booking_date'])
                df['booking_time'] = pd.to_datetime(df['booking_time'], format='%H:%M:%S').dt.time
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['updated_at'] = pd.to_datetime(df['updated_at'])
                df['number_of_guests'] = pd.to_numeric(df['number_of_guests'])
                df['seating_capacity'] = pd.to_numeric(df['seating_capacity'])
                
                # Calcular métricas adicionales
                df['hour'] = df['booking_time'].apply(lambda x: x.hour)
                df['day_of_week'] = df['booking_date'].dt.day_name()
                df['month'] = df['booking_date'].dt.month
                df['month_name'] = df['booking_date'].dt.month_name()
                df['capacity_utilization'] = df['number_of_guests'] / df['seating_capacity']
                
                # Días hasta la reserva (para reservas futuras)
                df['days_until_booking'] = (df['booking_date'] - pd.Timestamp.now()).dt.days
            
            self.logger.info(f"Datos de reservas obtenidos: {len(df)} registros")
            return df
            
        except Exception as e:
            self.logger.error(f"Error obteniendo datos de reservas: {e}")
            return pd.DataFrame()
    
    def analyze_sales_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analiza el rendimiento de ventas
        
        Args:
            df: DataFrame con datos de ventas
            
        Returns:
            Dict: Análisis de rendimiento
        """
        try:
            if df.empty:
                return {}
            
            analysis = {
                'total_revenue': df['total_amount'].sum(),
                'total_orders': df['order_id'].nunique(),
                'total_items_sold': df['quantity'].sum(),
                'average_order_value': df.groupby('order_id')['total_amount'].first().mean(),
                'total_profit': df['profit'].sum(),
                'profit_margin': (df['profit'].sum() / df['subtotal'].sum()) * 100,
                
                # Análisis por categoría
                'revenue_by_category': df.groupby('category_name')['subtotal'].sum().to_dict(),
                'quantity_by_category': df.groupby('category_name')['quantity'].sum().to_dict(),
                'profit_by_category': df.groupby('category_name')['profit'].sum().to_dict(),
                
                # Análisis temporal
                'revenue_by_month': df.groupby('month_name')['subtotal'].sum().to_dict(),
                'revenue_by_day_of_week': df.groupby('day_of_week')['subtotal'].sum().to_dict(),
                'revenue_by_hour': df.groupby('hour')['subtotal'].sum().to_dict(),
                
                # Top productos
                'top_selling_items': df.groupby('item_name')['quantity'].sum().sort_values(ascending=False).head(10).to_dict(),
                'top_revenue_items': df.groupby('item_name')['subtotal'].sum().sort_values(ascending=False).head(10).to_dict(),
                'most_profitable_items': df.groupby('item_name')['profit'].sum().sort_values(ascending=False).head(10).to_dict(),
                
                # Análisis de clientes
                'revenue_by_customer': df.groupby('customer_name')['subtotal'].sum().sort_values(ascending=False).head(10).to_dict(),
                'orders_by_customer': df.groupby('customer_name')['order_id'].nunique().sort_values(ascending=False).head(10).to_dict(),
                
                # Análisis de ubicaciones
                'revenue_by_location': df.groupby('table_location')['subtotal'].sum().to_dict(),
                'revenue_by_table_capacity': df.groupby('seating_capacity')['subtotal'].sum().to_dict(),
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error en análisis de ventas: {e}")
            return {}
    
    def analyze_booking_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analiza patrones de reservas
        
        Args:
            df: DataFrame con datos de reservas
            
        Returns:
            Dict: Análisis de patrones
        """
        try:
            if df.empty:
                return {}
            
            analysis = {
                'total_bookings': len(df),
                'confirmed_bookings': len(df[df['status'] == 'confirmed']),
                'cancelled_bookings': len(df[df['status'] == 'cancelled']),
                'completed_bookings': len(df[df['status'] == 'completed']),
                'cancellation_rate': (len(df[df['status'] == 'cancelled']) / len(df)) * 100,
                
                'average_party_size': df['number_of_guests'].mean(),
                'total_guests_served': df['number_of_guests'].sum(),
                'average_capacity_utilization': df['capacity_utilization'].mean(),
                
                # Análisis temporal
                'bookings_by_month': df.groupby('month_name').size().to_dict(),
                'bookings_by_day_of_week': df.groupby('day_of_week').size().to_dict(),
                'bookings_by_hour': df.groupby('hour').size().to_dict(),
                
                # Análisis de mesas
                'bookings_by_table_location': df.groupby('table_location').size().to_dict(),
                'bookings_by_table_capacity': df.groupby('seating_capacity').size().to_dict(),
                'most_requested_tables': df.groupby('table_number').size().sort_values(ascending=False).head(10).to_dict(),
                
                # Análisis de clientes
                'bookings_by_customer': df.groupby('customer_name').size().sort_values(ascending=False).head(10).to_dict(),
                'customers_by_city': df.groupby('customer_city').size().sort_values(ascending=False).head(10).to_dict(),
                
                # Análisis de empleados
                'bookings_by_employee': df.groupby('employee_name').size().sort_values(ascending=False).head(10).to_dict(),
                
                # Solicitudes especiales
                'bookings_with_special_requests': len(df[df['special_requests'].notna()]),
                'special_requests_rate': (len(df[df['special_requests'].notna()]) / len(df)) * 100,
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error en análisis de reservas: {e}")
            return {}
    
    def create_sales_visualizations(self, df: pd.DataFrame, save_path: str = "charts"):
        """
        Crea visualizaciones de ventas
        
        Args:
            df: DataFrame con datos de ventas
            save_path: Ruta donde guardar las gráficas
        """
        try:
            if df.empty:
                return
            
            # Crear directorio si no existe
            os.makedirs(save_path, exist_ok=True)
            
            # 1. Ventas por categoría
            plt.figure(figsize=(12, 8))
            category_sales = df.groupby('category_name')['subtotal'].sum().sort_values(ascending=False)
            
            plt.subplot(2, 2, 1)
            category_sales.plot(kind='bar', color='skyblue')
            plt.title('Ventas por Categoría')
            plt.xlabel('Categoría')
            plt.ylabel('Ventas ($)')
            plt.xticks(rotation=45)
            
            # 2. Ventas por día de la semana
            plt.subplot(2, 2, 2)
            day_sales = df.groupby('day_of_week')['subtotal'].sum()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_sales = day_sales.reindex(day_order)
            day_sales.plot(kind='line', marker='o', color='green')
            plt.title('Ventas por Día de la Semana')
            plt.xlabel('Día')
            plt.ylabel('Ventas ($)')
            plt.xticks(rotation=45)
            
            # 3. Top 10 productos más vendidos
            plt.subplot(2, 2, 3)
            top_items = df.groupby('item_name')['quantity'].sum().sort_values(ascending=False).head(10)
            top_items.plot(kind='barh', color='coral')
            plt.title('Top 10 Productos Más Vendidos')
            plt.xlabel('Cantidad')
            plt.ylabel('Producto')
            
            # 4. Ventas por hora
            plt.subplot(2, 2, 4)
            hour_sales = df.groupby('hour')['subtotal'].sum()
            hour_sales.plot(kind='bar', color='orange')
            plt.title('Ventas por Hora del Día')
            plt.xlabel('Hora')
            plt.ylabel('Ventas ($)')
            
            plt.tight_layout()
            plt.savefig(f"{save_path}/sales_analysis.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            # 5. Gráfico de dispersión: Precio vs Cantidad
            plt.figure(figsize=(10, 6))
            plt.scatter(df['unit_price'], df['quantity'], alpha=0.6, color='purple')
            plt.xlabel('Precio Unitario ($)')
            plt.ylabel('Cantidad')
            plt.title('Relación Precio vs Cantidad Vendida')
            plt.savefig(f"{save_path}/price_quantity_scatter.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Visualizaciones de ventas guardadas en {save_path}")
            
        except Exception as e:
            self.logger.error(f"Error creando visualizaciones: {e}")
    
    def create_booking_visualizations(self, df: pd.DataFrame, save_path: str = "charts"):
        """
        Crea visualizaciones de reservas
        
        Args:
            df: DataFrame con datos de reservas
            save_path: Ruta donde guardar las gráficas
        """
        try:
            if df.empty:
                return
            
            # Crear directorio si no existe
            os.makedirs(save_path, exist_ok=True)
            
            plt.figure(figsize=(12, 8))
            
            # 1. Estado de reservas
            plt.subplot(2, 2, 1)
            status_counts = df['status'].value_counts()
            plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%')
            plt.title('Distribución de Estados de Reserva')
            
            # 2. Reservas por día de la semana
            plt.subplot(2, 2, 2)
            day_bookings = df.groupby('day_of_week').size()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_bookings = day_bookings.reindex(day_order)
            day_bookings.plot(kind='bar', color='lightgreen')
            plt.title('Reservas por Día de la Semana')
            plt.xlabel('Día')
            plt.ylabel('Número de Reservas')
            plt.xticks(rotation=45)
            
            # 3. Utilización de capacidad
            plt.subplot(2, 2, 3)
            plt.hist(df['capacity_utilization'], bins=20, color='lightblue', alpha=0.7)
            plt.title('Distribución de Utilización de Capacidad')
            plt.xlabel('Utilización de Capacidad')
            plt.ylabel('Frecuencia')
            
            # 4. Reservas por hora
            plt.subplot(2, 2, 4)
            hour_bookings = df.groupby('hour').size()
            hour_bookings.plot(kind='bar', color='salmon')
            plt.title('Reservas por Hora del Día')
            plt.xlabel('Hora')
            plt.ylabel('Número de Reservas')
            
            plt.tight_layout()
            plt.savefig(f"{save_path}/booking_analysis.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Visualizaciones de reservas guardadas en {save_path}")
            
        except Exception as e:
            self.logger.error(f"Error creando visualizaciones de reservas: {e}")
    
    def export_data_for_tableau(self, output_path: str = "tableau_data"):
        """
        Exporta datos para uso en Tableau
        
        Args:
            output_path: Ruta donde exportar los datos
        """
        try:
            # Crear directorio si no existe
            os.makedirs(output_path, exist_ok=True)
            
            # Exportar datos de ventas
            sales_df = self.get_sales_data()
            if not sales_df.empty:
                sales_df.to_csv(f"{output_path}/little_lemon_sales_data.csv", index=False)
                self.logger.info(f"Datos de ventas exportados: {len(sales_df)} registros")
            
            # Exportar datos de reservas
            bookings_df = self.get_booking_data()
            if not bookings_df.empty:
                bookings_df.to_csv(f"{output_path}/little_lemon_bookings_data.csv", index=False)
                self.logger.info(f"Datos de reservas exportados: {len(bookings_df)} registros")
            
            # Exportar datos combinados para dashboard
            if not sales_df.empty and not bookings_df.empty:
                # Combinar datos por fecha
                combined_df = pd.merge(
                    sales_df.groupby('order_date').agg({
                        'total_amount': 'sum',
                        'order_id': 'nunique',
                        'quantity': 'sum'
                    }).reset_index(),
                    bookings_df.groupby('booking_date').agg({
                        'booking_id': 'count',
                        'number_of_guests': 'sum'
                    }).reset_index(),
                    left_on='order_date',
                    right_on='booking_date',
                    how='outer'
                )
                
                combined_df.to_csv(f"{output_path}/little_lemon_combined_data.csv", index=False)
                self.logger.info(f"Datos combinados exportados: {len(combined_df)} registros")
            
        except Exception as e:
            self.logger.error(f"Error exportando datos: {e}")
    
    def generate_comprehensive_report(self, output_path: str = "reports") -> Dict[str, Any]:
        """
        Genera un reporte completo de análisis
        
        Args:
            output_path: Ruta donde guardar el reporte
            
        Returns:
            Dict: Reporte completo
        """
        try:
            # Crear directorio si no existe
            os.makedirs(output_path, exist_ok=True)
            
            # Obtener datos
            sales_df = self.get_sales_data()
            bookings_df = self.get_booking_data()
            
            # Realizar análisis
            sales_analysis = self.analyze_sales_performance(sales_df)
            booking_analysis = self.analyze_booking_patterns(bookings_df)
            
            # Crear visualizaciones
            self.create_sales_visualizations(sales_df, f"{output_path}/charts")
            self.create_booking_visualizations(bookings_df, f"{output_path}/charts")
            
            # Exportar datos para Tableau
            self.export_data_for_tableau(f"{output_path}/tableau_data")
            
            # Compilar reporte
            report = {
                'generated_at': datetime.now().isoformat(),
                'sales_analysis': sales_analysis,
                'booking_analysis': booking_analysis,
                'data_summary': {
                    'total_sales_records': len(sales_df),
                    'total_booking_records': len(bookings_df),
                    'date_range': {
                        'sales_start': sales_df['order_date'].min().isoformat() if not sales_df.empty else None,
                        'sales_end': sales_df['order_date'].max().isoformat() if not sales_df.empty else None,
                        'bookings_start': bookings_df['booking_date'].min().isoformat() if not bookings_df.empty else None,
                        'bookings_end': bookings_df['booking_date'].max().isoformat() if not bookings_df.empty else None,
                    }
                }
            }
            
            # Guardar reporte en JSON
            import json
            with open(f"{output_path}/little_lemon_analysis_report.json", 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            self.logger.info(f"Reporte completo generado en {output_path}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generando reporte: {e}")
            return {}
    
    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self.db_connection:
            self.db_connection.close_pool()


def main():
    """Función principal para demostrar el análisis de datos"""
    print("=== Little Lemon Data Analysis ===")
    print("Database Engineer Capstone Project")
    print("===================================\n")
    
    try:
        # Crear analizador
        analyzer = LittleLemonDataAnalyzer("local")
        print("✅ Analizador de datos inicializado\n")
        
        # Generar reporte completo
        print("📊 Generando reporte completo...")
        report = analyzer.generate_comprehensive_report()
        
        if report:
            print("✅ Reporte generado exitosamente!")
            print(f"📈 Análisis de ventas completado")
            print(f"📅 Análisis de reservas completado")
            print(f"📊 Visualizaciones creadas")
            print(f"💾 Datos exportados para Tableau")
            
            # Mostrar resumen del reporte
            if 'sales_analysis' in report:
                sales = report['sales_analysis']
                print(f"\n📊 Resumen de Ventas:")
                print(f"   - Ingresos totales: ${sales.get('total_revenue', 0):,.2f}")
                print(f"   - Órdenes totales: {sales.get('total_orders', 0)}")
                print(f"   - Valor promedio de orden: ${sales.get('average_order_value', 0):,.2f}")
                print(f"   - Margen de ganancia: {sales.get('profit_margin', 0):.1f}%")
            
            if 'booking_analysis' in report:
                bookings = report['booking_analysis']
                print(f"\n📅 Resumen de Reservas:")
                print(f"   - Reservas totales: {bookings.get('total_bookings', 0)}")
                print(f"   - Tasa de cancelación: {bookings.get('cancellation_rate', 0):.1f}%")
                print(f"   - Tamaño promedio de grupo: {bookings.get('average_party_size', 0):.1f}")
                print(f"   - Utilización promedio de capacidad: {bookings.get('average_capacity_utilization', 0):.1f}")
        
        else:
            print("❌ Error generando reporte")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cerrar conexión
        if 'analyzer' in locals():
            analyzer.close_connection()
            print("\n🔒 Conexión cerrada correctamente")


if __name__ == "__main__":
    main()
