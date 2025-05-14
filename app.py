from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'  # Conexión a la base de datos
app.config['SECRET_KEY'] = 'secreto-seguro'

db = SQLAlchemy(app)

# Modelo
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Función para crear las tablas
def create_tables():
    with app.app_context():  # Aseguramos que el contexto de la app esté disponible
        db.create_all()

# Llamamos a la función directamente
create_tables()

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            return render_template('success.html', username=user.username)
        return 'Credenciales inválidas', 401
    return render_template('login.html')

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            return 'El usuario ya existe', 400
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=5001, debug=True)
