from flask import  redirect, render_template, url_for, flash, request, session, current_app
from .forms import Addproducts
from shop import db, app, photos
from .models import Brand, Category, Addproduct
import secrets, os
from shop.customers.models import CustomerOrderByOneClick


# чтобы отфильтровать те бренды которые не использует ни один продукт
def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

# чтобы отфильтровать те категории которые не использует ни один продукт
def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories


# -----------  main  page for user !!! ----------- \
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products, brands=brands(), categories=categories())
# -----  возможность во вкладке бренды, сортировать товар по брендам !!! ----- \

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html', product=product, brands=brands(), categories=categories())


@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand=get_b).paginate(page=page, per_page=8)
    return render_template('products/index.html', brand=brand, brands=brands(),
                           categories=categories(), get_b=get_b)

@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories(),
                           brands=brands(), get_cat=get_cat)


# ----------- page for add brands!!! ------- ---- \
@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    # if 'email' not in session:
    #     flash(f'Please login first', 'danger')
    #     return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')


# ----------- page for edit brands!!! ----------- \
@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name=brand
        flash(f'Your brand hes been update', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand1category.html', title='update brand', updatebrand=updatebrand)


# ----------- delete brand!!! ----------- \
@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} cant be delete', 'warning')
    return redirect(url_for('admin'))



# ----------- page for add categories!!! ----------- \
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    # if 'email' not in session:
    #     flash(f'Please login first', 'danger')
    #     return redirect(url_for('login'))
    if request.method == "POST":
        getcategory = request.form.get('category')
        cat = Category(name=getcategory)
        db.session.add(cat)
        flash(f'The Category {getcategory} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')


# ----------- page for edit categories!!! ----------- \
@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    # if 'email' not in session:
    #     flash(f'Please login first', 'danger')
    #     return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecategory.name = category
        flash(f'Your category hes been update', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand1category.html', title='update brand', updatecategory=updatecategory)


# ------------------ delete category!!! ------------------ \
@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'Category {category.name} hes been deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'The category {category.name} cant be delete', 'warning')
    return redirect(url_for('admin'))


# ----------- page for add product and photo!!! ----------- \
@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    # if 'email' not in session:
    #     flash(f'Please login first', 'danger')
    #     return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, desc=desc,
                            brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'The Product {name}, hes been added to your database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Add Product page', brands=brands,
                           categories=categories)


# ----------- page for update product!!! ----------- \
@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.desc = form.description.data
        # delete photo link
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                # save new link on photo
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                # save new link on photo
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                # save new link on photo
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'Your product hes been update', 'success')
        return redirect(url_for('admin'))

    # чтобы в форме были записи текущей конфигурации продукта
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.desc

    return render_template('products/updateproduct.html', form=form, product=product, categories=categories,
                           brands=brands)


# ----------- page for delete product!!! ----------- \
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)

        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was deleted form your record', 'success')
        return redirect(url_for('admin'))

    flash(f'Cant delete the product', 'danger')
    return redirect(url_for('admin'))

# --------------------- удаление заказав "один клик" ------------------
@app.route('/deleteorderbyoneclick/<int:id>', methods = ['POST'])
def deleteorderbyoneclick(id):
    order = CustomerOrderByOneClick.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(order)
        db.session.commit()
        return redirect(url_for('orderbyoneclick'))
    return redirect(url_for('admin'))

