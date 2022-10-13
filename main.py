from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required

app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREATE DATABASE


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# Optional: But it will silence the deprecation warning in the console.
app .config['SECRET_KEY'] = 'random'
db.init_app(app)

# CREATE TABLE


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


with app.app_context():
    db.create_all()


class DangKy(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField("Đăng Kí")


class DangNhap(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField("Đăng Nhập")


@app.route('/')
def home():
    return render_template('langla.html')


@app.route('/dungsirong')
def dsr():
    return render_template('dsr.html')


@app.route('/dangky', methods=['GET', 'POST'])
def dangky():
    form = DangKy()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Tài khoản đã tồn tại !")
            return redirect(url_for('dangnhap'))
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home', name=user.username))
    return render_template('dangky.html', form=form)


@app.route('/dangnhap', methods=['GET', 'POST'])
def dangnhap():
    form = DangNhap()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        username = User.query.filter_by(email=email).first()
        if username and password == username.password:
            login_user(username)
            return redirect(url_for('home'))
        else:
            flash('Tài khoản hoặc mật khẩu sai !')

    return render_template('dangnhap.html', form=form)


@app.route('/dangxuat')
def dangxuat():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
