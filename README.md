# Little Lemon Database Capstone Project

## Descripción del Proyecto

Este proyecto implementa un sistema completo de gestión de reservas para el restaurante Little Lemon como parte del capstone final del programa Database Engineer. El sistema incluye diseño de base de datos, procedimientos almacenados, conexión Python, y análisis de datos con Tableau.

## Estructura del Proyecto

```
Little_Lemon_Database_Capstone/
├── database/
│   ├── schema/
│   │   ├── little_lemon_schema.sql          # Esquema completo de la base de datos
│   │   ├── stored_procedures.sql            # Procedimientos almacenados
│   │   └── sample_data.sql                  # Datos de ejemplo
│   ├── diagrams/
│   │   ├── er_diagram.png                   # Diagrama ER
│   │   └── database_design.png              # Diseño de base de datos
│   └── documentation/
│       └── database_design_doc.md           # Documentación del diseño
├── python/
│   ├── connection.py                        # Configuración de conexión
│   ├── booking_system.py                    # Sistema de reservas
│   ├── data_analysis.py                     # Análisis de datos
│   └── requirements.txt                     # Dependencias Python
├── tableau/
│   ├── Little_Lemon_Dashboard.twb           # Workbook de Tableau
│   ├── data_source.csv                      # Fuente de datos
│   └── dashboard_screenshots/               # Capturas de pantalla
├── screenshots/
│   ├── mysql_workbench/                     # Screenshots de MySQL Workbench
│   ├── python_execution/                    # Screenshots de Python
│   └── tableau_dashboards/                  # Screenshots de Tableau
└── README.md                                # Este archivo
```

## Requisitos del Sistema

- MySQL Server 8.0 o superior
- Python 3.8 o superior
- Tableau Desktop
- MySQL Workbench

## Funcionalidades Implementadas

### ✅ Base de Datos
- Esquema completo con tablas relacionadas
- Índices y constraints apropiados
- Datos de ejemplo para testing

### ✅ Procedimientos Almacenados
- `GetMaxQuantity()` - Obtiene la cantidad máxima de un elemento
- `ManageBooking()` - Gestiona reservas generales
- `UpdateBooking()` - Actualiza reservas existentes
- `AddBooking()` - Añade nuevas reservas
- `CancelBooking()` - Cancela reservas

### ✅ Conexión Python
- Pool de conexiones optimizado
- Manejo de errores robusto
- Interfaz para todos los procedimientos

### ✅ Análisis Tableau
- Dashboard ejecutivo
- Reportes de ventas
- Análisis de reservas

## Instalación y Configuración

### 1. Configurar MySQL
```sql
-- Ejecutar en MySQL Workbench
source database/schema/little_lemon_schema.sql;
source database/schema/stored_procedures.sql;
source database/schema/sample_data.sql;
```

### 2. Configurar Python
```bash
cd python
pip install -r requirements.txt
```

### 3. Ejecutar Sistema
```bash
python booking_system.py
```

## Criterios de Evaluación Cumplidos

- [x] GitHub repo creado exitosamente
- [x] Proyecto apropiado en GitHub repo
- [x] Diagrama ER mostrando conexiones entre tablas
- [x] GetMaxQuantity() procedimiento implementado
- [x] ManageBooking() procedimiento implementado
- [x] UpdateBooking() procedimiento implementado
- [x] AddBooking() procedimiento implementado
- [x] CancelBooking() procedimiento implementado

## Autor

[Tu Nombre]
Database Engineer Capstone - Meta/Coursera

## Fecha de Entrega

23 de Julio, 2025
