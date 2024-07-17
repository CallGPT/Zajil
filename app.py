from flask import Flask, request, jsonify, send_file, Blueprint, render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import random
from models.askAi import chat_with_ai
from models.generatVoice import generatVoice

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'FoodPhone'
app.config['API_URL'] = 'https://api.call-gpt.tech'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'audio')

db = SQLAlchemy(app)

admin = Blueprint('admin', __name__)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    is_voice = db.Column(db.Boolean, default=False)
    voice = db.Column(db.String(100))
    language = db.Column(db.String(100), nullable=False, default="ar")
    create_at = db.Column(db.DateTime, server_default=db.func.now())

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(100), nullable=False)
    order = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    create_at = db.Column(db.DateTime, server_default=db.func.now())

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.String(100), nullable=False)
    create_at = db.Column(db.DateTime, server_default=db.func.now())

def generate_random_id():
    return str(random.randint(1000000000, 9999999999))

def get_chat_history(chat_id):
    return Chat.query.filter_by(chat_id=chat_id).all()

def get_system_parameters(lang):
    with open(f"parameters{lang}.txt", "r", encoding='utf-8') as file:
        return file.read()

def process_chat(chat_id, text, language, is_voice=False,prodeucts=None):
    chat_history = get_chat_history(chat_id)
    parameters = get_system_parameters(language)
    parameters = f"""{parameters} \n\n {prodeucts}""" if prodeucts else parameters
    chat_history_content = [{"role": "system", "content": parameters}]
    chat_history_content += [{"role": chat.role, "content": chat.content} for chat in chat_history]
    chat_history_content.append({"role": "user", "content": text})
    
    response, chat_history_content = chat_with_ai(chat_history_content)
    text = text.replace(" اجب بتلخيص لا باستفاضة اقل من 3 جمل", "").replace("Answer in a summary not in detail less than 3 sentences", "")
    new_chat_user = Chat(chat_id=chat_id, role="user", content=text, language=language)
    new_chat_ai = Chat(chat_id=chat_id, role="system", content=response, is_voice=is_voice, voice=generate_random_id() if is_voice else None, language=language)
    
    db.session.add(new_chat_user)
    db.session.add(new_chat_ai)
    db.session.commit()
    
    return response, new_chat_ai.voice if is_voice else None
def make_menu():
    products = Product.query.all()
    menu = ""
    categories = db.session.query(Product.category).distinct().all()
    for category in categories:
        menu += f"{category[0]}:\n"
        for product in products:
            if product.category == category[0]:
                menu += f"{product.name} -{product.ingredients} -{product.price}\n"
    return menu

@app.route('/')
def index():
    return jsonify({"message": "Welcome to FoodPhone"})

@app.route('/api/v1/order/voice/<chat_id>', methods=['POST'])
def get_voice(chat_id):
    data = request.json
    language = request.headers.get('language')
    text = data['text'] + (" اجب بتلخيص لا باستفاضة اقل من 3 جمل" if language == "ar" else " Answer in a summary not in detail less than 3 sentences")
    menu = make_menu()
    response, filename = process_chat(chat_id, text, language, is_voice=True,prodeucts=menu)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.mp3")
    
    generatVoice(response, file_path, voice="Dan Dan" if language == "en" else None)
    
    return jsonify({"voiceLink": f"{app.config['API_URL']}/api/v1/voice/{filename}"})

@app.route('/api/v1/order/chat/<chat_id>', methods=['POST'])
def chat(chat_id):
    data = request.json
    language = request.headers.get('language')
    text = data['text'] + (" اجب بتلخيص لا باستفاضة اقل من 3 جمل" if language == "ar" else " Answer in a summary not in detail less than 3 sentences")
    
    response, _ = process_chat(chat_id, text, language,prodeucts=make_menu())
    
    return jsonify({"response": response})

@app.route('/api/v1/order/history/<chat_id>', methods=['GET'])
def history(chat_id):
    chat_history = get_chat_history(chat_id)
    
    if chat_history:
        chat_history_content = [{"role": chat.role, "content": chat.content} for chat in chat_history]
        return jsonify({"chat_history": chat_history_content})
    
    return jsonify({"chat_history": []})

@app.route('/api/v1/order/close/<chat_id>', methods=['GET'])
def close(chat_id):
    chat_history = get_chat_history(chat_id)
    
    if chat_history:
        chat_history_content = [{"role": chat.role, "content": chat.content} for chat in chat_history]
        ask = "استخرج الفاتوره للادمن بهاذا الشكل<price> -- <order> -- <location> ولا تكتب اي شيء اخر"
        chat_history_content.append({"role": "system", "content": ask})
        
        response, _ = chat_with_ai(chat_history_content)
        price, order, location = map(str.strip, response.split("--"))
        new_order = Order(chat_id=chat_id, order=order, status="pending", price=price, location=location)
        
        db.session.add(new_order)
        db.session.commit()
        
        return jsonify({"response": "order closed successfully"})
    
    return jsonify({"response": "no chat history"})

@app.route('/api/v1/voice/<voice_id>', methods=['GET'])
def get_voice_file(voice_id):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{voice_id}.mp3")
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='audio/mpeg')
    return jsonify({"error": "File not found"}), 404
@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    ingredients = request.form['ingredients']
    category = request.form['category']
    stock = request.form['stock']
    new_product = Product(name=name, price=price, ingredients=ingredients, category=category, stock=stock)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('admin.products'))

@admin.route("/")
def admin_index():
    allOrders = Order.query.all()
    ordersCount = Order.query.count()
    chatids = db.session.query(Chat.chat_id).distinct().count()
    messages = Chat.query.count()
    productsCount = Product.query.count()
    return render_template("index.html", allOrders=allOrders, ordersCount=ordersCount, chatids=chatids, tokens=messages, productsCount=productsCount)
@admin.route("/calls")
def calls():
    allCalls = Chat.query.all()
    return render_template("calls.html", allCalls=allCalls)
@admin.route("/products")
def products():
    allProducts = Product.query.all()
    return render_template("products.html", allProducts=allProducts)
app.register_blueprint(admin, url_prefix="/admin")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8000)