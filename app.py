import streamlit as st

from currency_api import obter_cotacao, MENU_MOEDAS


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Cotação de Moedas",
    page_icon="💱",
    layout="centered",
)


# ==========================================================
# PALETA
# ==========================================================

AZUL_950 = "#020817"
AZUL_900 = "#06142E"
AZUL_800 = "#0A1F44"
AZUL_700 = "#0D2D66"
AZUL_600 = "#1456E8"
AZUL_500 = "#247BFF"
AZUL_400 = "#4BA3FF"
AZUL_300 = "#7DC4FF"
AZUL_200 = "#B9E0FF"

BRANCO = "#FFFFFF"
CINZA = "#AFC4DD"


# ==========================================================
# CSS
# ==========================================================

st.markdown(
    f"""
<style>

.stApp {{
    background:
        radial-gradient(
            circle at 5% 5%,
            rgba(20, 86, 232, 0.28),
            transparent 28%
        ),
        radial-gradient(
            circle at 95% 10%,
            rgba(75, 163, 255, 0.18),
            transparent 24%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(13, 45, 102, 0.30),
            transparent 32%
        ),
        linear-gradient(
            145deg,
            {AZUL_950},
            {AZUL_900} 45%,
            #030B19 100%
        );

    color: {BRANCO};
}}


/* ==========================================================
   CONTAINER PRINCIPAL
   ========================================================== */

.block-container {{
    max-width: 1050px;
    padding-top: 32px;
    padding-bottom: 60px;
}}


/* ==========================================================
   TÍTULOS
   ========================================================== */

h1 {{
    color: {BRANCO} !important;
    font-size: 46px !important;
    font-weight: 850 !important;
    letter-spacing: -1.5px;
}}

h2,
h3 {{
    color: {BRANCO} !important;
    font-weight: 800 !important;
}}

p {{
    color: {CINZA};
}}


/* ==========================================================
   CAPTIONS
   ========================================================== */

[data-testid="stCaptionContainer"] {{
    color: {CINZA} !important;
}}


/* ==========================================================
   LABELS
   ========================================================== */

[data-testid="stWidgetLabel"] p {{
    color: {AZUL_200} !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}}


/* ==========================================================
   CONTAINERS
   ========================================================== */

[data-testid="stVerticalBlockBorderWrapper"] {{
    background:
        linear-gradient(
            145deg,
            rgba(13, 45, 102, 0.54),
            rgba(4, 15, 35, 0.92)
        );

    border: 1px solid rgba(125, 196, 255, 0.18);

    border-radius: 20px;

    box-shadow:
        0 18px 45px rgba(0, 0, 0, 0.22),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
}}


/* ==========================================================
   SELECTBOX
   ========================================================== */

div[data-baseweb="select"] > div {{
    background:
        linear-gradient(
            135deg,
            rgba(8, 31, 67, 0.96),
            rgba(5, 19, 42, 0.96)
        ) !important;

    border: 1px solid rgba(125, 196, 255, 0.22) !important;

    border-radius: 11px !important;

    min-height: 44px;
}}

div[data-baseweb="select"] > div:hover {{
    border-color: {AZUL_400} !important;

    box-shadow:
        0 0 18px rgba(75, 163, 255, 0.14);
}}


/* ==========================================================
   NUMBER INPUT
   ========================================================== */

div[data-baseweb="input"] {{
    background:
        linear-gradient(
            135deg,
            rgba(8, 31, 67, 0.96),
            rgba(5, 19, 42, 0.96)
        ) !important;

    border: 1px solid rgba(125, 196, 255, 0.22) !important;

    border-radius: 11px !important;
}}

div[data-baseweb="input"]:focus-within {{
    border-color: {AZUL_400} !important;

    box-shadow:
        0 0 18px rgba(75, 163, 255, 0.14);
}}

input {{
    color: {BRANCO} !important;
}}


/* ==========================================================
   BOTÕES
   ========================================================== */

.stButton > button {{
    width: 100%;
    min-height: 48px;

    border-radius: 11px;

    border: 1px solid rgba(185, 224, 255, 0.25);

    background:
        linear-gradient(
            90deg,
            {AZUL_600},
            {AZUL_500},
            {AZUL_400}
        );

    color: {BRANCO};

    font-weight: 800;
    font-size: 14px;

    box-shadow:
        0 10px 25px rgba(20, 86, 232, 0.25);

    transition: 0.15s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);

    border-color: {AZUL_200};

    box-shadow:
        0 14px 32px rgba(75, 163, 255, 0.30);
}}


/* ==========================================================
   MÉTRICAS
   ========================================================== */

[data-testid="stMetric"] {{
    background:
        linear-gradient(
            145deg,
            rgba(13, 45, 102, 0.48),
            rgba(4, 15, 35, 0.95)
        );

    border: 1px solid rgba(125, 196, 255, 0.15);

    border-radius: 15px;

    padding: 16px;

    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
}}

[data-testid="stMetricLabel"] {{
    color: {CINZA} !important;
}}

[data-testid="stMetricValue"] {{
    color: {BRANCO} !important;
}}


/* ==========================================================
   TABS
   ========================================================== */

button[data-baseweb="tab"] {{
    color: {CINZA} !important;
    font-weight: 700;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: {AZUL_300} !important;
}}


/* ==========================================================
   EXPANDER
   ========================================================== */

details {{
    background:
        rgba(7, 27, 59, 0.70);

    border: 1px solid rgba(125, 196, 255, 0.15);

    border-radius: 15px;
}}


/* ==========================================================
   ALERTAS
   ========================================================== */

div[data-testid="stAlert"] {{
    border-radius: 12px;
}}


/* ==========================================================
   DIVISORES
   ========================================================== */

hr {{
    border-color: rgba(125, 196, 255, 0.13);
}}


/* ==========================================================
   FOOTER
   ========================================================== */

footer {{
    visibility: hidden;
}}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# CATEGORIAS
# ==========================================================

CATEGORIAS = {

    "USD": "América do Norte",
    "CAD": "América do Norte",
    "MXN": "América do Norte",
    "CRC": "América do Norte",
    "PAB": "América do Norte",

    "BBD": "Caribe",
    "JMD": "Caribe",
    "XCD": "Caribe",

    "ARS": "América do Sul",
    "CLP": "América do Sul",
    "COP": "América do Sul",
    "PYG": "América do Sul",
    "UYU": "América do Sul",
    "PEN": "América do Sul",
    "BOB": "América do Sul",
    "VEF": "América do Sul",

    "EUR": "Europa",
    "GBP": "Europa",
    "CHF": "Europa",
    "DKK": "Europa",
    "NOK": "Europa",
    "SEK": "Europa",
    "ISK": "Europa",
    "PLN": "Europa",
    "CZK": "Europa",
    "HUF": "Europa",
    "RON": "Europa",
    "RUB": "Europa",
    "RSD": "Europa",
    "TRY": "Europa",

    "JPY": "Ásia",
    "CNY": "Ásia",
    "HKD": "Ásia",
    "SGD": "Ásia",
    "TWD": "Ásia",
    "KRW": "Ásia",
    "INR": "Ásia",
    "IDR": "Ásia",
    "LKR": "Ásia",
    "NPR": "Ásia",
    "PKR": "Ásia",
    "THB": "Ásia",
    "MYR": "Ásia",
    "PHP": "Ásia",

    "ILS": "Oriente Médio",
    "AED": "Oriente Médio",
    "BHD": "Oriente Médio",
    "JOD": "Oriente Médio",
    "KWD": "Oriente Médio",
    "OMR": "Oriente Médio",
    "QAR": "Oriente Médio",
    "SAR": "Oriente Médio",
    "LBP": "Oriente Médio",

    "AUD": "Oceania",
    "NZD": "Oceania",

    "EGP": "África",
    "KES": "África",
    "MAD": "África",
    "NAD": "África",
    "ZAR": "África",
    "XAF": "África",
    "XOF": "África",
}


# ==========================================================
# INICIALIZAÇÃO DO HISTÓRICO
# ==========================================================

if "historico" not in st.session_state:
    st.session_state.historico = []


# ==========================================================
# CABEÇALHO
# ==========================================================

st.title("💱 Cotação de Moedas")

st.caption(
    "Um painel interativo para consultar, comparar e entender "
    "cotações de moedas do mundo inteiro."
)


# ==========================================================
# INDICADORES PRINCIPAIS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌎 Moedas",
        len(MENU_MOEDAS),
    )

with col2:
    st.metric(
        "🇧🇷 Base",
        "BRL",
    )

with col3:
    st.metric(
        "⚡ API",
        "ONLINE",
    )

with col4:
    st.metric(
        "🕘 Consultas",
        len(st.session_state.historico),
    )


st.markdown("---")


# ==========================================================
# MOEDAS POPULARES
# ==========================================================

st.subheader("⭐ Moedas populares")

populares = [
    "BRL-USD",
    "BRL-EUR",
    "BRL-GBP",
    "BRL-JPY",
    "BRL-ARS",
    "BRL-CNY",
]


moedas_populares = [
    moeda
    for moeda in populares
    if moeda in MENU_MOEDAS
]


colunas = st.columns(
    len(moedas_populares)
)


for coluna, moeda_popular in zip(
    colunas,
    moedas_populares
):

    codigo = moeda_popular.split("-")[1]

    with coluna:

        st.metric(
            codigo,
            MENU_MOEDAS[moeda_popular]
        )


st.markdown("---")


# ==========================================================
# ÁREA PRINCIPAL
# ==========================================================

st.subheader("🎯 Escolha sua conversão")


with st.container(border=True):

    # ------------------------------------------------------
    # REGIÃO
    # ------------------------------------------------------

    regioes = [
        "Todas",
        "América do Sul",
        "América do Norte",
        "Europa",
        "Ásia",
        "Oriente Médio",
        "África",
        "Oceania",
        "Caribe",
    ]


    regiao = st.selectbox(
        "🌐 Filtrar moedas por região",
        regioes,
    )


    # ------------------------------------------------------
    # FILTRO
    # ------------------------------------------------------

    moedas_filtradas = []


    for codigo, nome in MENU_MOEDAS.items():

        codigo_destino = codigo.split("-")[1]

        categoria = CATEGORIAS.get(
            codigo_destino,
            "Outras",
        )

        if (
            regiao == "Todas"
            or categoria == regiao
        ):
            moedas_filtradas.append(codigo)


    # ------------------------------------------------------
    # MOEDA
    # ------------------------------------------------------

    moeda = st.selectbox(
        "💵 Moeda de destino",
        moedas_filtradas,

        format_func=lambda codigo: (
            f"{codigo.split('-')[1]}"
            f"  •  "
            f"{MENU_MOEDAS[codigo]}"
        ),
    )


    # ------------------------------------------------------
    # VALOR
    # ------------------------------------------------------

    col1, col2 = st.columns(
        [1.4, 1],
        gap="medium",
    )


    with col1:

        valor = st.number_input(
            "💰 Valor em reais (R$)",
            min_value=0.01,
            value=100.00,
            step=10.00,
            format="%.2f",
        )


    with col2:

        st.write("")

        st.info(
            "🇧🇷 BRL → "
            f"{moeda.split('-')[1]}"
        )


    st.write("")


    consultar = st.button(
        "⚡ CONSULTAR E CONVERTER",
        use_container_width=True,
    )


# ==========================================================
# CONSULTA
# ==========================================================

if consultar:

    try:

        with st.spinner(
            "🔄 Consultando a AwesomeAPI..."
        ):

            cotacao = obter_cotacao(moeda)


        codigo_destino = moeda.split("-")[1]


        # --------------------------------------------------
        # CÁLCULO
        # --------------------------------------------------

        valor_convertido = (
            valor / cotacao["compra"]
        )


        # --------------------------------------------------
        # HISTÓRICO
        # --------------------------------------------------

        registro = {
            "moeda": codigo_destino,
            "nome": cotacao["nome"],
            "valor_brl": valor,
            "resultado": valor_convertido,
        }


        st.session_state.historico.insert(
            0,
            registro,
        )


        # Mantém somente as últimas 5
        st.session_state.historico = (
            st.session_state.historico[:5]
        )


        # --------------------------------------------------
        # RESULTADO
        # --------------------------------------------------

        st.markdown("---")

        st.subheader("💎 Resultado da conversão")


        with st.container(border=True):

            col1, col2 = st.columns(
                [1.6, 1],
                gap="large",
            )


            with col1:

                st.caption(
                    "VALOR CONVERTIDO"
                )

                st.markdown(
                    f"# {codigo_destino} "
                    f"{valor_convertido:,.2f}"
                )

                st.caption(
                    f"R$ {valor:,.2f} → "
                    f"{cotacao['nome']}"
                )


            with col2:

                st.metric(
                    "Cotação",
                    f"R$ {cotacao['compra']:.4f}",
                )

                st.metric(
                    "Variação",
                    f"{cotacao['variacao']:.2f}%",
                )


        # --------------------------------------------------
        # PAINEL
        # --------------------------------------------------

        st.write("")

        st.subheader("📊 Painel da cotação")


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Compra",
                f"R$ {cotacao['compra']:.4f}",
            )


        with col2:

            st.metric(
                "Venda",
                f"R$ {cotacao['venda']:.4f}",
            )


        with col3:

            st.metric(
                "Máxima",
                f"R$ {cotacao['maxima']:.4f}",
            )


        with col4:

            st.metric(
                "Mínima",
                f"R$ {cotacao['minima']:.4f}",
            )


        # --------------------------------------------------
        # TABS
        # --------------------------------------------------

        st.write("")


        tab1, tab2, tab3 = st.tabs(
            [
                "📈 Mercado",
                "🧮 Cálculo",
                "📘 Aprenda",
            ]
        )


        # ==================================================
        # MERCADO
        # ==================================================

        with tab1:

            col1, col2 = st.columns(2)


            with col1:

                st.markdown(
                    "#### 📊 Faixa de negociação"
                )

                amplitude = (
                    cotacao["maxima"]
                    - cotacao["minima"]
                )

                st.metric(
                    "Amplitude",
                    f"R$ {amplitude:.4f}",
                )


            with col2:

                st.markdown(
                    "#### 📍 Posição atual"
                )

                maxima = cotacao["maxima"]
                minima = cotacao["minima"]
                compra = cotacao["compra"]


                if maxima > minima:

                    posicao = (
                        (compra - minima)
                        / (maxima - minima)
                    )

                    posicao = max(
                        0,
                        min(
                            posicao,
                            1
                        )
                    )

                else:

                    posicao = 0


                st.progress(
                    posicao,
                    text=f"{posicao * 100:.1f}% da faixa diária",
                )


            st.write("")


            st.info(
                f"📉 Mínima: R$ {minima:.4f}   •   "
                f"📌 Atual: R$ {compra:.4f}   •   "
                f"📈 Máxima: R$ {maxima:.4f}"
            )


        # ==================================================
        # CÁLCULO
        # ==================================================

        with tab2:

            st.markdown(
                "#### 🧮 Como chegamos ao resultado?"
            )


            st.write(
                "Valor informado:"
            )

            st.code(
                f"R$ {valor:.2f}"
            )


            st.write(
                "Cotação utilizada:"
            )

            st.code(
                f"R$ {cotacao['compra']:.4f}"
            )


            st.write(
                "Fórmula:"
            )

            st.code(
                "Valor convertido = "
                "Valor em BRL ÷ Cotação"
            )


            st.write(
                "Resultado:"
            )

            st.code(
                f"{valor:.2f} ÷ "
                f"{cotacao['compra']:.4f}"
                f" = "
                f"{valor_convertido:.2f} "
                f"{codigo_destino}"
            )


        # ==================================================
        # APRENDA
        # ==================================================

        with tab3:

            st.markdown(
                """
                #### 📘 O que acontece por trás da interface?

                **1. Seleção**

                O usuário escolhe uma moeda disponível.

                **2. Requisição**

                O Python envia uma requisição para a
                AwesomeAPI.

                **3. JSON**

                A API retorna os dados da cotação.

                **4. Tratamento**

                O programa extrai o valor de compra,
                venda, máxima, mínima e variação.

                **5. Conversão**

                O valor em reais é dividido pela cotação.

                **6. Apresentação**

                O resultado é apresentado no dashboard.
                """
            )


            st.info(
                "💡 Este projeto demonstra a integração "
                "entre uma aplicação Python, uma API externa "
                "e uma interface construída com Streamlit."
            )


        # --------------------------------------------------
        # STATUS
        # --------------------------------------------------

        st.success(
            f"✅ Cotação de {cotacao['nome']} "
            f"consultada com sucesso."
        )


    except Exception as erro:

        st.error(
            f"❌ Não foi possível consultar a moeda.\n\n"
            f"{erro}"
        )


# ==========================================================
# HISTÓRICO
# ==========================================================

if st.session_state.historico:

    st.markdown("---")

    st.subheader("🕘 Últimas consultas")


    for item in st.session_state.historico:

        col1, col2, col3 = st.columns(
            [1, 2, 1]
        )


        with col1:

            st.markdown(
                f"**{item['moeda']}**"
            )


        with col2:

            st.caption(
                item["nome"]
            )


        with col3:

            st.markdown(
                f"**{item['resultado']:,.2f}**"
            )


# ==========================================================
# SOBRE O PROJETO
# ==========================================================

st.markdown("---")

st.subheader("🌍 Sobre este projeto")


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        **🇧🇷 Moeda base**

        O sistema utiliza o Real Brasileiro
        como moeda de origem.
        """
    )


with col2:

    st.markdown(
        """
        **🌎 Diversidade**

        As moedas são organizadas
        por regiões do mundo.
        """
    )


with col3:

    st.markdown(
        """
        **⚡ Dados**

        As cotações são obtidas
        através da AwesomeAPI.
        """
    )


# ==========================================================
# ARQUITETURA
# ==========================================================

with st.expander(
    "🔧 Ver arquitetura da aplicação"
):

    st.write(
        """
        **Interface**
        Streamlit

        ↓

        **Lógica**
        Python

        ↓

        **Requisição HTTP**
        Requests

        ↓

        **Fonte de dados**
        AwesomeAPI

        ↓

        **Resposta**
        JSON

        ↓

        **Tratamento**
        Python

        ↓

        **Resultado**
        Dashboard
        """
    )


# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")

st.caption(
    "💱 Cotação de Moedas  •  "
    "Projeto educacional  •  "
    "Python + Streamlit + AwesomeAPI"
)