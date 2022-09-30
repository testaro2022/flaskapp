from crypt import methods
from flask import Flask, request,redirect,render_template,jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
import pytz


application = Flask(__name__)


db_uri = 'mysql+pymysql://'+os.environ['RDS_USERNAME']+':' +os.environ['RDS_PASSWORD']+ '@' +os.environ['RDS_HOSTNAME']+ ':' +os.environ['RDS_PORT'] + '/' +os.environ['RDS_DB_NAME'] +'?charset=utf8'
application.config['SQLALCHEMY_DATABASE_URI'] = db_uri
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JSON_AS_ASCII'] = False 
db = SQLAlchemy(application)
SAVE_DIR = "./images"

class ramen(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    win = db.Column(db.Integer,nullable=False)
    lose = db.Column(db.Integer,nullable=False)
    title = db.Column(db.String(50), nullable=False)
    # body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))


# EB looks for an 'application' callable by default.

@application.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        newtitle = request.form.get('title')
        # body = request.form.get('body')
        # BlogArticleのインスタンスを作成
        ramen_instance = ramen(title=newtitle,win=1,lose=1)
        db.session.add(ramen_instance)
        db.session.commit()
        # 画像関連
        upload_name=request.form.get('image')
        if(request.files['image']):
            file = request.files['image']
            save_name = './static/images/'+ newtitle + '.jpg'
            file.save(save_name)
            file.save(os.path.join('./static/images', file.filename))
        return redirect('/')
    else:
        return render_template('create.html')


@application.route('/',methods=['GET'])
def home():
    if request.method == 'GET':
        ramens_db = ramen.query.all()
        return render_template("index.html",ramens_db = ramens_db)
    # return render_template("index.html",ranebs_db = ramens_db)

@application.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    # 引数idに一致するデータを取得する
    ramens_instance = ramen.query.get(id)
    db.session.delete(ramens_instance)
    db.session.commit()
    return redirect('/')

@application.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # 引数idに一致するデータを取得する
    ramens_instance = ramen.query.get(id)
    if request.method == "GET":
        return render_template('update.html', ramens_instance=ramens_instance)
    else:
        # 上でインスタンス化したblogarticleのプロパティを更新する
        ramens_instance.title = request.form.get('title')
        # ramens_instance.body = request.form.get('body')
        # 更新する場合は、add()は不要でcommit()だけでよい
        db.session.commit()
        return redirect('/')

@application.route('/getjson/<int:id>',methods=['GET', 'POST'])
def getjson(id):
    ramens_instance = ramen.query.get(id)
    if request.method == "GET":
        #jsonにして返す
        id = ramens_instance.id
        win = ramens_instance.win
        lose = ramens_instance.lose
        title = ramens_instance.title        
        info = {'id':id,'win':win,'lose':lose,'title':title}
        return jsonify(info)
    # else:
    #     return redirect('/')

@application.route('/updatewin/<int:id>', methods=['GET', 'POST'])
def updatewin(id):
    # 引数idに一致するデータを取得する
    ramens_instance = ramen.query.get(id)
    ramens_instance_id = ramens_instance.id
    if request.method == "GET":
        ramen_update = db.session.query(ramen).filter(ramen.id==ramens_instance_id).first()
        ramen_update.win += 1 
        db.session.commit()
        return redirect('/')

@application.route('/updatelose/<int:id>', methods=['GET', 'POST'])
def updatelose(id):
    # 引数idに一致するデータを取得する
    ramens_instance = ramen.query.get(id)
    ramens_instance_id = ramens_instance.id
    if request.method == "GET":
        ramen_update = db.session.query(ramen).filter(ramen.id==ramens_instance_id).first()
        ramen_update.lose += 1 
        db.session.commit()
        return redirect('/')
    
@application.route('/ranking',methods=['GET'])
def ranking():
    ranking = db.session.query(ramen).order_by(desc(ramen.win)).all()
    # print(ranking)
    info = {}
    for i in range(5):
        info["rank"+str(i) ] = ranking[i].title
    # return render_template('ranking.html',ranking=ranking)
    return jsonify(info)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()