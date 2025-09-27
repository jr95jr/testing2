import io, os, sqlite3
    import streamlit as st

    st.set_page_config(page_title="Demo: Pruebas Unitarias e Integración en Python", layout="wide")
    st.title("🧪 Demo Didáctica: Pruebas Unitarias e Integración en Python")
    st.caption("Hecha con Streamlit · unittest + SQLite · con laboratorio interactivo")

    st.sidebar.header("Navegación")
    choice = st.sidebar.radio(
        "Secciones",
        [
            "Introducción",
            "Código de ejemplo (src)",
            "Pruebas unitarias",
            "Pruebas de integración",
            "Laboratorio guiado",
            "Laboratorio interactivo",
            "Créditos"
        ],
        index=0
    )

    project_root = os.path.dirname(__file__)
    src_dir = os.path.join(project_root, "src")
    tests_dir = os.path.join(project_root, "tests")

    def read_file(path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    if choice == "Introducción":
        st.subheader("¿Qué veremos?")
        st.markdown(
            """
            **Objetivo:** Diferenciar **pruebas unitarias** (funciones aisladas) y **pruebas de integración** (componentes reales trabajando juntos).
            **Stack:** `unittest`, `sqlite3` en memoria, y Streamlit como UI.
            **Estructura:**
            ```
            streamlit_testing_demo/
            ├─ app.py
            ├─ src/
            │  ├─ calculator.py
            │  ├─ repository.py
            │  └─ service.py
            └─ tests/
               ├─ test_unit_calculator.py
               └─ test_integration_vehicle.py
            ```
            """
        )
        st.info("Usa el menú lateral para explorar el código y ejecutar pruebas.")

    elif choice == "Código de ejemplo (src)":
        st.subheader("Módulos de ejemplo")
        file = st.selectbox("Selecciona un archivo", ["calculator.py", "repository.py", "service.py"])
        path = os.path.join(src_dir, file)
        st.code(read_file(path), language="python")

    elif choice == "Pruebas unitarias":
        st.subheader("Ejecutar pruebas **unitarias**")
        st.write("Archivo: `tests/test_unit_calculator.py`")
        st.code(read_file(os.path.join(tests_dir, "test_unit_calculator.py")), language="python")

        if st.button("▶️ Ejecutar pruebas unitarias"):
            import unittest
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromName("tests.test_unit_calculator")
            stream = io.StringIO()
            runner = unittest.TextTestRunner(stream=stream, verbosity=2)
            result = runner.run(suite)
            st.text(stream.getvalue())
            st.success(f"OK: {result.wasSuccessful()} — Tests: {result.testsRun} · Fallos: {len(result.failures)} · Errores: {len(result.errors)}")

    elif choice == "Pruebas de integración":
        st.subheader("Ejecutar pruebas de **integración**")
        st.write("Archivo: `tests/test_integration_vehicle.py` (usa SQLite en memoria + capas repo/servicio)")
        st.code(read_file(os.path.join(tests_dir, "test_integration_vehicle.py")), language="python")

        if st.button("▶️ Ejecutar pruebas de integración"):
            import unittest
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromName("tests.test_integration_vehicle")
            stream = io.StringIO()
            runner = unittest.TextTestRunner(stream=stream, verbosity=2)
            result = runner.run(suite)
            st.text(stream.getvalue())
            st.success(f"OK: {result.wasSuccessful()} — Tests: {result.testsRun} · Fallos: {len(result.failures)} · Errores: {len(result.errors)}")

    elif choice == "Laboratorio guiado":
        st.subheader("Laboratorio: agrega un caso de prueba")
        st.markdown(
            """
            1. **Abre** `src/calculator.py` y revisa `power(a, b)`.
            2. **Crea** más tests en `tests/test_unit_calculator.py` (casos límite).
            3. **Vuelve** y ejecuta las pruebas unitarias.
            """
        )
        with st.expander("Ejemplos de casos límite"):
            st.code(
                """
                # tests/test_unit_calculator.py
                def test_divide_negative(self):
                    from src.calculator import divide
                    self.assertEqual(divide(-6, 2), -3)
                def test_mean_single(self):
                    from src.calculator import mean
                    self.assertEqual(mean([42]), 42)
                """, language="python"
            )

    elif choice == "Laboratorio interactivo":
        st.subheader("🧪 Laboratorio interactivo")
        st.markdown("Explora y **modifica valores** para comprender el testing.")

        # A) Calculadora
        st.markdown("### A) Calculadora (unit tests)")
        mode = st.selectbox("Función a probar", ["add", "divide", "mean", "power"], index=0)
        if mode in ("add", "divide", "power"):
            a = st.number_input("a", value=2.0)
            b = st.number_input("b", value=3.0)
            if st.button("Calcular", key="calc_btn"):
                if mode == "add":
                    from src.calculator import add as fn
                elif mode == "divide":
                    from src.calculator import divide as fn
                else:
                    from src.calculator import power as fn
                try:
                    res = fn(a, b)
                    st.success(f"Resultado: {res}")
                    st.code(f'''import unittest
from src.calculator import {mode}
class TestAuto(unittest.TestCase):
    def test_{mode}(self):
        self.assertEqual({mode}({a}, {b}), {res})
''', language="python")
                except Exception as e:
                    st.error(f"Excepción: {type(e).__name__}: {e}")
                    st.code(f'''import unittest
from src.calculator import {mode}
class TestAuto(unittest.TestCase):
    def test_{mode}_raises(self):
        with self.assertRaises({type(e).__name__}):
            {mode}({a}, {b})
''', language="python")
        else:
            raw = st.text_input("Valores (coma)", value="2,4,6")
            if st.button("Calcular promedio", key="mean_btn"):
                try:
                    data = [float(x.strip()) for x in raw.split(",") if x.strip()]
                    from src.calculator import mean
                    res = mean(data)
                    st.info(f"Lista: {data}")
                    st.success(f"Promedio: {res}")
                    expected = "None" if res is None else str(res)
                    st.code(f'''import unittest
from src.calculator import mean
class TestAuto(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean({data}), {expected})
''', language="python")
                except Exception as e:
                    st.error(f"Error: {e}")

        st.divider()

        # B) Inventario/Integración
        st.markdown("### B) Inventario de Vehículos (integration tests)")
        st.caption("SQLite en memoria + capas reales.")

        if "lab_conn" not in st.session_state:
            st.session_state.lab_conn = sqlite3.connect(":memory:")
            from src.service import VehicleService
            st.session_state.lab_service = VehicleService(st.session_state.lab_conn)

        brand = st.text_input("Marca", value="Toyota")
        model = st.text_input("Modelo", value="Corolla")
        year = st.number_input("Año", value=2020, step=1, min_value=1800, max_value=3000)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("➕ Registrar", key="add_btn"):
                try:
                    vid = st.session_state.lab_service.register_vehicle(brand, model, int(year))
                    st.success(f"ID registrado: {vid}")
                except Exception as e:
                    st.error(f"Error: {e}")
        with c2:
            if st.button("🔄 Reset DB", key="reset_btn"):
                try:
                    st.session_state.lab_conn.close()
                except Exception:
                    pass
                st.session_state.lab_conn = sqlite3.connect(":memory:")
                from src.service import VehicleService
                st.session_state.lab_service = VehicleService(st.session_state.lab_conn)
                st.warning("BD reiniciada.")

        items = st.session_state.lab_service.inventory()
        if items:
            import pandas as pd
            st.dataframe(pd.DataFrame([vars(x) for x in items]), use_container_width=True)
        else:
            st.info("Inventario vacío.")

        st.markdown("#### Snippet de prueba de integración")
        st.code(f'''import unittest, sqlite3
from src.service import VehicleService
class TestLab(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.svc = VehicleService(self.conn)
    def tearDown(self):
        self.conn.close()
    def test_register_and_list(self):
        vid = self.svc.register_vehicle("{brand}", "{model}", {int(year)})
        self.assertIsInstance(vid, int)
        items = self.svc.inventory()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].brand, "{brand}")
        self.assertEqual(items[0].model, "{model}")
        self.assertEqual(items[0].year, {int(year)})
''', language="python")

    else:
        st.subheader("Créditos")
        st.markdown("Hecho con ❤️ para demostrar buenas prácticas de testing en Python + Streamlit.")