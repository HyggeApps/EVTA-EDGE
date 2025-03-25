import random
import time
import streamlit as st
from streamlit_echarts import st_echarts

def render_ring_gauge(energia, agua, material, key):
    option = {
        "series": [
            {
                "type": "gauge",
                "startAngle": 0,
                "endAngle": 360,
                "pointer": {"show": False},
                "progress": {
                    "show": True,
                    "overlap": False,
                    "roundCap": True,
                    "clip": False,
                    "itemStyle": {"borderWidth": 1, "borderColor": "#464646"},
                },
                "axisLine": {"lineStyle": {"width": 40}},
                "splitLine": {"show": False, "distance": 0, "length": 10},
                "axisTick": {"show": False},
                "axisLabel": {"show": False, "distance": 50},
                "data": [
                    {
                        "value": agua,
                        "name": "Água",
                        "title": {"offsetCenter": ["0%", "-30%"]},
                        "detail": {"offsetCenter": ["0%", "-20%"]},
                    },
                    {
                        "value": energia,
                        "name": "Energia",
                        "title": {"offsetCenter": ["0%", "0%"]},
                        "detail": {"offsetCenter": ["0%", "10%"]},
                    },
                    {
                        "value": material,
                        "name": "Materiais",
                        "title": {"offsetCenter": ["0%", "30%"]},
                        "detail": {"offsetCenter": ["0%", "40%"]},
                    },
                ],
                "title": {"fontSize": 14},
                "detail": {
                    "width": 50,
                    "height": 14,
                    "fontSize": 14,
                    "color": "auto",
                    "borderColor": "auto",
                    "borderRadius": 20,
                    "borderWidth": 1,
                    "formatter": "{value}%",
                },
            }
        ]
    }

    st_echarts(option, height="500px", key=key)
    
#render_ring_gauge()