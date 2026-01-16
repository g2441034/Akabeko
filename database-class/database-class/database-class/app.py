from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groupflow.db'
db = SQLAlchemy(app)

# モデル定義
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Task', backref='assignee', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=10) # 作業の重み
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# データベース初期化
with app.app_context():
    db.create_all()

# API: 貢献度データの取得 (可視化用)
@app.route('/api/contributions', methods=['GET'])
def get_contributions():
    users = User.query.all()
    data = []
    for user in users:
        # 完了したタスクのポイント合計を計算
        total_points = sum(t.points for t in user.tasks if t.is_completed)
        data.append({"name": user.name, "score": total_points})
    return jsonify(data)

# API: タスクの追加
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(title=data['title'], points=data['points'], user_id=data['user_id'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added"}), 201

if __name__ == '__main__':
    app.run(debug=True)