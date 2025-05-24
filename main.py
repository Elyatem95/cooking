import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from src.models.recipe import db, Recipe, Ingredient
from src.routes.search import search_bp
from src.routes.ratings import ratings_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'shen_natbekhlek_ya_salem_secret_key'

# تهيئة قاعدة البيانات
db.init_app(app)

# تسجيل blueprints
app.register_blueprint(search_bp)
app.register_blueprint(ratings_bp)

# دالة لتهيئة قاعدة البيانات
def initialize_database():
    """تهيئة قاعدة البيانات تلقائياً"""
    try:
        # التحقق من وجود الجداول باستخدام inspect
        with app.app_context():
            inspector = inspect(db.engine)
            if not inspector.has_table('recipe'):
                print("جداول قاعدة البيانات غير موجودة. جاري التهيئة...")
                from src.seed import seed_database
                db.create_all()
                seed_database()
                print("تم تهيئة قاعدة البيانات بنجاح!")
    except Exception as e:
        print(f"حدث خطأ أثناء تهيئة قاعدة البيانات: {str(e)}")

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    # الحصول على أحدث الوصفات
    latest_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
    
    # الحصول على أعلى الوصفات تقييماً
    top_rated_recipes = Recipe.query.all()
    top_rated_recipes.sort(key=lambda x: x.average_rating, reverse=True)
    top_rated_recipes = top_rated_recipes[:6]
    
    return render_template('index.html', 
                          latest_recipes=latest_recipes,
                          top_rated_recipes=top_rated_recipes)

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    """صفحة تفاصيل الوصفة"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # الحصول على وصفات مشابهة
    similar_recipes = Recipe.query.filter_by(cuisine_type=recipe.cuisine_type).filter(Recipe.id != recipe.id).limit(3).all()
    
    return render_template('recipe_details.html', recipe=recipe, similar_recipes=similar_recipes)

@app.route('/arabic-recipes')
def arabic_recipes():
    """صفحة أشهر الأكلات العربية"""
    recipes = Recipe.query.filter_by(cuisine_type='عربي').all()
    return render_template('arabic_recipes.html', recipes=recipes)

@app.route('/international-recipes')
def international_recipes():
    """صفحة أشهر الأكلات العالمية"""
    recipes = Recipe.query.filter_by(cuisine_type='عالمي').all()
    return render_template('international_recipes.html', recipes=recipes)

@app.route('/init-db')
def init_db():
    """تهيئة قاعدة البيانات"""
    from src.seed import seed_database
    with app.app_context():
        db.create_all()
        seed_database()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # تهيئة قاعدة البيانات قبل بدء التطبيق
    initialize_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
