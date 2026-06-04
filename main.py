import requests
import area.py
import test.py


BASE_URL = "http://localhost:8000"


def print_header():
    print("\n" + "=" * 40)
    print("      CALCOLATORE AREA TRIANGOLO")
    print("=" * 40)


def print_menu():
    print("\nScegli il metodo di calcolo:")
    print("  1. Base e Altezza")
    print("  2. Tre Lati (Formula di Erone)")
    print("  3. Coordinate dei Vertici")
    print("  0. Esci")
    print("-" * 40)


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠  Inserisci un numero valido.")


def calcola_base_altezza():
    print("\n📐 Metodo: Base e Altezza")
    base = get_float("  Base   : ")
    height = get_float("  Altezza: ")

    resp = requests.post(f"{BASE_URL}/area/base-height", json={"base": base, "height": height})
    mostra_risultato(resp)


def calcola_erone():
    print("\n📐 Metodo: Formula di Erone (tre lati)")
    a = get_float("  Lato a: ")
    b = get_float("  Lato b: ")
    c = get_float("  Lato c: ")

    resp = requests.post(f"{BASE_URL}/area/heron", json={"a": a, "b": b, "c": c})
    mostra_risultato(resp)


def calcola_coordinate():
    print("\n📐 Metodo: Coordinate dei Vertici")
    print("  Inserisci le coordinate dei 3 vertici:")
    x1 = get_float("  Vertice 1 — x: ")
    y1 = get_float("  Vertice 1 — y: ")
    x2 = get_float("  Vertice 2 — x: ")
    y2 = get_float("  Vertice 2 — y: ")
    x3 = get_float("  Vertice 3 — x: ")
    y3 = get_float("  Vertice 3 — y: ")

    resp = requests.post(f"{BASE_URL}/area/coordinates",
                         json={"x1": x1, "y1": y1, "x2": x2, "y2": y2, "x3": x3, "y3": y3})
    mostra_risultato(resp)


def mostra_risultato(resp):
    print("-" * 40)
    if resp.status_code == 200:
        data = resp.json()
        print(f"  ✅ Area calcolata: {data['area']}")
        print(f"     Metodo usato : {data['method']}")
    else:
        try:
            detail = resp.json().get("detail", "Errore sconosciuto")
        except Exception:
            detail = resp.text
        print(f"  ❌ Errore: {detail}")
    print("-" * 40)


def main():
    print_header()

    # Verifica connessione all'API
    try:
        requests.get(BASE_URL, timeout=2)
    except requests.ConnectionError:
        print(f"\n  ❌ Impossibile connettersi all'API su {BASE_URL}")
        print("     Avvia prima il server con:")
        print("     uvicorn triangle_api:app --reload\n")
        return

    while True:
        print_menu()
        scelta = input("Scelta: ").strip()

        if scelta == "1":
            calcola_base_altezza()
        elif scelta == "2":
            calcola_erone()
        elif scelta == "3":
            calcola_coordinate()
        elif scelta == "0":
            print("\n  Arrivederci! 👋\n")
            break
        else:
            print("  ⚠  Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()