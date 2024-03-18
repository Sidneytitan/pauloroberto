import streamlit as st
import pandas as pd
import plotly.express as px

# Dicionário para converter nomes dos meses para português
meses_portugues = {
    'January': 'Janeiro',
    'February': 'Fevereiro',
    'March': 'Março',
    'April': 'Abril',
    'May': 'Maio',
    'June': 'Junho',
    'July': 'Julho',
    'August': 'Agosto',
    'September': 'Setembro',
    'October': 'Outubro',
    'November': 'Novembro',
    'December': 'Dezembro'
}

# Função para carregar e exibir a planilha
def mostrar_planilha(nome_arquivo, filtrar):
    try:
        # Lê os dados da planilha
        dados = pd.read_excel(nome_arquivo)

        # Verifica se existem dados na planilha
        if dados.empty:
            st.error("A planilha está vazia.")
            return

        # Adicionar filtro de data
        if filtrar:
            data_inicio = st.date_input("Selecione a data de início", pd.to_datetime('2023-01-01'), format='DD/MM/YYYY')
            data_fim = st.date_input("Selecione a data de fim", pd.to_datetime('2024-12-31'), format='DD/MM/YYYY')

            # Convertendo para datetime64[ns]
            dados['DATA'] = pd.to_datetime(dados['DATA'], errors='coerce')

            # Verifica se a conversão foi bem-sucedida
            if dados['DATA'].isnull().all():
                st.error("A coluna de DATA não está no formato correto de data.")
                return

            dados_filtrados = dados[(dados['DATA'] >= data_inicio) & (dados['DATA'] <= data_fim)]
        else:
            dados_filtrados = dados

        # Extrair o ano e o mês da coluna DATA
        dados_filtrados['ANO'] = dados_filtrados['DATA'].dt.year
        dados_filtrados['MÊS'] = dados_filtrados['DATA'].dt.month_name().map(meses_portugues)

        # Verifica se houve dados de DATA inválidos após a conversão
        if dados_filtrados['ANO'].isnull().any() or dados_filtrados['MÊS'].isnull().any():
            st.error("Há valores de data inválidos na planilha.")
            return

        # Agrupar os dados por ano, mês e tipo de evento e calcular a soma
        dados_agrupados = dados_filtrados.groupby(['ANO', 'MÊS', 'CLASS. EVENTO']).size().unstack(fill_value=0).reset_index()

        # Reorganizar os dados para ter uma coluna separada para o ano e outra para o mês
        dados_melted = pd.melt(dados_agrupados, id_vars=['ANO', 'MÊS'], var_name='Tipo de Evento', value_name='Quantidade')

        # Plotar gráfico
        fig = px.bar(dados_melted, x='MÊS', y='Quantidade', color='Tipo de Evento', barmode='group', facet_col='ANO',
                     text='Quantidade', title='Quantidade de Eventos por Ano e Mês')
        fig.update_traces(textposition='outside')
        fig.update_layout(
            yaxis_title='Quantidade',
            legend_title='Tipo de Evento',
            height=600,
            width=800
        )

        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar a planilha: {e}")

def main():
    st.title("Visualizador de Planilha")
    st.write("Este é um aplicativo simples para visualizar a quantidade de eventos (ACIDENTE NÍVEL 1, ACIDENTE NÍVEL 2, ACIDENTE NÍVEL 3 e INCIDENTE) por ano e mês.")

    # Localização do arquivo
    excel_file = 'SSMA.xlsx'

    # Adicionar botão de filtrar
    filtrar = st.checkbox("Filtrar por data")

    # Exibe o gráfico
    mostrar_planilha(excel_file, filtrar)

if __name__ == "__main__":
    main()
