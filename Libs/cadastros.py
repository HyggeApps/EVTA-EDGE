import streamlit as st
from pymongo import errors
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import yaml
import tempfile
from msal import ConfidentialClientApplication
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
import warnings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tempfile
import os
warnings.filterwarnings("ignore")

custom_color = Color(165/255.0, 154/255.0, 148/255.0)

def selecionar_alias_usuario(client, projeto_selecionado, username): 
    # Conectar ao banco de dados e obter a coleção de usuários
    db = client['certificacoes']
    users_collection = db['usuarios']
    
    # Buscar o usuário pelo username e carregar os projetos
    user_data = users_collection.find_one({'email': username}, {"_id": 0, "projetos": 1})
    if user_data and 'projetos' in user_data:
        projetos = user_data['projetos']
        
        if projetos:
            # Encontrar o alias correspondente ao projeto selecionado
            for projeto in projetos:
                if projeto['nome'] == projeto_selecionado:
                    return projeto['alias']
            
            # Caso não encontre o alias (não deveria ocorrer)
            st.error("Alias não encontrado para o projeto selecionado.")
        
        else:
            st.warning("Você não tem projetos associados.")
    else:
        st.error("Usuário não encontrado ou sem projetos.")

    return None

def selecionar_projeto_usuario(client, username):
    # Carregar projetos do usuário com base no username
    db = client['certificacoes']
    users_collection = db['usuarios']
    
    # Buscar o usuário pelo username
    user_data = users_collection.find_one({'email': username}, {"_id": 0, "projetos": 1})
    
    if user_data and 'projetos' in user_data:
        projetos = user_data['projetos']
        
        if projetos:
            # Filtrar apenas os projetos do tipo "EDGE"
            projetos_edge = [projeto for projeto in projetos if projeto.get('tipo') == "EDGE"]
            if projetos_edge:
                # Extrair apenas os nomes dos projetos EDGE
                nomes_projetos = [projeto['nome'] for projeto in projetos_edge]
                # Permitir que o usuário selecione um projeto pelo nome
                projeto_selecionado = new_func(nomes_projetos)
                return projeto_selecionado
            else:
                st.warning("Você não tem projetos do tipo 'EDGE' associados.")
        else:
            st.warning("Você não tem projetos associados.")
    else:
        st.error("Usuário não encontrado ou sem projetos.")

    return None

def new_func(nomes_projetos):
    projeto_selecionado = st.selectbox("Selecione um projeto:", nomes_projetos)
    return projeto_selecionado

# Função para adicionar nova construtora no MongoDB
def add_construtora_to_db(client, construtora_name, codigo_construtora, status_construtora):
    db = client['certificacoes']
    construtoras_collection = db['construtoras']
    
    construtora_data = {
        'construtora': construtora_name,
        'codigo': codigo_construtora,
        'projetos': []
    }
    
    try:
        construtoras_collection.insert_one(construtora_data)
        st.success("Construtora cadastrada com sucesso!")
    except errors.DuplicateKeyError:
        st.error("Erro: Construtora já cadastrada!")

# Função para adicionar novo projeto a uma construtora no MongoDB
def add_projeto_to_construtora(client, construtora_name, projeto_name, projeto_alias, projeto_tipo):
    db = client['certificacoes']
    construtoras_collection = db['construtoras']
    
    # Estrutura do projeto com nome e alias
    projeto_data = {
        'nome': projeto_name,
        'alias': projeto_alias,
        'tipo': projeto_tipo,
    }
    
    try:
        # Usando um único $push para adicionar o projeto como um objeto com nome e alias
        construtoras_collection.update_one(
            {'construtora': construtora_name},
            {'$push': {'projetos': projeto_data}}
        )
        st.success("Projeto adicionado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao adicionar projeto: {str(e)}")

def add_user_to_db(client, email, construtora, projetos, aliases, tipos):
    # Estruturar cada projeto com `nome` e `alias`
    projetos_data = [{'nome': projeto, 'alias': alias, 'tipo': tipo} for projeto, alias, tipo in zip(projetos, aliases, tipos)]
    
    # Dados do usuário, incluindo a lista de projetos com nome e alias
    user_data = {
        'email': email,
        'construtora': construtora,
        'projetos': projetos_data  # Lista de projetos com nome e alias
    }
    
    db = client['certificacoes']
    users_collection = db['usuarios']
    
    try:
        users_collection.insert_one(user_data)
        st.success("Usuário cadastrado com sucesso!")
    except errors.DuplicateKeyError:
        st.error("Erro: Usuário já cadastrado!")

# Carregar construtoras existentes
@st.cache_data
def get_construtoras(_client):
    db = _client['certificacoes']
    construtoras_collection = db['construtoras']
    return list(construtoras_collection.find({}, {"_id": 0, "construtora": 1}))

@st.cache_data
def get_projetos(_client, construtora):
    db = _client['certificacoes']
    construtoras_collection = db['construtoras']
    result = construtoras_collection.find_one({'construtora': construtora}, {"_id": 0, "projetos.nome": 1})
    
    # Retorna uma lista com os nomes dos projetos se houver resultados
    return [projeto['nome'] for projeto in result['projetos']] if result and 'projetos' in result else []

# Carregar aliases dos projetos de uma construtora
@st.cache_data
def get_alias(_client, construtora):
    db = _client['certificacoes']
    construtoras_collection = db['construtoras']
    result = construtoras_collection.find_one({'construtora': construtora}, {"_id": 0, "projetos.alias": 1})
    
    # Retorna uma lista com os aliases dos projetos se houver resultados
    return [projeto['alias'] for projeto in result['projetos']] if result and 'projetos' in result else []

# Carregar aliases dos projetos de uma construtora
@st.cache_data
def get_tipo_projeto(_client, construtora):
    db = _client['certificacoes']
    construtoras_collection = db['construtoras']
    result = construtoras_collection.find_one({'construtora': construtora}, {"_id": 0, "projetos.tipo": 1})
    
    # Retorna uma lista com os aliases dos projetos se houver resultados
    return [projeto['tipo'] for projeto in result['projetos']] if result and 'projetos' in result else []

@st.cache_data
def get_usuarios(_client):
    db = _client['certificacoes']
    users_collection = db['usuarios']
    return list(users_collection.find({}, {"_id": 0, "email": 1}))

def create_temp_config_from_mongo(mongo_uri, db_name, collection_name):
    # Conectar ao MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Buscar todos os usuários no MongoDB
    users_data = collection.find()

    # Criar um dicionário para armazenar os dados do config temporário
    temp_config_data = {
        'credentials': {
            'usernames': {}
        }
    }

    # Adicionar usuários do MongoDB ao config temporário
    for user_data in users_data:
        username = user_data['username']

        # Preparar os dados do usuário no formato do config.yaml
        user_yaml_data = {
            'email': user_data.get('email', ''),
            'failed_login_attempts': 0,
            'first_name': user_data.get('name', '').split()[0],
            'last_name': ' '.join(user_data.get('name', '').split()[1:]),
            'logged_in': False,
            'password': user_data.get('password', ''),  # Idealmente, a senha deve ser hasheada
            'roles': [user_data.get('funcao', 'viewer')]
        }

        # Adicionar o usuário ao config temporário
        temp_config_data['credentials']['usernames'][username] = user_yaml_data
        #print(f"Usuário {username} adicionado ao config temporário.")

    # Criar um arquivo temporário para salvar o config.yaml (como texto)
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml', encoding='utf-8') as temp_file:
        yaml.dump(temp_config_data, temp_file, default_flow_style=False)
        temp_file_path = temp_file.name

    #print(f"Arquivo config temporário criado: {temp_file_path}")
    return temp_file_path

def load_config_and_check_or_insert_cookies(config_file_path):
    # Carregar o arquivo YAML existente
    try:
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)
            if config_data is None:
                config_data = {}  # Caso o arquivo esteja vazio
    except FileNotFoundError:
        config_data = {}  # Se o arquivo não existir ainda

    # Verificar e garantir que a seção 'cookie' exista
    if 'cookie' not in config_data:
        config_data['cookie'] = {
            'expiry_days': 0,
            'key': 'some_signature_key',
            'name': 'some_cookie_name'
        }
        #print("Seção 'cookie' criada com valores padrão.")

    # Verificar se a chave 'name' está na seção 'cookie'
    cookie_name = config_data['cookie'].get('name')
    if not cookie_name:
        config_data['cookie']['name'] = 'some_cookie_name'
        #print("Chave 'name' na seção 'cookie' criada com valor padrão.")

    # Salvar o arquivo atualizado
    with open(config_file_path, 'w') as file:
        yaml.dump(config_data, file, default_flow_style=False)

    return config_data

def add_project_to_existing_user(client, email, novo_projeto, novo_alias, novo_tipo):
    db = client['certificacoes']
    users_collection = db['usuarios']
    
    # Estruturar o novo projeto como um objeto com `nome` e `alias`
    projeto_data = {
        'nome': novo_projeto,
        'alias': novo_alias,
        'tipo': novo_tipo
    }
    
    # Atualizar o cliente, adicionando o novo projeto na lista de projetos
    try:
        result = users_collection.update_one(
            {'email': email},  # Busca o cliente pelo username
            {'$addToSet': {'projetos': projeto_data}}  # Adiciona o projeto completo na lista, sem duplicar
        )
        
        if result.modified_count > 0:
            st.success(f"Projeto '{novo_projeto}/{novo_alias}' adicionado ao usuário '{email}' com sucesso!")
        else:
            st.warning(f"O projeto '{novo_projeto}/{novo_alias}' já está associado ao usuário '{email}' ou o usuário não 1encontrado.")
    
    except Exception as e:
        st.error(f"Erro ao atribuir o projeto: {str(e)}")

@st.cache_data
def get_from_3projetos(root_folder_name, file_name):
    # Azure credentials and MSAL Client Configuration
    CLIENT_ID = st.secrets['azure']['client_id']
    CLIENT_SECRET = st.secrets['azure']['client_secret']
    TENANT_ID = st.secrets['azure']['tenant_id']
    AUTHORITY_URL = f'https://login.microsoftonline.com/{TENANT_ID}'
    SCOPE = ['https://graph.microsoft.com/.default']
    
    # Shared drive and item IDs
    item_id = '013JXZXANIYRELCT76MZHYGO2OF6YB7XAR'
    drive_id = "b!yrE7SxqrykWOoQYwwGXFrzTd7LHaY8FOgzJR4akW6vvvT1mGsai9QqqR_4XDxhMj"
    
    # Folder structure
    folder_structure = [
        root_folder_name,
        "8-EVTAs"
    ]
    
    # Authenticate and get access token
    app = ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY_URL, client_credential=CLIENT_SECRET)
    result = app.acquire_token_for_client(SCOPE)

    if 'access_token' in result:
        access_token = result['access_token']
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        
        # Initialize the parent folder ID to start with the root
        parent_folder_id = item_id
        
        # Create each folder in the specified structure
        for folder_name in folder_structure:
            create_folder_url = f'https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_folder_id}/children'
            folder_response = requests.get(create_folder_url, headers=headers)
            if folder_response.status_code == 200:
                existing_folders = {item['name']: item['id'] for item in folder_response.json().get('value', [])}
                if folder_name in existing_folders:
                    parent_folder_id = existing_folders[folder_name]
                    #print(f"Folder '{folder_name}' already exists.")
                else:
                    # Create the folder if it does not exist
                    folder_data = {
                        "name": folder_name,
                        "folder": {},
                        "@microsoft.graph.conflictBehavior": "rename"
                    }
                    create_response = requests.post(create_folder_url, headers=headers, json=folder_data)
                    if create_response.status_code in [200, 201]:
                        parent_folder_id = create_response.json()['id']
                        #print(f"Folder '{folder_name}' created successfully.")
                    else:
                        #print(f"Error creating folder '{folder_name}': {create_response.status_code} {create_response.text}")
                        return None
            else:
                #print(f"Error checking folders: {folder_response.status_code} {folder_response.text}")
                return None

        # Look for the specified file in the final folder
        get_items_url = f'https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_folder_id}/children'
        items_response = requests.get(get_items_url, headers=headers)
        if items_response.status_code == 200:
            items = items_response.json().get('value', [])
            target_file = next((item for item in items if item['name'] == file_name), None)
            if target_file:
                # Download the specified file
                download_url = target_file['@microsoft.graph.downloadUrl']
                file_response = requests.get(download_url)
                if (file_response.status_code == 200):
                    #print(f"'{file_name}' downloaded successfully.")
                    # Create a temporary file to save the content
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_name.split('.')[-1]}") as temp_file:
                        temp_file.write(file_response.content)
                        temp_file_path = temp_file.name
                    #print(f"'{file_name}' saved to temporary file: {temp_file_path}")
                    # Return the path to the temporary file
                    return temp_file_path
                else:
                    #print(f"Error downloading '{file_name}': {file_response.status_code}")
                    return None
            else:
                #print(f"'{file_name}' not found in the folder.")
                return None
        else:
            #print(f"Error retrieving folder items: {items_response.status_code} {items_response.text}")
            return None
    else:
        #print("Error acquiring token:", result.get("error_description", ""))
        return None

def upload_to_3projetos(uploaded_files, root_folder_name, tipo_certificacao, credito, descritivo, revisao):
    # Azure credentials and MSAL Client Configuration
    CLIENT_ID = st.secrets['azure']['client_id']
    CLIENT_SECRET = st.secrets['azure']['client_secret']
    TENANT_ID = st.secrets['azure']['tenant_id']
    AUTHORITY_URL = f'https://login.microsoftonline.com/{TENANT_ID}'
    SCOPE = ['https://graph.microsoft.com/.default']
    
    # Shared drive and item IDs
    item_id = '013JXZXANIYRELCT76MZHYGO2OF6YB7XAR'
    drive_id = "b!yrE7SxqrykWOoQYwwGXFrzTd7LHaY8FOgzJR4akW6vvvT1mGsai9QqqR_4XDxhMj"
    
    #Se o 'descritivo' tiver mais que o limite de caracteres para criação de uma pasta no Windows, alterar para o limite de 255 caracteres
    if len(descritivo) > 255:
        descritivo = descritivo[:255]

    # Folder structure
    folder_structure = [
        root_folder_name,
        "8-EVTAs",
        tipo_certificacao,
        "01. Créditos e Pré-requisitos",
        credito,
        descritivo,
        revisao
    ]
    
    # Authenticate and get access token
    app = ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY_URL, client_credential=CLIENT_SECRET)
    result = app.acquire_token_for_client(SCOPE)

    if 'access_token' in result:
        access_token = result['access_token']
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        
        # Initialize the parent folder ID to start with the root
        parent_folder_id = item_id
        
        # Create each folder in the specified structure if it doesn't exist
        for folder_name in folder_structure:
            create_folder_url = f'https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_folder_id}/children'
            folder_data = {
                "name": folder_name,
                "folder": {},
                "@microsoft.graph.conflictBehavior": "rename"
            }
            
            # Check if folder exists, otherwise create it
            folder_response = requests.get(create_folder_url, headers=headers)
            if folder_response.status_code == 200:
                existing_folders = {item['name']: item['id'] for item in folder_response.json().get('value', [])}
                if folder_name in existing_folders:
                    parent_folder_id = existing_folders[folder_name]
                    #print(f"Folder '{folder_name}' already exists.")
                else:
                    # Create the folder if it does not exist
                    create_response = requests.post(create_folder_url, headers=headers, json=folder_data)
                    if create_response.status_code in [200, 201]:
                        parent_folder_id = create_response.json()['id']
                        #print(f"Folder '{folder_name}' created successfully.")
                    else:
                        #print(f"Error creating folder '{folder_name}': {create_response.status_code} {create_response.text}")
                        return
            else:
                #print(f"Error checking folders: {folder_response.status_code} {folder_response.text}")
                return

        # Step 2: Upload each file to the final folder
        for uploaded_file in uploaded_files:
            upload_url = f'https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_folder_id}:/{uploaded_file.name}:/content'
            upload_response = requests.put(upload_url, headers={'Authorization': f'Bearer {access_token}'}, data=uploaded_file.getbuffer())
            
            if upload_response.status_code in [200, 201]:
                #print(f"File '{uploaded_file.name}' successfully uploaded to the final folder.")
                st.success(f"Arquivo '{uploaded_file.name}' enviado com sucesso para a estrutura de pastas especificada!")
                #receivers = ['maiz@hygge.eco.br', 'joao@hygge.eco.br']
                receivers = ['rodrigo@hygge.eco.br']
                message = MIMEMultipart()
                message["From"] = 'admin@hygge.eco.br'
                message["To"] = ", ".join(receivers)
                message["Subject"] = f'{root_folder_name} - Envio de arquivo para o {credito} - {descritivo} - {revisao}'

                # Corpo do email original
                body = f"""<p>Existem atualizações para o projeto {root_folder_name}.<br></p>
                <p>O(s) arquivo(s) {uploaded_file.name} para o crédito {credito} - {descritivo} foi adicionado a pasta do projeto no servidor.<br></p>"""

                # Anexa o corpo do email completo no formato HTML
                message.attach(MIMEText(body, "html"))

                    # Sending the email
                try:
                    server = smtplib.SMTP('smtp.office365.com', 587)
                    server.starttls()
                    server.login(st.secrets['microsoft']['email'], st.secrets['microsoft']['password'])
                    server.sendmail(st.secrets['microsoft']['email'], receivers, message.as_string())
                    server.quit()
                except Exception as e:
                    st.error(f"Falha no envio do email: {e}")
            else:
                #print(f"Error uploading file '{uploaded_file.name}': {upload_response.status_code} {upload_response.text}")
                st.error(f"Erro ao fazer upload do arquivo '{uploaded_file.name}': {upload_response.status_code} {upload_response.text}")
    else:
        #print("Error acquiring token:", result.get("error_description", ""))
        st.error(f"Erro ao adquirir token: {result.get('error_description', '')}")

class MyDocTemplate(SimpleDocTemplate):
    """
    Subclasse de SimpleDocTemplate para adicionar números de página a um documento PDF.

    Métodos:
    - __init__(*args, **kwargs): Inicializa a subclasse MyDocTemplate chamando o construtor da classe base SimpleDocTemplate.
    - handle_pageBegin(): Método sobrescrito para adicionar um número de página ao início de cada página.
    - _add_page_number(canvas): Adiciona o número da página ao canvas do PDF.

    Atributos:
    - None

    Uso:
    - Esta classe é usada para criar documentos PDF com números de página automaticamente adicionados no canto inferior direito de cada página.
    """
    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)

    def handle_pageBegin(self):
        self._handle_pageBegin()
        #self._add_page_number(self.canv)

    #def _add_page_number(self, canvas):
        #page_num = canvas.getPageNumber()
        #text = f"{page_num}"
        #canvas.drawRightString(200 * mm - 10 * mm, 10 * mm, text)

def data_detalhada(data_proposta):
    """
    Função para formatar uma data em um formato detalhado em português.

    Args:
    - data_proposta (datetime.date): Objeto de data a ser formatado.

    Returns:
    - str: Data formatada no formato 'XX de XXXXX de XXXX', onde 'XXXXX' é o nome do mês em português.
    """
    # Portuguese month names
    months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    # Format the date: 'XX de XXXXX de XXXX'
    formatted_date = f'{data_proposta.day} de {months[data_proposta.month - 1]} de {data_proposta.year}'
    return formatted_date

def gerar_relatorio(construtora, nome_projeto, df):

    # Path to the font file
    font_path = Path(__file__).parent / "Fonts/Hero-Regular.ttf"

    # Ensure the font file exists
    if not font_path.is_file():
        raise FileNotFoundError(f"Font file not found: {font_path}")

    # Create a temporary file for the font
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ttf') as tmp_font:
        # Read the font file and write its content to the temporary file
        with open(font_path, 'rb') as font_file:
            tmp_font.write(font_file.read())

    # Register the font with a name (e.g., 'HeroLightRegular')
    pdfmetrics.registerFont(TTFont('HeroLightRegular', tmp_font.name))

        #visualizar_por_uh(df)
    # Path to the font file
    font_path = Path(__file__).parent / "Fonts/Hero-Bold.ttf"

    # Ensure the font file exists
    if not font_path.is_file():
        raise FileNotFoundError(f"Font file not found: {font_path}")

    # Create a temporary file for the font
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ttf') as tmp_font:
        # Read the font file and write its content to the temporary file
        with open(font_path, 'rb') as font_file:
            tmp_font.write(font_file.read())

    # Register the font with a name (e.g., 'HeroLightRegular')
    pdfmetrics.registerFont(TTFont('HeroLightBold', tmp_font.name))

            # Path to the font file
    font_path = Path(__file__).parent / "Fonts/calibri.ttf"

    # Ensure the font file exists
    if not font_path.is_file():
        raise FileNotFoundError(f"Font file not found: {font_path}")

    # Create a temporary file for the font
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ttf') as tmp_font:
        # Read the font file and write its content to the temporary file
        with open(font_path, 'rb') as font_file:
            tmp_font.write(font_file.read())

    # Register the font with a name (e.g., 'HeroLightRegular')
    pdfmetrics.registerFont(TTFont('Calibri', tmp_font.name))

    def blank_line(elements, x):
        for i in range(x):
            elements.append(Spacer(1, 12)) 
            
    def add_background(canvas, doc):
        # Define your background drawing code here
        canvas.saveState()
        canvas.drawImage(image_reader, 0, 0, width=doc.pagesize[0], height=doc.pagesize[1])
        canvas.restoreState()

    image_reader = Path(__file__).parent / "Imgs/Template.png"

    # Create a temporary directory for the PDF
    temp_dir = tempfile.mkdtemp()
    pdf_filename = f'Relatório de Checklist - {nome_projeto}.pdf'
    pdf_path = os.path.join(temp_dir, pdf_filename)

    # Initialize the BaseDocTemplate
    # Define seu documento usando a nova classe
    doc = MyDocTemplate(pdf_path, pagesize=landscape(A4))
    #doc = BaseDocTemplate(pdf_path, pagesize=letter)

    # Create a frame and a page template with the background
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='background', frames=frame, onPage=add_background)
    doc.addPageTemplates([template])
    
    # Define your styles and elements
    styles = getSampleStyleSheet()
    hero_light_style = ParagraphStyle(
        'HeroLight',
        parent=styles['Normal'],
        fontName='HeroLightRegular',
        fontSize=11,
        leftIndent=-0,
        leading=16,
        wordWrap='CJK'  # Adiciona wordWrap para não quebrar palavras
    )
    
    calibri_style = ParagraphStyle(
        'Calibri',
        parent=styles['Normal'],
        fontName='Calibri',
        fontSize=12,
        leftIndent=-0,
        leading=16,
        wordWrap='CJK'  # Adiciona wordWrap para não quebrar palavras
    )

    # Define your styles and elements
    styles = getSampleStyleSheet()

    hero_bold_style = ParagraphStyle(
        'HeroLightBold',
        parent=styles['Normal'],
        fontName='HeroLightBold',
        fontSize=12,
        leftIndent=0,
        leading=16
    )

    right_aligned_style = ParagraphStyle(
        'RightAlignedHeroLight',
        parent=hero_light_style,
        alignment=TA_RIGHT
    )

    title_style = ParagraphStyle(
        'TitleAlignedHeroLight',
        parent=hero_bold_style,
        fontSize=18,
        alignment=TA_CENTER
    )
    
    legenda_style = ParagraphStyle(
        'LegendaAlignedHeroLight',
        parent=hero_light_style,
        fontSize=9,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleAlignedHeroLight',
        parent=hero_light_style,
        fontSize=11,
        alignment=TA_CENTER
    )
    
    justify_style = ParagraphStyle(
        'JustifyStyle',
        parent=calibri_style,
        alignment=TA_JUSTIFY
    )
    
    style2 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), custom_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        # Align all elements in the table to the center (both horizontally and vertically)
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Font for the entire table
        ('FONT', (0, 0), (-1, -1), 'Calibri', 8),

        # Specific font for the first row
        ('FONT', (0, 0), (-1, 0), 'Calibri', 8),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
    ])

    style4 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), custom_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        # Align all elements in the table to the center (both horizontally and vertically)
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Font for the entire table
        ('FONT', (0, 0), (-1, -1), 'Calibri', 9.5),

        # Specific font for the first row
        ('FONT', (0, 0), (-1, 0), 'Calibri', 9.5),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),

        # Define the column widths: first column 20%, second column 80%
        ('COLWIDTHS', (0, 0), (0, -1), '20%'),
        ('COLWIDTHS', (1, 0), (1, -1), '80%'),
    ])

    style_ambsnros = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), custom_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        # Align all elements in the table to the center (both horizontally and vertically)
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Font for the entire table
        ('FONT', (0, 0), (-1, -1), 'Calibri', 8),

        # Specific font for the first row
        ('FONT', (0, 0), (-1, 0), 'Calibri', 8),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
    ])
    
    style3 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), custom_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        # Align all elements in the table to the center (both horizontally and vertically)
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Font for the entire table
        ('FONT', (0, 0), (-1, -1), 'Calibri', 8.5),

        # Specific font for the first row
        ('FONT', (0, 0), (-1, 0), 'Calibri', 8.5),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
    ])

    indent_style = ParagraphStyle('Indented', parent=calibri_style, leftIndent=20)    
    

    # Conteúdo do documento
    ### ----------------------- Página de introdução -------------------------
    elements = []
    blank_line(elements,2)
    elements.append(Paragraph(f'Relatório de acompanhamento de documentação', title_style)) 
    blank_line(elements,1)
    elements.append(Paragraph(f'{construtora}: {nome_projeto}', title_style)) 
    blank_line(elements,1)
    elements.append(Paragraph(f'{data_detalhada(datetime.now())}', subtitle_style))
    blank_line(elements,2)
    elements.append(Paragraph('1. Introdução', hero_bold_style))
    blank_line(elements,1)
    elements.append(Paragraph('O Relatório de Acompanhamento de Documentação elaborado pela Hygge é uma ferramenta para gerenciar e monitorar a documentação enviada. Este documento permite um registro de todos os itens que precisam ser entregues, com o intuito de facilitar a comunicação e o acompanhamento do progresso.', justify_style))
    elements.append(Paragraph('O relatório traz, de forma resumida e com visualização geral, os itens já descritos no Checklist Hygge que é apresentado via Streamlit. As informações são as seguintes:', justify_style))
    blank_line(elements,1)
    elements.append(Paragraph('Arquivo anexado;', justify_style))
    blank_line(elements,1)
    elements.append(Paragraph('Observação do cliente;', justify_style))  
    blank_line(elements,1)
    elements.append(Paragraph('Situação do item/documento;', justify_style))  
    blank_line(elements,1)
    elements.append(Paragraph('Filtro personalizado;', justify_style))  
    blank_line(elements,1)
    elements.append(Paragraph('Comentário Hygge;', justify_style))  
    blank_line(elements,1)
    elements.append(Paragraph('Revisão.', justify_style))  

    elements.append(PageBreak())
    
    # Define um estilo para o corpo das células com fonte menor
    cell_style = ParagraphStyle(
        'BodyTextReduced',
        parent=styles["BodyText"],
        fontName='Helvetica',
        fontSize=8,     # Fonte reduzida
        leading=10,     # Espaçamento entre linhas reduzido
        wordWrap='LTR'
    )

    # Define um estilo específico para o cabeçalho da tabela
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles["BodyText"],
        fontName='Helvetica-Bold',
        fontSize=8,     # Fonte reduzida
        leading=10,     # Espaçamento reduzido
        alignment=TA_CENTER,
        wordWrap='LTR'
    )

    ### ----------------------- Página de Resumo -------------------------

    #blank_line(elements,2)
    #elements.append(Paragraph('2. Resumo', hero_bold_style))
    #blank_line(elements,1)
        
    # Configura a largura da tabela conforme o tamanho da página
    page_width, page_height = landscape(A4)
    table_width = page_width * 0.9
    column_width = table_width / len(df.columns)

    # Cria os dados da tabela convertendo as células em Paragraphs
    # Usando o estilo reduzido para o cabeçalho
    #header_data = [Paragraph(str(col), table_header_style) for col in df.columns]
    #body_data = [[Paragraph(str(cell), cell_style) for cell in row] for row in df.values]
    #data = [header_data] + body_data

    # Cria a tabela com as larguras definidas e repetição do cabeçalho
    #table = Table(data, colWidths=[column_width] * len(df.columns), repeatRows=1)
    
    # Aplica o estilo à tabela (ajuste conforme necessário)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), custom_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1), 'LTR')
    ])
    #table.setStyle(style)

    # Adicionar a tabela à lista de elementos
    #elements.append(table)
    #elements.append(PageBreak())

    # Adicionando título principal ao documento
    elements.append(Paragraph('2. Créditos', hero_bold_style))
    blank_line(elements,1)

    # Agrupando por 'Categoria', 'Crédito' e 'Tipo'
    grouped = df.groupby(['categoria', 'credito', 'tipo'], sort=False)
    #st.write(df.columns)

    # Iterando por cada grupo
    for (category, credit, type), group in grouped:
        # Exibe a categoria e o crédito como títulos fora da tabela
        elements.append(Paragraph(f"Categoria: {category}", hero_bold_style))
        elements.append(Paragraph(f"Crédito: {credit}", hero_bold_style))
        elements.append(Paragraph(f"Tipo: {type}", hero_bold_style))
        
        # Espaço antes da tabela principal
        elements.append(Spacer(1, 12))
        
        # Extrair os dados de 'Descrição' e 'Comentário HYGGE' para exibir em tabela separada
        comentarios_df = group[['title', 'revisao', 'revision_at', 'comentario_hygge']].rename(columns={
            'title': 'Descrição',
            'revisao': 'Revisão',
            'revision_at': 'Data Revisão',
            'comentario_hygge': 'Comentário HYGGE'
        })
        
        # Cria um DataFrame simplificado removendo colunas indesejadas
        group_simplificado = group.drop(columns=['tipo', 'title', 'id', 'depth', '__parent', 'categoria', 'credito', 'atribuicao', 'revisao', 'comentario_hygge', 'update_status', 'percentual', '__depth', 'revision_at'])
        
        # Renomear as colunas do grupo simplificado conforme solicitado
        group_simplificado = group_simplificado[['item', 'situacao', 'arquivos','observacao', 'upload_at']].rename(columns={
            'item': 'Descrição',
            'situacao': 'Situação',
            'arquivos': 'Arquivo(s)',
            'observacao': 'Observação',
            'upload_at': 'Data de Upload'
        })
        
        # Recalcular largura das colunas para o grupo simplificado
        table_width = page_width * 0.9
        column_width = table_width / len(group_simplificado.columns)
        
        # Converter o grupo simplificado em uma lista de listas com Paragraph para cada célula
        data = [[Paragraph(str(cell), cell_style) for cell in row] for row in group_simplificado.values]
        # Adicionar o cabeçalho utilizando as colunas do DataFrame simplificado
        data.insert(0, [Paragraph(str(col), cell_style) for col in group_simplificado.columns])
        
        # Definir a tabela com larguras de coluna e repetição de cabeçalho nas páginas
        table = Table(data, colWidths=[column_width] * len(group_simplificado.columns), repeatRows=1)
        
        # Estilo da tabela principal
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), custom_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('WORDWRAP', (0, 0), (-1, -1), 'LTR')
        ])
        table.setStyle(style)
        
        # Adicionar a tabela principal ao documento
        elements.append(table)
        
        # Espaço entre as tabelas
        elements.append(Spacer(1, 12))
        
        # Criar tabela para 'Descrição' e 'Comentário Hygge'
        comentarios_data = [[Paragraph(str(cell), cell_style) for cell in row] for row in comentarios_df.values]
        comentarios_data.insert(0, [Paragraph(str(col), cell_style) for col in comentarios_df.columns])
        
        # Recalcular a largura das colunas para a tabela de comentários
        comentarios_table_width = page_width * 0.9
        comentarios_column_width = comentarios_table_width / len(comentarios_df.columns)
        
        comentarios_table = Table(
            comentarios_data,
            colWidths=[comentarios_column_width] * len(comentarios_df.columns),
            repeatRows=1
        )
        
        # Estilo para a tabela de comentários
        comentarios_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), custom_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('WORDWRAP', (0, 0), (-1, -1), 'LTR')
        ])
        comentarios_table.setStyle(comentarios_style)
        
        # Adicionar a tabela de comentários ao documento
        elements.append(comentarios_table)
        
        # Quebra de página após cada grupo
        elements.append(PageBreak())

    # Building the document
    doc.build(elements)


    # -------- Geração do relatório --------------------------

    
    cover_filename = Path(__file__).parent / "Imgs/Capa.pdf"
    back_cover_filename = Path(__file__).parent / "Imgs/ContraCapa.pdf"
    
    pdfs = [cover_filename, pdf_path, back_cover_filename] # pdf_path is the path to your main PDF

    writer = PdfWriter()

    for pdf in pdfs:
        reader = PdfReader(open(pdf, 'rb'))
        for i in range(len(reader.pages)):
            writer.add_page(reader.pages[i])

    with open(pdf_path, 'wb') as f_out:
        writer.write(f_out)
        st.success('Relatório gerado com sucesso! Clique no botão abaixo para fazer o download.')
    
    return pdf_path