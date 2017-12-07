# Specifies the presentation of the user pages, forms, depending on the request.

from flask import render_template, request, jsonify, flash, redirect, session, url_for, json, g
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db, lm
from werkzeug.utils import secure_filename
import os
# import re
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

from .forms import *
from .models import *

@lm.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.cart = Orders.query.filter_by(id_user = g.user.id, order_status = IN_CART).all()
        g.count = Orders.query.filter_by(id_user = g.user.id, order_status = IN_CART).count()
        g.id_other = Orders.query.filter_by(id_user = g.user.id, order_status = IN_CART).all()
        g.prod = Products.query.filter_by().all()
        g.car = []
        sum = 0
        for i in range(len(g.id_other)):
            add = Products.query.filter_by(id = g.id_other[i].id_product).first()
            if add is not None:
                g.car.append(add)
                sum = sum + add.cost
        g.costs = int(sum)

def usd(value):
    """Formats value as USD."""
    return "{:,.2f}$".format(value)
# custom filter
app.jinja_env.filters["usd"] = usd

def allowed_file(filename):
                return '.' in filename and \
                      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
################################################
@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():

    # print(g.id_other[0].id_product)
    return render_template("index.html",
                        title = 'Sahola - Luxury Flowers Shop, Flowers delivery in NYC, Summit Nj » Feed')

################################################
@app.route('/login', methods=["GET", "POST"])
def login():
    """ display registration and login forms, their processing """

    form_login = LoginForm()
    form_register = RegisterForm()

    if request.method == "POST":
        # form processing login
        if form_login.validate_on_submit() and request.form.get("submit") == "Log in":
            # query the database and verify that the user exists and passwords match
            user = Users.query.filter_by(email = request.form.get("email").lower()).first()
            if user is not None and user.password_hash is not None and \
                     user.verify_password(form_login.password.data):
                login_user(user, form_login.remember_me.data)
                flash('You are now logged in. Welcome back!', 'success')
                return redirect(url_for('index')) #request.args.get('next') or
            else:
                flash('Invalid email or password.', 'form-error')
                return render_template("login.html", title = 'Sing In',
                    form_login = form_login, form_register = form_register)

        # form processing register
        elif form_register.validate_on_submit() and request.form.get("submit") == "Register":
            # database query and verification, mailing address is not yet registered
            user = Users.query.filter_by(email = request.form.get("email").lower()).first()
            if user is None:
                if request.form.get("password") == request.form.get("password_again"):
                    new_user = Users(email = request.form.get("email").lower(),
                        password_hash = generate_password_hash(request.form.get("password")))
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(Users.query.filter_by(email = new_user.email).first())
                    flash('You are now registered in. Welcome back!', 'success')
                    return redirect(url_for('index')) #request.args.get('next') or
                else:
                    flash('Passwords do not match', 'form-error')
                    return render_template("login.html", title = 'Sing In',
                        form_login = form_login, form_register = form_register)
            else:
                flash('User with such a mail already exists, please login', 'form-error')
                return render_template("login.html", title = 'Sing In',
                    form_login = form_login, form_register = form_register)

    else:
        return render_template("login.html", title = 'Sing In',
            form_login = form_login, form_register = form_register)

################################################
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

################################################
@app.route('/my-account')
def my_account():

    return render_template("my_account.html",
                            title = 'My Account')

################################################
@app.route('/my-account/edit-account/', methods=["GET", "POST"])
def edit_account():

    form_edit = UserAccountForm()
    form_chang_pass = ChangePasswordForm()

    if request.method == "POST":
        if form_edit.validate_on_submit() and request.form.get("submit") == "Save change":
            if form_edit.email.data is None:
                email = current_user.email
            else:
                user = Users.query.filter_by(email = current_user.email).first()
                user.email = form_edit.email.data
                db.session.add(user)
                db.session.commit()
            user_acc = User_account.query.filter_by(user_id = current_user.id).first()
            if user_acc is None:
                user_acc = User_account(user_id = current_user.id, first_name = form_edit.first_name.data,
                    last_name=form_edit.last_name.data, email = current_user.email)
                db.session.add(user_acc)
                db.session.commit()
            else:
                db.session.delete(user_acc)
                db.session.commit()
                user_acc = User_account(user_id = current_user.id, first_name = form_edit.first_name.data,
                    last_name=form_edit.last_name.data, email = current_user.email)
                db.session.add(user_acc)
                db.session.commit()

            flash('Your changees has been save.')
            return redirect(url_for('my_account'))

        elif form_chang_pass.validate_on_submit():
            if current_user.verify_password(form_chang_pass.old_password.data):
                current_user.password_hash = generate_password_hash(request.form.get("new_password"))
                db.session.add(current_user)
                db.session.commit()
                flash('Your password has been updated.')
                return redirect(url_for('index'))
            else:
                flash('Original password is invalid.')
                return render_template("edit_account.html", title = 'My Account',
                                        form_edit = form_edit,
                                        form_chang_pass = form_chang_pass)
        else:
            flash('form is filled in incorrectly')
            return redirect(url_for('edit_account'))

    return render_template("edit_account.html", title = 'My Account',
                            form_edit = form_edit,
                            form_chang_pass = form_chang_pass)

################################################
@app.route('/shop', methods=["GET", "POST"])
def shop():
    """  """
    products = Products.query.all()
    return render_template("shop.html",
                            title = 'Online Florist and Flowers Shop in New York (NYC) - Sahola',
                            products = products)

################################################
@app.route('/about_product/<prod>', methods=["GET", "POST"])
def about_product(prod):
    """  """
    product = Products.query.filter_by(id = prod).first()
    form_to_cart = AddToCartForm()

    if request.method == "POST":
        if form_to_cart.validate_on_submit():
            new_other = Orders(id_product = product.id,
                                id_user = current_user.id)
            db.session.add(new_other)
            db.session.commit()
            flash('Your cart has been updated.')
            return redirect(url_for('shop'))

    return render_template("about_product.html",
                            title = product.name_of_product,
                            prod = product,
                            form_to_cart = form_to_cart)

################################################
@app.route('/confirm/<prod>', methods=["GET", "POST"])
def confirm(prod):
    """  """
    product = Products.query.filter_by(id = prod).first()
    form_conf = ConfirmCancelOtherForm()

    if request.method == "POST":
        if form_conf.validate_on_submit() and request.form.get("submit") == 'Cancel':

            del_other = Orders.query.filter_by(id_product = product.id,
                                id_user = current_user.id).first()
            db.session.delete(del_other)
            db.session.commit()
            flash('Your other has been cansel.')
            return redirect(url_for('cart'))

        elif form_conf.validate_on_submit():

            conf_other = Orders.query.filter_by(id_product = product.id,
                                id_user = current_user.id).first()
            conf_other.order_status = NEW_ORDER
            db.session.add(conf_other)
            db.session.commit()
            flash('Your order has been accepted, we will contact you.')
            return redirect(url_for('cart'))

    return render_template("cart_confirm.html",
                            title = product.name_of_product,
                            prod = product,
                            form_conf = form_conf)

################################################
@app.route('/cart', methods=["GET", "POST"])
def cart():
    """  """
    if g.user.is_authenticated:

        return render_template("cart.html")
    else:
        flash('Please login or register')
        return redirect(url_for('index'))
################################################
@app.route('/admin', methods=["GET", "POST"])
def admin():
    if g.user.is_authenticated:

        return render_template("admin.html", title = 'Admin')
    else:
        return redirect(url_for('index'))

################################################
@app.route('/admin/add-admin', methods=["GET", "POST"])
def add_admin():

    if g.user.is_authenticated:

        form_add_admin = AddAdminForm()

        if request.method == "POST":
            if form_add_admin.validate_on_submit():

                new_admin = Users.query.filter_by(email = form_add_admin.email.data.lower()).first()
                if new_admin is None:
                    flash('First register a new user.')
                    return redirect(url_for('login'))
                new_admin.role = ROLE_ADMIN
                db.session.add(new_admin)
                db.session.commit()

                flash('Admin has been save.')
                return redirect(url_for('add_admin'))
            else:
                flash('form is filled in incorrectly')
                return redirect(url_for('add_admin'))

        return render_template("add_admin.html",
                                title = 'Admin', form_add_admin = form_add_admin)
    else:
        return redirect(url_for('index'))

################################################
@app.route('/admin/add-product', methods=["GET", "POST"])
def add_product():

    if g.user.is_authenticated:

        form_add = AddProductForm()

        if request.method == "POST":
            if form_add.validate_on_submit():

                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(url_for('add_product'))
                file = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return redirect(url_for('add_product'))
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                new_product = Products(name_of_product = form_add.name_of_product.data.lower(),
                                        size = form_add.size.data,
                                        cost = form_add.cost.data,
                                        product_description = form_add.product_description.data,
                                        img = filename)
                db.session.add(new_product)
                db.session.commit()

                flash('Your product has been save.')
                return redirect(url_for('add_product'))
            else:
                flash('form is filled in incorrectly')
                return redirect(url_for('add_product'))

        return render_template("add_product.html",
                                title = 'Admin', form_add = form_add)
    else:
        return redirect(url_for('index'))

################################################
@app.route('/admin/del-product', methods=["GET", "POST"])
def del_product():

    if g.user.is_authenticated:

        form_del = DelProductForm()

        if request.method == "POST":
            if form_del.validate_on_submit():

                del_product = Products.query.filter_by(name_of_product = form_del.name_of_product.data,
                                                    size = form_del.size.data).first()
                if del_product is None:
                    flash('No such product was found.')
                    return redirect(url_for('del_product'))

                del_file = del_product.img
                os.remove(os.path.join(UPLOAD_FOLDER, del_file))

                db.session.delete(del_product)
                db.session.commit()

                flash('Your product has been delete.')
                return redirect(url_for('del_product'))
            else:
                flash('form is filled in incorrectly')
                return redirect(url_for('del_product'))

        return render_template("del_product.html",
                                title = 'Admin', form_del = form_del)
    else:
        return redirect(url_for('index'))
################################################
@app.route('/contact', methods=["GET", "POST"])
def contact():
    """  """
    forn_contact = ContactUsForm()

    return render_template("contact.html",
                            title = 'Contact Us', forn_contact = forn_contact)

################################################
@app.route('/about-us', methods=["GET", "POST"])
def about_us():
    """  """

    return render_template("about.html",
                            title = 'About Us')


#################################################
@app.route('/my-account/edit-Billing-address', methods=["GET", "POST"])
def billing_address():

    form_billing_address = AddressForm()

    user_billing_address = Billing_address.query.filter_by(user_id = current_user.id).first()
    print(user_billing_address)


    if request.method == "POST":
        if form_billing_address.validate_on_submit():
            if user_billing_address is not None:
                db.session.delete(user_billing_address)
                db.session.commit()
            if form_billing_address.email.data is None:
                email = current_user.email
            else:
                user = Users.query.filter_by(email = current_user.email).first()
                user.email = form_billing_address.email.data
                db.session.add(user)
                db.session.commit()
            bill_address = Billing_address(user_id = current_user.id,
                                            first_name = form_billing_address.first_name.data,
                                            last_name=form_billing_address.last_name.data,
                                            email = current_user.email,
                                            phone = form_billing_address.phone.data,
                                            street = form_billing_address.street.data,
                                            apartment = form_billing_address.apartment.data,
                                            town = form_billing_address.town.data,
                                            state = form_billing_address.state.data,
                                            zip = form_billing_address.zips.data)
            db.session.add(bill_address)
            db.session.commit()

            flash('Your billing address has been save.')
            return redirect(url_for('my_account'))



        else:
            flash('form is filled in incorrectly')
            return redirect(url_for('billing_address'))

    return render_template("billing_address.html", title = 'Billing_address',
                            form_billing_address = form_billing_address,
                            user_billing_address = user_billing_address)



################################################
@app.route('/my-account/edit-Shipping-address', methods=["GET", "POST"])
def shipping_address():

    form_shipping_address = AddressForm()

    user_shipping_address = Shipping_address.query.filter_by(user_id = current_user.id).first()

    if request.method == "POST":
        if form_shipping_address.validate_on_submit():
            if user_shipping_address is not None:
                db.session.delete(user_shipping_address)
                db.session.commit()
            if form_shipping_address.email.data is None:
                email = current_user.email
            else:
                user = Users.query.filter_by(email = current_user.email).first()
                user.email = form_shipping_address.email.data
                db.session.add(user)
                db.session.commit()
            shipp_address = Shipping_address(user_id = current_user.id,
                                            first_name = form_shipping_address.first_name.data,
                                            last_name=form_shipping_address.last_name.data,
                                            email = current_user.email,
                                            phone = form_shipping_address.phone.data,
                                            street = form_shipping_address.street.data,
                                            apartment = form_shipping_address.apartment.data,
                                            town = form_shipping_address.town.data,
                                            state = form_shipping_address.state.data,
                                            zip = form_shipping_address.zips.data)
            db.session.add(shipp_address)
            db.session.commit()

            flash('Your billing address has been save.')
            return redirect(url_for('my_account'))



        else:
            flash('form is filled in incorrectly')
            return redirect(url_for('billing_address'))

    return render_template("shipping_address.html", title = 'Billing_address',
                            form_shipping_address = form_shipping_address,
                            user_shipping_address = user_shipping_address)



################################################