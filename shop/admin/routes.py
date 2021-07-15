from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import AddProducts, Brand, Category



@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for("login"))
    products = AddProducts.query.all()
    brands = Brand.query.order_by(Brand.id.desc()).all()
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/index.html', title="Admin Page", products=products, brands=brands,
                           categories=categories)


@app.route('/brand')
def brand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for("login"))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Brand Page', brands=brands)


@app.route('/category')
def category():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for("login"))

    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Category Page', categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        flash(f'Welcome {form.name.data}, Registration Successful!',"success")
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Registration Page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["email"] = form.email.data
            flash(f'Welcome, You are Logged in!', "success")
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Wrong email id or password! Please try again',"danger")
            return redirect(url_for('login'))
    return render_template('admin/login.html', form=form, title="Login Page")
