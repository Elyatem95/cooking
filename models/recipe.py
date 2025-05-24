from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# جدول العلاقة بين الوصفات والمكونات
recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
    db.Column('amount', db.String(50)),
    db.Column('unit', db.String(20)),
    db.Column('is_optional', db.Boolean, default=False)
)

class Recipe(db.Model):
    """نموذج الوصفة"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    preparation_time = db.Column(db.Integer)  # بالدقائق
    cooking_time = db.Column(db.Integer)  # بالدقائق
    servings = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))  # سهل، متوسط، صعب
    cuisine_type = db.Column(db.String(50))  # عربي، عالمي
    cuisine_region = db.Column(db.String(50))  # سعودي، مصري، إيطالي، إلخ
    meal_type = db.Column(db.String(20))  # فطور، غداء، عشاء، وجبة خفيفة
    calories = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients, lazy='subquery',
                                 backref=db.backref('recipes', lazy=True))
    steps = db.relationship('PreparationStep', backref='recipe', lazy=True, cascade="all, delete-orphan")
    ratings = db.relationship('Rating', backref='recipe', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='recipe', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Recipe {self.name}>'
    
    @property
    def average_rating(self):
        """حساب متوسط التقييم للوصفة"""
        if not self.ratings:
            return 0
        return sum(rating.value for rating in self.ratings) / len(self.ratings)
    
    @property
    def total_time(self):
        """حساب الوقت الإجمالي للتحضير والطهي"""
        return (self.preparation_time or 0) + (self.cooking_time or 0)
    
    def match_ingredients(self, user_ingredients, partial_match=False):
        """
        حساب نسبة تطابق المكونات المتوفرة لدى المستخدم مع مكونات الوصفة
        
        Args:
            user_ingredients: قائمة بمعرفات المكونات المتوفرة لدى المستخدم
            partial_match: ما إذا كان البحث بتطابق جزئي أم كامل
            
        Returns:
            نسبة التطابق كقيمة عشرية بين 0 و 1
        """
        recipe_ingredient_ids = [ingredient.id for ingredient in self.ingredients]
        
        # عدد المكونات المتطابقة
        matching_ingredients = set(user_ingredients).intersection(set(recipe_ingredient_ids))
        matching_count = len(matching_ingredients)
        
        # إذا كان البحث بتطابق كامل ولم تتطابق جميع مكونات الوصفة
        if not partial_match and matching_count < len(recipe_ingredient_ids):
            return 0
        
        # حساب نسبة التطابق
        if len(recipe_ingredient_ids) == 0:
            return 0
        
        return matching_count / len(recipe_ingredient_ids)


class Ingredient(db.Model):
    """نموذج المكون"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50))  # خضروات، لحوم، ألبان، بقوليات، إلخ
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'


class PreparationStep(db.Model):
    """نموذج خطوة التحضير"""
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<PreparationStep {self.step_number} for Recipe {self.recipe_id}>'


class Rating(db.Model):
    """نموذج التقييم"""
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    value = db.Column(db.Integer, nullable=False)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Rating {self.value} for Recipe {self.recipe_id}>'


class Comment(db.Model):
    """نموذج التعليق"""
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment for Recipe {self.recipe_id}>'


class User(db.Model):
    """نموذج المستخدم"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات
    ratings = db.relationship('Rating', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
