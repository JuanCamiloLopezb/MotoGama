from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'moto_gama_alta_2024_secret'

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'concesionario.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db()
        schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Base de datos inicializada correctamente.")



@app.route('/')
def index():
    conn = get_db()
    total_vehiculos = conn.execute("SELECT COUNT(*) FROM vehiculos").fetchone()[0]
    disponibles = conn.execute("SELECT COUNT(*) FROM vehiculos WHERE estado='disponible'").fetchone()[0]
    vendidos = conn.execute("SELECT COUNT(*) FROM vehiculos WHERE estado='vendido'").fetchone()[0]
    total_clientes = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    total_ventas = conn.execute("SELECT COUNT(*) FROM ventas").fetchone()[0]
    ingresos = conn.execute("SELECT COALESCE(SUM(valor), 0) FROM ventas").fetchone()[0]
    ultimas_ventas = conn.execute("""
        SELECT v.id, c.nombre, vh.marca, vh.modelo, v.valor, v.fecha_venta
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id
        JOIN vehiculos vh ON v.id_vehiculo = vh.id
        ORDER BY v.created_at DESC LIMIT 5
    """).fetchall()
    conn.close()
    return render_template('index.html',
                           total_vehiculos=total_vehiculos,
                           disponibles=disponibles,
                           vendidos=vendidos,
                           total_clientes=total_clientes,
                           total_ventas=total_ventas,
                           ingresos=ingresos,
                           ultimas_ventas=ultimas_ventas)


@app.route('/vehiculos')
def vehiculos():
    conn = get_db()
    marca = request.args.get('marca', '')
    modelo = request.args.get('modelo', '')
    precio_min = request.args.get('precio_min', '')
    precio_max = request.args.get('precio_max', '')
    estado = request.args.get('estado', '')

    query = "SELECT * FROM vehiculos WHERE 1=1"
    params = []
    if marca:
        query += " AND marca LIKE ?"
        params.append(f'%{marca}%')
    if modelo:
        query += " AND modelo LIKE ?"
        params.append(f'%{modelo}%')
    if precio_min:
        query += " AND precio >= ?"
        params.append(float(precio_min))
    if precio_max:
        query += " AND precio <= ?"
        params.append(float(precio_max))
    if estado:
        query += " AND estado = ?"
        params.append(estado)
    query += " ORDER BY created_at DESC"

    lista = conn.execute(query, params).fetchall()
    marcas = conn.execute("SELECT DISTINCT marca FROM vehiculos ORDER BY marca").fetchall()
    conn.close()
    return render_template('vehiculos.html', vehiculos=lista, marcas=marcas,
                           filtros={'marca': marca, 'modelo': modelo, 'precio_min': precio_min,
                                    'precio_max': precio_max, 'estado': estado})


@app.route('/vehiculos/nuevo', methods=['GET', 'POST'])
def nuevo_vehiculo():
    if request.method == 'POST':
        try:
            conn = get_db()
            conn.execute("""
                INSERT INTO vehiculos (marca, modelo, precio, cilindraje, estado, color, anio)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                request.form['marca'],
                request.form['modelo'],
                float(request.form['precio']),
                int(request.form['cilindraje']),
                request.form.get('estado', 'disponible'),
                request.form.get('color', ''),
                request.form.get('anio', datetime.now().year)
            ))
            conn.commit()
            conn.close()
            flash('Motocicleta registrada exitosamente.', 'success')
            return redirect(url_for('vehiculos'))
        except Exception as e:
            flash(f'Error al registrar: {str(e)}', 'error')
    return render_template('vehiculo_form.html', vehiculo=None, titulo='Nueva Motocicleta')


@app.route('/vehiculos/editar/<int:id>', methods=['GET', 'POST'])
def editar_vehiculo(id):
    conn = get_db()
    vehiculo = conn.execute("SELECT * FROM vehiculos WHERE id=?", (id,)).fetchone()
    if not vehiculo:
        flash('Vehículo no encontrado.', 'error')
        return redirect(url_for('vehiculos'))
    if request.method == 'POST':
        try:
            conn.execute("""
                UPDATE vehiculos SET marca=?, modelo=?, precio=?, cilindraje=?, estado=?, color=?, anio=?
                WHERE id=?
            """, (
                request.form['marca'],
                request.form['modelo'],
                float(request.form['precio']),
                int(request.form['cilindraje']),
                request.form.get('estado', 'disponible'),
                request.form.get('color', ''),
                request.form.get('anio', datetime.now().year),
                id
            ))
            conn.commit()
            conn.close()
            flash('Motocicleta actualizada exitosamente.', 'success')
            return redirect(url_for('vehiculos'))
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    conn.close()
    return render_template('vehiculo_form.html', vehiculo=vehiculo, titulo='Editar Motocicleta')


@app.route('/vehiculos/eliminar/<int:id>', methods=['POST'])
def eliminar_vehiculo(id):
    conn = get_db()
    venta = conn.execute("SELECT id FROM ventas WHERE id_vehiculo=?", (id,)).fetchone()
    if venta:
        flash('No se puede eliminar: el vehículo tiene ventas asociadas.', 'error')
    else:
        conn.execute("DELETE FROM vehiculos WHERE id=?", (id,))
        conn.commit()
        flash('Motocicleta eliminada exitosamente.', 'success')
    conn.close()
    return redirect(url_for('vehiculos'))


@app.route('/clientes')
def clientes():
    conn = get_db()
    nombre = request.args.get('nombre', '')
    documento = request.args.get('documento', '')
    telefono = request.args.get('telefono', '')

    query = "SELECT * FROM clientes WHERE 1=1"
    params = []
    if nombre:
        query += " AND nombre LIKE ?"
        params.append(f'%{nombre}%')
    if documento:
        query += " AND documento LIKE ?"
        params.append(f'%{documento}%')
    if telefono:
        query += " AND telefono LIKE ?"
        params.append(f'%{telefono}%')
    query += " ORDER BY created_at DESC"

    lista = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('clientes.html', clientes=lista,
                           filtros={'nombre': nombre, 'documento': documento, 'telefono': telefono})


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        try:
            conn = get_db()
            conn.execute("""
                INSERT INTO clientes (nombre, documento, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?)
            """, (
                request.form['nombre'],
                request.form['documento'],
                request.form['telefono'],
                request.form.get('email', ''),
                request.form.get('direccion', '')
            ))
            conn.commit()
            conn.close()
            flash('Cliente registrado exitosamente.', 'success')
            return redirect(url_for('clientes'))
        except sqlite3.IntegrityError:
            flash('El documento ya está registrado.', 'error')
        except Exception as e:
            flash(f'Error al registrar: {str(e)}', 'error')
    return render_template('cliente_form.html', cliente=None, titulo='Nuevo Cliente')


@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    conn = get_db()
    cliente = conn.execute("SELECT * FROM clientes WHERE id=?", (id,)).fetchone()
    if not cliente:
        flash('Cliente no encontrado.', 'error')
        return redirect(url_for('clientes'))
    if request.method == 'POST':
        try:
            conn.execute("""
                UPDATE clientes SET nombre=?, documento=?, telefono=?, email=?, direccion=?
                WHERE id=?
            """, (
                request.form['nombre'],
                request.form['documento'],
                request.form['telefono'],
                request.form.get('email', ''),
                request.form.get('direccion', ''),
                id
            ))
            conn.commit()
            conn.close()
            flash('Cliente actualizado exitosamente.', 'success')
            return redirect(url_for('clientes'))
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'error')
    conn.close()
    return render_template('cliente_form.html', cliente=cliente, titulo='Editar Cliente')


@app.route('/clientes/eliminar/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    conn = get_db()
    venta = conn.execute("SELECT id FROM ventas WHERE id_cliente=?", (id,)).fetchone()
    if venta:
        flash('No se puede eliminar: el cliente tiene ventas asociadas.', 'error')
    else:
        conn.execute("DELETE FROM clientes WHERE id=?", (id,))
        conn.commit()
        flash('Cliente eliminado exitosamente.', 'success')
    conn.close()
    return redirect(url_for('clientes'))



@app.route('/ventas')
def ventas():
    conn = get_db()
    lista = conn.execute("""
        SELECT v.id, c.nombre AS cliente, c.documento, vh.marca, vh.modelo,
               v.fecha_venta, v.valor, v.notas
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id
        JOIN vehiculos vh ON v.id_vehiculo = vh.id
        ORDER BY v.fecha_venta DESC
    """).fetchall()
    conn.close()
    return render_template('ventas.html', ventas=lista)


@app.route('/ventas/nueva', methods=['GET', 'POST'])
def nueva_venta():
    conn = get_db()
    if request.method == 'POST':
        try:
            id_vehiculo = int(request.form['id_vehiculo'])
            vehiculo = conn.execute("SELECT * FROM vehiculos WHERE id=?", (id_vehiculo,)).fetchone()
            if not vehiculo or vehiculo['estado'] != 'disponible':
                flash('El vehículo no está disponible para la venta.', 'error')
            else:
                conn.execute("""
                    INSERT INTO ventas (id_cliente, id_vehiculo, fecha_venta, valor, notas)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    int(request.form['id_cliente']),
                    id_vehiculo,
                    request.form['fecha_venta'],
                    float(request.form['valor']),
                    request.form.get('notas', '')
                ))
                conn.execute("UPDATE vehiculos SET estado='vendido' WHERE id=?", (id_vehiculo,))
                conn.commit()
                flash('Venta registrada exitosamente.', 'success')
                conn.close()
                return redirect(url_for('ventas'))
        except Exception as e:
            flash(f'Error al registrar venta: {str(e)}', 'error')

    clientes_list = conn.execute("SELECT id, nombre, documento FROM clientes ORDER BY nombre").fetchall()
    vehiculos_list = conn.execute(
        "SELECT id, marca, modelo, precio FROM vehiculos WHERE estado='disponible' ORDER BY marca"
    ).fetchall()
    conn.close()
    return render_template('venta_form.html', clientes=clientes_list,
                           vehiculos=vehiculos_list, hoy=datetime.now().strftime('%Y-%m-%d'))



@app.route('/reportes')
def reportes():
    conn = get_db()
    disponibles = conn.execute(
        "SELECT * FROM vehiculos WHERE estado='disponible' ORDER BY marca"
    ).fetchall()
    vendidos = conn.execute("""
        SELECT vh.*, v.fecha_venta, v.valor AS valor_venta, c.nombre AS comprador
        FROM vehiculos vh
        JOIN ventas v ON vh.id = v.id_vehiculo
        JOIN clientes c ON v.id_cliente = c.id
        WHERE vh.estado='vendido'
        ORDER BY v.fecha_venta DESC
    """).fetchall()
    historial = conn.execute("""
        SELECT v.id, c.nombre AS cliente, vh.marca, vh.modelo,
               v.fecha_venta, v.valor, v.notas
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id
        JOIN vehiculos vh ON v.id_vehiculo = vh.id
        ORDER BY v.fecha_venta DESC
    """).fetchall()
    total_ingresos = conn.execute("SELECT COALESCE(SUM(valor), 0) FROM ventas").fetchone()[0]
    ventas_por_marca = conn.execute("""
        SELECT vh.marca, COUNT(*) as cantidad, SUM(v.valor) as total
        FROM ventas v JOIN vehiculos vh ON v.id_vehiculo = vh.id
        GROUP BY vh.marca ORDER BY cantidad DESC
    """).fetchall()
    conn.close()
    return render_template('reportes.html',
                           disponibles=disponibles,
                           vendidos=vendidos,
                           historial=historial,
                           total_ingresos=total_ingresos,
                           ventas_por_marca=ventas_por_marca)


@app.route('/api/vehiculo/<int:id>')
def api_vehiculo(id):
    conn = get_db()
    v = conn.execute("SELECT * FROM vehiculos WHERE id=?", (id,)).fetchone()
    conn.close()
    if v:
        return jsonify(dict(v))
    return jsonify({'error': 'No encontrado'}), 404


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
