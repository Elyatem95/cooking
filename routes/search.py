from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from src.models.recipe import Recipe, Ingredient, db

# إنشاء blueprint للمسارات المتعلقة بالبحث عن الوصفات
search_bp = Blueprint('search', __name__)

@search_bp.route('/ingredient-search')
def ingredient_search():
    """عرض صفحة البحث عن الوصفات بناءً على المكونات"""
    # الحصول على جميع المكونات مصنفة حسب الفئة
    vegetables = Ingredient.query.filter_by(category='vegetables').all()
    meats = Ingredient.query.filter_by(category='meats').all()
    dairy = Ingredient.query.filter_by(category='dairy').all()
    legumes = Ingredient.query.filter_by(category='legumes').all()
    spices = Ingredient.query.filter_by(category='spices').all()
    
    return render_template('ingredient_search.html', 
                          vegetables=vegetables,
                          meats=meats,
                          dairy=dairy,
                          legumes=legumes,
                          spices=spices)

@search_bp.route('/search-results')
def search_results():
    """عرض نتائج البحث عن الوصفات بناءً على المكونات المختارة"""
    # الحصول على المكونات المختارة من الاستعلام
    selected_ingredients = request.args.getlist('ingredients')
    partial_match = request.args.get('partial_match', 'false') == 'true'
    sort_by = request.args.get('sort_by', 'match')  # match, time, difficulty, rating
    
    # تحويل المكونات المختارة إلى قائمة من المعرفات
    ingredient_ids = []
    for ingredient_id in selected_ingredients:
        try:
            ingredient_ids.append(int(ingredient_id))
        except ValueError:
            # تجاهل القيم غير الصالحة
            pass
    
    # الحصول على جميع الوصفات
    all_recipes = Recipe.query.all()
    
    # حساب نسبة التطابق لكل وصفة
    matching_recipes = []
    for recipe in all_recipes:
        match_percentage = recipe.match_ingredients(ingredient_ids, partial_match)
        if match_percentage > 0:  # إضافة الوصفة فقط إذا كان هناك تطابق
            matching_recipes.append({
                'recipe': recipe,
                'match_percentage': match_percentage
            })
    
    # ترتيب النتائج حسب المعيار المحدد
    if sort_by == 'match':
        matching_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)
    elif sort_by == 'time':
        matching_recipes.sort(key=lambda x: x['recipe'].total_time)
    elif sort_by == 'difficulty':
        # ترتيب حسب مستوى الصعوبة (سهل، متوسط، صعب)
        difficulty_order = {'سهل': 1, 'متوسط': 2, 'صعب': 3}
        matching_recipes.sort(key=lambda x: difficulty_order.get(x['recipe'].difficulty, 2))
    elif sort_by == 'rating':
        matching_recipes.sort(key=lambda x: x['recipe'].average_rating, reverse=True)
    
    # الحصول على المكونات المختارة للعرض
    selected_ingredients_objects = Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
    
    return render_template('search_results.html', 
                          matching_recipes=matching_recipes,
                          selected_ingredients=selected_ingredients_objects,
                          partial_match=partial_match,
                          sort_by=sort_by)

@search_bp.route('/api/ingredients')
def get_ingredients():
    """واجهة برمجية للحصول على جميع المكونات"""
    category = request.args.get('category')
    
    if category:
        ingredients = Ingredient.query.filter_by(category=category).all()
    else:
        ingredients = Ingredient.query.all()
    
    return jsonify([{
        'id': ingredient.id,
        'name': ingredient.name,
        'category': ingredient.category
    } for ingredient in ingredients])

@search_bp.route('/api/search')
def api_search():
    """واجهة برمجية للبحث عن الوصفات بناءً على المكونات"""
    ingredient_ids = request.args.getlist('ingredients')
    partial_match = request.args.get('partial_match', 'false') == 'true'
    
    # تحويل المكونات المختارة إلى قائمة من المعرفات
    ingredient_ids = [int(id) for id in ingredient_ids if id.isdigit()]
    
    # الحصول على جميع الوصفات
    all_recipes = Recipe.query.all()
    
    # حساب نسبة التطابق لكل وصفة
    matching_recipes = []
    for recipe in all_recipes:
        match_percentage = recipe.match_ingredients(ingredient_ids, partial_match)
        if match_percentage > 0:  # إضافة الوصفة فقط إذا كان هناك تطابق
            matching_recipes.append({
                'id': recipe.id,
                'name': recipe.name,
                'match_percentage': match_percentage,
                'preparation_time': recipe.preparation_time,
                'cooking_time': recipe.cooking_time,
                'difficulty': recipe.difficulty,
                'cuisine_type': recipe.cuisine_type,
                'image_url': recipe.image_url,
                'average_rating': recipe.average_rating
            })
    
    # ترتيب النتائج حسب نسبة التطابق
    matching_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    return jsonify(matching_recipes)
