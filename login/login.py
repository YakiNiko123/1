import hashlib
import mysql.connector
from flask import Flask, request, redirect, session, render_template
from flask_jwt_extended import JWTManager, create_access_token
from email.message import EmailMessage
import ssl
import smtplib
import os

programa = Flask(__name__)
# Configura la clave secreta para JWT (debe ser segura en un entorno real)
programa.config['SECRET_KEY'] = os.urandom(24)

# Configura el JWT Manager
jwt = JWTManager(programa)

# MySQL Connector
conexion = mysql.connector.connect(user='root', password='', host='localhost', database='bcap')
cursor = conexion.cursor()

@programa.route('/')
def index():
    return render_template('login.html')

@programa.route('/recuperar')
def boton_recuperar():
    return render_template('recuperar.html')

@programa.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo_enviado']
        contrasena = request.form['contrasena']
        hashed_contrasena = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()
        consulta = f"SELECT contrasena FROM instructor WHERE correo_electronico='{correo}'"
        
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        conexion.commit()
        
        print(hashed_contrasena)
        
        if resultado:
            if resultado[0][0] == hashed_contrasena:

                session['logueado'] = True
                return render_template('recuperar.html')
            else:
                return render_template('login.html', error2='Contraseña incorrecta')
        else:
            return render_template('login.html', error1='Email incorrecto')



if __name__ == "__main__":
    programa.run(debug=True, host='0.0.0.0', port='5000')
