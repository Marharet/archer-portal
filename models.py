from app import db
from flask_login import UserMixin
from sqlalchemy.schema import CheckConstraint
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# спортсмен
class Athlete(UserMixin, db.Model):
    __tablename__ = 'athletes'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    password_hash = db.Column(db.String(256), nullable=False)  
    fio = db.Column(db.String(100), nullable=False) 
    start_date = db.Column(db.Date, default=datetime.now) 
    rank = db.Column(db.String(50)) 
    role = db.Column(db.String(10), default='Athlete') 
    
    # зв'язок з луками (один спортсмен до багатьох луків)
    bows = db.relationship('Bow', backref='owner', lazy='dynamic')
    
    def __repr__(self):
        return f'<Athlete {self.fio}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    

# лук
class Bow(db.Model):
    __tablename__ = 'bows'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)
    
    # FK до таблиці athletes 
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id'), nullable=False) 
    
    shoulders = db.Column(db.String(100))
    draw_weight = db.Column(db.Float)
    draw_length = db.Column(db.Float)
    
    # обмеження на модель лука 
    model = db.Column(db.String(50), nullable=False) 
    
    __table_args__ = (
        CheckConstraint(model.in_(['Hotr', 'WiaWis', 'WNS']), name='model_types'),
    )

    def __repr__(self):
        return f'<Bow {self.name} by {self.athlete_id}>'