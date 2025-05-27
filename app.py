from flask import Flask, render_template, request, redirect, session
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'supersecret'

users = {'admin': 'admin123'}
products = []

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
        session['user'] = username
        return redirect('/dashboard')
    return render_template('login.html', error='Credenciales incorrectas')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    if 'user' not in session:
        return redirect('/')
    name = request.form['name']
    quantity = request.form['quantity']
    products.append({'name': name, 'quantity': quantity})
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
@app.route('/api/add_product', methods=['POST'])
def api_add_product():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')
    if name and quantity:
        products.append({'name': name, 'quantity': quantity})
        return jsonify({'status': 'success', 'message': 'Producto agregado vía API'}), 201
    else:
        return jsonify({'status': 'error', 'message': 'Faltan datos'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)

