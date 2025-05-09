from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

app = Flask(__name__)


def get_db_connection():
    """
    Izveido un atgriež savienojumu ar SQLite datubāzi.
    """
    # Atrod ceļu uz datubāzes failu (tas atrodas tajā pašā mapē, kur šis fails)
    db = Path(__file__).parent/"tejas.db"
    # Izveido savienojumu ar SQLite datubāzi
    conn = sqlite3.connect(db)
    # Nodrošina, ka rezultāti būs pieejami kā vārdnīcas (piemēram: product["name"])
    conn.row_factory = sqlite3.Row
    # Atgriež savienojumu
    return conn

@app.route("/")

def index():
    return render_template("index.html")


@app.route("/produkti")
def products():
    conn = get_db_connection() # Pieslēdzas datubāzei

    # Izpilda SQL vaicājumu, kas atlasa visus produktus
    products = conn.execute("SELECT * FROM teja").fetchall()

    conn.close() # Aizver savienojumu ar datubāzi

    # Atgriežam HTML veidni "products.html", padodot produktus veidnei
    return render_template("products.html", products=products)



# Maršruts, kas atbild uz pieprasījumu, piemēram: /produkti/3
# Šeit <int:product_id> nozīmē, ka URL daļā gaidāms produkta ID kā skaitlis
@app.route("/produkti/<int:product_id>")
def products_show(product_id):

    conn = get_db_connection() # Pieslēdzas datubāzei

    # Izpilda SQL vaicājumu, kurš atgriež tikai vienu produktu pēc ID
    product = conn.execute(
    # "SELECT * FROM teja WHERE id = ?",
    # (product_id,),
    # ).fetchone()
    
    """SELECT
    "teja"."id",
    "teja"."nosaukums",
    "teja"."cena",
    "teja"."foto",
    "teja"."sastavs",
    "veikals"."vnosaukums",
    "iepakojums"."veids",
    "iepakojums"."masa",
    "razotajs"."name"
    FROM
    "teja"
    LEFT JOIN "veikals" ON "teja"."veikala_id" = "veikals"."id"
    LEFT JOIN "iepakojums" ON "teja"."iepakojuma_id" = "iepakojums"."id"
    LEFT JOIN "razotajs" ON "teja"."razotaja_id" = "razotajs"."id"
    WHERE teja.id = ?""",
    (product_id,),
    ).fetchone()




    # product = conn.execute(
    # """SELECT
    # "iepakojums"."veids",
    # "iepakojums"."masa"
    # -- "teja"."id",
    # -- "teja"."nosaukums"
    # FROM
    # "teja"
    # LEFT JOIN "iepakojums" ON "teja"."iepakojuma_id" = "iepakojums"."id"
    # WHERE teja.id = ?""",
    # (product_id,),
    # ).fetchone()









    # ? ir vieta, kur tiks ievietota vērtība – šajā gadījumā product_id

    conn.close() # Aizver savienojumu ar datubāzi
    
    # Atgriežam HTML veidni 'products_show.html', padodot konkrēto produktu veidnei
    return render_template("products_show.html", product=product)





@app.route("/par-mums")
def about():
    return render_template("about.html")




# ----------------------------








# IR - CREATE/INSERT PIEVIENOT PRODUKTU
@app.route("/produkts/pievienot", methods=["GET", "POST"])
def create_product():
    if request.method == "POST":
        nosaukums = request.form["nosaukums"]
        cena = request.form["cena"]
        sastavs = request.form["sastavs"]
        foto = request.form["foto"]
        veikala_id = request.form["veikala_id"]
        iepakojuma_id = request.form["iepakojuma_id"]
        razotaja_id = request.form["razotaja_id"]


        conn = get_db_connection()
        conn.execute("""
            INSERT INTO teja (nosaukums, cena, sastavs, foto, veikala_id, iepakojuma_id, razotaja_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nosaukums, cena, sastavs, foto, veikala_id, iepakojuma_id, razotaja_id))
        conn.commit()
        conn.close()
        return redirect(url_for("products"))

    return render_template("product_form.html")





# UPDATE - LABOT PRODUKTU
@app.route("/produkts/rediget/<int:id>", methods=["GET", "POST"])
def update_product(id):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM teja WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        nosaukums = request.form["nosaukums"]
        cena = request.form["cena"]
        sastavs = request.form["sastavs"]
        foto = request.form["foto"]
        veikala_id = request.form["veikala_id"]
        iepakojuma_id = request.form["iepakojuma_id"]
        razotaja_id = request.form["razotaja_id"]

        conn.execute("""
            UPDATE teja
            SET nosaukums = ?, cena = ?, sastavs = ?, foto = ?, veikala_id = ?, iepakojuma_id = ?, razotaja_id = ?
            WHERE id = ?
        """, (nosaukums, cena, sastavs, foto, veikala_id, iepakojuma_id, razotaja_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for("products"))

    conn.close()
    return render_template("product_edit.html", product=product)




# DELETE - IZDZĒST PRODUKTU
@app.route("/produkts/dzest/<int:id>", methods=["POST"])
def delete_product(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM teja WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("products"))


if __name__ == "__main__":
    app.run(debug=True)