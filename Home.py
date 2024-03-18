import streamlit as st

import streamlit as st

def app():
    st.set_page_config(layout="wide")  # Define o layout da página como "wide" para maximizar o espaço

    # Exibir a imagem da logo no local das páginas
    logo_path = "https://github.com/Sidneytitan/ayla/raw/main/Logo.png"
    logo_size = (200, 75)  # Tamanho da imagem (largura, altura)

    col1, col2 = st.columns([1, 4])  # Divide a largura da página em 5 partes, reservando 1 parte para o logo

    with col1:
        st.image(logo_path, width=logo_size[0])

    with col2:
        # Opções de seleção de página
        page = st.radio("Selecione uma página", ["Página 1", "Página 2", "Página 3"])

        # Conteúdo da página selecionada
        if page == "Página 1":
            st.title("Conteúdo da Página 1")
            # Adicione o conteúdo da Página 1 aqui
        elif page == "Página 2":
            st.title("Conteúdo da Página 2")
            # Adicione o conteúdo da Página 2 aqui
        elif page == "Página 3":
            st.title("Conteúdo da Página 3")
            # Adicione o conteúdo da Página 3 aqui

if __name__ == "__main__":
    app()


def main():
    st.title('Introdução ao Sistema de Cadastro de Infrações e Controle de SSMA')

    st.write("""
    No ambiente corporativo moderno, a priorização da Saúde, Segurança e Meio Ambiente (SSMA) é fundamental para o sucesso sustentável das organizações. 
    A implementação de políticas eficazes de SSMA não apenas garante a conformidade regulatória, mas também promove uma cultura de responsabilidade ambiental e bem-estar dos funcionários.

    Um componente crucial para a gestão eficaz da SSMA é a capacidade de registrar, rastrear e analisar infrações e outros incidentes relacionados à segurança, saúde e meio ambiente. 
    É aqui que entra o Sistema de Cadastro de Infrações e Controle de SSMA, uma ferramenta vital para monitorar o desempenho, identificar áreas de melhoria e mitigar riscos potenciais.
    """)

    st.header('Objetivo do Sistema:')
    st.write("""
    O Sistema de Cadastro de Infrações e Controle de SSMA tem como objetivo centralizar e automatizar o processo de registro de infrações, acidentes, doenças ocupacionais e impactos ambientais. 
    Por meio deste sistema, as organizações podem documentar detalhes cruciais sobre cada ocorrência, como data, hora, local, causas prováveis, lesões ou danos associados e ações corretivas tomadas.
    """)

    st.header('Benefícios Principais:')
    st.write("""
    1. **Melhoria da Conformidade**: O sistema facilita a conformidade com regulamentos e normas aplicáveis, fornecendo uma estrutura para documentar e monitorar o cumprimento das obrigações legais.
    2. **Identificação de Tendências e Padrões**: Ao analisar os dados coletados pelo sistema, as organizações podem identificar tendências, padrões e áreas de risco recorrentes, permitindo a implementação proativa de medidas preventivas.
    3. **Gestão de Riscos Eficiente**: Ao registrar e analisar incidentes passados, as empresas podem identificar e priorizar áreas de alto risco, direcionando recursos e esforços para mitigar esses riscos de maneira eficaz.
    4. **Criação de uma Cultura de Segurança**: Ao promover a transparência e responsabilidade no relato de incidentes, o sistema ajuda a cultivar uma cultura de segurança onde os funcionários se sintam incentivados a relatar preocupações e contribuir para um ambiente de trabalho mais seguro e saudável.
    """)

    st.header('Considerações Importantes:')
    st.write("""
    Embora o Sistema de Cadastro de Infrações e Controle de SSMA ofereça uma série de benefícios, é crucial que sua implementação seja acompanhada por treinamento adequado dos funcionários, compromisso da alta administração e uma abordagem holística para a gestão da SSMA. 
    Além disso, a confidencialidade e integridade dos dados devem ser rigorosamente mantidas para garantir a confiança dos colaboradores e a eficácia do sistema.

    Em resumo, o Sistema de Cadastro de Infrações e Controle de SSMA desempenha um papel essencial na promoção de práticas seguras, saudáveis e sustentáveis dentro das organizações, contribuindo para o bem-estar dos funcionários, a proteção do meio ambiente e o sucesso a longo prazo dos negócios.
    """)

if __name__ == '__main__':
    main()
