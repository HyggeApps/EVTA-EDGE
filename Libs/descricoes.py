import streamlit as st
from pathlib import Path
from PIL import Image

# st expander para as categorias do EDGE

def descricoes_categorias():
    st.title('Fluxograma das etapas de certificação')
    st.write('----')
    png_fluxo = Path(__file__).parent / "Imgs/fluxoEDGE.png"

    img = Image.open(png_fluxo)
    width, height = img.size
    st.image(img.resize((int(width * 0.3), int(height * 0.3))))
    st.write('----')
    st.title('Etapas de certificação')

    cols = st.columns(2)

    with cols[0]:
        st.subheader('Preliminar')
        with st.expander("Descrição", expanded=False):
            st.write("A Certificação Preliminar do projeto é realizada com base nas estratégias adotadas nos projetos arquitetônicos e de disciplinas complementares do empreendimento.")
            st.write("Dentre os documentos a serem submetidos para a certificação estão pranchas dos projetos, memoriais descritivos, memoriais de cálculo e fichas técnicas que comprovem as medidas que serão implementadas.")

    with cols[1]:
        st.subheader('Pós-Construção')
        with st.expander("Descrição", expanded=False):
            st.write("A certificação Pós-Construção diz respeito à implementação, em obra, das medidas previstas em projeto na fase de Certificação Preliminar, além da atualização de quaisquer alterações realizadas durante a construção do empreendimento.")
            st.write("Dentre os documentos a serem submetidos, estão os projetos e memoriais descritivos atualizados conforme construção, fotos da implementação das medidas em obra e documentos de compra dos materiais.")
    
    st.write('----')
    st.title('Categorias')
    st.info('O EDGE é composto por 3 categorias principais: **Energia**, **Água** e **Materiais**. Os detalhes de cada categoria são apresentados abaixo.')
    cols = st.columns(3)

    with cols[0]:
        st.subheader('Energia')
        with st.expander('Descrição', expanded=False):
            st.write("A eficiência energética é uma das três categorias de recursos que compõem o padrão EDGE, com requisito mínimo de eficiência de 20%, que deve ser conquistado através de medidas de redução de consumo energético do edifício ou de geração de energia.")
            st.write("Para fins de certificação, a equipe de projeto e construção deve revisar os requisitos para as medidas apresentadas e fornecer as informações solicitadas.")

    with cols[1]:
        st.subheader('Água')
        with st.expander("Descrição", expanded=False):
            st.write("A eficiência hídrica é uma das três categorias de recursos que compõem o padrão EDGE, com requisito mínimo de eficiência de 20%, que deve ser conquistado através de medidas de redução de consumo de água potável do empreendimento.")
            st.write("Para fins de certificação, a equipe de projeto e construção deve revisar os requisitos para as medidas apresentadas e fornecer as informações solicitadas.")

    with cols[2]:
        st.subheader('Materiais')
        with st.expander("Descrição", expanded=False):
            st.write("A eficiência de materiais é uma das três categorias de recursos que compõem o padrão EDGE, com requisito mínimo de eficiência de 20%, que deve ser conquistado através da melhoria do sistema construtivo para menor incorporação de carbono na edificação.")
            st.write("Para fins de certificação, a equipe de projeto e construção deve revisar os requisitos para as medidas apresentadas e fornecer as informações solicitadas.")
    

    st.write('----')
    st.title('Etapas de documentação')

    cols = st.columns(3)

    with cols[0]:
        st.subheader('Projeto')
        with st.expander("Descrição", expanded=False):
            st.write("* Momento em que as estratégias precisam ser incorporadas e registradas nos projetos arquitetônicos e de disciplinas complementares do empreendimento.")
            st.write("* Os itens dessa fase são referentes às informações que precisam estar contidas nos projetos, memoriais e fichas técnicas para envio para a Certificação Preliminar.")

    with cols[1]:
        st.subheader('Obra')
        with st.expander("Descrição", expanded=False):
            st.write("* Fase de execução da construção do edifício, na qual devem ser implementadas as soluções previstas na fase de projeto.")
            st.write("* Os itens dessa fase são referentes ao registro e comprovação da implementação das estratégias, para envio para a Certificação Pós-Construção.")

    with cols[2]:
        st.subheader("Pós-construção")
        with st.expander("Descrição", expanded=False):
            st.write("* Fase de revisão da documentação considerando quaisquer alterações realizadas durante a construção em relação ao que foi previsto para a Certificação Preliminar.")
            st.write("* Os itens dessa fase são referentes à apresentação de projetos e memoriais atualizados, conforme o que foi construído, bem como documentos de compra, para envio para a Certificação Pós-Construção.")
    st.write('----')
    st.title('Pré-requisitos e créditos')
    st.info('Todos os itens marcados com **(*)** são pré-requisitos')

    cols = st.columns(3)

    with cols[0]:
        st.subheader('Energia')
        with st.expander('EEM01*'):
            st.write("Diz respeito ao equilíbrio dos benefícios de iluminação e ventilação dos vidros, garantindo níveis mínimos de iluminação sem exceder significativamente os ganhos de calor solar.")
            st.write("É avaliada a proporção entre janelas e paredes do edifício (WWR).")
        with st.expander('EEM02'):
            st.write("Diz respeito à especificação de coberturas com maior refletância solar, para reduzir a carga de resfriamento em espaços com ar-condicionado e melhorar o conforto térmico em espaços sem ar-condicionado.")
            st.write("É avaliado o valor de Índice de Refletância Solar (SRI) dos materiais.")
        with st.expander('EEM03'):
            st.write("Diz respeito à especificação de paredes externas com maior refletância solar, para reduzir a carga de resfriamento em espaços com ar-condicionado e melhorar o conforto térmico em espaços sem ar-condicionado.")
            st.write("É avaliado o valor de Índice de Refletância Solar (SRI) dos materiais.")
        with st.expander('EEM04'):
            st.write("É necessário proteger os elementos envidraçados da radiação solar direta, reduzindo o brilho e o ganho de calor solar radiante em climas em que o resfriamento é dominante.")
            st.write("É avaliado o (fator de sombreamento médio anual (AASF).")
        with st.expander('EEM05*'):
            st.write("Diz respeito ao desempenho térmico do telhado, que visa evitar a transmissão de calor do ambiente externo para o ambiente interno (em climas quentes) e do espaço interno para o ambiente externo (em climas frios).")
            st.write("É avaliada a Transmitância Térmica da cobertura (U em W/m²K).")
        with st.expander('EEM06*'):
            st.write("Diz respeito ao desempenho térmico da laje, que visa evitar a transmissão de calor do ambiente externo para o ambiente interno (em climas quentes) e do espaço interno para o ambiente externo (em climas frios).")
            st.write("É avaliada a Transmitância Térmica da laje (U em W/m²K).")
        with st.expander('EEM07'):
            st.write("A intenção é a utilização do solo e de vegetação para isolar e sombrear o telhado, reduzindo assim a transferência de calor através dele. A transpiração da vegetação também proporciona um efeito refrescante.")
            st.write("São avaliadas a área de telhado e a profundidade da camada de cultivo.")
        with st.expander('EEM08*'):
            st.write("Diz respeito ao desempenho térmico das paredes externas, que visa evitar a transmissão de calor do ambiente externo para o ambiente interno (em climas quentes) e do espaço interno para o ambiente externo (em climas frios).")
            st.write("É avaliada a Transmitância Térmica das paredes (U em W/m²K).")
        with st.expander('EEM09*'):
            st.write("Diz respeito à eficiência dos vidros, que visa reduzir a transferência de calor de um lado para o outro, refletindo a energia térmica.")
            st.write("São avaliados o U-value (em W/m²), o Fator Solar (SHGC) e a Transmissão Luminosa (VT) do vidro.")
        with st.expander('EEM10'):
            st.write("O propósito é reduzir a infiltração de ar, assim a carga no sistema de ar-condicionado pode ser reduzida significativamente.")
            st.write("São avaliadas as estratégias de vedação de ar do edifício.")
        with st.expander('EEM11'):
            st.write("Diz respeito à estratégia de ventilação natural, que pode melhorar o conforto dos ocupantes, fornecendo acesso ao ar fresco e reduzindo a temperatura. Isso resulta em uma redução da carga de resfriamento, o que reduz o capital inicial e os custos de manutenção.")
            st.write("São avaliadas as dimensões das janelas e o controle de desligamento do ar-condicionado.")
        with st.expander('EEM12'):
            st.write("A intenção é a utilização de ventiladores de teto, para aumentar o movimento do ar, ajudando a melhorar o conforto humano ao promover a evaporação da transpiração (resfriamento evaporativo).")
            st.write("É avaliada a previsão de ventiladores e o tamanho dos equipamentos.")
        with st.expander('EEM13*'):
            st.write("Diz respeito ao nível de eficiência dos sistemas de ar-condicionado.")
            st.write("É avaliado o COP (W/W) dos sistemas.")
        with st.expander('EEM14'):
            st.write("A intenção é a instalação de inversores de velocidade variável, pois serão reduzidos os gastos de energia e, portanto, os custos da concessionária. Os ventiladores VSD oferecem maior confiabilidade e controle dos processos.")
            st.write("É avaliada a implementação ou não de VSD.")
        with st.expander('EEM15'):
            st.write("Diz respeito à instalação de sistema de precondicionamento de ar, para reduzir a diferença de temperatura entre o ar externo que entra na edificação e o ar-condicionado interno, reduzindo a carga no sistema de condicionamento do espaço.")
            st.write("É avaliada a eficiência de transferência de temperatura (TTE) dos equipamentos.")
        with st.expander('EEM16*'):
            st.write("Diz respeito à eficiência do sistema de aquecimento de ar do ambiente, que é responsável pelos maiores usos de energia em edificações e, muitas vezes, usa combustíveis fósseis.")
            st.write("É avaliado o COP (W/W) dos sistemas.")
        with st.expander('EEM17'):
            st.write("Diz respeito à utilização de válvulas termostáticas para o controle de temperatura dos ambientes, impedindo que os espaços fiquem muito quentes e que os ocupantes precisem controlar os radiadores manualmente.")
            st.write("É avaliada a instalação ou não de válvulas termostáticas.")
        with st.expander('EEM18'):
            st.write("Diz respeito à instalação de aquecimento de água eficiente, pois o fornecimento de água quente com alta eficiência reduz o consumo de combustível e as emissões de carbono relacionadas ao aquecimento da água.")
            st.write("É avaliada a eficiência do sistema de aquecimento de água.")
        with st.expander('EEM19'):
            st.write("Diz respeito à utilização de um dispositivo de recuperação de calor para capturar e reutilizar o calor residual para preaquecimento da água fornecida pelo sistema de água quente, para auxiliar na redução da capacidade projetada dos aquecedores de água.")
            st.write("É avaliada a eficiência do sistema de preaquecimento.")
        with st.expander('EEM20'):
            st.write("Diz respeito à instalação de economizadores no sistema de HVAC, para reduzir o uso de energia do sistema de resfriamento.")
            st.write("É avaliada a instalação ou não de economizadores.")
        with st.expander('EEM21'):
            st.write("Diz respeito à utilização de sensores de CO2 para controle de, pelo menos, 50% do sistema de ventilação mecânica do edifício, para reduzir o consumo energético.")
            st.write("É avaliada a instalação ou não de sensores de CO2.")
        with st.expander('EEM22'):
            st.write("Diz respeito à utilização de lâmpadas de alta eficiência nas áreas internas, visto que produzem mais luz com menos energia em comparação com lâmpadas convencionais, reduzindo o uso de energia para iluminação.")
            st.write("É avaliada a densidade de potência (DPI em W/m²) ou a eficácia luminosa (lm/W).")
        with st.expander('EEM23'):
            st.write("Diz respeito à utilização de lâmpadas de alta eficiência nas áreas externas, visto que produzem mais luz com menos energia em comparação com lâmpadas convencionais, reduzindo o uso de energia para iluminação.")
            st.write("É avaliada a densidade de potência (DPI em W/m²) ou a eficácia luminosa (lm/W).")
        with st.expander('EEM24'):
            st.write("Trata da previsão de iluminação controlada por tecnologias como sensores de presença, temporizadores [timers] ou sensores de luz natural.")
            st.write("É avaliada a instalação ou não de controle de iluminação nos ambientes do edifício.")
        with st.expander('EEM25'):
            st.write("Diz respeito à utilização da luz natural de claraboia(s) para iluminar o interior, reduzindo o uso de iluminação artificial durante o dia.")
            st.write("É avaliada a implementação de claraboias e o atendimento de níveis mínimos de iluminação natural.")
        with st.expander('EEM26'):
            st.write("Diz respeito à utilização de sensores de CO2 para controle de, pelo menos, 50% do sistema de ventilação mecânica dos estacionamentos.")
            st.write("É avaliada a instalação ou não de sensores de CO2.")
        with st.expander('EEM27*'):
            st.write("Diz respeito ao desempenho térmico da envoltória de armazenamentos a frio, que visa evitar a transmissão de calor do ambiente externo para o ambiente interno.")
            st.write("É avaliada a Transmitância Térmica da cobertura (U em W/m²K).")
        with st.expander('EEM28'):
            st.write("Diz respeito ao uso de câmaras frigoríficas e qualquer outro refrigerador ou frigorífico energeticamente eficientes no edifício.")
            st.write("É avaliada a certificação dos equipamentos por selos de eficiência.")
        with st.expander('EEM29'):
            st.write("Diz respeito ao uso de refrigeradores e máquinas de lavar roupa energeticamente eficientes no edifício.")
            st.write("É avaliada a certificação dos equipamentos por selos de eficiência.")
        with st.expander('EEM30'):
            st.write("Trata da instalação de medidores dedicados para os sistemas de aquecimento e refrigeração do edifício, com o objetivo de redução de consumo energético e aumento de consciência.")
            st.write("É avaliada a instalação ou não de medidores dedicados.")
        with st.expander('EEM31'):
            st.write("Se refere à redução da demanda de energia por meio de uma maior conscientização sobre o consumo, pelo uso de medidores inteligentes na edificação.")
            st.write("É avaliada a instalação ou não de medidores inteligentes.")
        with st.expander('EEM32'):
            st.write("Diz respeito à instalação de dispositivos de correção do fator de potência, como estabilizadores de tensão, na corrente que entra na edificação.")
            st.write("É avaliada a instalação ou não de dispositivos de correção.")
        with st.expander('EEM33'):
            st.write("Diz respeito à redução do uso de eletricidade gerada a partir de combustíveis fósseis, como, por exemplo, o carvão com geração de energia renovável no local.")
            st.write("É avaliada a geração de energia renovável do edifício em relação ao consumo total de energia (%).")
        with st.expander('EEM34'):
            st.write("Esta medida pode ser usada para reivindicar economias de energia de estratégias e tecnologias que não façam parte da lista de medidas EDGE. O projeto deve apresentar uma solicitação de resolução especial para obter a aprovação para reivindicar as economias.")
            st.write("São avaliadas medidas adicionais que gere redução no consumo de energia.")
        with st.expander('EEM35'):
            st.write("Esta medida trata da firmação de um contrato para a aquisição de novas energias renováveis fora do local especificamente atribuídas ao projeto de construção.")
            st.write("É avaliada a quantidade de energia adquirida externamente.")
        with st.expander('EEM36'):
            st.write("Diz respeito à redução da pegada de carbono total do projeto através da contratação de investimento em um projeto de compensação de carbono.")
            st.write("É avaliada a quantidade de compensação de carbono adquirida para o projeto.")
        with st.expander('EEM37'):
            st.write("Diz respeito à implementação de agentes refrigerantes com baixo potencial de aquecimento global.")
            st.write("São avaliados os tamanhos do sistema (kW), o tipo de agente refrigerante, a carga de agente refrigerante (kg/KW) e o vazamento (%).")

    with cols[1]:
        st.subheader('Água')
        with st.expander('WEM01*'):
            st.write("Diz respeito à utilização de chuveiros com uma baixa vazão sem afetar a funcionalidade. É necessário que os chuveiros apresentem vazão eficiente para causar impacto para a certificação. Tal vazão pode ser alcançada com materiais mais eficientes ou com a combinação de um chuveiro e arejador/restritor para melhor regulagem.")
            st.write("É avaliada a vazão dos chuveiros (em L/min).")
        with st.expander('WEM02*'):
            st.write("Diz respeito à utilização de torneiras de banheiros com uma baixa vazão sem afetar a funcionalidade. É necessário que as torneiras apresentem vazão eficiente para a certificação. Tal vazão pode ser alcançada com materiais mais eficientes ou com a combinação de uma torneira e arejador/restritor para melhor regulagem.")
            st.write("É avaliada a vazão das torneiras (em L/min).")
        with st.expander('WEM03*'):
            st.write("Diz respeito à utilização de torneiras de banheiros públicos com uma baixa vazão sem afetar a funcionalidade. É necessário que as torneiras apresentem vazão eficiente para a certificação. Tal vazão pode ser alcançada com materiais mais eficientes ou com a combinação de uma torneira e arejador/restritor para melhor regulagem.")
            st.write("É avaliada a vazão das torneiras (em L/min).")
        with st.expander('WEM04*'):
            st.write("Diz respeito à utilização de bacias sanitárias de todos os banheiros com um baixo consumo por acionamento sem afetar a funcionalidade.")
            st.write("É avaliada a vazão das bacias sanitárias (L/fluxo).")
        with st.expander('WEM05*'):
            st.write("Diz respeito à utilização de bacias sanitárias de todos os banheiros públicos com um baixo consumo por acionamento sem afetar a funcionalidade.")
            st.write("É avaliada a vazão das bacias sanitárias (L/fluxo).")
        with st.expander('WEM06'):
            st.write("Diz respeito à utilização de bidês de todos os banheiros com uma baixa vazão sem afetar a funcionalidade.")
            st.write("É avaliada a vazão dos bidês (L/min).")
        with st.expander('WEM07'):
            st.write("Diz respeito à utilização de mictórios de todos os banheiros com um baixo consumo por acionamento sem afetar a funcionalidade.")
            st.write("É avaliada a vazão dos bidês (L/fluxo).")
        with st.expander('WEM08*'):
            st.write("Diz respeito à utilização de torneiras de cozinha com uma baixa vazão sem afetar a funcionalidade. É necessário que as torneiras apresentem vazão eficiente para a certificação. Tal vazão pode ser alcançada com materiais mais eficientes ou com a combinação de uma torneira e arejador/restritor para melhor regulagem.")
            st.write("É avaliada a vazão das torneiras (em L/min).")
        with st.expander('WEM09'):
            st.write("Diz respeito à utilização de máquinas de lavar louças com um baixo consumo de água por ciclo.")
            st.write("É avaliado o consumo de água por ciclo (L/ciclo).")
        with st.expander('WEM10'):
            st.write("Diz respeito à utilização de esguichos pré-lavagem com baixa vazão sem afetar a funcionalidade.")
            st.write("É avaliada a vazão dos esguichos (em L/min).")
        with st.expander('WEM11'):
            st.write("Diz respeito à utilização de máquinas de lavar roupas com um baixo consumo de água por quilograma de roupa lavada.")
            st.write("É avaliado o consumo de água por ciclo (L/kg).")
        with st.expander('WEM12'):
            st.write("Diz respeito à piscina(s) equipadas com coberturas ou capas para evitar perdas de calor e água por evaporação.")
            st.write("É avaliada a cobertura de todas as piscinas do edifício.")
        with st.expander('WEM13'):
            st.write("Trata da implementação de um sistema de paisagismo com eficiência hídrica à edificação a fim de reduzir o consumo de água destinada a esse uso.")
            st.write("É avaliado o consumo de água do sistema de irrigação (L/m²/dia).")
        with st.expander('WEM14'):
            st.write("Diz respeito à redução do uso de água potável do abastecimento municipal com a implementação de um sistema de coleta de águas pluviais para fornecer água dentro do empreendimento.")
            st.write("É avaliada a área de telhado para captação de água da chuva e os usos finais dessa água.")
        with st.expander('WEM15'):
            st.write("Diz respeito à implementação de um sistema de reciclagem de águas negras ou cinzentas que trate as águas residuais da edificação. A água reciclada deve ser reutilizada no local do projeto para substituir o consumo de água do abastecimento municipal. Os usos finais podem incluir descarga de vasos sanitários, sistema de AVAC, limpeza da edificação ou irrigação/paisagismo.")
            st.write("É avaliada a porcentagem de água reciclada e os usos finais dessa água.")
        with st.expander('WEM16'):
            st.write("Diz respeito à instalação de um dispositivo de recuperação de água condensada com capacidade para coletar toda a água condensada do sistema de refrigeração, e essa água condensada for usada para paisagismo, descargas de vasos sanitários ou uso externo.")
            st.write("É verificada a porcentagem de água recuperada e os usos finais dessa água.")
        with st.expander('WEM17'):
            st.write("Trata do fornecimento de medição inteligente para cada proprietário ou inquilino da edificação. Os proprietários podem assinar um sistema de monitoramento on-line.")
            st.write("É verificada a instalação de hidrômetros inteligentes nas unidades habitacionais.")

    with cols[2]:
        st.subheader('Materiais')
        with st.expander('MEM01*'):
            st.write("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado da laje do piso inferior.")
            st.write("São avaliadas a tipologia do sistema construtivo, a sua espessura e taxa de consumo de aço.")
        with st.expander('MEM02*'):
            st.write("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado nas lajes intermediárias.")
            st.write("São avaliadas a tipologia do sistema construtivo e suas características principais (como espessura e taxa de consumo de aço).")
        with st.expander('MEM03*'):
            st.write("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado no acabamento dos pisos.")
            st.write("São consideradas a espessura e tipologia de piso.")
        with st.expander('MEM04*'):
            st.write("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado da laje da cobertura.")
            st.write("São avaliadas a tipologia do sistema construtivo e suas características principais (como espessura e taxa de consumo de aço).")
        with st.expander('MEM05*'):
            st.write("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado das paredes externas.")
            st.write("São avaliadas as camadas de cada tipologia de sistema construtivo e suas espessuras.")
        with st.expander('MEM06*'):
            st.write("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado das paredes internas.")
            st.write("São avaliadas as camadas de cada tipologia de sistema construtivo e suas espessuras.")
        with st.expander('MEM07*'):
            st.write("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado das esquadrias de janela.")
            st.write("São avaliados os materiais que compõem as esquadrias externas.")
        with st.expander('MEM08*'):
            st.write("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado nos vidros instalados.")
            st.write("São avaliados o modelo e a tipologia de vidro instalados.")
        with st.expander('MEM09*'):
            st.write("Diz respeito à utilização de materiais de isolamento da cobertura com redução no carbono incorporado.")
            st.write("São avaliadas a tipologia de isolamento e a sua espessura.")
        with st.expander('MEM10*'):
            st.write("Diz respeito à utilização de materiais de isolamento das paredes externas com redução no carbono incorporado.")
            st.write("São avaliadas a tipologia de isolamento e a sua espessura.")
        with st.expander('MEM11*'):
            st.write("Diz respeito à utilização de materiais de isolamento dos pisos com redução no carbono incorporado.")
            st.write("São avaliadas a tipologia de isolamento e a sua espessura.")
        
    st.write('----')


def descricoes_creditos(credito):
    if 'EEM01' in credito:
        with st.expander('EEM01*', expanded=True):
            st.info("Diz respeito ao equilíbrio dos benefícios de iluminação e ventilação dos vidros, garantindo níveis mínimos de iluminação sem exceder significativamente os ganhos de calor solar.")
            st.info("É avaliada a proporção entre janelas e paredes do edifício (WWR).")
    elif 'EEM02' in credito:
        with st.expander('EEM02', expanded=True):
            st.info("Diz respeito à especificação de coberturas com maior refletância solar, para reduzir a carga de resfriamento em espaços com ar-condicionado e melhorar o conforto térmico em espaços sem ar-condicionado.")
            st.info("É avaliado o valor de Índice de Refletância Solar (SRI) dos materiais.")
    elif 'EEM03' in credito:
        with st.expander('EEM03', expanded=True):
            st.info("Diz respeito à especificação de paredes externas com maior refletância solar, para reduzir a carga de resfriamento em espaços com ar-condicionado e melhorar o conforto térmico em espaços sem ar-condicionado.")
            st.info("É avaliado o valor de Índice de Refletância Solar (SRI) dos materiais.")
    elif 'EEM04' in credito:
        with st.expander('EEM04', expanded=True):
            st.info("É necessário proteger os elementos envidraçados da radiação solar direta, reduzindo o brilho e o ganho de calor solar radiante em climas em que o resfriamento é dominante.")
            st.info("É avaliado o (fator de sombreamento médio anual (AASF).")
    elif 'EEM05' in credito:
        with st.expander('EEM05*', expanded=True):
            st.info("Diz respeito ao desempenho térmico do telhado, que visa evitar a transmissão de calor do ambiente externo para o ambiente interno (em climas quentes) e do espaço interno para o ambiente externo (em climas frios).")
            st.info("É avaliada a Transmitância Térmica da cobertura (U em W/m²K).")
    elif 'EEM06' in credito:
        with st.expander('EEM06*', expanded=True):
            st.info("Diz respeito ao desempenho térmico da laje, que visa evitar a transmissão de calor do ambiente externo para o ambiente interno (em climas quentes) e do espaço interno para o ambiente externo (em climas frios).")
            st.info("É avaliada a Transmitância Térmica da laje (U em W/m²K).")
    elif 'EEM07' in credito:
        with st.expander('EEM07', expanded=True):
            st.info("A intenção é a utilização do solo e de vegetação para isolar e sombrear o telhado, reduzindo assim a transferência de calor através dele. A transpiração da vegetação também proporciona um efeito refrescante.")
            st.info("São avaliadas a área de telhado e a profundidade da camada de cultivo.")
    elif 'EEM08' in credito:
        with st.expander('EEM08*', expanded=True):
            st.info("Diz respeito ao desempenho térmico das paredes externas, que visa evitar a transmissão de calor do ambiente externo para o ambiente interno (em climas quentes) e do espaço interno para o ambiente externo (em climas frios).")
            st.info("É avaliada a Transmitância Térmica das paredes (U em W/m²K).")
    elif 'EEM09' in credito:
        with st.expander('EEM09*', expanded=True):
            st.info("Diz respeito à eficiência dos vidros, que visa reduzir a transferência de calor de um lado para o outro, refletindo a energia térmica.")
            st.info("São avaliados o U-value (em W/m²), o Fator Solar (SHGC) e a Transmissão Luminosa (VT) do vidro.")
    elif 'EEM10' in credito:
        with st.expander('EEM10', expanded=True):
            st.info("O propósito é reduzir a infiltração de ar, assim a carga no sistema de ar-condicionado pode ser reduzida significativamente.")
            st.info("São avaliadas as estratégias de vedação de ar do edifício.")
    elif 'EEM11' in credito:
        with st.expander('EEM11', expanded=True):
            st.info("Diz respeito à estratégia de ventilação natural, que pode melhorar o conforto dos ocupantes, fornecendo acesso ao ar fresco e reduzindo a temperatura. Isso resulta em uma redução da carga de resfriamento, o que reduz o capital inicial e os custos de manutenção.")
            st.info("São avaliadas as dimensões das janelas e o controle de desligamento do ar-condicionado.")
    elif 'EEM12' in credito:
        with st.expander('EEM12', expanded=True):
            st.info("A intenção é a utilização de ventiladores de teto, para aumentar o movimento do ar, ajudando a melhorar o conforto humano ao promover a evaporação da transpiração (resfriamento evaporativo).")
            st.info("É avaliada a previsão de ventiladores e o tamanho dos equipamentos.")
    elif 'EEM13' in credito:
        with st.expander('EEM13*', expanded=True):
            st.info("Diz respeito ao nível de eficiência dos sistemas de ar-condicionado.")
            st.info("É avaliado o COP (W/W) dos sistemas.")
    elif 'EEM14' in credito:
        with st.expander('EEM14', expanded=True):
            st.info("A intenção é a instalação de inversores de velocidade variável, pois serão reduzidos os gastos de energia e, portanto, os custos da concessionária. Os ventiladores VSD oferecem maior confiabilidade e controle dos processos.")
            st.info("É avaliada a implementação ou não de VSD.")
    elif 'EEM15' in credito:
        with st.expander('EEM15', expanded=True):
            st.info("Diz respeito à instalação de sistema de precondicionamento de ar, para reduzir a diferença de temperatura entre o ar externo que entra na edificação e o ar-condicionado interno, reduzindo a carga no sistema de condicionamento do espaço.")
            st.info("É avaliada a eficiência de transferência de temperatura (TTE) dos equipamentos.")
    elif 'EEM16' in credito:
        with st.expander('EEM16*', expanded=True):
            st.info("Diz respeito à eficiência do sistema de aquecimento de ar do ambiente, que é responsável pelos maiores usos de energia em edificações e, muitas vezes, usa combustíveis fósseis.")
            st.info("É avaliado o COP (W/W) dos sistemas.")
    elif 'EEM17' in credito:
        with st.expander('EEM17', expanded=True):
            st.info("Diz respeito à utilização de válvulas termostáticas para o controle de temperatura dos ambientes, impedindo que os espaços fiquem muito quentes e que os ocupantes precisem controlar os radiadores manualmente.")
            st.info("É avaliada a instalação ou não de válvulas termostáticas.")
    elif 'EEM18' in credito:
        with st.expander('EEM18', expanded=True):
            st.info("Diz respeito à instalação de aquecimento de água eficiente, pois o fornecimento de água quente com alta eficiência reduz o consumo de combustível e as emissões de carbono relacionadas ao aquecimento da água.")
            st.info("É avaliada a eficiência do sistema de aquecimento de água.")
    elif 'EEM19' in credito:
        with st.expander('EEM19', expanded=True):
            st.info("Diz respeito à utilização de um dispositivo de recuperação de calor para capturar e reutilizar o calor residual para preaquecimento da água fornecida pelo sistema de água quente, para auxiliar na redução da capacidade projetada dos aquecedores de água.")
            st.info("É avaliada a eficiência do sistema de preaquecimento.")
    elif 'EEM20' in credito:
        with st.expander('EEM20', expanded=True):
            st.info("Diz respeito à instalação de economizadores no sistema de HVAC, para reduzir o uso de energia do sistema de resfriamento.")
            st.info("É avaliada a instalação ou não de economizadores.")
    elif 'EEM21' in credito:
        with st.expander('EEM21', expanded=True):
            st.info("Diz respeito à utilização de sensores de CO2 para controle de, pelo menos, 50% do sistema de ventilação mecânica do edifício, para reduzir o consumo energético.")
            st.info("É avaliada a instalação ou não de sensores de CO2.")
    elif 'EEM22' in credito:
        with st.expander('EEM22', expanded=True):
            st.info("Diz respeito à utilização de lâmpadas de alta eficiência nas áreas internas, visto que produzem mais luz com menos energia em comparação com lâmpadas convencionais, reduzindo o uso de energia para iluminação.")
            st.info("É avaliada a densidade de potência (DPI em W/m²) ou a eficácia luminosa (lm/W).")
    elif 'EEM23' in credito:
        with st.expander('EEM23', expanded=True):
            st.info("Diz respeito à utilização de lâmpadas de alta eficiência nas áreas externas, visto que produzem mais luz com menos energia em comparação com lâmpadas convencionais, reduzindo o uso de energia para iluminação.")
            st.info("É avaliada a densidade de potência (DPI em W/m²) ou a eficácia luminosa (lm/W).")
    elif 'EEM24' in credito:
        with st.expander('EEM24', expanded=True):
            st.info("Trata da previsão de iluminação controlada por tecnologias como sensores de presença, temporizadores [timers] ou sensores de luz natural.")
            st.info("É avaliada a instalação ou não de controle de iluminação nos ambientes do edifício.")
    elif 'EEM25' in credito:
        with st.expander('EEM25', expanded=True):
            st.info("Diz respeito à utilização da luz natural de claraboia(s) para iluminar o interior, reduzindo o uso de iluminação artificial durante o dia.")
            st.info("É avaliada a implementação de claraboias e o atendimento de níveis mínimos de iluminação natural.")
    elif 'EEM26' in credito:
        with st.expander('EEM26', expanded=True):
            st.info("Diz respeito à utilização de sensores de CO2 para controle de, pelo menos, 50% do sistema de ventilação mecânica dos estacionamentos.")
            st.info("É avaliada a instalação ou não de sensores de CO2.")
    elif 'EEM27' in credito:
        with st.expander('EEM27*', expanded=True):
            st.info("Diz respeito ao desempenho térmico da envoltória de armazenamentos a frio, que visa evitar a transmissão de calor do ambiente externo para o ambiente interno.")
            st.info("É avaliada a Transmitância Térmica da cobertura (U em W/m²K).")
    elif 'EEM28' in credito:
        with st.expander('EEM28', expanded=True):
            st.info("Diz respeito ao uso de câmaras frigoríficas e qualquer outro refrigerador ou frigorífico energeticamente eficientes no edifício.")
            st.info("É avaliada a certificação dos equipamentos por selos de eficiência.")
    elif 'EEM29' in credito:
        with st.expander('EEM29', expanded=True):
            st.info("Diz respeito ao uso de refrigeradores e máquinas de lavar roupa energeticamente eficientes no edifício.")
            st.info("É avaliada a certificação dos equipamentos por selos de eficiência.")
    elif 'EEM30' in credito:
        with st.expander('EEM30', expanded=True):
            st.info("Trata da instalação de medidores dedicados para os sistemas de aquecimento e refrigeração do edifício, com o objetivo de redução de consumo energético e aumento de consciência.")
            st.info("É avaliada a instalação ou não de medidores dedicados.")
    elif 'EEM31' in credito:
        with st.expander('EEM31', expanded=True):
            st.info("Se refere à redução da demanda de energia por meio de uma maior conscientização sobre o consumo, pelo uso de medidores inteligentes na edificação.")
            st.info("É avaliada a instalação ou não de medidores inteligentes.")
    elif 'EEM32' in credito:
        with st.expander('EEM32', expanded=True):
            st.info("Diz respeito à instalação de dispositivos de correção do fator de potência, como estabilizadores de tensão, na corrente que entra na edificação.")
            st.info("É avaliada a instalação ou não de dispositivos de correção.")
    elif 'EEM33' in credito:
        with st.expander('EEM33', expanded=True):
            st.info("Diz respeito à redução do uso de eletricidade gerada a partir de combustíveis fósseis, como, por exemplo, o carvão com geração de energia renovável no local.")
            st.info("É avaliada a geração de energia renovável do edifício em relação ao consumo total de energia (%).")
    elif 'EEM34' in credito:
        with st.expander('EEM34', expanded=True):
            st.info("Esta medida pode ser usada para reivindicar economias de energia de estratégias e tecnologias que não façam parte da lista de medidas EDGE. O projeto deve apresentar uma solicitação de resolução especial para obter a aprovação para reivindicar as economias.")
            st.info("São avaliadas medidas adicionais que gere redução no consumo de energia.")
    elif 'EEM35' in credito:
        with st.expander('EEM35', expanded=True):
            st.info("Esta medida trata da firmação de um contrato para a aquisição de novas energias renováveis fora do local especificamente atribuídas ao projeto de construção.")
            st.info("É avaliada a quantidade de energia adquirida externamente.")
    elif 'EEM36' in credito:
        with st.expander('EEM36', expanded=True):
            st.info("Diz respeito à redução da pegada de carbono total do projeto através da contratação de investimento em um projeto de compensação de carbono.")
            st.info("É avaliada a quantidade de compensação de carbono adquirida para o projeto.")
    elif 'EEM37' in credito:
        with st.expander('EEM37', expanded=True):
            st.info("Diz respeito à implementação de agentes refrigerantes com baixo potencial de aquecimento global.")
            st.info("São avaliados os tamanhos do sistema (kW), o tipo de agente refrigerante, a carga de agente refrigerante (kg/KW) e o vazamento (%).")
    elif 'WEM01' in credito:
        with st.expander('WEM01*', expanded=True):
            st.info("Diz respeito à utilização de chuveiros com uma baixa vazão sem afetar a funcionalidade. É necessário que os chuveiros apresentem vazão eficiente para causar impacto para a certificação. Tal vazão pode ser alcançada com materiais mais eficientes ou com a combinação de um chuveiro e arejador/restritor para melhor regulagem.")
            st.info("É avaliada a vazão dos chuveiros (em L/min).")
    elif 'WEM02' in credito:
        with st.expander('WEM02*', expanded=True):
            st.info("Diz respeito à utilização de torneiras de banheiros com uma baixa vazão sem afetar a funcionalidade. É necessário que as torneiras apresentem vazão eficiente para a certificação. Tal vazão pode ser alcançada com materiais mais eficientes ou com a combinação de uma torneira e arejador/restritor para melhor regulagem.")
            st.info("É avaliada a vazão das torneiras (em L/min).")
    elif 'WEM03' in credito:
        with st.expander('WEM03*', expanded=True):
            st.info("Diz respeito à utilização de torneiras de banheiros públicos com uma baixa vazão sem afetar a funcionalidade. É necessário que as torneiras apresentem vazão eficiente para a certificação. Tal vazão pode ser alcançada com materiais mais eficientes ou com a combinação de uma torneira e arejador/restritor para melhor regulagem.")
            st.info("É avaliada a vazão das torneiras (em L/min).")
    elif 'WEM04' in credito:
        with st.expander('WEM04*', expanded=True):
            st.info("Diz respeito à utilização de bacias sanitárias de todos os banheiros com um baixo consumo por acionamento sem afetar a funcionalidade.")
            st.info("É avaliada a vazão das bacias sanitárias (L/fluxo).")
    elif 'WEM05' in credito:
        with st.expander('WEM05*', expanded=True):
            st.info("Diz respeito à utilização de bacias sanitárias de todos os banheiros públicos com um baixo consumo por acionamento sem afetar a funcionalidade.")
            st.info("É avaliada a vazão das bacias sanitárias (L/fluxo).")
    elif 'WEM06' in credito:
        with st.expander('WEM06', expanded=True):
            st.info("Diz respeito à utilização de bidês de todos os banheiros com uma baixa vazão sem afetar a funcionalidade.")
            st.info("É avaliada a vazão dos bidês (L/min).")
    elif 'WEM07' in credito:
        with st.expander('WEM07', expanded=True):
            st.info("Diz respeito à utilização de mictórios de todos os banheiros com um baixo consumo por acionamento sem afetar a funcionalidade.")
            st.info("É avaliada a vazão dos bidês (L/fluxo).")
    elif 'WEM08' in credito:
        with st.expander('WEM08*', expanded=True):
            st.info("Diz respeito à utilização de torneiras de cozinha com uma baixa vazão sem afetar a funcionalidade. É necessário que as torneiras apresentem vazão eficiente para a certificação. Tal vazão pode ser alcançada com materiais mais eficientes ou com a combinação de uma torneira e arejador/restritor para melhor regulagem.")
            st.info("É avaliada a vazão das torneiras (em L/min).")
    elif 'WEM09' in credito:
        with st.expander('WEM09', expanded=True):
            st.info("Diz respeito à utilização de máquinas de lavar louças com um baixo consumo de água por ciclo.")
            st.info("É avaliado o consumo de água por ciclo (L/ciclo).")
    elif 'WEM10' in credito:
        with st.expander('WEM10', expanded=True):
            st.info("Diz respeito à utilização de esguichos pré-lavagem com baixa vazão sem afetar a funcionalidade.")
            st.info("É avaliada a vazão dos esguichos (em L/min).")
    elif 'WEM11' in credito:
        with st.expander('WEM11', expanded=True):
            st.info("Diz respeito à utilização de máquinas de lavar roupas com um baixo consumo de água por quilograma de roupa lavada.")
            st.info("É avaliado o consumo de água por ciclo (L/kg).")
    elif 'WEM12' in credito:
        with st.expander('WEM12', expanded=True):
            st.info("Diz respeito à piscina(s) equipadas com coberturas ou capas para evitar perdas de calor e água por evaporação.")
            st.info("É avaliada a cobertura de todas as piscinas do edifício.")
    elif 'WEM13' in credito:
        with st.expander('WEM13', expanded=True):
            st.info("Trata da implementação de um sistema de paisagismo com eficiência hídrica à edificação a fim de reduzir o consumo de água destinada a esse uso.")
            st.info("É avaliado o consumo de água do sistema de irrigação (L/m²/dia).")
    elif 'WEM14' in credito:
        with st.expander('WEM14', expanded=True):
            st.info("Diz respeito à redução do uso de água potável do abastecimento municipal com a implementação de um sistema de coleta de águas pluviais para fornecer água dentro do empreendimento.")
            st.info("É avaliada a área de telhado para captação de água da chuva e os usos finais dessa água.")
    elif 'WEM15' in credito:
        with st.expander('WEM15', expanded=True):
            st.info("Diz respeito à implementação de um sistema de reciclagem de águas negras ou cinzentas que trate as águas residuais da edificação. A água reciclada deve ser reutilizada no local do projeto para substituir o consumo de água do abastecimento municipal. Os usos finais podem incluir descarga de vasos sanitários, sistema de AVAC, limpeza da edificação ou irrigação/paisagismo.")
            st.info("É avaliada a porcentagem de água reciclada e os usos finais dessa água.")
    elif 'WEM16' in credito:
        with st.expander('WEM16', expanded=True):
            st.info("Diz respeito à instalação de um dispositivo de recuperação de água condensada com capacidade para coletar toda a água condensada do sistema de refrigeração, e essa água condensada for usada para paisagismo, descargas de vasos sanitários ou uso externo.")
            st.info("É verificada a porcentagem de água recuperada e os usos finais dessa água.")
    elif 'WEM17' in credito:
        with st.expander('WEM17', expanded=True):
            st.info("Trata do fornecimento de medição inteligente para cada proprietário ou inquilino da edificação. Os proprietários podem assinar um sistema de monitoramento on-line.")
            st.info("É verificada a instalação de hidrômetros inteligentes nas unidades habitacionais.")
    elif 'MEM01' in credito:
        with st.expander('MEM01*', expanded=True):
            st.info("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado da laje do piso inferior.")
            st.info("São avaliadas a tipologia do sistema construtivo, a sua espessura e taxa de consumo de aço.")
    elif 'MEM02' in credito:
        with st.expander('MEM02*', expanded=True):
            st.info("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado nas lajes intermediárias.")
            st.info("São avaliadas a tipologia do sistema construtivo e suas características principais (como espessura e taxa de consumo de aço).")
    elif 'MEM03' in credito:
        with st.expander('MEM03*', expanded=True):
            st.info("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado no acabamento dos pisos.")
            st.info("São consideradas a espessura e tipologia de piso.")
    elif 'MEM04' in credito:
        with st.expander('MEM04*', expanded=True):
            st.info("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado da laje da cobertura.")
            st.info("São avaliadas a tipologia do sistema construtivo e suas características principais (como espessura e taxa de consumo de aço).")
    elif 'MEM05' in credito:
        with st.expander('MEM05*', expanded=True):
            st.info("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado das paredes externas.")
            st.info("São avaliadas as camadas de cada tipologia de sistema construtivo e suas espessuras.")
    elif 'MEM06' in credito:
        with st.expander('MEM06*', expanded=True):
            st.info("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado das paredes internas.")
            st.info("São avaliadas as camadas de cada tipologia de sistema construtivo e suas espessuras.")
    elif 'MEM07' in credito:
        with st.expander('MEM07*', expanded=True):
            st.info("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado das esquadrias de janela.")
            st.info("São avaliados os materiais que compõem as esquadrias externas.")
    elif 'MEM08' in credito:
        with st.expander('MEM08*', expanded=True):
            st.info("Diz respeito à utilização de materiais e sistemas construtivos com redução no carbono incorporado nos vidros instalados.")
            st.info("São avaliados o modelo e a tipologia de vidro instalados.")
    elif 'MEM09' in credito:
        with st.expander('MEM09*', expanded=True):
            st.info("Diz respeito à utilização de materiais de isolamento da cobertura com redução no carbono incorporado.")
            st.info("São avaliadas a tipologia de isolamento e a sua espessura.")
    elif 'MEM10' in credito:
        with st.expander('MEM10*', expanded=True):
            st.info("Diz respeito à utilização de materiais de isolamento das paredes externas com redução no carbono incorporado.")
            st.info("São avaliadas a tipologia de isolamento e a sua espessura.")
    elif 'MEM11' in credito:
        with st.expander('MEM11*', expanded=True):
            st.info("Diz respeito à utilização de materiais de isolamento dos pisos com redução no carbono incorporado.")
            st.info("São avaliadas a tipologia de isolamento e a sua espessura.")
        
    st.write('----')