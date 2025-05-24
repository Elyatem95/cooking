from src.models.recipe import db, Ingredient, Recipe, PreparationStep, Rating, Comment
from datetime import datetime

def seed_ingredients():
    """إضافة المكونات الأساسية إلى قاعدة البيانات"""
    
    # الخضروات
    vegetables = [
        {'name': 'طماطم', 'category': 'vegetables'},
        {'name': 'خيار', 'category': 'vegetables'},
        {'name': 'بصل', 'category': 'vegetables'},
        {'name': 'ثوم', 'category': 'vegetables'},
        {'name': 'بطاطس', 'category': 'vegetables'},
        {'name': 'جزر', 'category': 'vegetables'},
        {'name': 'فلفل', 'category': 'vegetables'},
        {'name': 'باذنجان', 'category': 'vegetables'},
        {'name': 'كوسة', 'category': 'vegetables'},
        {'name': 'خس', 'category': 'vegetables'},
        {'name': 'سبانخ', 'category': 'vegetables'},
        {'name': 'ملوخية', 'category': 'vegetables'},
        {'name': 'بقدونس', 'category': 'vegetables'},
        {'name': 'كزبرة', 'category': 'vegetables'},
        {'name': 'نعناع', 'category': 'vegetables'},
    ]
    
    # اللحوم
    meats = [
        {'name': 'دجاج', 'category': 'meats'},
        {'name': 'لحم بقري', 'category': 'meats'},
        {'name': 'لحم ضأن', 'category': 'meats'},
        {'name': 'سمك', 'category': 'meats'},
        {'name': 'تونة', 'category': 'meats'},
        {'name': 'روبيان', 'category': 'meats'},
        {'name': 'لحم مفروم', 'category': 'meats'},
        {'name': 'نقانق', 'category': 'meats'},
    ]
    
    # منتجات الألبان
    dairy = [
        {'name': 'حليب', 'category': 'dairy'},
        {'name': 'زبادي', 'category': 'dairy'},
        {'name': 'جبن', 'category': 'dairy'},
        {'name': 'زبدة', 'category': 'dairy'},
        {'name': 'كريمة', 'category': 'dairy'},
        {'name': 'لبنة', 'category': 'dairy'},
    ]
    
    # البقوليات والحبوب
    legumes = [
        {'name': 'أرز', 'category': 'legumes'},
        {'name': 'معكرونة', 'category': 'legumes'},
        {'name': 'عدس', 'category': 'legumes'},
        {'name': 'حمص', 'category': 'legumes'},
        {'name': 'فاصوليا', 'category': 'legumes'},
        {'name': 'برغل', 'category': 'legumes'},
        {'name': 'كسكس', 'category': 'legumes'},
        {'name': 'فريكة', 'category': 'legumes'},
    ]
    
    # البهارات والتوابل
    spices = [
        {'name': 'ملح', 'category': 'spices'},
        {'name': 'فلفل أسود', 'category': 'spices'},
        {'name': 'كمون', 'category': 'spices'},
        {'name': 'كركم', 'category': 'spices'},
        {'name': 'قرفة', 'category': 'spices'},
        {'name': 'هيل', 'category': 'spices'},
        {'name': 'زعفران', 'category': 'spices'},
        {'name': 'بهارات مشكلة', 'category': 'spices'},
        {'name': 'بهارات كبسة', 'category': 'spices'},
        {'name': 'فلفل حار', 'category': 'spices'},
        {'name': 'زيت زيتون', 'category': 'spices'},
        {'name': 'زيت نباتي', 'category': 'spices'},
    ]
    
    # دمج جميع المكونات
    all_ingredients = vegetables + meats + dairy + legumes + spices
    
    # إضافة المكونات إلى قاعدة البيانات
    for ingredient_data in all_ingredients:
        # التحقق من وجود المكون
        existing = Ingredient.query.filter_by(name=ingredient_data['name']).first()
        if not existing:
            ingredient = Ingredient(**ingredient_data)
            db.session.add(ingredient)
    
    db.session.commit()
    print(f"تمت إضافة {len(all_ingredients)} مكون إلى قاعدة البيانات")


def seed_recipes():
    """إضافة مجموعة أولية من الوصفات إلى قاعدة البيانات"""
    
    # الحصول على المكونات من قاعدة البيانات
    ingredients = {ingredient.name: ingredient for ingredient in Ingredient.query.all()}
    
    # وصفات عربية
    arabic_recipes = [
        {
            'name': 'كبسة لحم',
            'description': 'الكبسة هي طبق سعودي تقليدي شهير في منطقة الخليج العربي، تتكون من الأرز واللحم المتبل بالبهارات العربية الأصيلة. تتميز بنكهتها الغنية ورائحتها الشهية، وتعتبر من أشهر الأطباق في المناسبات والولائم.',
            'preparation_time': 20,
            'cooking_time': 40,
            'servings': 4,
            'difficulty': 'متوسط',
            'cuisine_type': 'عربي',
            'cuisine_region': 'سعودي',
            'meal_type': 'غداء',
            'calories': 650,
            'image_url': 'images/kabsa.png',
            'ingredients': [
                ingredients['لحم ضأن'], ingredients['بصل'], ingredients['ثوم'], 
                ingredients['طماطم'], ingredients['جزر'], ingredients['قرفة'], 
                ingredients['هيل'], ingredients['فلفل أسود'], ingredients['ملح'], 
                ingredients['زيت نباتي'], ingredients['أرز'], ingredients['بهارات كبسة']
            ],
            'steps': [
                {'step_number': 1, 'description': 'في قدر كبير، سخني الزيت على نار متوسطة، ثم أضيفي البصل المفروم وقلبيه حتى يذبل.'},
                {'step_number': 2, 'description': 'أضيفي الثوم المهروس وقلبي لمدة دقيقة حتى تفوح رائحته.'},
                {'step_number': 3, 'description': 'أضيفي قطع اللحم وقلبيها حتى يتغير لونها من جميع الجهات.'},
                {'step_number': 4, 'description': 'أضيفي معجون الطماطم والطماطم المقطعة والجزر والبهارات (القرفة، الهيل، الفلفل الأسود) والملح.'},
                {'step_number': 5, 'description': 'أضيفي الماء الساخن حتى يغطي اللحم، ثم اتركيه على نار متوسطة حتى يغلي.'},
                {'step_number': 6, 'description': 'خففي النار، غطي القدر واتركيه لمدة 30-40 دقيقة حتى ينضج اللحم.'},
                {'step_number': 7, 'description': 'صفي مرق اللحم واحتفظي به جانباً.'},
                {'step_number': 8, 'description': 'في قدر كبير، ضعي الأرز المنقوع والمصفى، ثم أضيفي 5 أكواب من مرق اللحم وبهارات الكبسة.'},
                {'step_number': 9, 'description': 'اتركي الأرز على نار عالية حتى يغلي، ثم خففي النار وغطي القدر واتركيه لمدة 15-20 دقيقة حتى ينضج الأرز.'},
                {'step_number': 10, 'description': 'ضعي الأرز في طبق التقديم، ثم ضعي قطع اللحم فوقه.'},
                {'step_number': 11, 'description': 'قدميها ساخنة مع السلطة الخضراء واللبن الزبادي.'}
            ]
        },
        {
            'name': 'ملوخية',
            'description': 'الملوخية هي طبق مصري تقليدي يتكون من أوراق الملوخية المطبوخة مع مرق الدجاج أو اللحم، وتقدم مع الأرز أو الخبز. تتميز بقوامها اللزج ونكهتها المميزة.',
            'preparation_time': 15,
            'cooking_time': 30,
            'servings': 4,
            'difficulty': 'سهل',
            'cuisine_type': 'عربي',
            'cuisine_region': 'مصري',
            'meal_type': 'غداء',
            'calories': 450,
            'image_url': 'images/molokhia.png',
            'ingredients': [
                ingredients['ملوخية'], ingredients['دجاج'], ingredients['بصل'], 
                ingredients['ثوم'], ingredients['كزبرة'], ingredients['زيت نباتي'], 
                ingredients['ملح'], ingredients['فلفل أسود'], ingredients['أرز']
            ],
            'steps': [
                {'step_number': 1, 'description': 'اسلقي الدجاج مع البصل والملح والفلفل الأسود حتى ينضج.'},
                {'step_number': 2, 'description': 'اطحني أوراق الملوخية الجافة أو استخدمي الملوخية المجمدة المفرومة.'},
                {'step_number': 3, 'description': 'في قدر، سخني الزيت وأضيفي الثوم المهروس والكزبرة وقلبي حتى تفوح رائحتهما.'},
                {'step_number': 4, 'description': 'أضيفي الملوخية إلى مرق الدجاج واتركيها على نار هادئة لمدة 15-20 دقيقة.'},
                {'step_number': 5, 'description': 'قدمي الملوخية مع الأرز المطبوخ وقطع الدجاج.'}
            ]
        },
        {
            'name': 'فتوش',
            'description': 'الفتوش هو سلطة لبنانية تقليدية تتكون من الخضروات الطازجة وقطع الخبز المحمص، وتتميز بنكهة السماق والليمون وزيت الزيتون.',
            'preparation_time': 15,
            'cooking_time': 0,
            'servings': 4,
            'difficulty': 'سهل',
            'cuisine_type': 'عربي',
            'cuisine_region': 'لبناني',
            'meal_type': 'مقبلات',
            'calories': 250,
            'image_url': 'images/fattoush.png',
            'ingredients': [
                ingredients['خس'], ingredients['خيار'], ingredients['طماطم'], 
                ingredients['بصل'], ingredients['فلفل'], ingredients['بقدونس'], 
                ingredients['نعناع'], ingredients['زيت زيتون'], ingredients['ملح']
            ],
            'steps': [
                {'step_number': 1, 'description': 'قطعي الخضروات (الخس، الخيار، الطماطم، البصل، الفلفل) إلى قطع متوسطة الحجم.'},
                {'step_number': 2, 'description': 'أضيفي البقدونس والنعناع المفروم.'},
                {'step_number': 3, 'description': 'حمصي قطع الخبز في الفرن حتى تصبح مقرمشة.'},
                {'step_number': 4, 'description': 'اخلطي زيت الزيتون مع عصير الليمون والسماق والملح والفلفل الأسود.'},
                {'step_number': 5, 'description': 'أضيفي الصلصة إلى الخضروات وقلبي جيداً.'},
                {'step_number': 6, 'description': 'أضيفي قطع الخبز المحمص قبل التقديم مباشرة.'}
            ]
        },
        {
            'name': 'حمص',
            'description': 'الحمص هو طبق شامي شهير يتكون من حبوب الحمص المهروسة مع الطحينة وزيت الزيتون والليمون، ويقدم كمقبلات مع الخبز.',
            'preparation_time': 10,
            'cooking_time': 0,
            'servings': 4,
            'difficulty': 'سهل',
            'cuisine_type': 'عربي',
            'cuisine_region': 'شامي',
            'meal_type': 'مقبلات',
            'calories': 300,
            'image_url': 'images/hummus.png',
            'ingredients': [
                ingredients['حمص'], ingredients['ثوم'], ingredients['زيت زيتون'], 
                ingredients['ملح'], ingredients['كمون']
            ],
            'steps': [
                {'step_number': 1, 'description': 'انقعي حبوب الحمص في الماء لمدة 8 ساعات أو طوال الليل.'},
                {'step_number': 2, 'description': 'اسلقي حبوب الحمص حتى تنضج تماماً.'},
                {'step_number': 3, 'description': 'في محضر الطعام، اهرسي الحمص مع الثوم والطحينة وعصير الليمون والملح والكمون.'},
                {'step_number': 4, 'description': 'أضيفي القليل من ماء الحمص تدريجياً حتى تحصلي على القوام المطلوب.'},
                {'step_number': 5, 'description': 'ضعي الحمص في طبق التقديم وزينيه بزيت الزيتون والبقدونس المفروم.'}
            ]
        }
    ]
    
    # وصفات عالمية
    international_recipes = [
        {
            'name': 'باستا بصلصة الطماطم',
            'description': 'باستا سريعة التحضير مع صلصة الطماطم الطازجة والريحان، طبق إيطالي كلاسيكي سهل التحضير ولذيذ.',
            'preparation_time': 10,
            'cooking_time': 20,
            'servings': 4,
            'difficulty': 'سهل',
            'cuisine_type': 'عالمي',
            'cuisine_region': 'إيطالي',
            'meal_type': 'غداء',
            'calories': 450,
            'image_url': 'images/pasta.png',
            'ingredients': [
                ingredients['معكرونة'], ingredients['طماطم'], ingredients['بصل'], 
                ingredients['ثوم'], ingredients['زيت زيتون'], ingredients['ملح'], 
                ingredients['فلفل أسود']
            ],
            'steps': [
                {'step_number': 1, 'description': 'اسلقي المعكرونة في ماء مملح حتى تنضج.'},
                {'step_number': 2, 'description': 'في مقلاة، سخني زيت الزيتون وأضيفي البصل المفروم وقلبي حتى يذبل.'},
                {'step_number': 3, 'description': 'أضيفي الثوم المهروس وقلبي لمدة دقيقة.'},
                {'step_number': 4, 'description': 'أضيفي الطماطم المقطعة واتركيها على نار متوسطة لمدة 10 دقائق.'},
                {'step_number': 5, 'description': 'أضيفي الملح والفلفل الأسود والريحان.'},
                {'step_number': 6, 'description': 'صفي المعكرونة وأضيفيها إلى صلصة الطماطم وقلبي جيداً.'},
                {'step_number': 7, 'description': 'قدميها ساخنة مع جبن البارميزان المبشور.'}
            ]
        },
        {
            'name': 'كسكس مغربي',
            'description': 'طبق مغربي تقليدي من الكسكس مع الخضروات واللحم المطهو ببطء، يتميز بنكهة البهارات المغربية الغنية.',
            'preparation_time': 20,
            'cooking_time': 40,
            'servings': 6,
            'difficulty': 'متوسط',
            'cuisine_type': 'عالمي',
            'cuisine_region': 'مغربي',
            'meal_type': 'غداء',
            'calories': 550,
            'image_url': 'images/couscous.png',
            'ingredients': [
                ingredients['كسكس'], ingredients['لحم ضأن'], ingredients['بصل'], 
                ingredients['جزر'], ingredients['كوسة'], ingredients['طماطم'], 
                ingredients['ثوم'], ingredients['كمون'], ingredients['كركم'], 
                ingredients['فلفل أسود'], ingredients['ملح'], ingredients['زيت زيتون']
            ],
            'steps': [
                {'step_number': 1, 'description': 'في قدر كبير، سخني الزيت وأضيفي قطع اللحم وقلبيها حتى يتغير لونها.'},
                {'step_number': 2, 'description': 'أضيفي البصل المفروم والثوم وقلبي لمدة دقيقتين.'},
                {'step_number': 3, 'description': 'أضيفي البهارات (الكمون، الكركم، الفلفل الأسود، الملح) وقلبي.'},
                {'step_number': 4, 'description': 'أضيفي الطماطم المقطعة والماء واتركي المزيج يغلي.'},
                {'step_number': 5, 'description': 'خففي النار وأضيفي الجزر والكوسة واتركي المزيج على نار هادئة لمدة 30 دقيقة.'},
                {'step_number': 6, 'description': 'في وعاء آخر، حضري الكسكس حسب التعليمات على العبوة.'},
                {'step_number': 7, 'description': 'قدمي الكسكس مع اللحم والخضروات والمرق.'}
            ]
        },
        {
            'name': 'كاري دجاج',
            'description': 'طبق هندي غني بالتوابل والبهارات مع الدجاج والخضروات، يتميز بنكهته الحارة والغنية.',
            'preparation_time': 15,
            'cooking_time': 30,
            'servings': 4,
            'difficulty': 'متوسط',
            'cuisine_type': 'عالمي',
            'cuisine_region': 'هندي',
            'meal_type': 'عشاء',
            'calories': 500,
            'image_url': 'images/curry.png',
            'ingredients': [
                ingredients['دجاج'], ingredients['بصل'], ingredients['ثوم'], 
                ingredients['طماطم'], ingredients['فلفل'], ingredients['كركم'], 
                ingredients['كمون'], ingredients['فلفل حار'], ingredients['زيت نباتي'], 
                ingredients['ملح'], ingredients['كريمة']
            ],
            'steps': [
                {'step_number': 1, 'description': 'قطعي الدجاج إلى مكعبات متوسطة الحجم.'},
                {'step_number': 2, 'description': 'في قدر، سخني الزيت وأضيفي البصل المفروم وقلبي حتى يذبل.'},
                {'step_number': 3, 'description': 'أضيفي الثوم المهروس والزنجبيل وقلبي لمدة دقيقة.'},
                {'step_number': 4, 'description': 'أضيفي البهارات (الكركم، الكمون، الكزبرة، الفلفل الحار) وقلبي.'},
                {'step_number': 5, 'description': 'أضيفي قطع الدجاج وقلبيها حتى يتغير لونها من جميع الجهات.'},
                {'step_number': 6, 'description': 'أضيفي الطماطم المقطعة والفلفل واتركي المزيج على نار متوسطة لمدة 5 دقائق.'},
                {'step_number': 7, 'description': 'أضيفي الماء واتركي المزيج يغلي، ثم خففي النار واتركيه لمدة 15-20 دقيقة.'},
                {'step_number': 8, 'description': 'أضيفي الكريمة وقلبي برفق.'},
                {'step_number': 9, 'description': 'قدمي الكاري مع الأرز المطبوخ.'}
            ]
        }
    ]
    
    # دمج جميع الوصفات
    all_recipes = arabic_recipes + international_recipes
    
    # إضافة الوصفات إلى قاعدة البيانات
    for recipe_data in all_recipes:
        # استخراج المكونات وخطوات التحضير
        ingredients_list = recipe_data.pop('ingredients')
        steps_list = recipe_data.pop('steps')
        
        # التحقق من وجود الوصفة
        existing = Recipe.query.filter_by(name=recipe_data['name']).first()
        if not existing:
            # إنشاء وصفة جديدة
            recipe = Recipe(**recipe_data)
            
            # إضافة المكونات
            for ingredient in ingredients_list:
                recipe.ingredients.append(ingredient)
            
            # إضافة خطوات التحضير
            for step_data in steps_list:
                step = PreparationStep(**step_data, recipe=recipe)
                db.session.add(step)
            
            db.session.add(recipe)
    
    db.session.commit()
    print(f"تمت إضافة {len(all_recipes)} وصفة إلى قاعدة البيانات")


def seed_ratings_and_comments():
    """إضافة تقييمات وتعليقات وهمية للوصفات"""
    
    # الحصول على جميع الوصفات
    recipes = Recipe.query.all()
    
    # تقييمات وتعليقات وهمية
    ratings_data = [
        {'value': 5, 'created_at': datetime.utcnow()},
        {'value': 4, 'created_at': datetime.utcnow()},
        {'value': 5, 'created_at': datetime.utcnow()},
        {'value': 3, 'created_at': datetime.utcnow()},
        {'value': 4, 'created_at': datetime.utcnow()},
    ]
    
    comments_data = [
        {'content': 'وصفة رائعة! جربتها البارحة وكانت النتيجة مذهلة.', 'created_at': datetime.utcnow()},
        {'content': 'طعم لذيذ جداً، سأجربها مرة أخرى قريباً.', 'created_at': datetime.utcnow()},
        {'content': 'وصفة سهلة وسريعة، مناسبة للعشاء اليومي.', 'created_at': datetime.utcnow()},
        {'content': 'أضفت بعض البهارات الإضافية وكانت النتيجة رائعة.', 'created_at': datetime.utcnow()},
        {'content': 'من أفضل الوصفات التي جربتها، شكراً على المشاركة.', 'created_at': datetime.utcnow()},
    ]
    
    # إضافة تقييمات وتعليقات لكل وصفة
    for recipe in recipes:
        for rating_data in ratings_data:
            rating = Rating(**rating_data, recipe=recipe)
            db.session.add(rating)
        
        for comment_data in comments_data:
            comment = Comment(**comment_data, recipe=recipe)
            db.session.add(comment)
    
    db.session.commit()
    print(f"تمت إضافة {len(ratings_data) * len(recipes)} تقييم و {len(comments_data) * len(recipes)} تعليق إلى قاعدة البيانات")


def seed_database():
    """تهيئة قاعدة البيانات بالبيانات الأولية"""
    print("بدء تهيئة قاعدة البيانات...")
    
    # إنشاء الجداول
    db.create_all()
    
    # إضافة البيانات
    seed_ingredients()
    seed_recipes()
    seed_ratings_and_comments()
    
    print("تمت تهيئة قاعدة البيانات بنجاح!")


if __name__ == "__main__":
    seed_database()
