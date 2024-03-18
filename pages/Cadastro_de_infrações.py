import streamlit as st
import pandas as pd
import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
from reportlab.lib.utils import ImageReader



# Função para gerar PDF
def generate_pdf(driver_list, monitor_name, font_size, filial, operacao, periodo_infra, custom_text=None,
                 text_position=(0, 0), text_font_size=12):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as buffer:
        cnv = canvas.Canvas(buffer.name, pagesize=A4)
        cnv.setFontSize(font_size)

        # Desenha o cabeçalho
        x_start = 50
        y = 700  # Posição vertical inicial do cabeçalho

        # Adiciona informações da filial, operação e período de infrações ao cabeçalho
        if filial or operacao or periodo_infra:
            x_filial = 100  # Posição X inicial da filial
            x_operacao = 250  # Posição X inicial da operação
            x_periodo_infra = 400  # Posição X inicial do período de infrações
            y_header = y  # Posição Y do cabeçalho

            header_info = ""
            if filial:
                header_info += f"Filial: {filial} "
            if operacao:
                header_info += f"Operação: {operacao} "
            if periodo_infra:
                header_info += f"Período de Infrações: {periodo_infra}"

            # Desenha as informações do cabeçalho
            cnv.setFont("Helvetica-Bold", font_size)  # Define a fonte como negrito
            cnv.drawString(x_filial, y_header, "FILIAL")
            cnv.drawString(x_operacao, y_header, "OPERAÇÃO")
            cnv.drawString(x_periodo_infra, y_header, "PERÍODO DE INFRAÇÕES")
            cnv.setFont("Helvetica", font_size)  # Retorna à fonte padrão

            # Desenha as entradas de filial, operação e período de infrações logo abaixo do cabeçalho
            y -= 1
            if filial or operacao or periodo_infra:
                x_input_filial = 100  # Posição X da entrada da filial
                x_input_operacao = 250  # Posição X da entrada da operação
                x_input_periodo_infra = 400  # Posição X da entrada do período de infrações
                input_info = ""
                if filial:
                    input_info += f"{filial} "
                if operacao:
                    input_info += f"{operacao} "
                if periodo_infra:
                    # Converte as datas para strings antes de desenhar
                    periodo_infra_str = f"{periodo_infra[0].strftime('%d/%m/%Y')} - {periodo_infra[1].strftime('%d/%m/%Y')}"
                    input_info += periodo_infra_str
                # Desenha as entradas
                cnv.drawString(x_input_filial, y - 20, filial)
                cnv.drawString(x_input_operacao, y - 20, operacao)
                cnv.drawString(x_input_periodo_infra, y - 20, periodo_infra_str)

        # Desenha os detalhes de cada motorista
        y -= 60  # Aumenta o espaço entre os inputs e o cabeçalho dos motoristas

        # Desenha o cabeçalho do cadastro de motorista
        cnv.setFont("Helvetica-Bold", font_size)  # Define a fonte como negrito
        cnv.drawString(x_start - 2, y, "ID")
        cnv.drawString(x_start + 26, y, "Nome")
        cnv.drawString(x_start + 200, y, "CPF")
        cnv.drawString(x_start + 280, y, "Infração")
        cnv.drawString(x_start + 370, y, "Data")
        cnv.drawString(x_start + 430, y, "Horário")
        cnv.drawString(x_start + 470, y, "Tipo de Contato")
        y -= 6  # Adicione um espaço entre o cabeçalho e os inputs do cadastro do motorista

        for driver_data in driver_list:
            y -= 12  # Move para a próxima linha
            cnv.setFont("Helvetica", font_size)  # Define a fonte como padrão
            cnv.drawString(x_start - 2, y, str(driver_data.get('ID', '')))
            cnv.drawString(x_start + 26, y, str(driver_data.get('Nome do Motorista', '')))
            cnv.drawString(x_start + 200, y, str(driver_data.get('CPF', '')))
            cnv.drawString(x_start + 280, y, str(driver_data.get('Infração', '')))
            cnv.drawString(x_start + 370, y, str(driver_data.get('Data', '')))
            cnv.drawString(x_start + 430, y, str(driver_data.get('Horário', '')))
            cnv.drawString(x_start + 470, y, str(driver_data.get('Tipo de Contato', '')))

        # Adiciona a imagem PNG (logo)
        logo_path = "https://github.com/Sidneytitan/ayla/raw/main/Logo.png"
        logo_size = (80, 30)  # Tamanho da imagem (largura, altura)
        logo_position = (20, A4[1] - logo_size[1] - 40)  # Posição da imagem (horizontal, vertical)
        image = ImageReader(logo_path)
        cnv.drawImage(image, logo_position[0], logo_position[1], width=logo_size[0], height=logo_size[1])

        # Mostra os detalhes do motorista monitor
        if monitor_name:
            st.subheader("Detalhes do Motorista Monitor")
            # Adiciona o texto "Motorista Monitor" em negrito
            cnv.setFont("Helvetica-Bold", font_size)  # Define a fonte como negrito
            text_width = cnv.stringWidth(f"Motorista Monitor")
            x_position = (A4[0] - text_width) / 2  # Centraliza horizontalmente
            y -= 15
            cnv.drawString(x_position, y - 60, f"Motorista Monitor")
            # Adiciona o nome do motorista monitor como texto normal
            cnv.setFont("Helvetica", font_size)  # Retorna à fonte padrão
            cnv.drawString(x_position - 30, y - 50, f"{monitor_name}")

            # Adiciona um risco com a distância especificada
            risco_x = x_position - 35
            risco_y = y - 40  # Ajuste necessário
            cnv.line(risco_x, risco_y, risco_x + text_width + 90, risco_y)

        # Adiciona um texto personalizado, se fornecido
        if custom_text:
            cnv.setFont("Helvetica", text_font_size)  # Define a fonte e o tamanho do texto
            cnv.drawString(text_position[0], text_position[1], custom_text)

        cnv.save()

        buffer.seek(0)
        pdf = buffer.read()

    return pdf


# Função para salvar os dados do cadastro de motoristas no arquivo Excel
def save_data_to_excel(driver_list):
    # Cria um DataFrame com os dados dos motoristas
    df = pd.DataFrame(driver_list)

    # Salva o DataFrame em um arquivo Excel
    excel_file_name = "motoristas.xlsx"
    if os.path.exists(excel_file_name):
        # Carrega o arquivo Excel existente
        existing_df = pd.read_excel(excel_file_name)
        # Concatena os DataFrames (existente e novo)
        df = pd.concat([existing_df, df], ignore_index=True)

    # Salva o DataFrame no arquivo Excel
    df.to_excel(excel_file_name, index=False)

    return excel_file_name


# Função para verificar o login do usuário
def login(username, password):
    # Carrega as credenciais dos usuários do arquivo Excel
    users_df = pd.read_excel("usuariosinfracoes.xlsx")

    # Verifica se o usuário e a senha fornecidos estão na planilha de usuários
    if username in users_df["usuario"].values:
        correct_password = users_df.loc[users_df["usuario"] == username, "senha"].iloc[0]
        if password == correct_password:
            return True
    return False


def app():
    st.sidebar.title('')  # se eu quiser colocar texto no login
    # Exibir a imagem da logo no sidebar
    logo_path = "https://github.com/Sidneytitan/ayla/raw/main/Logo.png"
    logo_size = (200, 40)  # Tamanho da imagem (largura, altura)

    st.image(logo_path, width=logo_size[0], caption='')

    # Tela de Login
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:

        username = st.sidebar.text_input("Usuário")
        password = st.sidebar.text_input("Senha", type="password")
        if st.sidebar.button("Login"):
            if login(username, password):
                st.session_state['logged_in'] = True
                st.success(f"Bem-vindo, {username}!")
            else:
                st.error("Usuário ou senha incorretos.")

    if st.session_state['logged_in']:
        # Cadastro de Motoristas e Geração de PDF
        st.title('CADASTRO DE INFRAÇÕES')

        if 'driver_list' not in st.session_state:
            st.session_state.driver_list = []

        # Cadastro de Filial, Operação e Período de Infrações
        st.subheader("")  # SE EU QUISER COLOCAR UM TEXTO EM CIMA DE FILIAL E OPERAÇÃO
        col1, col2, col3 = st.columns(3)  # Divide em três colunas

        with col1:
            # Agora utilizamos selectbox para permitir a seleção da filial
            filial_options = ['Barueri', 'Paulinia', 'Uberlândia']
            filial = st.selectbox('Filial', filial_options)

        with col2:
            # Utilizamos selectbox para permitir a seleção da operação
            operacao_options = ['Distribuição', 'Cotela e Transferencia']
            operacao = st.selectbox('Operação', operacao_options)

        with col3:
            hoje = datetime.date.today()
            data_inicial_default = hoje - datetime.timedelta(days=365)  # 1 ano atrás
            data_final_default = hoje  # Hoje
            periodo_infra = st.date_input('Período', value=(data_inicial_default, data_final_default),
                                          key="periodo_infra")

        # Carregar nomes dos motoristas do arquivo Excel
        df_nomes = pd.read_excel('LISTAMOTSSMA.xlsx')

        # Filtrar nomes dos motoristas de acordo com a filial selecionada
        filtered_driver_names = df_nomes[df_nomes['Filial'] == filial]['Nome do Motorista'].tolist()

        # Adiciona um motorista
        st.subheader("Cadastro de Motorista")
        col1, col2 = st.columns(2)  # Divide em duas colunas

        with col1:
            id_motorista = st.text_input('ID do Motorista')
            nome_motorista = st.selectbox('Nome do Motorista', filtered_driver_names)
            # Atualiza o CPF automaticamente com base no nome do motorista selecionado
            cpf_options = df_nomes.loc[df_nomes["Nome do Motorista"] == nome_motorista, "CPF"].tolist()
            cpf = st.selectbox('CPF', cpf_options)

        with col2:
            infracao_options = ['Sem EPI', 'Excesso veloc. PM', 'Celular']
            infracao = st.selectbox('Infração', infracao_options)
            data = st.date_input('Data')
            horario = st.time_input('Horário')
            tipo_contato_options = ['Telefone', 'E-mail', 'WhatsApp']
            tipo_contato = st.selectbox('Tipo de Contato', tipo_contato_options)

        if st.button('Adicionar Motorista'):
            data_dict = {
                'ID': id_motorista,
                'Nome do Motorista': nome_motorista,
                'CPF': cpf,
                'Infração': infracao,
                'Data': data,
                'Horário': horario,
                'Tipo de Contato': tipo_contato
            }

            st.session_state.driver_list.append(data_dict)
            st.success("Motorista adicionado com sucesso!")

        # Exibe os motoristas cadastrados
        if st.session_state.driver_list:
            st.subheader("Motoristas Cadastrados")
            for i, driver_data in enumerate(st.session_state.driver_list):
                st.markdown('---')
                st.subheader(f"Motorista {i + 1}")
                st.write(f"ID: {driver_data['ID']}")
                st.write(f"Nome: {driver_data['Nome do Motorista']}")
                st.write(f"CPF: {driver_data['CPF']}")
                st.write(f"Infração: {driver_data['Infração']}")
                st.write(f"Data: {driver_data['Data']}")
                st.write(f"Horário: {driver_data['Horário']}")
                st.write(f"Tipo de Contato: {driver_data['Tipo de Contato']}")

                # Adicionar botão de exclusão do motorista
                if st.button(f"Excluir Motorista {i + 1}"):
                    st.session_state.driver_list.pop(i)
                    st.success("Motorista excluído com sucesso!")
                    break  # Termina o loop após a exclusão

        # Cadastro do Motorista Monitor
        st.subheader("Selecione o motorista monitor")
        monitor_name_options = ['ALEX LUIZ DE SOUZA NUNES', 'VANDERLEI DE OLIVEIRA PENTEADO', 'JOVAIR ROSA RODRIGUES']
        monitor_name = st.selectbox('Nome do Motorista Monitor', monitor_name_options)

        # Mostra os detalhes do motorista monitor
        if monitor_name and st.session_state.driver_list:
            st.subheader("Detalhes do Motorista Monitor")
            st.write(f"Nome do Motorista Monitor: {monitor_name}")

        # Botão para gerar PDF e Salvar Excel
        if st.button('Gerar PDF e Salvar Excel'):
            if st.session_state.driver_list:
                # Adiciona um texto personalizado ao PDF
                custom_text = "RELATÓRIO DE COMUNICAÇÃO DE INFRAÇÕES."
                # Define a posição do texto
                text_position = (190, 780)  # Posição (x, y) em pontos (72 pontos = 1 polegada)
                # Define o tamanho da fonte do texto
                text_font_size = 12
                # Gerar PDF
                pdf = generate_pdf(st.session_state.driver_list, monitor_name, 8, filial, operacao, periodo_infra,
                                   custom_text, text_position, text_font_size)

                # Salvar dados no Excel
                excel_file_name = save_data_to_excel(st.session_state.driver_list)

                st.download_button(label="Baixar PDF", data=pdf, file_name="SSMA_pdf.pdf", mime="application/pdf")
                st.success("Dados salvos com sucesso!")


if __name__ == '__main__':
    app()
