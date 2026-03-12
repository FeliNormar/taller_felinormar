"""
Rutas para dashboard analítico

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Blueprint, render_template, request, session, jsonify
from datetime import date, timedelta
from app.models.database import get_db
from app.utils.decorators import login_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Página del dashboard"""
    return render_template(
        'dashboard.html',
        usuario=session['usuario'],
        rol=session['rol']
    )


@dashboard_bp.route('/api/dashboard')
@login_required
def api_dashboard():
    """API REST para datos del dashboard"""
    periodo = request.args.get('periodo', 'mes')
    conn = get_db()

    # Top 5 modelos
    top_modelos = conn.execute('''
        SELECT modelo, COUNT(*) as total
        FROM ordenes
        GROUP BY modelo
        ORDER BY total DESC
        LIMIT 5
    ''').fetchall()

    # Ingresos filtrados por período
    hoy = date.today()
    
    if periodo == 'semana':
        lunes = hoy - timedelta(days=hoy.weekday())
        desde = lunes.isoformat()
        query_fin = '''
            SELECT fecha_ingreso as periodo, SUM(costo_total) as ingreso
            FROM ordenes WHERE fecha_ingreso >= ? AND estatus='Entregado'
            GROUP BY fecha_ingreso ORDER BY fecha_ingreso
        '''
        params = (desde,)
    elif periodo == 'ano':
        desde = f'{hoy.year}-01-01'
        query_fin = '''
            SELECT strftime('%m', fecha_ingreso) as periodo, SUM(costo_total) as ingreso
            FROM ordenes WHERE fecha_ingreso >= ? AND estatus='Entregado'
            GROUP BY strftime('%m', fecha_ingreso) ORDER BY periodo
        '''
        params = (desde,)
    else:  # mes
        desde = f'{hoy.year}-{hoy.month:02d}-01'
        query_fin = '''
            SELECT fecha_ingreso as periodo, SUM(costo_total) as ingreso
            FROM ordenes WHERE fecha_ingreso >= ? AND estatus='Entregado'
            GROUP BY fecha_ingreso ORDER BY fecha_ingreso
        '''
        params = (desde,)

    ingresos = conn.execute(query_fin, params).fetchall()

    # Distribución por estatus
    estatus_rows = conn.execute('''
        SELECT estatus, COUNT(*) as total FROM ordenes GROUP BY estatus
    ''').fetchall()

    # Totales generales
    totales = conn.execute('''
        SELECT COUNT(*) as total_ordenes,
               SUM(CASE WHEN estatus='Entregado' THEN costo_total ELSE 0 END) as ingresos_total,
               SUM(CASE WHEN estatus NOT IN ('Entregado') THEN 1 ELSE 0 END) as pendientes
        FROM ordenes
    ''').fetchone()

    return jsonify({
        'top_modelos': [
            {'modelo': r['modelo'], 'total': r['total']} 
            for r in top_modelos
        ],
        'ingresos': [
            {'periodo': r['periodo'], 'ingreso': r['ingreso'] or 0} 
            for r in ingresos
        ],
        'estatus': [
            {'estatus': r['estatus'], 'total': r['total']} 
            for r in estatus_rows
        ],
        'totales': {
            'ordenes': totales['total_ordenes'] or 0,
            'ingresos': totales['ingresos_total'] or 0,
            'pendientes': totales['pendientes'] or 0,
        }
    })
