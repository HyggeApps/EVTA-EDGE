from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
import streamlit as st

st.set_page_config(layout="wide")
def fluxo_teste():
    nodes = [
        StreamlitFlowNode('1', (10, 10), {'content': 'ETAPA 1 - Envio de projetos para a Hygge'}, 'input', 'right', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('1-1', (10, 100), {'content': 'Data:\na definir pelo cliente'}, 'input', 'right', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        
        StreamlitFlowNode('2', (300, 10), {'content': 'ETAPA 2 - EVTA Hygge com cenário de certificação'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('2-1', (300, 100), {'content': 'Prazo: 20 dias úteis'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        
        StreamlitFlowNode('3', (490, 10), {'content': 'ETAPA 3'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('3-1', (490, 60), {'content': 'Decisões do cliente'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('3-2', (490, 110), {'content': 'Data:\na definir pelo cliente'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        
        StreamlitFlowNode('4', (730, 10), {'content': 'ETAPA 4'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('4-1', (730, 60), {'content': 'Aplicação das medidas em projeto'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('4-2', (730, 110), {'content': 'Data:\na definir pelo cliente'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        
        StreamlitFlowNode('5', (970, 10), {'content': 'ETAPA 5'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('5-1', (970, 60), {'content': 'Envio de documentos no Checklist Hygge'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('5-2', (970, 110), {'content': 'Data:\na definir pelo cliente'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        
        StreamlitFlowNode('6', (1210, 10), {'content': 'ETAPA 6'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        StreamlitFlowNode('6-1', (1210, 60), {'content': 'Envio para o EDGE'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        StreamlitFlowNode('6-2', (1210, 110), {'content': 'Prazo: assim que a documentação estiver completa'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        
        StreamlitFlowNode('7', (1450, 10), {'content': 'ETAPA 7'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        StreamlitFlowNode('7-1', (1450, 60), {'content': 'Verificação pelo EDGE'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        StreamlitFlowNode('7-2', (1450, 110), {'content': 'Prazo: 21 dias'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        
        StreamlitFlowNode('8', (1690, 10), {'content': 'CERTIFICAÇÃO PRELIMINAR EDGE'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#6aa84f', 'border': '2px solid white'}),
        
        StreamlitFlowNode('9', (10, 250), {'content': 'ETAPA 1'}, 'input', 'right', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('9-1', (10, 300), {'content': 'Aplicação das medidas na obra'}, 'input', 'right', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('9-2', (10, 350), {'content': 'Data:\ninício ao fim da obra'}, 'input', 'right', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        
        StreamlitFlowNode('10', (250, 250), {'content': 'ETAPA 2'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('10-1', (250, 300), {'content': 'Envio de documentos no Checklist Hygge'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('10-2', (250, 350), {'content': 'Data:\na definir pelo cliente\n(no mínimo um mês antes da Etapa 4)'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        
        StreamlitFlowNode('11', (490, 250), {'content': 'ETAPA 3'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        StreamlitFlowNode('11-1', (490, 300), {'content': 'Envio para o EDGE'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        StreamlitFlowNode('11-2', (490, 350), {'content': 'Data:\na definir pela Hygge\n(no mínimo 5 dias antes da visita à obra)'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        
        StreamlitFlowNode('12', (730, 250), {'content': 'ETAPA 4'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('12-1', (730, 300), {'content': 'Visita à Obra'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        StreamlitFlowNode('12-2', (730, 350), {'content': 'Data:\na definir por todos\n(quando a obra estiver finalizada, mas ainda com acesso às UH)'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}),
        
        StreamlitFlowNode('13', (970, 250), {'content': 'ETAPA 4'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        StreamlitFlowNode('13-1', (970, 300), {'content': 'Verificação pelo EDGE'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        StreamlitFlowNode('13-2', (970, 350), {'content': 'Prazo: 21 dias'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}),
        
        StreamlitFlowNode('14', (1210, 250), {'content': 'CERTIFICAÇÃO EDGE'}, 'input', 'right', 'left', draggable=False, style={'color': 'white', 'backgroundColor': '#6aa84f', 'border': '2px solid white'})
    ]

    edges = [
        StreamlitFlowEdge('1-2', '1', '2', animated=True),
        StreamlitFlowEdge('2-3', '2', '3', animated=True),
        StreamlitFlowEdge('3-4', '3', '4', animated=True),
        StreamlitFlowEdge('4-5', '4', '5', animated=True),
        StreamlitFlowEdge('5-6', '5', '6', animated=True),
        StreamlitFlowEdge('6-7', '6', '7', animated=True),
        StreamlitFlowEdge('7-8', '7', '8', animated=True),
        StreamlitFlowEdge('9-10', '9', '10', animated=True),
        StreamlitFlowEdge('10-11', '10', '11', animated=True),
        StreamlitFlowEdge('11-12', '11', '12', animated=True),
        StreamlitFlowEdge('12-13', '12', '13', animated=True),
        StreamlitFlowEdge('13-14', '13', '14', animated=True)
    ]

    if 'custom_styles_state' not in st.session_state:
        st.session_state.custom_styles_state = StreamlitFlowState(nodes, edges)

    streamlit_flow('custom_style_flow',
            st.session_state.custom_styles_state,
            fit_view=True,
            show_minimap=False,
            show_controls=True,
            pan_on_drag=True,
            allow_zoom=True)

fluxo_teste()