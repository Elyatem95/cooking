from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from src.models.recipe import Recipe, Rating, Comment, db
from datetime import datetime

# إنشاء blueprint للمسارات المتعلقة بالتقييمات والتعليقات
ratings_bp = Blueprint('ratings', __name__)

@ratings_bp.route('/api/rate/<int:recipe_id>', methods=['POST'])
def rate_recipe(recipe_id):
    """إضافة تقييم جديد لوصفة"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # الحصول على بيانات التقييم من النموذج
    rating_value = request.form.get('rating', type=int)
    
    # التحقق من صحة التقييم
    if not rating_value or rating_value < 1 or rating_value > 5:
        return jsonify({'status': 'error', 'message': 'قيمة التقييم غير صالحة'}), 400
    
    # في الإصدار الحالي، نستخدم تقييمات بدون مستخدمين مسجلين
    # يمكن تحسين هذا لاحقاً بإضافة نظام تسجيل دخول
    
    # إنشاء تقييم جديد
    new_rating = Rating(
        recipe_id=recipe_id,
        value=rating_value,
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_rating)
    db.session.commit()
    
    # حساب متوسط التقييم الجديد
    avg_rating = recipe.average_rating
    
    return jsonify({
        'status': 'success',
        'message': 'تم إضافة التقييم بنجاح',
        'average_rating': avg_rating,
        'ratings_count': len(recipe.ratings)
    })

@ratings_bp.route('/api/comment/<int:recipe_id>', methods=['POST'])
def add_comment(recipe_id):
    """إضافة تعليق جديد لوصفة"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # الحصول على بيانات التعليق من النموذج
    comment_content = request.form.get('comment')
    
    # التحقق من صحة التعليق
    if not comment_content or len(comment_content.strip()) < 3:
        return jsonify({'status': 'error', 'message': 'محتوى التعليق غير صالح'}), 400
    
    # في الإصدار الحالي، نستخدم تعليقات بدون مستخدمين مسجلين
    # يمكن تحسين هذا لاحقاً بإضافة نظام تسجيل دخول
    
    # إنشاء تعليق جديد
    new_comment = Comment(
        recipe_id=recipe_id,
        content=comment_content,
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    # تحويل التعليق إلى تنسيق JSON
    comment_data = {
        'id': new_comment.id,
        'content': new_comment.content,
        'created_at': new_comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'user': 'زائر'  # في الإصدار الحالي، جميع التعليقات من زوار
    }
    
    return jsonify({
        'status': 'success',
        'message': 'تم إضافة التعليق بنجاح',
        'comment': comment_data,
        'comments_count': len(recipe.comments)
    })

@ratings_bp.route('/api/comments/<int:recipe_id>')
def get_comments(recipe_id):
    """الحصول على جميع تعليقات وصفة معينة"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # ترتيب التعليقات من الأحدث إلى الأقدم
    comments = Comment.query.filter_by(recipe_id=recipe_id).order_by(Comment.created_at.desc()).all()
    
    # تحويل التعليقات إلى تنسيق JSON
    comments_data = []
    for comment in comments:
        comments_data.append({
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'زائر' if not comment.user_id else comment.user.username
        })
    
    return jsonify({
        'status': 'success',
        'comments': comments_data,
        'comments_count': len(comments)
    })
