import streamlit as st

from currency_api import obter_cotacao, MENU_MOEDAS


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Cotação de Moedas",
    page_icon="💱",
    layout="centered",
)


# ==========================================================
# CSS
# ==========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0F1117;
    }

    .titulo {
        font-size: 38px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 5px;
    }

    .subtitulo {
        font-size: 16px;
        color: #7FA6D8;
        margin-bottom: 30px;
    }

    .resultado {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 15px;
        padding: 25px;
        margin-top: 25px;
        text-align: center;
    }

    .resultado-titulo {
        font-size: 15px;
        color: #475569;
    }

    .resultado-valor {
        font-size: 42px;
        font-weight: 700;
        color: #047857;
        margin-top: 5px;
    }

    .info {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }

    .rodape {
        text-align: center;
        color: #94A3B8;
        font-size: 13px;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# CABEÇALHO
# ==========================================================

st.markdown(
    '<div class="titulo">💱 Cotação de Moedas</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitulo">
        Consulte a cotação atual e simule a conversão de valores
        utilizando dados da AwesomeAPI.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# SELEÇÃO DE MOEDA
# ==========================================================

opcoes_moedas = list(MENU_MOEDAS.keys())

moeda = st.selectbox(
    "Selecione a moeda para consulta:",
    opcoes_moedas,
    format_func=lambda codigo: (
        f"{codigo} — {MENU_MOEDAS[codigo]}"
    ),
)


# ==========================================================
# VALOR PARA CONVERSÃO
# ==========================================================

valor = st.number_input(
    "Digite o valor em reais (R$):",
    min_value=0.01,
    value=100.00,
    step=10.00,
    format="%.2f",
)


# ==========================================================
# BOTÃO
# ==========================================================

consultar = st.button(
    "💱 Consultar e Converter",
    use_container_width=True,
)


# ==========================================================
# CONSULTA
# ==========================================================

if consultar:

    try:

        cotacao = obter_cotacao(moeda)

        valor_convertido = valor / cotacao["compra"]

        # --------------------------------------------------
        # RESULTADO
        # --------------------------------------------------

        st.markdown(
            f"""
            <div class="resultado">

                <div class="resultado-titulo">
                    {valor:,.2f} BRL equivalem aproximadamente a
                </div>

                <div class="resultado-valor">
                    {valor_convertido:,.2f} {moeda.split("-")[0]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        # --------------------------------------------------
        # INFORMAÇÕES DA COTAÇÃO
        # --------------------------------------------------

        st.markdown(
            '<div class="info">',
            unsafe_allow_html=True,
        )

        st.subheader("📊 Informações da cotação")

        col1, col2 = st.columns(2)

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

        col3, col4 = st.columns(2)

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

        st.write(
            f"**Variação:** {cotacao['variacao']:.2f}%"
        )

        st.write(
            f"**Última atualização:** {cotacao['data']}"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

    except Exception as erro:

        st.error(
            f"❌ Não foi possível consultar a moeda.\n\n{erro}"
        )


# ==========================================================
# EXPLICAÇÃO DIDÁTICA
# ==========================================================

st.markdown("---")

st.subheader("📘 Como funciona?")

st.write(
    """
    O sistema consulta uma API de cotações para obter o valor atual
    da moeda selecionada.

    Depois disso, o valor informado em reais é dividido pela cotação
    da moeda para gerar uma estimativa de conversão.

    **Fórmula utilizada:**

    Valor convertido = Valor em BRL ÷ Cotação
    """
)


# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown(
    """
    <div class="rodape">
        Projeto desenvolvido para fins educacionais.
        Dados de cotação obtidos por meio da AwesomeAPI.
    </div>
    """,
    unsafe_allow_html=True,
)