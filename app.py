from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    area = None
    errore = None
    if request.method == "POST":
        metodo = request.form.get("metodo")
        try:
            if metodo == "base_altezza":
                base = float(request.form["base"])
                altezza = float(request.form["altezza"])
                area = (base * altezza) / 2
            elif metodo == "erone":
                a = float(request.form["a"])
                b = float(request.form["b"])
                c = float(request.form["c"])
                if a+b > c and a+c > b and b+c > a:
                    s = (a+b+c) / 2
                    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
                else:
                    errore = "I lati non formano un triangolo valido."
        except ValueError:
            errore = "Inserisci solo numeri validi."
    return render_template("index.html", area=area, errore=errore)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)