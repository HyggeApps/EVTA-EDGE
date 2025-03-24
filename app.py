import streamlit as st
import json
import uuid
from streamlit_slickgrid import slickgrid, Formatters, Filters, FieldType, OperatorType, StreamlitSlickGridFormatters
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

st.set_page_config(page_title="HYGGE | EDGE - Checklist", layout="wide")
st.info('🖱️ **Clique na linha desejada** na tabela abaixo para preencher ou conferir as informações.')

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

@st.cache_resource
def conecta_banco():
    username = quote_plus(st.secrets['database']['username'])
    password = quote_plus(st.secrets['database']['password'])
    uri = f"mongodb+srv://{username}:{password}@evta.lxx4c.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client

client = conecta_banco()
db = client['certificacoes']

with st.sidebar:
    st.info(f'Bem-vindo(a), **TESTE**!')
    st.info('Este é o ambiente de **admin** para preenchimento das informações referentes ao EVTA de projetos.')
    # Persistência da seleção do projeto: se o projeto for alterado, reseta os dados e recarrega a aplicação
    if "projeto_selecionado" not in st.session_state:
        st.session_state.projeto_selecionado = cadastros.selecionar_projeto_usuario(client, "admin")
    else:
        novo_projeto = cadastros.selecionar_projeto_usuario(client, "admin")
        if novo_projeto != st.session_state.projeto_selecionado:
            st.session_state.projeto_selecionado = novo_projeto
            # Reseta as variáveis dependentes para forçar o recarregamento dos dados
            st.session_state.pop("rows", None)
            st.session_state.pop("grid_key", None)
            st.rerun()

    alias_selecionado = cadastros.selecionar_alias_usuario(client, st.session_state.projeto_selecionado, "admin")
    itens_json = cadastros.get_from_3projetos(alias_selecionado, 'creditos_default.json')

@st.cache_data
def read_json_creditos(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

data_json = read_json_creditos(itens_json)

#st.write(data_json)



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
    "pos-construcao": "03. Pós‑construção"
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

            # Para cada etapa (Projeto, Obra, Pós‑construção)
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

@st.dialog("Detalhes da Seleção", width="large")
def show_dialog(item):
    global db, collection_name  # Acesso às variáveis globais definidas no app.py
    title = item.get("title", "")
    depth = item.get("__depth", 0)
    st.write('---')
    
    if 'Energia' in title:
        st.title('Categoria de Energia')
        st.info("lorem ipsum...")
    elif 'Água' in title:
        st.title('Categoria de Água')
        st.info("lorem ipsum...")
    elif "Materiais" in title:
        st.title('Categoria de Materiais')
        st.info("lorem ipsum...")
    elif depth == 1:
        st.title(f"Crédito {title}")
        st.info("lorem ipsum...")
    elif depth == 2:
        if 'Projeto' in title: 
            st.title("Etapa de Projeto")
            st.info("lorem ipsum...")
        elif 'Obra' in title: 
            st.title("Etapa de Obra")
            st.info("lorem ipsum...")
        elif 'construção' in title:
            st.title("Etapa de Pós-construção")
            st.info("lorem ipsum...")
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
            credito = credit_node.get('title', 'Sem crédito')
        else:
            st.write("**Crédito:** Não disponível")
        
        st.write(f"**Item selecionado:** {title}")

        st.write('----')
        st.write("Edite os campos abaixo:")
        cols = st.columns(2)
        with cols[0]:
            situacoes = ["🟥 Pendente", "🟩 Aprovado", "🟨 Em aprovação", "🟧 Necessário adequações"]
            default_val = item.get("situacao", "🟥 Pendente")
            default_index_situacao = situacoes.index(default_val) if default_val in situacoes else 0
            situacao = st.selectbox("Situação", options=situacoes, index=default_index_situacao, placeholder="Selecione uma situação")
        with cols[1]:
            default_revisao = item.get("revisao", "R01")
            revisoes = ['R01', 'R02', 'R03']
            default_index_revisao = revisoes.index(default_revisao) if default_revisao in revisoes else 0
            revisao = st.selectbox("Revisão", options=revisoes, index=default_index_revisao)

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
                st.write('')
                st.info("Nenhuma opção de filtro para excluir.")
        
        default_atribuicao = item.get("atribuicao")
        if isinstance(default_atribuicao, list):
            selected_options = default_atribuicao
        elif isinstance(default_atribuicao, str) and default_atribuicao in st.session_state.custom_filter_options:
            selected_options = [default_atribuicao]
        else:
            selected_options = []

        # Consulta opções "atribuicao" já existentes no banco para o projeto em questão
        db_options = db[collection_name].distinct("atribuicao")
        # Filtra valores não vazios e combina com as opções customizadas já presentes
        db_options = [opt for opt in db_options if opt]  
        combined_options = list(set(st.session_state.custom_filter_options + db_options))
        combined_options.sort()  # Opcional: para ordenar as opções alfabeticamente
        
        filtro_personalizado = st.selectbox(
            "Filtro Personalizado", 
            options=combined_options, 
            key="filtro_personalizado",
            placeholder="Selecione um filtro"
        )

        observacao = st.text_area("Observação", value=item.get("observacao", ""))
        comentario_hygge = st.text_area("Comentário HYGGE", value=item.get("comentario_hygge", ""))

        liberar_edicao = st.checkbox("Liberar Edição (Admin)", key="liberar_edicao")

        if st.button("Salvar Alterações"):
            if item.get("update_status") == "atualizado" and not liberar_edicao:
                st.warning("❗Atualização já realizada para este crédito. Só pode ser alterado novamente quando liberado pelo administrador.")
            else:
                item["observacao"] = observacao
                item["comentario_hygge"] = comentario_hygge
                item["revisao"] = revisao
                item["atribuicao"] = filtro_personalizado

                if uploaded_files:
                    item["arquivos"] = ", ".join([f.name for f in uploaded_files])
                    item["situacao"] = "🟨 Em aprovação"
                    cadastros.upload_to_3projetos(uploaded_files, alias_selecionado,'EDGE',credito, title,revisao) 
                else:
                    item["arquivos"] = item.get("arquivos", "")
                    item["situacao"] = situacao

                if not liberar_edicao:
                    item["update_status"] = "atualizado"
                else:
                    item["update_status"] = ""
                
                # Atualiza o registro correspondente na collection do MongoDB
                db[collection_name].update_one({"id": item["id"]}, {"$set": item})
                
                st.success("Alterações salvas!")
                st.write("Dados atualizados:")
                compute_percent_complete(st.session_state.rows)
                st.session_state.grid_key += 1
                with st.spinner("Atualizando dados..."):
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
                 {"value": "🟧 Necessário adequações", "label": "🟧 Necessário adequações"}
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
                [{"value": op, "label": op} for op in (st.session_state.custom_filter_options if "custom_filter_options" in st.session_state else [])]
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
    "noDataMessage": "Nenhum dado para o filtro aplicado"
}

menu_principal = st.tabs(['Página inicial', 'Informações adicionais', 'Resumo', 'Cadastros'])

with menu_principal[0]:
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
        if out_geral is not None:
            row, col = out_geral
            show_dialog(st.session_state.rows[row])

    st.write('----')

    # --- Expander para exibir os anexos ---
    with st.expander("Anexos"):
        for categoria, cat_data in data_json.items():
            if "anexos" in cat_data:
                st.write('----')
                st.subheader(categoria)
                for anexo_key, anexo_detail in cat_data["anexos"].items():
                    descricao = anexo_detail.get("descricao", "Sem descrição")
                    st.markdown(f"**{anexo_key}:** {descricao}")
                    

with menu_principal[1]:
    st.info(1)

with menu_principal[2]:
    st.info(2)

with menu_principal[3]:
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
                        cadastros.add_user_to_db(client, username, name, password, email, view_type, construtora_name, projetos_selecionados, alias_selecionados)
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