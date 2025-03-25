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

def selecionar_alias_usuario(client, projeto_selecionado, username): 
    # Conectar ao banco de dados e obter a coleção de usuários
    db = client['certificacoes']
    users_collection = db['users']
    
    # Buscar o usuário pelo username e carregar os projetos
    user_data = users_collection.find_one({'username': username}, {"_id": 0, "projetos": 1})
    
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
    users_collection = db['users']
    
    # Buscar o usuário pelo username
    user_data = users_collection.find_one({'username': username}, {"_id": 0, "projetos": 1})
    
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

def add_user_to_db(client, username, name, password, email, view_type, construtora, projetos, aliases, tipo):
    # Estruturar cada projeto com `nome` e `alias`
    projetos_data = [{'nome': projeto, 'alias': alias, 'tipo': tipo} for projeto, alias in zip(projetos, aliases)]
    
    # Dados do usuário, incluindo a lista de projetos com nome e alias
    user_data = {
        'username': username,
        'name': name,
        'password': password,
        'email': email,
        'funcao': view_type,
        'construtora': construtora,
        'projetos': projetos_data  # Lista de projetos com nome e alias
    }
    
    db = client['certificacoes']
    users_collection = db['users']
    
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
    users_collection = db['users']
    return list(users_collection.find({}, {"_id": 0, "username": 1}))

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

def add_project_to_existing_user(client, username, novo_projeto, novo_alias, novo_tipo):
    db = client['certificacoes']
    users_collection = db['users']
    
    # Estruturar o novo projeto como um objeto com `nome` e `alias`
    projeto_data = {
        'nome': novo_projeto,
        'alias': novo_alias,
        'tipo': novo_tipo
    }
    
    # Atualizar o cliente, adicionando o novo projeto na lista de projetos
    try:
        result = users_collection.update_one(
            {'username': username},  # Busca o cliente pelo username
            {'$addToSet': {'projetos': projeto_data}}  # Adiciona o projeto completo na lista, sem duplicar
        )
        
        if result.modified_count > 0:
            st.success(f"Projeto '{novo_projeto}/{novo_alias}' adicionado ao usuário '{username}' com sucesso!")
        else:
            st.warning(f"O projeto '{novo_projeto}/{novo_alias}' já está associado ao usuário '{username}' ou o usuário não 1encontrado.")
    
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

def create_temp_config_from_mongo(db):
    # Buscar todos os usuários no MongoDB
    users_data = db['users'].find()

    # Criar um dicionário para armazenar os dados do config temporário
    temp_config_data = {
        'credentials': {
            'usernames': {}
        }
    }

    # Adicionar usuários do MongoDB ao config temporário
    for user_data in users_data:
        username = user_data['username']

        # Gerar a senha hasheada usando stauth.Hasher
        # Cria um dicionário de credenciais para o usuário atual
        credentials = {
            'usernames': {
            user_data['username']: {
                'password': user_data.get('password', '')
            }
            }
        }
        # Gera as credenciais com a senha hasheada
        hashed_credentials = Hasher.hash_passwords(credentials)
        # Extrai a senha hasheada para poder ser utilizada na criação do config
        hashed_passwords = [hashed_credentials['usernames'][user_data['username']]['password']]

        # Preparar os dados do usuário no formato do config.yaml
        user_yaml_data = {
            'email': user_data.get('email', ''),
            'failed_login_attempts': 0,
            'first_name': user_data.get('name', '').split()[0],
            'last_name': ' '.join(user_data.get('name', '').split()[1:]),
            'logged_in': False,
            'password': hashed_passwords[0],
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