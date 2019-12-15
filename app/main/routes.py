from flask import render_template, redirect, url_for, abort, session

from app.main import bp
from app.main.forms import AddNewDepForm

from connection import connection


def get_objects_or_404(sql_connection, request):
    sql_response = sql_connection.execute(request)
    if not sql_response:
        abort(404)
    return sql_response


@bp.route("/")
def main():
    sql_request = "SELECT * FROM shop"
    sql_response = get_objects_or_404(connection, sql_request).fetchall()
    return render_template("main/index.html", shops=sql_response)


@bp.route("/shop/<name>")
def shop(name):
    sql_request = "SELECT * FROM shop_with_departaments WHERE shop_name='{}'".format(name)
    sql_response = get_objects_or_404(connection, sql_request).fetchall()
    shop_info = sql_response[0][1:4]
    departaments = [x[4:] for x in sql_response]
    try:
        owned = False
        if departaments[0][0] == session["user"]["username"]:
            owned = True
    except KeyError:
        pass
    return render_template("main/shopPage.html", shop=shop_info, departaments=departaments, owned=owned)


@bp.route("/shop/<name>/products")
def shop_products(name):
    sql_request = """
        SELECT shop_name, shop_class, shop_num, stock_number, product_name, price,
            CASE WHEN count = 0
            THEN 'Нет в наличии' ELSE CAST (count AS char(4)) END count  
        FROM product_in_the_shop  WHERE shop_name='{}'
    """.format(name)
    sql_response = get_objects_or_404(connection, sql_request).fetchall()
    shop_owner = get_objects_or_404(connection, "SELECT owner FROM shop WHERE name='{}'".format(name)).fetchone()[0]
    if session.get("user", None) and shop_owner == session["user"]["username"]:
        owned = True
    else:
        owned = False
    print(owned)
    shop = sql_response[0][:3]
    products = [x[3:] for x in sql_response]
    return render_template("main/products.html", shop=shop, products=products, owned=owned)


@bp.route("/shop/<name>/dep_heads")
def shop_departaments_heads(name):
    sql_request = "SELECT head_of FROM departament WHERE shop_id=(" \
                  "     SELECT id FROM shop WHERE name='{}'" \
                  ")".format(name)
    sql_request_owner = "SELECT owner FROM shop WHERE name='{}'".format(name)
    owner = connection.execute(sql_request_owner).fetchone()[0]
    sql_response = connection.execute(sql_request).fetchall()
    pairs = list()
    try:
        for i in range(0, len(sql_response), 2):
            pairs.append((sql_response[i], sql_response[i+1]))
    except IndexError:
        if session.get("user", None) and session["user"]["username"] == owner:
            pairs.append((sql_response[i], "ADD_NEW_BLOCK"))
        else:
            pairs.append((sql_response[i],))
    else:
        if session.get("user", None) and session["user"]["username"] == owner:
            pairs.append(("ADD_NEW_BLOCK", ))
    return render_template("main/departaments_head_of.html", pairs=pairs, shop_name=name)


@bp.route("/shop/<name>/dep_heads/add-new-dep", methods=["GET", "POST"])
def add_new_dep(name):
    form = AddNewDepForm()
    if form.validate_on_submit():
        head_of = form.head_of.data
        password = form.password.data
        address = form.address.data
        if connection.execute(f"SELECT * FROM _user WHERE username='{head_of}'").fetchone() is None:
            connection.execute(f"INSERT INTO _user VALUES ('{head_of}', '{password}', FALSE, TRUE)")
        shop_id_request = f"SELECT id FROM shop WHERE name='{name}'"
        shop_id = connection.execute(shop_id_request).fetchone()[0]
        connection.execute(f"INSERT INTO departament VALUES('{head_of}', {shop_id}, '{address}')")
        return redirect(url_for("main.shop_departaments_heads", name=name))
    return render_template("main/create_new_dep.html", form=form)


@bp.route("/shop/<name>/<dep_id>")
def prod_in_dep(name, dep_id):
    sql_request = "SELECT stock_number, name, price, " \
                  "    CASE WHEN count=0" \
                  "    THEN 'Нет в наличии'" \
                  "    ELSE CAST(count AS CHAR(4)) END count " \
                  "FROM products_in_the_departament_info " \
                  "WHERE departament_id = '{}'".format(dep_id)
    sql_response = connection.execute(sql_request).fetchall()
    return render_template("main/prod_in_dep.html", products=sql_response, departament=dep_id)


@bp.route("/shop/<name>/products/<product_id>")
def common_products(name, product_id):
    sql_request = "SELECT name, stock_number, departament_id, count FROM products_in_the_departament_info " \
                  "WHERE stock_number='{}'".format(product_id)
    sql_response = get_objects_or_404(connection, sql_request).fetchall()
    product_info = sql_response[0][0:2]

    departaments = list(map(lambda x: x[2:], sql_response))
    return render_template("main/common_products.html", product=product_info, departaments=departaments)




