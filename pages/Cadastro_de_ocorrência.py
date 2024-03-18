import streamlit as st
import pandas as pd
from datetime import datetime

# Carregar dados do Excel
excel_file = 'SSMA.xlsx'
selected_sheet_name = 'Sheet1'


# Função para carregar dados das ocorrências
def load_data():
    try:
        df = pd.read_excel(excel_file, sheet_name=selected_sheet_name)
    except FileNotFoundError:
        st.error(f"Arquivo {excel_file} não encontrado. Um novo arquivo será criado.")
        df = pd.DataFrame(
            columns=["DATA", "HORA", "CLASS. EVENTO", "DESC. EVENTO", "UNIDADE", "TP.OCORRENCIA", "EMBARCADOR",
                     "OCORRENCIA", "OPERAÇÃO", "VOL.", "CAVALO", "CARRETA", "MOTORISTA", "TRANSPORTADORA", "NF",
                     "CLIENTE", "MÊS DO EVENTO", "ANO DO EVENTO"])
    return df


# Função para carregar dados dos usuários
def load_users():
    try:
        users_df = pd.read_excel('usuarios.xlsx')
    except FileNotFoundError:
        st.error("Arquivo de usuários não encontrado.")
        return None
    return users_df


# Função para autenticar usuário
def authenticate(username, password):
    users_df = load_users()
    if users_df is None:
        return False

    user_data = users_df[users_df['usuario'] == username]
    if not user_data.empty:
        stored_password = user_data.iloc[0]['senha']
        if str(stored_password) == str(password):
            return True
    return False


# Função principal
def main():
    st.title("")
    # Exibir a imagem da logo no sidebar
    logo_path = "https://github.com/Sidneytitan/ayla/raw/main/Logo.png"
    logo_size = (200, 40)  # Tamanho da imagem (largura, altura)

    st.image(logo_path, width=logo_size[0], caption='')

    # Verifica se o usuário está autenticado
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # Tela de login
        username = st.sidebar.text_input("Usuário")
        password = st.sidebar.text_input("Senha", type="password")

        if st.sidebar.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.sidebar.error("Credenciais inválidas. Tente novamente.")
    else:
        # Conteúdo após o login
        opcao = st.sidebar.selectbox("Selecione uma opção:", ["Mostrar Formulário", "Mostrar Tabela"])
        df = load_data()

        if opcao == "Mostrar Formulário":
            # Coletar dados da ocorrência através de um formulário
            data = st.date_input("Data da ocorrência:", value=datetime.today())
            hora = st.time_input("Hora da ocorrência:")
            class_evento_options = ["Leve", "Medio", "Grave"]
            class_evento = st.selectbox("Classificação do evento:", class_evento_options)
            desc_evento = st.text_input("Descrição do evento:")
            unidade_options = ["CUBATÃO", "BARUERI", "UBERLÂNDIA", "PAULINIA"]
            unidade = st.selectbox("Unidade:", unidade_options)
            tipo_ocorrencia_options = ["MÉDIA", "EMERGÊNCIA"]
            tp_ocorrencia = st.selectbox("Tipo de ocorrência:", tipo_ocorrencia_options)
            embarcador_options = ["IPIRANGA", "TOTAL"]
            embarcador = st.selectbox("Embarcador:", embarcador_options)
            ocorrencia_options = ["AVA", "CONTAMINAÇÃO", "DERRAME", "INCIDENTE","ROUBO/FURTO"]
            ocorrencia = st.selectbox("Ocorrência:", ocorrencia_options)
            operacao_options = ["OUTBOUND", "INBOUND"]
            operacao = st.selectbox("Operação:", operacao_options)
            vol = st.number_input("Volume:", min_value=0)
            cavalo = st.text_input("Cavalo:")
            carreta = st.text_input("Carreta:")
            motorista = st.text_input("Motorista:")
            transportadora = st.text_input("Transportadora:")
            nf = st.text_input("Nota Fiscal:")
            cliente = st.text_input("Cliente:")

            # Botão para cadastrar a ocorrência
            if st.button("Cadastrar Ocorrência"):
                # Criar um novo registro de ocorrência
                novo_registro = pd.DataFrame({
                    "DATA": [datetime.combine(data, hora)],  # Combinar data e hora
                    "CLASS. EVENTO": [class_evento],
                    "DESC. EVENTO": [desc_evento],
                    "UNIDADE": [unidade],
                    "TP.OCORRENCIA": [tp_ocorrencia],
                    "EMBARCADOR": [embarcador],
                    "OCORRENCIA": [ocorrencia],
                    "OPERAÇÃO": [operacao],
                    "VOL.": [vol],
                    "CAVALO": [cavalo],
                    "CARRETA": [carreta],
                    "MOTORISTA": [motorista],
                    "TRANSPORTADORA": [transportadora],
                    "NF": [nf],
                    "CLIENTE": [cliente],

                })
                # Adicionar o novo registro ao DataFrame
                df = pd.concat([df, novo_registro], ignore_index=True)
                # Salvar os dados atualizados no arquivo Excel
                df.to_excel(excel_file, index=False)
                st.success("Ocorrência cadastrada com sucesso!")

        elif opcao == "Mostrar Tabela":
            # Exibir a tabela de ocorrências
            st.header("Ocorrências Cadastradas")
            st.write(df)


if __name__ == "__main__":
    main()
