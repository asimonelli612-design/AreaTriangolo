"""
Test suite per Triangle Area API
Esegui con: pytest test_triangle_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from triangle_api import app


client = TestClient(app)


# ============================================================
# ROOT
# ============================================================


class TestRoot:
    def test_root_status(self):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_root_message(self):
        resp = client.get("/")
        assert "message" in resp.json()



# ============================================================
# BASE E ALTEZZA
# ============================================================


class TestBaseHeight:

    # --- Casi validi ---

    def test_triangolo_intero(self):
        resp = client.post("/area/base-height", json={"base": 10, "height": 5})
        assert resp.status_code == 200
        assert resp.json()["area"] == 25.0


    def test_triangolo_decimale(self):
        resp = client.post("/area/base-height", json={"base": 3.5, "height": 2.0})
        assert resp.status_code == 200
        assert resp.json()["area"] == pytest.approx(3.5, rel=1e-5)


    def test_valori_molto_grandi(self):
        resp = client.post("/area/base-height", json={"base": 1e6, "height": 1e6})
        assert resp.status_code == 200
        assert resp.json()["area"] == pytest.approx(5e11, rel=1e-5)


    def test_valori_molto_piccoli(self):
        # round(0.001 * 0.001 / 2, 6) = round(5e-7, 6) = 0.0
        # L'API arrotonda a 6 decimali: valori < 5e-7 vengono restituiti come 0.0
        resp = client.post("/area/base-height", json={"base": 0.001, "height": 0.001})
        assert resp.status_code == 200
        assert resp.json()["area"] == 0.0


    def test_metodo_restituito(self):
        resp = client.post("/area/base-height", json={"base": 4, "height": 6})
        assert resp.json()["method"] == "base-height"


    # --- Casi non validi ---


    def test_base_zero(self):
        resp = client.post("/area/base-height", json={"base": 0, "height": 5})
        assert resp.status_code == 422


    def test_altezza_zero(self):
        resp = client.post("/area/base-height", json={"base": 5, "height": 0})
        assert resp.status_code == 422


    def test_base_negativa(self):
        resp = client.post("/area/base-height", json={"base": -3, "height": 5})
        assert resp.status_code == 422


    def test_altezza_negativa(self):
        resp = client.post("/area/base-height", json={"base": 5, "height": -3})
        assert resp.status_code == 422


    def test_campo_mancante(self):
        resp = client.post("/area/base-height", json={"base": 5})
        assert resp.status_code == 422


    def test_campo_stringa(self):
        resp = client.post("/area/base-height", json={"base": "abc", "height": 5})
        assert resp.status_code == 422



# ============================================================
# FORMULA DI ERONE
# ============================================================


class TestHeron:


    # --- Casi validi ---


    def test_triangolo_3_4_5(self):
        resp = client.post("/area/heron", json={"a": 3, "b": 4, "c": 5})
        assert resp.status_code == 200
        assert resp.json()["area"] == pytest.approx(6.0, rel=1e-5)


    def test_triangolo_equilatero(self):
        # Area = (sqrt(3)/4) * lato^2  →  lato=2 → area ≈ 1.732051
        resp = client.post("/area/heron", json={"a": 2, "b": 2, "c": 2})
        assert resp.status_code == 200
        assert resp.json()["area"] == pytest.approx(1.732051, rel=1e-4)


    def test_triangolo_isoscele(self):
        resp = client.post("/area/heron", json={"a": 5, "b": 5, "c": 6})
        assert resp.status_code == 200
        assert resp.json()["area"] == pytest.approx(12.0, rel=1e-4)


    def test_triangolo_decimale(self):
        resp = client.post("/area/heron", json={"a": 2.5, "b": 3.5, "c": 4.0})
        assert resp.status_code == 200
        assert resp.json()["area"] > 0


    def test_metodo_restituito(self):
        resp = client.post("/area/heron", json={"a": 3, "b": 4, "c": 5})
        assert resp.json()["method"] == "heron"


    # --- Casi non validi ---


    def test_disuguaglianza_triangolare_violata(self):
        resp = client.post("/area/heron", json={"a": 1, "b": 2, "c": 10})
        assert resp.status_code == 422


    def test_lato_zero(self):
        resp = client.post("/area/heron", json={"a": 0, "b": 4, "c": 5})
        assert resp.status_code == 422


    def test_lato_negativo(self):
        resp = client.post("/area/heron", json={"a": -3, "b": 4, "c": 5})
        assert resp.status_code == 422


    def test_lati_degeneri_uguali_somma(self):
        # a + b == c → triangolo degenere
        resp = client.post("/area/heron", json={"a": 1, "b": 2, "c": 3})
        assert resp.status_code == 422


    def test_campo_mancante(self):
        resp = client.post("/area/heron", json={"a": 3, "b": 4})
        assert resp.status_code == 422


# ============================================================
# COORDINATE DEI VERTICI
# ============================================================


class TestCoordinates:


    # --- Casi validi ---


    def test_triangolo_semplice(self):
        # Vertici (0,0), (4,0), (0,3) → area = 6
        resp = client.post("/area/coordinates",
                           json={"x1": 0, "y1": 0, "x2": 4, "y2": 0, "x3": 0, "y3": 3})
        assert resp.status_code == 200
        assert resp.json()["area"] == pytest.approx(6.0, rel=1e-5)


    def test_triangolo_coordinate_negative(self):
        resp = client.post("/area/coordinates",
                           json={"x1": -1, "y1": -1, "x2": 3, "y2": -1, "x3": 0, "y3": 3})
        assert resp.status_code == 200
        assert resp.json()["area"] > 0


    def test_triangolo_quadrante_misto(self):
        resp = client.post("/area/coordinates",
                           json={"x1": 0, "y1": 0, "x2": 6, "y2": 0, "x3": 3, "y3": 4})
        assert resp.status_code == 200
        assert resp.json()["area"] == pytest.approx(12.0, rel=1e-5)


    def test_ordine_vertici_non_cambia_area(self):
        payload_a = {"x1": 0, "y1": 0, "x2": 4, "y2": 0, "x3": 0, "y3": 3}
        payload_b = {"x1": 4, "y1": 0, "x2": 0, "y2": 3, "x3": 0, "y3": 0}
        area_a = client.post("/area/coordinates", json=payload_a).json()["area"]
        area_b = client.post("/area/coordinates", json=payload_b).json()["area"]
        assert area_a == pytest.approx(area_b, rel=1e-5)


    def test_metodo_restituito(self):
        resp = client.post("/area/coordinates",
                           json={"x1": 0, "y1": 0, "x2": 4, "y2": 0, "x3": 0, "y3": 3})
        assert resp.json()["method"] == "coordinates"


    # --- Casi non validi ---


    def test_punti_collineari(self):
        # Tre punti sulla stessa retta → area = 0
        resp = client.post("/area/coordinates",
                           json={"x1": 0, "y1": 0, "x2": 1, "y2": 1, "x3": 2, "y3": 2})
        assert resp.status_code == 422


    def test_punti_coincidenti(self):
        resp = client.post("/area/coordinates",
                           json={"x1": 1, "y1": 1, "x2": 1, "y2": 1, "x3": 1, "y3": 1})
        assert resp.status_code == 422


    def test_campo_mancante(self):
        resp = client.post("/area/coordinates",
                           json={"x1": 0, "y1": 0, "x2": 4, "y2": 0})
        assert resp.status_code == 422


    def test_campo_stringa(self):
        resp = client.post("/area/coordinates",
                           json={"x1": "abc", "y1": 0, "x2": 4, "y2": 0, "x3": 0, "y3": 3})
        assert resp.status_code == 422


# ============================================================
# CONSISTENZA TRA METODI
# ============================================================


class TestConsistenza:
    """Verifica che metodi diversi diano lo stesso risultato sullo stesso triangolo."""


    def test_3_4_5_base_height_vs_heron(self):
        # Triangolo 3-4-5: base=3, altezza=4 → area=6
        r1 = client.post("/area/base-height", json={"base": 3, "height": 4}).json()["area"]
        r2 = client.post("/area/heron", json={"a": 3, "b": 4, "c": 5}).json()["area"]
        assert r1 == pytest.approx(r2, rel=1e-4)


    def test_heron_vs_coordinates(self):
        # Triangolo (0,0),(3,0),(0,4) → lati 3,4,5 → area=6
        r1 = client.post("/area/heron", json={"a": 3, "b": 4, "c": 5}).json()["area"]
        r2 = client.post("/area/coordinates",
                         json={"x1": 0, "y1": 0, "x2": 3, "y2": 0,
                               "x3": 0, "y3": 4}).json()["area"]
        assert r1 == pytest.approx(r2, rel=1e-4)