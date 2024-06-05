from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='TheScott23',
        database='ta'
        )
    return connection

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
    except Exception as ex:
        print(ex)
        productos = []
    finally:
        if connection:
            connection.close()
    
    return render_template('productos.html', productos=productos)

@app.route('/empleados')
def empleados():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()
    except Exception as ex:
        print(ex)
        empleados = []
    finally:
        if connection:
            connection.close()
    
    return render_template('empleados.html', empleados=empleados)

@app.route('/categorias')
def categorias():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categorias_producto")
        categorias_producto = cursor.fetchall()
    except Exception as ex:
        print(ex)
        categorias_producto = []
    finally:
        if connection:
            connection.close()
    
    return render_template('categorias.html', categorias_producto=categorias_producto)

@app.route('/nuevo_empleado', methods=['GET', 'POST'])
def nuevo_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        salario = request.form['salario']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO empleados (nombre, apellido, edad, direccion, telefono, salario) VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, apellido, edad, direccion, telefono, salario)
            )
            connection.commit()
        except Exception as ex:
            print(ex)
        finally:
            if connection:
                connection.close()
        
        return redirect(url_for('empleados'))
    
    return render_template('nuevo_empleado.html')

if __name__ == '__main__':
    app.run(debug=True)
