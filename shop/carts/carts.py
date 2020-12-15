from flask import  redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct, Brand, Category
from shop.products.routes import brands, categories
import simplejson

# если товаров > 1
def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


# добавления товара в корзину
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == "POST":
            DictItems = {product_id:{'name': product.name, 'price':product.price, 'discount':product.discount,
                                     'quantity':quantity, 'image':product.image_1}}


            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                         if int(key) == int(product_id):
                             session.modified = True
                             item['quantity'] += 1
                    print("Этот товар уже добавлен в карзину")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    redirect(request.referrer)
            else:
                session ['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


# цифры в корзине
@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%0.2f" % (.06 * float(subtotal)))
        grandtotal = float("%0.2f" % (1 * subtotal))
    return render_template('customer/carts.html', grandtotal=grandtotal, brands=brands(), categories=categories())


# обновление количества товаров если их > 1
@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity']=quantity
                    flash(f'Товар был обновлен')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

    return


# чтобы очистить корзину для Admin
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)


# удаление отдельных товаров в корзине
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
            return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


# очистка всей корзины через кнопку
@app.route('/clearcart')
def clearcart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
