import streamlit as st
import pandas as pd

def view_excel_data():
    try:
        df = pd.read_excel("motoristas.xlsx")
        st.dataframe(df)
    except FileNotFoundError:
        st.warning("Arquivo 'motoristas.xlsx' não encontrado. Por favor, verifique se o arquivo está no mesmo diretório do script Python.")

def main():
    st.title('Visualizador de Dados do Excel')
    st.write("Aqui você pode visualizar os dados do arquivo Excel de motoristas.")

    if st.button("Visualizar Excel"):
        st.write("Dados do arquivo Excel:")
        view_excel_data()

if __name__ == '__main__':
    main()
