from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
import streamlit as st

def fluxo_diagnostico_preliminar():
    format = 10
    nodes = [
        StreamlitFlowNode(
            '1',
            (10, 10),
            {'content': "###### **ETAPA 1**<br>Envio de projeto para<br>a HYGGE"},
            'default',
            'right',
            draggable=False,
            style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}
        ),
        StreamlitFlowNode(
            '2',
            (10, 120),
            {'content': "Data: **a definir pelo cliente**"},
            'default',
            'right',
            draggable=False,
            style={'color': 'white', 'backgroundColor': 'gray', 'border': '2px solid white'}
        ),
        
        StreamlitFlowNode(
            '3',
            (250, 10),
            {'content': "###### **ETAPA 2**<br>EVTA Hygge com<br>cenário de certificação"},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': '#3B3032', 'border': '2px solid white'}
        ),
        StreamlitFlowNode(
            '4',
            (250, 120),
            {'content': "Prazo: **20 dias úteis**"},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': 'gray', 'border': '2px solid white'}
        ),
        
        StreamlitFlowNode(
            '5',
            (490, 10),
            {'content': "###### **ETAPA 3**<br>Decisões do cliente<br> sobre o projeto"},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}
        ),
        StreamlitFlowNode(
            '6',
            (490, 120),
            {'content': 'Data: **a definir pelo cliente**'},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': 'gray', 'border': '2px solid white'}
        ),
        
        StreamlitFlowNode(
            '7',
            (730, 10),
            {'content': "###### **ETAPA 4**<br>Aplicação das<br>medidas em projeto"},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}
        ),
        StreamlitFlowNode(
            '8',
            (730, 120),
            {'content': 'Data: **a definir pelo cliente**'},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': 'gray', 'border': '2px solid white'}
        ),
        
        StreamlitFlowNode(
            '9',
            (980, 10),
            {'content': "###### **ETAPA 5**<br>Envio de documentos<br>no Checklist Hygge"},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': '#b45f06', 'border': '2px solid white'}
        ),
        StreamlitFlowNode(
            '10',
            (980, 120),
            {'content': 'Data: **a definir pelo cliente**'},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': 'gray', 'border': '2px solid white'}
        ),
        
        StreamlitFlowNode(
            '11',
            (1250, 10),
            {'content': "###### **ETAPA 6**<br>Envio dos documentos<br>para o EDGE"},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': '#3B3032', 'border': '2px solid white'}
        ),
        StreamlitFlowNode(
            '12',
            (1250, 120),
            {'content': 'Prazo: **assim que a documentação<br>estiver completa**'},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': 'gray', 'border': '2px solid white'}
        ),
        
        StreamlitFlowNode(
            '13',
            (1500, 10),
            {'content': "###### **ETAPA 7**<br>Verificação da documentação<br>pelo EDGE"},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': '#3d85c6', 'border': '2px solid white'}
        ),
        StreamlitFlowNode(
            '14',
            (1500, 120),
            {'content': 'Prazo: **21 dias**'},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': 'gray', 'border': '2px solid white'}
        ),
        
        StreamlitFlowNode(
            '15',
            (1790, 10),
            {'content': '###### **CERTIFICAÇÃO<br>PRELIMINAR<br>EDGE**'},
            'default',
            'right',
            'left',
            draggable=False,
            style={'color': 'white', 'backgroundColor': '#6aa84f', 'border': '2px solid white'}
        ),
        
    ]

    edges = [StreamlitFlowEdge('1-3', '1', '3', animated=True, marker_end={'type': 'arrow'}),
             StreamlitFlowEdge('3-5', '3', '5', animated=True, marker_end={'type': 'arrow'}),
             StreamlitFlowEdge('5-7', '5', '7', animated=True, marker_end={'type': 'arrow'}),
             StreamlitFlowEdge('7-9', '7', '9', animated=True, marker_end={'type': 'arrow'}),
             StreamlitFlowEdge('9-11', '9', '11', animated=True, marker_end={'type': 'arrow'}),
             StreamlitFlowEdge('11-13', '11', '13', animated=True, marker_end={'type': 'arrow'}),
             StreamlitFlowEdge('13-15', '13', '15', animated=True, marker_end={'type': 'arrow'})
             ]

    if 'static_flow_state' not in st.session_state:
        st.session_state.static_flow_state = StreamlitFlowState(nodes, edges)

    streamlit_flow('static_flow',
        st.session_state.static_flow_state,
        fit_view=True,
        show_minimap=False,
        show_controls=False,
        pan_on_drag=True,
        allow_zoom=True,
        hide_watermark=True)