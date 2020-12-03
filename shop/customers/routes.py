from flask import  redirect, render_template, url_for, flash, request, session, current_app, jsonify, json
from shop.products.forms import Addproducts
from shop import db, app, photos, bcrypt, login_manager, client
from flask_login import login_required, current_user, logout_user, login_user
from shop.products.models import Brand, Category, Addproduct
import secrets, os
from .forms import CustomerRegisterForm, CustomerLoginForm, OrderForm
from .models import Register, CustomerOrder, CustomerOrderByOneClick
from shop.admin.models import  NPWarehouse
from pprint import pprint

 # !!!!!!СТРАНИЦА РЕГИСТРАЦИИ!!!!!!
@app.route('/customer/register', methods= ['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        register = Register(mobile=form.mobile.data, password=hash_password,
                            FirstName=form.first_name.data, LastName=form.last_name.data)
        db.session.add(register)
        db.session.commit()
        flash(f'Добро пожаловать!', 'success')
        return redirect(url_for('customerLogin'))

    return render_template('customer/register.html', form=form)


# !!!!!!СТРАНИЦА ВХОДА!!!!!!
@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(mobile=form.number.data).first()
        print(user.password)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Отлично!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash(f'Неверный логин или пароль', 'danger')
        return redirect(url_for('customerLogin'))

    return render_template('customer/login.html', form=form)


# !!!!!!КНОПКА ВЫХОДА!!!!!!
@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))


# запись в бд данных о заказе
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id,
                                  orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash(f'Your order has been sent', 'success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash(f'Something wrong while get order', 'danger')
            return redirect(url_for('getCart'))


# Из БД достает информацию о заказк
@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if   current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            grandTotal = float('%.2f' % (1.0 * subTotal))

    else:
        return redirect(url_for('customerLogin'))

    return render_template('customer/order.html', invoice=invoice,
                               subTotal=subTotal, grandTotal=grandTotal,
                           customer=customer, orders=orders)


#!!!!!!!!!!!!!!!!! Покупка в один клик !!!!!!!!
@app.route('/orderoneclick/<int:id>', methods=['POST'])
def orderoneclick(id):
    product = Addproduct.query.get_or_404(id)
    name = request.form.get('name')
    number = request.form.get('number')
    if request.method == 'POST':
        order = CustomerOrderByOneClick(name=name, number=number, product_name=product.name,
                                        product_price=product.price, product_discount=product.discount)
        db.session.add(order)
        db.session.commit()
        flash(f'Ваша заявка обрабатывается', 'success')
        return redirect(url_for('home'))
    return render_template(url_for('home'))


@app.route('/mainorders')
def mainorders():
    form = OrderForm()
    warehouses = NPWarehouse.query.all()

    return render_template('customer/mainorder.html', form=form, warehouses=warehouses)


@app.route('/warehouse/<get_warehouse>')
def citybyregion(get_warehouse):
    warehouses = NPWarehouse.query.filter_by(city_id=get_warehouse).all()
    warehousesArray = []
    for warehouse in warehouses:
        warehouseObj = {}
        warehouseObj['title'] = warehouse.title
        warehousesArray.append(warehouseObj)
    return jsonify({'warehousecity' : warehousesArray})


@app.route('/novaposhta')
def novaposhta():
    response = client.address.get_warehouses()
    pprint(response.json()['data'][0])
    for warehouses in response.json()['data']:
        city_json = warehouses['CityDescriptionRu']
        title_json = warehouses['DescriptionRu']
        name_json =city_json +", "+ title_json
        warehouse = NPWarehouse(name = name_json)


        db.session.add(warehouse)
        db.session.commit()

        print('Victory')


# @app.route('/novaposhta')
# def novaposhta():
#     response = client.address.get_warehouses()
#     pprint(response.json()['data'][0])
#     for warehouses in response.json()['data']:
#         cityref_json = warehouses['CityRef']
#         city_json = warehouses['CityDescriptionRu']
#         area_json = warehouses['SettlementAreaDescription']
#         get_city = NPCity.query.filter_by(ref=cityref_json).first()
#
#         title_json = warehouses['DescriptionRu']
#         number_json = warehouses['Number']
#         warehousesref_json = warehouses['Ref']
#         if get_city:
#             warehouse = NPWarehouse(title=title_json, number=number_json,
#                                          ref=warehousesref_json, city = get_city)
#
#             db.session.add(warehouse)
#             db.session.commit()
#         else:
#             city = NPCity(ref = cityref_json, area = area_json, city = city_json)
#             warehouse = NPWarehouse(title=title_json, number=number_json,
#                                          ref=warehousesref_json, city=city)
#
#             db.session.add(city)
#             db.session.add(warehouse)
#             db.session.commit()
#
#
#     print('Victory')




