import os
from bson import ObjectId  
from flask import send_from_directory  
from flask import jsonify  
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 初始化应用
load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

# 配置上传
UPLOAD_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 常量定义
CATEGORIES = [
    '电子产品', '家具', '车辆', '服装', '书籍', '动漫', '其他'
]

# 表单定义
class AdForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    description = TextAreaField('描述', validators=[DataRequired()])
    price = FloatField('价格', validators=[DataRequired()])
    category = SelectField('分类', choices=[(c, c) for c in CATEGORIES])
    contact = StringField('联系方式', validators=[DataRequired()])

# 广告模型
class Ad:
    @staticmethod
    def create(title, description, price, category, image_path, contact):
        return {
            'title': title,
            'description': description,
            'price': float(price),
            'category': category,
            'image': image_path,
            'contact': contact,
            'created_at': datetime.now(),
            'views': 0
        }
    def delete(ad_id, user_id=None):
        query = {'_id': ObjectId(ad_id)}
        if user_id:  # 如果需要验证用户权限
            query['user_id'] = user_id
        result = mongo.db.ads.delete_one(query)
        return result.deleted_count > 0

# 辅助函数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 路由定义
@app.route('/')
def home():
    ads = mongo.db.ads.find().sort('created_at', -1).limit(20)
    return render_template('index.html', ads=ads, categories=CATEGORIES)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    search_filter = {}
    if query:
        search_filter['$or'] = [
            {'title': {'$regex': query, '$options': 'i'}},
            {'description': {'$regex': query, '$options': 'i'}}
        ]
    if category:
        search_filter['category'] = category
    
    ads = mongo.db.ads.find(search_filter).sort('created_at', -1)
    return render_template('index.html', ads=ads, categories=CATEGORIES)


@app.route('/ad/<ad_id>')
def view_ad(ad_id):
    try:
        # 使用bson.ObjectId转换字符串ID
        ad = mongo.db.ads.find_one_or_404({'_id': ObjectId(ad_id)})
        mongo.db.ads.update_one(
            {'_id': ObjectId(ad_id)},
            {'$inc': {'views': 1}}
        )
        return render_template('ad.html', ad=ad)
    except:
        flash('广告不存在或ID无效', 'danger')
        return redirect(url_for('home'))


@app.route('/create', methods=['GET', 'POST'])
def create_ad():
    form = AdForm()
    if form.validate_on_submit():
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                # 修正1：使用正斜杠保存路径
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                # 修正2：存储相对URL路径（使用正斜杠）
                image_path = f"images/{filename}"
        
        ad = Ad.create(
            form.title.data,
            form.description.data,
            form.price.data,
            form.category.data,
            image_path,  # 这里存储的是URL路径
            form.contact.data
        )
        mongo.db.ads.insert_one(ad)
        flash('广告创建成功!', 'success')
        return redirect(url_for('home'))
    
    return render_template('create.html', form=form)


@app.route('/delete/<ad_id>', methods=['POST'])
def delete_ad(ad_id):
    try:
        # 删除前先获取广告信息（用于删除关联图片）
        ad = mongo.db.ads.find_one({'_id': ObjectId(ad_id)})
        
        if ad:
            # 删除关联图片（如果存在）
            if ad.get('image'):
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                        os.path.basename(ad['image']))
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            # 从数据库删除广告
            mongo.db.ads.delete_one({'_id': ObjectId(ad_id)})
            flash('广告删除成功', 'success')
        else:
            flash('广告不存在', 'danger')
            
    except Exception as e:
        print(f"删除出错: {str(e)}")
        flash('删除广告时出错', 'danger')
    
    return redirect(url_for('home'))

@app.route('/stats')
def stats():
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    one_month_ago = today - timedelta(days=30)
    
    # 基础统计
    total_ads = mongo.db.ads.count_documents({})
    new_today = mongo.db.ads.count_documents({'created_at': {'$gte': today}})
    
    # 分类统计增强
    category_stats = list(mongo.db.ads.aggregate([
        {'$group': {
            '_id': '$category',
            'count': {'$sum': 1},
            'avg_price': {'$avg': '$price'},
            'max_price': {'$max': '$price'},
            'min_price': {'$min': '$price'}
        }},
        {'$sort': {'count': -1}}
    ]))
    
    # 价格分布
    price_distribution = {
        '0-100': mongo.db.ads.count_documents({'price': {'$lt': 100}}),
        '100-500': mongo.db.ads.count_documents({'price': {'$gte': 100, '$lt': 500}}),
        '500-1000': mongo.db.ads.count_documents({'price': {'$gte': 500, '$lt': 1000}}),
        '1000+': mongo.db.ads.count_documents({'price': {'$gte': 1000}})
    }
    
    # 7天趋势
    date_counts = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        next_date = date + timedelta(days=1)
        count = mongo.db.ads.count_documents({
            'created_at': {'$gte': date, '$lt': next_date}
        })
        date_counts.append({
            'date': date.strftime('%m-%d'),
            'count': count
        })
    
    # 计算平均价格
    avg_price_result = mongo.db.ads.aggregate([
        {'$group': {'_id': None, 'avg': {'$avg': '$price'}}}
    ])
    avg_price = avg_price_result.next()['avg'] if total_ads > 0 else 0
    
    # 计算月增长率
    last_month_count = mongo.db.ads.count_documents({
        'created_at': {'$gte': one_month_ago, '$lt': today}
    })
    prev_month_count = mongo.db.ads.count_documents({
        'created_at': {'$gte': one_month_ago - timedelta(days=30), '$lt': one_month_ago}
    })
    monthly_growth = round(((last_month_count - prev_month_count) / prev_month_count * 100), 2) if prev_month_count > 0 else 0
    
    # 活跃用户数（假设有用户集合）
    active_users = mongo.db.users.count_documents({
        'last_active': {'$gte': today - timedelta(days=7)}
    }) if 'users' in mongo.db.list_collection_names() else 0
    
    # 活跃广告数（假设有状态字段）
    active_ads = mongo.db.ads.count_documents({
        'status': 'active',
        'expires_at': {'$gte': now}
    }) if 'status' in mongo.db.ads.find_one({}, {'status': 1}) else total_ads
    
    # 总浏览量（假设有点击记录集合）
    if 'ad_views' in mongo.db.list_collection_names():
        total_views_result = mongo.db.ad_views.aggregate([
            {'$group': {'_id': None, 'total': {'$sum': '$count'}}}
        ])
        total_views = total_views_result.next()['total'] if total_views_result.alive else 0
    else:
        # 如果没有点击记录集合，使用广告浏览数字段求和
        total_views_result = mongo.db.ads.aggregate([
            {'$group': {'_id': None, 'total': {'$sum': '$views'}}}
        ]) if 'views' in mongo.db.ads.find_one({}, {'views': 1}) else None
        total_views = total_views_result.next()['total'] if total_views_result and total_views_result.alive else 0
    
    return render_template('stats.html',
                         now=now,
                         total_ads=total_ads,
                         new_today=new_today,
                         category_stats=category_stats,
                         price_distribution=price_distribution,
                         date_counts=date_counts,
                         avg_price=avg_price,
                         monthly_growth=monthly_growth,
                         active_users=active_users,
                         active_ads=active_ads,
                         total_views=total_views,
                         categories=category_stats)


@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
