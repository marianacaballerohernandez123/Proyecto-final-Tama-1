import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.sidebar.title("Navegación")


def pagina_principal():
    st.title("Página Principal")
    st.write("Bienvenido a la aplicación de demostración")
    st.write("Usa el menú de la izquierda para navegar entre las páginas")


def visualizar_datos():
    st.title("Visualización de Datos")
    st.write("Carga un archivo CSV para visualizar los datos.")
    archivo_cargado = st.file_uploader("Elige un archivo CSV", type="csv")

    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.write("Datos del archivo CSV:")
        st.write(df)
        st.write("Estadísticas descriptivas:")
        st.write(df.describe())


def graficos_interactivos():
    st.title("Gráficos Interactivos")
    st.write("Carga un archivo CSV para crear gráficos interactivos")
    archivo_cargado = st.file_uploader("Elige un archivo CSV", type="csv", key="2")

    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.write("Elige una columna para el eje X:")
        eje_x = st.selectbox("Eje X", df.columns)
        st.write("Elige una columna para el eje Y:")
        eje_y = st.selectbox("Eje Y", df.columns)

        if st.button("Crear Gráfico"):
            fig = px.bar(df, x=eje_x, y=eje_y, title=f"{eje_y} por {eje_x}")
            st.plotly_chart(fig)


def filtrar_datos():
    st.title("Filtrar Datos")
    st.write("Carga un archivo CSV para aplicar filtros a los datos")
    archivo_cargado = st.file_uploader("Elige un archivo CSV", type="csv", key="3")

    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.write("Datos del archivo CSV:")
        st.write(df)
        columna = st.selectbox("Selecciona una columna para filtrar", df.columns)
        valores_unicos = df[columna].unique()
        valor_filtro = st.multiselect(
            "Selecciona los valores para filtrar", valores_unicos
        )

        if valor_filtro:
            df_filtrado = df[df[columna].isin(valor_filtro)]
            st.write("Datos filtrados:")
            st.write(df_filtrado)


def agrupar_datos():
    st.title("Agrupar Datos")
    st.write("Carga un archivo CSV para realizar agrupaciones")
    archivo_cargado = st.file_uploader("Elige un archivo CSV", type="csv", key="4")

    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.write("Datos del archivo CSV:")
        st.write(df)
        columna_agrupacion = st.selectbox(
            "Selecciona una columna para agrupar", df.columns
        )
        columna_calculo = st.selectbox(
            "Selecciona una columna para calcular (suma)", df.columns
        )

        if st.button("Agrupar Datos"):
            df_agrupado = (
                df.groupby(columna_agrupacion)[columna_calculo].sum().reset_index()
            )
            st.write("Datos agrupados:")
            st.write(df_agrupado)


def correlacion_datos():
    st.title("Correlación de Datos")
    st.write("Carga un archivo CSV para analizar correlaciones")
    archivo_cargado = st.file_uploader("Elige un archivo CSV", type="csv", key="5")

    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.write("Datos del archivo CSV:")
        st.write(df)
        columnas_numericas = df.select_dtypes(include=["float64", "int64"]).columns
        st.write("Selecciona dos columnas numéricas para calcular la correlación:")
        col1 = st.selectbox("Columna 1", columnas_numericas, key="col1")
        col2 = st.selectbox("Columna 2", columnas_numericas, key="col2")

        if st.button("Calcular Correlación"):
            correlacion = df[col1].corr(df[col2])
            st.write(f"La correlación entre {col1} y {col2} es: {correlacion}")


def descripcion_estadistica():
    st.title("Descripción Estadística Mejorada")
    st.write("Carga un archivo CSV para obtener una descripción estadística completa.")
    archivo_cargado = st.file_uploader("Elige un archivo CSV", type="csv", key="6")

    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.write("Datos del archivo CSV:")
        st.write(df)

        # Descripción estadística básica
        st.subheader("1. Descripción estadística básica")
        st.write(df.describe(include="all"))

        # Identificación de valores faltantes
        st.subheader("2. Identificación de valores faltantes")
        valores_faltantes = df.isnull().sum()
        st.write("Valores faltantes por columna:")
        st.write(valores_faltantes[valores_faltantes > 0])

        if valores_faltantes.any():
            st.write(
                "Puedes rellenar los valores faltantes con la mediana para columnas numéricas "
                "y con la moda para columnas no numéricas."
            )
            if st.button("Rellenar valores faltantes"):
                # Tratamiento de valores faltantes
                for col in df.select_dtypes(include=["float64", "int64"]):
                    df[col] = df[col].fillna(df[col].median())
                for col in df.select_dtypes(exclude=["float64", "int64"]):
                    if not df[col].mode().empty:
                        df[col] = df[col].fillna(df[col].mode()[0])
                st.write("Valores faltantes tratados con éxito.")
                st.write("Datos después del tratamiento:")
                st.write(df)


def analizar_columnas():
    st.title("Análisis Personalizado de Columnas")
    st.write("Carga un archivo CSV para seleccionar las columnas que deseas analizar.")
    archivo_cargado = st.file_uploader("Elige un archivo CSV", type="csv", key="7")

    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.write("Datos del archivo CSV:")
        st.write(df)

        # Permitir seleccionar columnas para agrupar
        columnas_seleccionadas = st.multiselect(
            "Selecciona las columnas para analizar", df.columns
        )

        if len(columnas_seleccionadas) >= 2:
            st.write("Seleccionaste las columnas:", columnas_seleccionadas)

            # Realizar agrupación o análisis según las columnas seleccionadas
            if st.button("Analizar Datos"):
                try:
                    # Agrupar los datos seleccionados y contar las ocurrencias
                    tabla = (
                        df.groupby(columnas_seleccionadas)
                        .size()
                        .reset_index(name="cantidad")
                    )
                    st.write("Análisis agrupado de las columnas seleccionadas:")
                    st.write(tabla)
                except Exception as e:
                    st.write(f"Ocurrió un error: {e}")
        else:
            st.write(
                "Por favor, selecciona al menos dos columnas para realizar el análisis."
            )


pagina = st.sidebar.selectbox(
    "Selecciona una página",
    [
        "Página Principal",
        "Visualización de Datos",
        "Gráficos Interactivos",
        "Filtrar Datos",
        "Agrupar Datos",
        "Correlación de Datos",
        "Descripción Estadística Mejorada",
        "Análisis Personalizado de Columnas",  # Nueva página añadida
    ],
)

if pagina == "Página Principal":
    pagina_principal()
elif pagina == "Visualización de Datos":
    visualizar_datos()
elif pagina == "Gráficos Interactivos":
    graficos_interactivos()
elif pagina == "Filtrar Datos":
    filtrar_datos()
elif pagina == "Agrupar Datos":
    agrupar_datos()
elif pagina == "Correlación de Datos":
    correlacion_datos()
elif pagina == "Descripción Estadística Mejorada":
    descripcion_estadistica()
elif pagina == "Análisis Personalizado de Columnas":
    analizar_columnas()  # Llamar a la nueva página
