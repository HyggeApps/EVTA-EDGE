import streamlit as st
import json
import uuid
from streamlit_slickgrid import slickgrid, Formatters, Filters, FieldType, OperatorType, StreamlitSlickGridFormatters, ExportServices
import warnings
import time
warnings.filterwarnings("ignore")
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from pymongo import errors
import sys
sys.path.append('../')
import Libs.cadastros as cadastros
import yaml
from urllib.parse import quote_plus
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities import LoginError
import streamlit_authenticator as stauth
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import pandas as pd
import altair as alt
import Libs.descricoes as desc
import Libs.resumo as res
import random
import string

st.set_page_config(page_title="HYGGE | EDGE - Checklist", layout="wide")

image1 = 'https://hygge.eco.br/wp-content/uploads/2025/03/marrom_escolhido.png'
image_width_percent = 60

html_code1 = f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 100%; ">
        <img src="{image1}" alt="Image" style="width: {image_width_percent}%;"/>
    </div>
"""
st.sidebar.markdown(html_code1, unsafe_allow_html=True)


image2 = 'https://hygge.eco.br/wp-content/uploads/2025/03/RECORTADO-MARROM-SLOGAN.png'
image_width_percent = 80

html_code2 = f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 100%; ">
        <img src="{image2}" alt="Image" style="width: {image_width_percent}%;"/>
    </div>
"""
st.sidebar.markdown(html_code2, unsafe_allow_html=True)

custom_css = """
    <style>
    .main {
        max-width: 80%;
        margin: 0 auto;
    }
    section[data-testid="stSidebar"] {
        width: 400px !important;
    }
    </style>
"""

st.sidebar.write('----')

def get_ancestor_by_depth(item, target_depth):
    parent_id = item.get("__parent")
    while parent_id is not None:
        parent = id_map.get(parent_id)
        if parent and parent.get("__depth") == target_depth:
            return parent
        parent_id = parent.get("__parent") if parent else None
    return None

def conecta_banco():
    username = quote_plus(st.secrets['database']['username'])
    password = quote_plus(st.secrets['database']['password'])
    uri = f"mongodb+srv://{username}:{password}@evta.lxx4c.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"
    return MongoClient(uri, server_api=ServerApi('1'))

client = conecta_banco()
db = client['certificacoes']

# Criar um arquivo temporário com os usuários do MongoDB
temp_config_path = cadastros.create_temp_config_from_mongo(db)

# Carregar e verificar as chaves no arquivo config.yaml
config_data = cadastros.load_config_and_check_or_insert_cookies(temp_config_path)

with st.sidebar:
    # Loading config file
    with open(temp_config_path, 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)


    # Creating the authenticator object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # Só tenta fazer o login quando o botão for pressionado
    try:
        aux = authenticator.login()
    except LoginError as e:
        st.error(e)
    
    # Autenticando usuário
    if st.session_state['authentication_status']:
        if 'admin' in st.session_state["roles"]:
            st.sidebar.info(f"Bem-vindo(a), **{st.session_state['name']}**!")
            st.sidebar.info('Este é o ambiente de **admin** para preenchimento das informações referentes ao check-list HYGGE para certificação do seu projeto.')
        else:
            st.sidebar.info(f"Bem-vindo(a), **{st.session_state['name']}**!")
            st.sidebar.info('Este é o ambiente de **usuário** para preenchimento das informações referentes ao check-list HYGGE para certificação do seu projeto.')
            
        # Persistência da seleção do projeto: se o projeto for alterado, reseta os dados e recarrega a aplicação
        if "projeto_selecionado" not in st.session_state:
            st.session_state.projeto_selecionado = cadastros.selecionar_projeto_usuario(client, st.session_state["username"])
        else:
            novo_projeto = cadastros.selecionar_projeto_usuario(client, st.session_state["username"])
            if novo_projeto != st.session_state.projeto_selecionado:
                st.session_state.projeto_selecionado = novo_projeto
                # Reseta as variáveis dependentes para forçar o recarregamento dos dados
                st.session_state.pop("rows", None)
                st.session_state.pop("grid_key", None)
                st.rerun()

        alias_selecionado = cadastros.selecionar_alias_usuario(client, st.session_state.projeto_selecionado, "admin")
        itens_json = cadastros.get_from_3projetos(alias_selecionado, 'creditos_default.json')



if st.session_state['authentication_status']:
    @st.cache_data
    def read_json_creditos(path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    data_json = read_json_creditos(itens_json)

    # Função auxiliar para gerar IDs únicos (utilizando UUID)
    def gen_id():
        return str(uuid.uuid4())

    # Variável global para contar os IDs
    id_counter = 0
    def create_node(title, depth, parent_id=None):
        global id_counter
        if depth == 3:
            node = {
                "id": id_counter,
                "title": title,
                "__depth": depth,
                "categoria": "",
                "credito": "",
                "tipo": "",
                "item": "",
                "situacao": "🟥 Pendente",
                "arquivos": "",
                "observacao": "",
                "atribuicao": "",
                "comentario_hygge": "",
                "revisao": "R01",
                "update_status": "",
                "percentual": 0
            }
        else:
            node = {
                "id": id_counter,
                "title": title,
                "__depth": depth,
                "categoria": "",
                "credito": "",
                "tipo": "",
                "item": "",
                "situacao": "",
                "arquivos": "",
                "observacao": "",
                "atribuicao": "",
                "comentario_hygge": "",
                "revisao": "",
                "update_status": "",
                "percentual": 0
            }

        if parent_id is not None:
            node["__parent"] = parent_id
        id_counter += 1
        return node

    # Mapeamento para exibir os nomes corretos no nível de etapa
    tipo_mapping = {
        "projeto": "01. Projeto",
        "obra": "02. Obra",
        "pos-construcao": "03. Pós construção"
    }

    # Constrói a árvore manualmente com 4 níveis
    _rows = []  # Dados iniciais

    # Nível 0: Categoria
    for categoria, cat_data in data_json.items():
        cat_node = create_node(categoria, 0)
        _rows.append(cat_node)
        cat_id = cat_node["id"]

        # Processa créditos
        if "creditos" in cat_data:
            for credit_key, credit_detail in cat_data["creditos"].items():
                credit_node = create_node(credit_key, 1, parent_id=cat_id)
                _rows.append(credit_node)
                credit_id = credit_node["id"]

                # Para cada etapa (Projeto, Obra, Pós construção)
                for subkey in ["projeto", "obra", "pos-construcao"]:
                    items = credit_detail.get(subkey, [])
                    if items:
                        subtype_label = tipo_mapping.get(subkey, subkey)
                        subtype_node = create_node(subtype_label, 2, parent_id=credit_id)
                        _rows.append(subtype_node)
                        subtype_id = subtype_node["id"]

                        # Cada item individual (nível 3)
                        for item in items:
                            item_node = create_node(item, 3, parent_id=subtype_id)
                            _rows.append(item_node)

    # Inicializa st.session_state.rows apenas se ainda não existir
    if "rows" not in st.session_state:
        st.session_state.rows = _rows

    # Define o nome da collection baseado no projeto selecionado.
    collection_name = f"{st.session_state.projeto_selecionado} - EDGE"
    id_map = {node["id"]: node for node in st.session_state.rows}
    # Verifica se a collection já existe
    if collection_name in db.list_collection_names():
        stored_rows = list(db[collection_name].find({}, {"_id": 0}))
        # Ajusta os registros para que contenham os campos usados na árvore
        for row in stored_rows:
            row["__depth"] = row.get("depth", row.get("__depth", 0))
            if "__parent" not in row and row.get("parent"):
                row["__parent"] = row.get("parent")
        # Ordena pela sequência do "id"
        stored_rows.sort(key=lambda n: n.get("id", 0))
        st.session_state.rows = stored_rows
        id_map = {node["id"]: node for node in st.session_state.rows}
        
    else:
        # Se a collection não existir, cria-a e insere os dados default
        db.create_collection(collection_name)
        default_rows = []
        for item in st.session_state.rows:
            if item.get("__depth", 0) == 0:
                categoria = item.get("title", "")
            else:
                categoria_node = get_ancestor_by_depth(item, 0)
                categoria = categoria_node.get("title", "") if categoria_node else ""
            
            credito_node = get_ancestor_by_depth(item, 1)
            credito = credito_node.get("title", "") if credito_node else ""
            
            tipo_node = get_ancestor_by_depth(item, 2)
            tipo = tipo_node.get("title", "") if tipo_node else ""
            if item.get("__depth", 0) == 3:
                update_data = {
                    "id": item["id"],
                    "title": item.get("title", ""),
                    "depth": item.get("__depth", 0),  # salvando a profundidade com outra chave
                    "__parent": item.get("__parent"),  # importante para manter a hierarquia
                    "categoria": categoria,
                    "credito": credito,
                    "tipo": tipo,
                    "item": item.get("title", ""),
                    "situacao": "🟥 Pendente",
                    "revisao": "R01",
                    "observacao": "",
                    "comentario_hygge": "",
                    "atribuicao": "",
                    "arquivos": "",
                    "update_status": "",
                    "percentual": 0
                }
                default_rows.append(update_data)
            else:    
                update_data = {
                    "id": item["id"],
                    "title": item.get("title", ""),
                    "depth": item.get("__depth", 0),  # salvando a profundidade com outra chave
                    "__parent": item.get("__parent"),  # importante para manter a hierarquia
                    "categoria": categoria,
                    "credito": credito,
                    "tipo": tipo,
                    "item": item.get("title", ""),
                    "situacao": "",
                    "revisao": "",
                    "observacao": "",
                    "comentario_hygge": "",
                    "atribuicao": "",
                    "arquivos": "",
                    "update_status": "",
                    "percentual": 0
                }
                default_rows.append(update_data)
        
        if default_rows:
            db[collection_name].insert_many(default_rows)
        else:
            st.warning("Não há dados default para inserir.")
        
        st.session_state.rows = default_rows

    def get_db_options(collection_name):
        # Consulta opções "atribuicao" existentes e filtra valores não vazios
        options = db[collection_name].distinct("atribuicao")
        return sorted([opt for opt in options if opt])

    @st.dialog("Detalhes da Seleção", width="large")
    def show_dialog(item, permission):
        global db, collection_name  # Acesso às variáveis globais definidas no app.py
        title = item.get("title", "")
        depth = item.get("__depth", 0)
        st.write('---')
        
        if 'Energia' in title:
            st.title('Categoria de Energia')
            st.info("A eficiência energética é uma das três categorias de recursos que compõem o padrão EDGE, com requisito mínimo de eficiência de 20%, que deve ser conquistado através de medidas de redução de consumo energético do edifício ou de geração de energia.")
            st.info("Para fins de certificação, a equipe de projeto e construção deve revisar os requisitos para as medidas apresentadas e fornecer as informações solicitadas.")
        elif 'Água' in title:
            st.title('Categoria de Água')
            st.info("A eficiência hídrica é uma das três categorias de recursos que compõem o padrão EDGE, com requisito mínimo de eficiência de 20%, que deve ser conquistado através de medidas de redução de consumo de água potável do empreendimento.")
            st.info("Para fins de certificação, a equipe de projeto e construção deve revisar os requisitos para as medidas apresentadas e fornecer as informações solicitadas.")
        elif "Materiais" in title:
            st.title('Categoria de Materiais')
            st.info("A eficiência de materiais é uma das três categorias de recursos que compõem o padrão EDGE, com requisito mínimo de eficiência de 20%, que deve ser conquistado através da melhoria do sistema construtivo para menor incorporação de carbono na edificação.")
            st.info("Para fins de certificação, a equipe de projeto e construção deve revisar os requisitos para as medidas apresentadas e fornecer as informações solicitadas.")
        elif depth == 1:
            st.info("O **'*'** ao lado do título representa que trata-se de um pré-requisito obrigatório para a certificação.")
            st.title(f"Crédito {title}")
            desc.descricoes_creditos(title)
            
        elif depth == 2:
            if 'Projeto' in title: 
                st.title("Etapa de Projeto")
                st.info("Momento em que as estratégias precisam ser incorporadas e registradas nos projetos arquitetônicos e de disciplinas complementares do empreendimento.")
                st.info("Os itens dessa fase são referentes às informações que precisam estar contidas nos projetos, memoriais e fichas técnicas para envio para a Certificação Preliminar.")
            elif 'Obra' in title: 
                st.title("Etapa de Obra")
                st.info("Fase de execução da construção do edifício, na qual devem ser implementadas as soluções previstas na fase de projeto.")
                st.info("Os itens dessa fase são referentes ao registro e comprovação da implementação das estratégias, para envio para a Certificação Pós construção.")
            elif 'construção' in title:
                st.title("Etapa de Pós construção")
                st.info("Fase de revisão da documentação considerando quaisquer alterações realizadas durante a construção em relação ao que foi previsto para a Certificação Preliminar.")
                st.info("Os itens dessa fase são referentes à apresentação de projetos e memoriais atualizados, conforme o que foi construído, bem como documentos de compra, para envio para a Certificação Pós construção.")
        else:
            st.write(f"**Categoria:** {item.get('categoria', 'Sem categoria')}")
            categoria = item.get('categoria', 'Sem categoria')
            id_map = {n["id"]: n for n in st.session_state.rows}
            credit_node = None
            parent_id = item.get("__parent")
            while parent_id is not None:
                parent_node = id_map.get(parent_id)
                if parent_node.get("__depth") == 1:
                    credit_node = parent_node
                    break
                parent_id = parent_node.get("__parent")
            
            if credit_node:
                st.write(f"**Crédito:** {credit_node.get('title', 'Sem crédito')}")
            else:
                st.write("**Crédito:** Não disponível")
            
            st.write(f"**Item selecionado:** {title}")

            st.write('----')
            st.write("Edite os campos abaixo:")
            cols = st.columns(2)
            with cols[0]:
                situacoes = ["🟥 Pendente", "🟩 Aprovado", "🟨 Em aprovação", "🟧 Necessário adequações", "🟪 Solicitação de edição"]
                default_val = item.get("situacao", "🟥 Pendente")
                default_index_situacao = situacoes.index(default_val) if default_val in situacoes else 0
                if 'admin' in permission:
                    situacao = st.selectbox("Situação", options=situacoes, index=default_index_situacao, placeholder="Selecione uma situação")
                else:
                    situacao = st.selectbox("Situação", options=situacoes, index=default_index_situacao, placeholder="Selecione uma situação", disabled=True)
            with cols[1]:
                default_revisao = item.get("revisao", "R01")
                revisoes = ['R01', 'R02', 'R03']
                default_index_revisao = revisoes.index(default_revisao) if default_revisao in revisoes else 0
                if 'admin' in permission:
                    revisao = st.selectbox("Revisão", options=revisoes, index=default_index_revisao)
                else:
                    revisao = st.selectbox("Revisão", options=revisoes, index=default_index_revisao, disabled=True)

            uploaded_files = st.file_uploader("Arquivo(s)", accept_multiple_files=True)

            cols = st.columns(2)
            with cols[0]:
                if "custom_filter_options" not in st.session_state:
                    st.session_state.custom_filter_options = []

                nova_opcao = st.text_input("Novo filtro personalizado", key="nova_opcao")
                if st.button("Adicionar filtro", use_container_width=True, key="adicionar_filtro"):
                    if nova_opcao and nova_opcao not in st.session_state.custom_filter_options:
                        st.session_state.custom_filter_options.append(nova_opcao)
                        st.success(f"Opção '{nova_opcao}' adicionada.")
                    else: 
                        st.warning("❗Opção inválida ou já existente.")
            with cols[1]:
                if st.session_state.custom_filter_options:
                    excluir_opcao = st.selectbox(
                        "Selecione a opção para excluir", 
                        st.session_state.custom_filter_options, 
                        key="excluir_filter", placeholder="Selecione uma opção"
                    )
                    if st.button("Excluir filtro", use_container_width=True, key="excluir_filtro"):
                        st.session_state.custom_filter_options.remove(excluir_opcao)
                        st.success(f"Opção '{excluir_opcao}' excluída.")
                else:
                    st.info("Nenhuma opção de filtro para excluir.")
            
            default_atribuicao = item.get("atribuicao")
            if isinstance(default_atribuicao, list):
                selected_options = default_atribuicao
            elif isinstance(default_atribuicao, str):
                selected_options = [default_atribuicao]
            else:
                selected_options = []

            # Se o projeto selecionado mudou, reinicia a lista de filtros personalizados
            if st.session_state.get("previous_project") != st.session_state.projeto_selecionado:
                st.session_state.custom_filter_options = []
                st.session_state.previous_project = st.session_state.projeto_selecionado

            # Usa o cache para buscar as opções já existentes no banco para o projeto em questão
            db_options = get_db_options(collection_name)
            combined_options = list(set(st.session_state.custom_filter_options + db_options))
            combined_options.sort()
            st.session_state.custom_filter_options = combined_options

            filtro_personalizado = st.selectbox(
                "Filtro Personalizado", 
                options=st.session_state.custom_filter_options, 
                key="filtro_personalizado",
                placeholder="Selecione um filtro"
            )

            observacao = st.text_area("Observação", value=item.get("observacao", ""))
            if 'admin' in permission:
                comentario_hygge = st.text_area("Comentário HYGGE", value=item.get("comentario_hygge", ""))
            else:
                comentario_hygge = st.text_area("Comentário HYGGE", value=item.get("comentario_hygge", ""), disabled=True)

            # Exibe o status atual da edição
            current_doc = db[collection_name].find_one({"id": item["id"]})
            current_status = current_doc.get("update_status", "") if current_doc else ""
        
            # Se o admin detectar que o item está com 'solicitação de edição',
            # libera a edição mudando o status para 'Pendente'
            if 'admin' in permission and situacao == "🟪 Solicitação de edição":
                email_confirmacao = st.text_input("Email para confirmação", value=item.get("email", ""))
                if st.button("Liberar edição"):
                    db[collection_name].update_one(
                        {"id": item["id"]},
                        {"$set": {"update_status": "", "situacao": "🟥 Pendente"}}
                    )
                    st.success("Permissão liberada! Status atualizado para Pendente.")
                    
                    # Envia email para o cliente com a confirmação da liberação da edição
                    try:
                        # Obtém o email do cliente a partir do item ou use um email padrão
                        client_email = email_confirmacao
                        message = MIMEMultipart()
                        message["From"] = 'admin@hygge.eco.br'
                        message["To"] = client_email
                        message["Subject"] = f"Confirmação: Liberação de Edição - {item.get('title', '')[:15]}..."
                        body = f"Olá,\n\nSua solicitação de edição para o item '{item.get('title', '')}' foi liberada. " \
                               f"Você pode realizar as alterações necessárias agora.\n\nAtenciosamente,\nEquipe de Certificações HYGGE"
                        message.attach(MIMEText(body, "plain"))
                        
                        server = smtplib.SMTP('smtp.office365.com', 587)
                        server.starttls()
                        server.login(st.secrets['microsoft']['email'], st.secrets['microsoft']['password'])
                        server.sendmail('admin@hygge.eco.br', client_email, message.as_string())
                        server.quit()
                        st.success("Email de confirmação enviado para o cliente.")
                    except Exception as e:
                        st.error(f"Falha ao enviar email de confirmação: {e}")
                    
                    st.rerun()

            st.info("Clique em 'Salvar Informações' para salvar as alterações realizadas acima.")
            
            # Para usuários (não-admin), determinar se a edição pode ser feita diretamente.
            # A primeira alteração ou depois de uma aprovação do admin permite editar sem solicitação.
            # Caso contrário, se o status estiver 'atualizado' (alteração já feita e não aprovada), a edição direta não é permitida.
            allow_direct_save = True
            if 'admin' not in permission and current_status == "atualizado":
                allow_direct_save = False

            if st.button("Salvar Informações"):
                if 'admin' in permission or allow_direct_save:
                    # Atualização dos campos conforme entrada do formulário
                    item["observacao"] = observacao
                    item["comentario_hygge"] = comentario_hygge
                    item["revisao"] = revisao
                    item["atribuicao"] = filtro_personalizado

                    if uploaded_files:
                        item["arquivos"] = ", ".join([f.name for f in uploaded_files])
                        item["situacao"] = "🟥 Pendente"
                        cadastros.upload_to_3projetos(
                            uploaded_files,
                            alias_selecionado,
                            'EDGE',
                            credit_node.get("title", ""),
                            title,
                            revisao
                        )
                    else:
                        item["arquivos"] = item.get("arquivos", "")
                        item["situacao"] = situacao

                    # Se for usuário, e não for a primeira alteração, marcar como "atualizado"
                    if 'admin' not in permission:
                        item["update_status"] = "atualizado"
                    else:
                        item["update_status"] = ""

                    db[collection_name].update_one({"id": item["id"]}, {"$set": item})
                    st.success("Alterações salvas!")
                    compute_percent_complete(st.session_state.rows)
                    st.session_state.grid_key += 1
                    with st.spinner("Atualizando dados..."):
                        st.rerun()
                else:
                    st.warning("Edição não permitida. Se desejar alterar este item, por favor, solicite uma edição.")

            # Para usuários que não são admin e quando a edição direta não é permitida,
            # oferece a opção de solicitar uma alteração.
            if 'admin' not in permission and not allow_direct_save:
                st.info("Clique em 'Solicitar Edição' para registrar a solicitação de alteração.")
                if st.button("Solicitar Edição"):
                    item["situacao"] = "🟪 Solicitação de edição"
                    db[collection_name].update_one({"id": item["id"]}, {"$set": item})
                    
                    # Enviando email para os responsáveis pela aprovação da edição
                    try:
                        receivers = ['maiz@hygge.eco.br', 'joao@hygge.eco.br']
                        #receivers = ['rodrigo@hygge.eco.br']
                        message = MIMEMultipart()
                        message["From"] = 'admin@hygge.eco.br'
                        message["To"] = ", ".join(receivers)
                        message["Subject"] = f'Solicitação de edição - {alias_selecionado} - {credit_node.get("title", "")}'

                        # Corpo do email original
                        body = f"""<p>Foi solicitada uma edição por {st.session_state['name']} para o item "{item.get("title", "")}" do crédito "{credit_node.get("title", "")}" do projeto "{alias_selecionado}".</p>"""
                        message.attach(MIMEText(body, "html"))

                        # Sending the email
                        try:
                            server = smtplib.SMTP('smtp.office365.com', 587)
                            server.starttls()
                            server.login(st.secrets['microsoft']['email'], st.secrets['microsoft']['password'])
                            server.sendmail('admin@hygge.eco.br', receivers, message.as_string())
                            server.quit()
                        except Exception as e:
                            st.error(f"Falha no envio do email: {e}")

                        st.success("Solicitação de edição registrada com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao enviar email: {e}")
                    st.rerun()



    # --- Calcula o campo "categoria" para cada nó ---
    # Cria um mapeamento id -> node
    for node in st.session_state.rows:
        if node.get("__depth", 0) == 0:
            node["categoria"] = node["title"]
        else:
            parent_id = node.get("__parent")
            while parent_id is not None:
                parent_node = id_map.get(parent_id)
                if parent_node.get("__depth", 0) == 0:
                    node["categoria"] = parent_node["title"]
                    break
                parent_id = parent_node.get("__parent")

    # --- Função para recacular o percentual de conclusão ---
    def compute_percent_complete(rows):
        # Ordena os nós por profundidade decrescente
        for node in sorted(rows, key=lambda n: n.get("__depth", 0), reverse=True):
            depth = node.get("__depth", 0)
            if depth == 3:
                # Nó folha: se a situação contém "🟩 Aprovado", então 100, senão 0.
                node["percentual"] = 100 if node.get("situacao", "").find("🟩 Aprovado") != -1 else 0
            else:
                filhos = [child for child in rows if child.get("__parent") == node["id"]]
                if filhos:
                    node["percentual"] = sum(child.get("percentual", 0) for child in filhos) / len(filhos)
                else:
                    node["percentual"] = 0

    compute_percent_complete(st.session_state.rows)

    # Atualiza a chave dinâmica para forçar a atualização do grid
    if "grid_key" not in st.session_state:
        st.session_state.grid_key = 0

    # Define as colunas para o grid
    columns = [
        {
            "id": "title",
            "name": "Título",
            "field": "title",
            "minWidth": 350,
            "formatter": Formatters.tree,
            "exportCustomFormatter": Formatters.treeExport,
            "filterable": True,
            "filter": {"model": Filters.text}
        },
        {
            "id": "categoria",
            "name": "Categoria",
            "field": "categoria",
            "minWidth": 50,
            "filterable": True,
            "filter": {
                "model": Filters.multipleSelect,
                "multiSelect": True,
                "collection": [
                    {"value": "01. Energia", "label": "Energia"},
                    {"value": "02. Água", "label": "Água"},
                    {"value": "03. Materiais", "label": "Materiais"}
                ]
            },
        },
        {
            "id": "percentual",
            "name": "% Completo",
            "field": "percentual",
            "sortable": True,
            "minWidth": 150,
            "editable": True,
            "type": FieldType.number,
            "filterable": True,
            "filter": {
                "model": Filters.sliderRange,
                "maxValue": 100,
                "operator": OperatorType.rangeInclusive,
                "filterOptions": {"hideSliderNumbers": False, "min": 0, "step": 5},
            },
            "formatter": StreamlitSlickGridFormatters.barFormatter,
            "params": {
                "colors": [
                    [0, "#ffffff", "#ff4b4b"],
                    [50, "#ffffff", "#ffcc00"],
                    [100, "#ffffff", "#21c354"]
                ],
                "minDecimal": 0,
                "maxDecimal": 1,
                "numberSuffix": "%",
            },
        },
        {
            "id": "situacao",
            "name": "Situação",
            "field": "situacao",
            "minWidth": 150,
            "filterable": True,
            "filter": {
                "model": Filters.multipleSelect,
                "collection": [
                    {"value": "🟥 Pendente", "label": "🟥 Pendente"},
                    {"value": "🟩 Aprovado", "label": "🟩 Aprovado"},
                    {"value": "🟨 Em aprovação", "label": "🟨 Em aprovação"},
                    {"value": "🟧 Necessário adequações", "label": "🟧 Necessário adequações"},
                    {"value": "🟪 Solicitação de edição", "label": "🟪 Solicitação de edição"}
                ]
            },
        },
        {
            "id": "arquivos",
            "name": "Arquivo(s)",
            "field": "arquivos",
            "minWidth": 100,
            "filterable": True,
        },
        {
            "id": "atribuicao",
            "name": "Filtro personalizado",
            "field": "atribuicao",
            "minWidth": 150,
            "filterable": True,
            "filter": {
                "model": Filters.singleSelect,
                "multiSelect": True,
                "collection": (
                    [{"value": "", "label": "Todos"}] +
                    [{"value": op, "label": op} for op in sorted(
                        set(
                            st.session_state.get("custom_filter_options", []) +
                            [db_val for db_val in db[collection_name].distinct("atribuicao") if db_val]
                        )
                    )]
                ),
            },
        },
        {
            "id": "revisao",
            "name": "Revisão",
            "field": "revisao",
            "minWidth": 50,
            "filterable": True,
            "filter": {
                "model": Filters.multipleSelect,
                "multiSelect": True,
                "collection": [
                    {"value": "R01", "label": "R01"},
                    {"value": "R02", "label": "R02"},
                    {"value": "R03", "label": "R03"}
                ]
            }
        },
    ]

    # Configura as opções do grid
    options = {
        "enableFiltering": True,
        "autoResize": {"minHeight": 400},
        "enableTreeData": True,
        "multiColumnSort": False,
        "enableHtml": True,
        # Ativa o ajuste dinâmico do tamanho das colunas baseado no conteúdo
        "resizeByContent": False,
        # Caso queira que a última coluna use todo o espaço restante, pode adicionar:
        "forceFitColumns": False,
        "treeDataOptions": {
            "columnId": "title",
            "indentMarginLeft": 15,
            "initiallyCollapsed": False,
            "parentPropName": "__parent",
            "levelPropName": "__depth"
        },
        "noDataMessage": "Nenhum dado para o filtro aplicado",
        "enableTextExport": True,
        "enableExcelExport": True,
        "excelExportOptions": {"sanitizeDataExport": True},
        "textExportOptions": {"sanitizeDataExport": True},
        "externalResources": [
            ExportServices.ExcelExportService,
            ExportServices.TextExportService,
        ],
    }



    if 'admin' in st.session_state["roles"]:
        menu_principal = st.tabs(['Página inicial', 'Entenda o EDGE', 'Cadastros'])

    else: menu_principal = st.tabs(['Página inicial', 'Entenda o EDGE'])

    with menu_principal[0]:
        st.title('Check-list de acompanhamento das informações do EDGE')
        st.info('🖱️ **Clique na linha desejada** na tabela abaixo para preencher ou conferir as informações.')
        with st.container():
            # Atualiza a key do slickgrid incluindo o projeto selecionado para forçar o refresh
            grid_key = f"{st.session_state.projeto_selecionado}_{st.session_state.grid_key}"
            out_geral = slickgrid(
                st.session_state.rows,
                columns,
                options,
                key=f"energy_grid_{grid_key}",
                on_click="rerun"
            )
            
            # Se o slickgrid retornar um dicionário com a chave "data", usamos ela para criar o DataFrame filtrado.
            df_filtered = pd.DataFrame(st.session_state.rows)
            # Se uma linha foi clicada, exibe o diálogo de detalhes.
            # Para isso, assumimos que o slickgrid pode retornar uma tupla (row, col)
            if out_geral is not None:
                row, col = out_geral
                show_dialog(st.session_state.rows[row], st.session_state["roles"])

            # Exibe um DataFrame com os dados filtrados atualmente no grid.
            # Caso o slickgrid retorne um dicionário com a chave "data", usamos ele;
            # caso contrário, exibimos todos os dados.

            filtered_data = st.session_state.rows
            # Mantém no DataFrame apenas os registros de profundidade 3.
            filtered_data = [item for item in filtered_data if item.get("__depth", 0) == 3]

            df_filtered = pd.DataFrame(filtered_data)
        
        if st.button('Gerar o relatário do projeto'):
            pdf_path = cadastros.gerar_relatorio('Projeto', st.session_state.projeto_selecionado, df_filtered)
            codigo_aleatorio = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            #Exibir botão de download para o usuário
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Baixar Relatório",
                    data=pdf_file,
                    file_name=f"Relatório_{st.session_state.projeto_selecionado}_{codigo_aleatorio}.pdf",
                    mime="application/pdf"
                )

        st.write('----')
        st.title('Anexos')
        # --- Criar expander para cada anexo ---
        for categoria, cat_data in data_json.items():
            if "anexos" in cat_data:
                st.subheader(categoria)
                for anexo_key, anexo_detail in cat_data["anexos"].items():
                    with st.expander(f"{anexo_key}"):
                        descricao = anexo_detail.get("descricao", "Sem descrição")
                        st.markdown(descricao)
                    
        st.write('----')
        st.title('Resumo das informações preenchidas')
        if st.button('Gerar resumo'):
            # Filtra apenas os itens (nós de profundidade 3)
            itens = [r for r in st.session_state.rows if r.get("__depth") == 3]

            # Cria uma lista de registros com categoria, etapa e situação
            dados = []
            for item in itens:
                dados.append({
                    "Categoria": item.get("categoria", "Sem categoria"),
                    "Etapa": item.get("tipo", "Desconhecido"),
                    "Situacao": item.get("situacao", "Sem situação")
                })

            if dados:
                df = pd.DataFrame(dados)
                # Classifica a situação: se contiver "Aprovado", é "Aprovados", senão "Não aprovados"
                df["Situacao"] = df["Situacao"].apply(lambda x: "Aprovados" if "Aprovado" in x else "Não aprovados")
                # Agrupa as Etapas: "Projeto" e "Obra" se tornam "Preliminar"; "Pós construção" permanece
                df["Etapa"] = df["Etapa"].apply(
                    lambda x: "Preliminar" if any(sub in x for sub in ["Projeto", "Obra"])
                        else ("Pós construção" if "Pós" in x or "Pós construção" in x else x)
                )
                # Gera resumo para exibir combinando todas as situações mesmo que 0 ou vazio
                categorias = sorted(df["Categoria"].unique())
                etapas = ["Preliminar", "Pós construção"]
                situacoes = ["Aprovados", "Não aprovados"]
                summary_list = []
                for cat in categorias:
                    for etapa in etapas:
                        for situacao in situacoes:
                            count = df[(df["Categoria"] == cat) & (df["Etapa"] == etapa) & (df["Situacao"] == situacao)].shape[0]
                            summary_list.append({"Categoria": cat, "Etapa": etapa, "Situação": situacao, "Qtde.": count})
                resumo = pd.DataFrame(summary_list)
                
                # Calcula o percentual de aprovados para cada categoria nos grupos "Preliminar" e "Pós construção"
                approved_percentages = {}
                for cat in categorias:
                    df_cat = df[df["Categoria"] == cat]
                    for etapa in etapas:
                        df_etapa = df_cat[df_cat["Etapa"] == etapa]
                        total = len(df_etapa)
                        if total > 0:
                            approved_count = df_etapa[df_etapa["Situacao"] == "Aprovados"].shape[0]
                            percentage = approved_count / total * 100
                        else:
                            percentage = 0
                        approved_percentages[f"{cat} - {etapa}"] = percentage

                # Divide o resumo em duas partes: uma para Preliminar e outra para Pós construção
                resumo_preliminar = resumo[resumo["Etapa"] == "Preliminar"]
                resumo_pos = resumo[resumo["Etapa"] == "Pós construção"]

                cols = st.columns(2)
                with cols[0]:
                    st.subheader("Preliminar")
                    st.info('A Certificação Preliminar do projeto é realizada com base nas estratégias adotadas nos projetos arquitetônicos e de disciplinas complementares do empreendimento. Englobando, portanto, as etapas de Projeto e Obra.')
                    st.info('Dentre os documentos a serem submetidos para a certificação estão pranchas dos projetos, memoriais descritivos, memoriais de cálculo e fichas técnicas que comprovem as medidas que serão implementadas.')
                    # Exibe os dados agregados em um DataFrame para Preliminar
                    
                    res.render_ring_gauge(
                        round(approved_percentages.get('01. Energia - Preliminar', 0), 2),
                        round(approved_percentages.get('02. Água - Preliminar', 0), 2),
                        round(approved_percentages.get('03. Materiais - Preliminar', 0), 2),
                        key_data=f'ring_gauge_preliminar_{random.randint(0, 100000)}'
                    )
                    st.dataframe(resumo_preliminar.reset_index(drop=True), use_container_width=True)
                with cols[1]:
                    st.subheader("Pós construção")
                    st.info('A certificação Pós construção diz respeito à implementação, em obra, das medidas previstas em projeto na fase de Certificação Preliminar, além da atualização de quaisquer alterações realizadas durante a construção do empreendimento.')
                    st.info('Dentre os documentos a serem submetidos, estão os projetos e memoriais descritivos atualizados conforme construção, fotos da implementação das medidas em obra e documentos de compra dos materiais.')
                    
                    # Exibe os dados agregados em um DataFrame para Pós construção
                    res.render_ring_gauge(
                        round(approved_percentages.get('01. Energia - Pós construção', 0), 2),
                        round(approved_percentages.get('02. Água - Pós construção', 0), 2),
                        round(approved_percentages.get('03. Materiais - Pós construção', 0), 2),
                        key_data=f'ring_gauge_pos_construcao_{random.randint(0, 100000)}'
                    )
                    st.dataframe(resumo_pos.reset_index(drop=True), use_container_width=True)

    with menu_principal[1]:
        desc.descricoes_categorias()


    if 'admin' in st.session_state["roles"]:
        with menu_principal[2]:
            st.info("Cadastros de construtoras, projetos, clientes e adição de projetos aos clientes")
            pagina_cad_construtora, pagina_cad_projetos, cadastro_cliente, adicao_projeto_cliente = st.tabs(
                ["Cadastro de Construtora", "Cadastro de Projetos", "Cadastro de Cliente", "Adição de projeto ao cliente"]
            )

            # Página 1: Cadastro de Construtora
            with pagina_cad_construtora:
                st.subheader("Cadastro de Construtora")
                construtora_name = st.text_input("Nome da Construtora")
                codigo_construtora = st.text_input("Código da Construtora")
                status_construtora = st.selectbox("Status da Construtora", options=['Ativa', 'Inativa'])

                if st.button("Cadastrar Construtora"):
                    if construtora_name and codigo_construtora and status_construtora:
                        cadastros.add_construtora_to_db(client, construtora_name, codigo_construtora, status_construtora)
                    else:
                        st.error("Preencha todos os campos!")

            # Página 2: Cadastro de Projetos
            with pagina_cad_projetos:
                st.subheader("Cadastro de Projetos")
                construtoras = [c['construtora'] for c in cadastros.get_construtoras(client)]

                if construtoras:
                    construtora_name = st.selectbox("Selecione a Construtora", construtoras, key='construtora_cad_projeto')
                    projeto_name = st.text_input("Nome do Projeto")
                    projeto_alias = st.text_input("Nome da pasta do projeto (3 PROJETOS)")
                    tipo_projeto_name = st.selectbox("Tipo de projeto", ['LEED', 'GBC', 'EDGE', 'HYGGE'])

                    if st.button("Cadastrar Projeto"):
                        if construtora_name and projeto_name and projeto_alias:
                            cadastros.add_projeto_to_construtora(client, construtora_name, projeto_name, projeto_alias, tipo_projeto_name)
                        else:
                            st.error("Preencha todos os campos!")
                else:
                    st.error("Nenhuma construtora cadastrada. Cadastre uma construtora primeiro.")

            # Página 3: Cadastro de Cliente
            with cadastro_cliente:
                st.subheader("Cadastro de Cliente (Usuário)")
                construtoras = [c['construtora'] for c in cadastros.get_construtoras(client)]

                if construtoras:
                    construtora_name = st.selectbox("Selecione a Construtora", construtoras, key='construtora_cad_cliente')
                    projetos = cadastros.get_projetos(client, construtora_name)
                    alias = cadastros.get_alias(client, construtora_name)
                    tipos_projetos = cadastros.get_tipo_projeto(client, construtora_name)

                    projetos_selecionados = st.multiselect("Selecione os Projetos", projetos) if projetos else []
                    alias_selecionados = st.multiselect("Selecione os alias", alias) if alias else []
                    tipos_projetos_selecionados = st.multiselect("Selecione os tipos dos projetos", tipos_projetos) if tipos_projetos else []

                    username = st.text_input("Nome de usuário")
                    name = st.text_input("Nome completo")
                    email = st.text_input("Email")
                    password = st.text_input("Senha", type="password")
                    confirm_password = st.text_input("Confirme a senha", type="password")
                    view_type = st.selectbox("Selecione o tipo de usuário", options=['viewer', 'editor', 'admin'])

                    if st.button("Cadastrar Usuário"):
                        if password == confirm_password:
                            if username and name and email and construtora_name and projetos_selecionados:
                                cadastros.add_user_to_db(client, username, name, password, email, view_type, construtora_name, projetos_selecionados, alias_selecionados, tipos_projetos_selecionados)
                            else:
                                st.error("Preencha todos os campos!")
                        else:
                            st.error("As senhas não coincidem!")
                else:
                    st.error("Nenhuma construtora cadastrada. Cadastre uma construtora primeiro.")

            # Página 4: Atribuição de Projeto a Cliente Existente
            with adicao_projeto_cliente:
                st.subheader("Atribuir Projeto a Cliente Existente")

                # Listar todos os usuários cadastrados
                usuarios = [u['username'] for u in cadastros.get_usuarios(client)]

                if usuarios:
                    username_selecionado = st.selectbox("Selecione o Cliente", usuarios)

                    # Listar as construtoras e projetos disponíveis
                    construtoras = [c['construtora'] for c in cadastros.get_construtoras(client)]
                    if construtoras:
                        construtora_name = st.selectbox("Selecione a Construtora", construtoras, key='construtora_cad_projeto_cliente')
                        projetos = cadastros.get_projetos(client, construtora_name)
                        alias = cadastros.get_alias(client, construtora_name)
                        tipo_projeto = cadastros.get_tipo_projeto(client, construtora_name)

                        novo_projeto = st.selectbox("Selecione o Projeto", projetos) if projetos else None
                        novo_alias = st.selectbox("Selecione o alias", alias) if alias else None
                        novo_tipo_projeto = st.selectbox("Selecione o tipo do projeto", tipo_projeto) if tipo_projeto else None

                        if st.button("Atribuir Projeto"):
                            if novo_projeto and username_selecionado:
                                cadastros.add_project_to_existing_user(client, username_selecionado, novo_projeto, novo_alias, novo_tipo_projeto)
                            else:
                                st.error("Preencha todos os campos necessários!")
                    else:
                        st.error("Nenhuma construtora cadastrada.")
                else:
                    st.error("Nenhum cliente cadastrado.")