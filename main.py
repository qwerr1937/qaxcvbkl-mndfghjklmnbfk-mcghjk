from flask import Flask, redirect, render_template, url_for
from data import db_session
import flask
from data.articles import Article
from data.users import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qsxvp976awwkmjmwmocisdim8yn9cali'
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

class LoginForm(FlaskForm):
    name = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    name = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


@app.route("/article/<int:article_id>")
def article(article_id):
    session = db_session.create_session()
    article = session.query(Article).filter(Article.id == article_id).first()
    articles = session.query(Article)
    user = session.query(User).filter(User.id == article.user_id).first()
    i = -1
    j = -1
    le = 0
    for item in articles:
        le += 1
    with open(article.content, "r") as file:
        txt_st = file.readlines()
    return render_template("article.html", article=article, user=user, txt_st=txt_st, articles=articles, i=i, j=j, len=le)


@app.route("/")
@app.route("/main")
def main():
    id_zakr_st = 1
    id_zakr_st -= 1
    session = db_session.create_session()
    articles = session.query(Article)
    user = session.query(User).filter(User.id == articles[id_zakr_st - 1].user_id).first()
    users = session.query(User)
    return render_template("main.html", id_zakr_st=id_zakr_st, articles=articles, user=user, users=users)


@app.route("/genre")
def genre():
    session = db_session.create_session()
    articles = session.query(Article)
    users = session.query(User)
    return render_template("genre.html", articles=articles, users=users)


@app.route("/books")
def books():
    session = db_session.create_session()
    articles = session.query(Article)
    users = session.query(User)
    return render_template("books.html", articles=articles, users=users)


@app.route("/other")
def other():
    session = db_session.create_session()
    articles = session.query(Article)
    users = session.query(User)
    return render_template("other.html", articles=articles, users=users)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.name == form.name.data).first():
            return render_template('registration.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user1 = User(name=form.name.data)
        user1.set_password(form.password.data)
        session.add(user1)
        session.commit()
        return flask.redirect('/main')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

def main():
    db_session.global_init("db/blogs.sqlite")
    app.run()


if __name__ == '__main__':
    main()
