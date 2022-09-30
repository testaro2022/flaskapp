# # from flask import Flask
# from flask import Flask, request,redirect,render_template
# # from flask import Flask, jsonify, request, render_template,redirect
# import os
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# import pytz
# # import numpy as np
# # from PIL import Image
# # from google.cloud import storage
# # from google.cloud.storage import Blob
# # import inspect
# # import numpy as np
# # import cv2

# app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ramen.db'
# db_uri = 'mysql+pymysql://'+os.environ['RDS_USERNAME']+':' +os.environ['RDS_PASSWORD']+ '@' +os.environ['RDS_HOSTNAME']+ ':' +os.environ['RDS_PORT'] + '/' +os.environ['RDS_DB_NAME'] +'?charset=utf8'

# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# SAVE_DIR = "./images"

# class ramen(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     win = db.Column(db.Integer,nullable=False)
#     lose = db.Column(db.Integer,nullable=False)
#     title = db.Column(db.String(50), nullable=False)
#     # body = db.Column(db.String(500), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))


# @app.route('/create', methods=['GET', 'POST'])
# def create():
#     if request.method == "POST":
#         title = request.form.get('title')
#         # body = request.form.get('body')
#         # BlogArticleのインスタンスを作成
#         ramen_instance = ramen(title=title,win=1,lose=1)
#         db.session.add(ramen_instance)
#         db.session.commit()
#         # 画像関連
#         # upload_name=request.form.get('image')
#         if(request.files['image']):
#             file = request.files['image']
#             save_name = './static/images/'+ title + '.jpg'
#             file.save(save_name)
#             # file.save(os.path.join('./static/images', file.filename))
#         return redirect('/')
#     else:
#         return render_template('create.html')

# # ホーム画面にhtmlを読み込んでみる。
# # GET /
# @app.route('/',methods=['GET'])
# def home():
#     if request.method == 'GET':
#         # ramens_db = ramen.query.all()
#         # return render_template("index.html",ramens_db = ramens_db)
#         return render_template("index.html")
#     # ramens_db = ramen.query.all()
#     # return render_template("index.html",ranebs_db = ramens_db)

# @app.route('/delete/<int:id>', methods=['GET'])
# def delete(id):
#     # 引数idに一致するデータを取得する
#     ramens_instance = ramen.query.get(id)
#     db.session.delete(ramens_instance)
#     db.session.commit()
#     return redirect('/')

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     # 引数idに一致するデータを取得する
#     ramens_instance = ramen.query.get(id)
#     if request.method == "GET":
#         return render_template('update.html', ramens_instance=ramens_instance)
#     else:
#         ramens_instance.title = request.form.get('title')
#         # ramens_instance.body = request.form.get('body')
#         db.session.commit()
#         return redirect('/')

# if __name__ == "__main__":
#     app.run(debug=True)
