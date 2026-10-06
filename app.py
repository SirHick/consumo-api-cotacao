"""
Cotação de Moedas — painel em Streamlit.

Visual maximalista inspirado em cédulas e casas de câmbio:
guilloché, selos, bordas duplas, papel-moeda em tons de azul por região
e um ticker de cotações ao vivo no topo.

A lógica de consulta (currency_api.py) continua a mesma.
"""

import html as _html
from datetime import datetime

import streamlit as st

from currency_api import MENU_MOEDAS, consultar_moeda, obter_cotacao

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Cotação de Moedas",
    page_icon="💱",
    layout="wide",
)

# ==========================================================
# DADOS DE APOIO
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

# Cada região tem o seu tom de azul de papel-moeda (todos aceitam texto em tinta escura).
REGIAO_COR = {
    "América do Sul": "#3F8CFF",
    "América do Norte": "#5CA8FF",
    "Caribe": "#7FBFFF",
    "Europa": "#9CCBFF",
    "Ásia": "#6F94FF",
    "Oriente Médio": "#A5B8FF",
    "África": "#55C2F5",
    "Oceania": "#C4E4FF",
    "Outras": "#EAF4FF",
}

BANDEIRAS = {
    "BRL": "🇧🇷", "USD": "🇺🇸", "CAD": "🇨🇦", "MXN": "🇲🇽", "CRC": "🇨🇷",
    "PAB": "🇵🇦", "BBD": "🇧🇧", "JMD": "🇯🇲", "XCD": "🏝️", "ARS": "🇦🇷",
    "CLP": "🇨🇱", "COP": "🇨🇴", "PYG": "🇵🇾", "UYU": "🇺🇾", "PEN": "🇵🇪",
    "BOB": "🇧🇴", "VEF": "🇻🇪", "EUR": "🇪🇺", "GBP": "🇬🇧", "CHF": "🇨🇭",
    "DKK": "🇩🇰", "NOK": "🇳🇴", "SEK": "🇸🇪", "ISK": "🇮🇸", "PLN": "🇵🇱",
    "CZK": "🇨🇿", "HUF": "🇭🇺", "RON": "🇷🇴", "RUB": "🇷🇺", "RSD": "🇷🇸",
    "TRY": "🇹🇷", "JPY": "🇯🇵", "CNY": "🇨🇳", "HKD": "🇭🇰", "SGD": "🇸🇬",
    "TWD": "🇹🇼", "KRW": "🇰🇷", "INR": "🇮🇳", "IDR": "🇮🇩", "LKR": "🇱🇰",
    "NPR": "🇳🇵", "PKR": "🇵🇰", "THB": "🇹🇭", "MYR": "🇲🇾", "PHP": "🇵🇭",
    "ILS": "🇮🇱", "AED": "🇦🇪", "BHD": "🇧🇭", "JOD": "🇯🇴", "KWD": "🇰🇼",
    "OMR": "🇴🇲", "QAR": "🇶🇦", "SAR": "🇸🇦", "LBP": "🇱🇧", "AUD": "🇦🇺",
    "NZD": "🇳🇿", "EGP": "🇪🇬", "KES": "🇰🇪", "MAD": "🇲🇦", "NAD": "🇳🇦",
    "ZAR": "🇿🇦", "XAF": "🌍", "XOF": "🌍",
}

POPULARES = [
    "BRL-USD",
    "BRL-EUR",
    "BRL-GBP",
    "BRL-JPY",
    "BRL-ARS",
    "BRL-CNY",
]

# Pares buscados de uma vez para o ticker e para as moedas em destaque.
VITRINE_PARES = POPULARES + [
    "BRL-CHF",
    "BRL-CAD",
    "BRL-AUD",
    "BRL-CLP",
    "BRL-MXN",
    "BRL-COP",
]

# "R$" escrito como entidade HTML, para o Markdown não confundir com LaTeX.
RS = "R&#36;"

# ==========================================================
# UTILITÁRIOS
# ==========================================================


def h(texto: str) -> str:
    """Remove indentação e linhas vazias de um bloco HTML.

    O Markdown do Streamlit trata linhas indentadas como código e
    encerra blocos HTML em linhas vazias; compactar evita os dois problemas.
    """
    return "\n".join(
        linha.strip() for linha in texto.strip().splitlines() if linha.strip()
    )


def mostrar(texto: str) -> None:
    st.markdown(h(texto), unsafe_allow_html=True)


def esc(valor) -> str:
    return _html.escape(str(valor))


def br(numero: float, casas: int = 2) -> str:
    """Formata no padrão brasileiro: 1.234,56."""
    texto = f"{numero:,.{casas}f}"
    return texto.replace(",", "§").replace(".", ",").replace("§", ".")


def formatar_data(texto) -> str:
    try:
        return datetime.strptime(texto, "%Y-%m-%d %H:%M:%S").strftime(
            "%d/%m/%Y às %H:%M"
        )
    except Exception:
        return str(texto or "")


def cor_da_moeda(codigo: str) -> str:
    regiao = CATEGORIAS.get(codigo, "Outras")
    return REGIAO_COR.get(regiao, REGIAO_COR["Outras"])


def secao(titulo: str) -> None:
    mostrar(
        f"""
        <div class="secao">
        <span class="secao-orn">❖</span>
        <div class="secao-titulo" role="heading" aria-level="2">{esc(titulo)}</div>
        <span class="secao-linha"></span>
        <span class="secao-orn">❖</span>
        </div>
        """
    )


# ==========================================================
# DADOS AO VIVO (ticker e moedas em destaque)
# ==========================================================


@st.cache_data(ttl=120, show_spinner=False)
def _buscar_vitrine(pares: tuple) -> dict:
    dados = consultar_moeda(",".join(pares))
    resultado = {}
    for par in pares:
        item = dados.get(par.replace("-", ""))
        if item:
            resultado[par] = {
                "compra": float(item.get("bid", 0)),
                "variacao": float(item.get("pctChange", 0)),
            }
    return resultado


def carregar_vitrine(pares: list) -> dict:
    """Busca várias cotações numa chamada só. Se falhar, devolve vazio
    e a página continua funcionando sem os valores ao vivo."""
    try:
        return _buscar_vitrine(tuple(pares))
    except Exception:
        return {}


# ==========================================================
# CSS
# ==========================================================

ESTILO = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..900;1,9..144,400..900&family=Bricolage+Grotesque:opsz,wght@12..96,400..800&display=swap');

:root {
  --tinta: #030F2B;
  --tinta-2: #08205E;
  --tinta-3: #0F3A9E;
  --papel: #EAF4FF;
  --gelo: #B9E0FF;
  --claro: #8FD0FF;
  --ceu: #5CB2FF;
  --pervinca: #7FA6FF;
  --royal: #1456E8;
  --display: 'Fraunces', Georgia, serif;
  --corpo: 'Bricolage Grotesque', system-ui, sans-serif;
}

/* ---------- Base ---------- */

.stApp {
  color: var(--papel);
  overflow-x: hidden;
  background:
    radial-gradient(circle at 8% 0%, rgba(20, 86, 232, .42), transparent 32%),
    radial-gradient(circle at 100% 12%, rgba(92, 178, 255, .22), transparent 28%),
    radial-gradient(circle at 70% 100%, rgba(47, 123, 255, .24), transparent 34%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'%3E%3Cg fill='none' stroke='%235CB2FF' stroke-opacity='.11' stroke-width='1'%3E%3Ccircle cx='60' cy='60' r='58'/%3E%3Ccircle cx='60' cy='60' r='46'/%3E%3Ccircle cx='60' cy='60' r='34'/%3E%3Ccircle cx='60' cy='60' r='22'/%3E%3Ccircle cx='0' cy='0' r='58'/%3E%3Ccircle cx='120' cy='0' r='58'/%3E%3Ccircle cx='0' cy='120' r='58'/%3E%3Ccircle cx='120' cy='120' r='58'/%3E%3C/g%3E%3C/svg%3E"),
    linear-gradient(160deg, #030F2B, #061A4A 55%, #020A1F);
  background-size: auto, auto, auto, 120px 120px, auto;
  background-attachment: fixed;
}

[data-testid="stMain"], section.main { overflow-x: hidden; }

header[data-testid="stHeader"] { background: transparent; }

.stApp, .stApp p, .stApp label, .stApp li, .stApp input, .stApp button {
  font-family: var(--corpo);
}

.block-container {
  max-width: 1180px;
  padding-top: 3.2rem;
  padding-bottom: 60px;
}

footer { visibility: hidden; }

*:focus-visible {
  outline: 3px solid var(--gelo) !important;
  outline-offset: 2px;
}

/* ---------- Ticker ---------- */

.ticker {
  width: 100vw;
  margin: 0 0 30px calc(50% - 50vw);
  overflow: hidden;
  background: var(--ceu);
  border-block: 3px solid var(--tinta);
  box-shadow: 0 5px 0 var(--royal), 0 9px 0 var(--gelo);
}
.ticker-trilho {
  display: flex;
  width: max-content;
  animation: correr 70s linear infinite;
}
.ticker:hover .ticker-trilho { animation-play-state: paused; }
.tk {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 24px;
  color: var(--tinta);
  font-weight: 700;
  white-space: nowrap;
  border-right: 2px dashed rgba(3, 15, 43, .45);
  font-variant-numeric: tabular-nums;
}
.tk b { font-family: var(--display); font-weight: 900; font-size: 1.05rem; color: var(--tinta); }
.tk .alta { color: #062C8F; font-style: normal; }
.tk .queda { color: #0A1F5C; font-style: normal; }
@keyframes correr { to { transform: translateX(-50%); } }

/* ---------- Hero ---------- */

.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 36px;
  flex-wrap: wrap;
  margin: 8px 0 34px;
}
.hero-txt { flex: 1 1 520px; max-width: 780px; }
.hero-titulo {
  font-family: var(--corpo);
  font-weight: 800;
  font-size: clamp(2.4rem, 6vw, 4.9rem);
  line-height: 1.08;
  letter-spacing: -.01em;
  color: var(--papel);
  text-shadow:
    3px 3px 0 var(--royal),
    6px 6px 0 var(--tinta-3);
}
.hero-sub {
  font-size: 1.15rem;
  line-height: 1.5;
  max-width: 46ch;
  margin-top: 34px;
  color: var(--papel);
}
.selo {
  width: clamp(150px, 18vw, 210px);
  flex: 0 0 auto;
  transform: rotate(-9deg);
  filter: drop-shadow(8px 8px 0 rgba(0, 0, 0, .35));
}

/* ---------- Números do topo ---------- */

.numeros {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 20px;
  margin: 0 0 12px;
}
.numero {
  padding: 14px 18px 12px;
  color: var(--tinta);
  border: 3px solid var(--tinta);
  border-radius: 6px;
  box-shadow: 6px 6px 0 var(--papel);
}
.numero b {
  display: block;
  font-family: var(--display);
  font-weight: 900;
  font-size: 2.4rem;
  line-height: 1.05;
  color: var(--tinta);
}
.numero span { font-weight: 600; font-size: .95rem; color: var(--tinta); }
.numero:nth-child(1) { background: #5CB2FF; }
.numero:nth-child(2) { background: #8FC7FF; }
.numero:nth-child(3) { background: #B9E0FF; }
.numero:nth-child(4) { background: #7FA6FF; }

/* ---------- Títulos de seção ---------- */

.secao {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 48px 0 24px;
}
.secao-titulo {
  font-family: var(--display);
  font-weight: 800;
  font-size: clamp(1.6rem, 3.4vw, 2.4rem);
  color: var(--papel);
  line-height: 1.1;
}
.secao-orn { color: var(--ceu); font-size: 1.5rem; }
.secao-linha {
  flex: 1;
  height: 9px;
  min-width: 24px;
  border-block: 2px solid var(--ceu);
}

/* ---------- Moedas em destaque ---------- */

.carteira {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 22px;
  padding: 6px 6px 10px;
}
.cedula-mini {
  position: relative;
  overflow: hidden;
  padding: 14px 16px 14px;
  background: var(--cor);
  color: var(--tinta);
  border: 3px solid var(--tinta);
  border-radius: 8px;
  box-shadow: 0 0 0 3px var(--papel), 6px 6px 0 3px rgba(0, 0, 0, .35);
}
.cedula-mini::before {
  content: "";
  position: absolute;
  inset: 0;
  background: repeating-radial-gradient(circle at 100% 100%, transparent 0 6px, rgba(3, 15, 43, .14) 6px 7px);
  pointer-events: none;
}
.cedula-mini > * { position: relative; }
.cedula-mini:nth-child(odd) { transform: rotate(-1.2deg); }
.cedula-mini:nth-child(even) { transform: rotate(1deg); }
.cm-bandeira { font-size: 2.1rem; line-height: 1.1; }
.cm-codigo {
  font-family: var(--display);
  font-weight: 900;
  font-size: 1.9rem;
  line-height: 1.05;
  color: var(--tinta);
}
.cm-nome { font-size: .85rem; font-weight: 600; min-height: 2.3em; color: var(--tinta); }
.cm-taxa {
  margin-top: 8px;
  font-family: var(--display);
  font-weight: 800;
  font-size: 1.3rem;
  color: var(--tinta);
  font-variant-numeric: tabular-nums;
}
.cm-var {
  display: inline-block;
  margin-top: 6px;
  padding: 2px 10px;
  border-radius: 99px;
  background: var(--tinta);
  font-weight: 700;
  font-size: .8rem;
  font-variant-numeric: tabular-nums;
}
.cm-var.alta { color: var(--claro); }
.cm-var.queda { color: #7FA0E8; }

/* ---------- Guichê (container do formulário) ---------- */

.st-key-guiche {
  padding: 16px 18px 12px;
  background: linear-gradient(145deg, var(--tinta-2), #051646);
  border: 3px solid var(--ceu) !important;
  border-radius: 10px;
  outline: 2px dashed var(--royal);
  outline-offset: 7px;
  box-shadow: 12px 12px 0 var(--tinta-3);
}

[data-testid="stWidgetLabel"] p {
  color: var(--papel) !important;
  font-weight: 700 !important;
  font-size: .95rem !important;
}

div[data-baseweb="select"] > div {
  min-height: 50px;
  background: var(--tinta) !important;
  border: 2px solid var(--papel) !important;
  border-radius: 6px !important;
}
div[data-baseweb="select"] > div:hover { border-color: var(--ceu) !important; }
div[data-baseweb="select"] span,
div[data-baseweb="select"] div { color: var(--papel) !important; }
div[data-baseweb="select"] svg { fill: var(--ceu) !important; }

div[data-baseweb="popover"] > div {
  background: var(--tinta-2) !important;
  border: 2px solid var(--ceu) !important;
}
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] [role="listbox"] { background: var(--tinta-2) !important; }
div[data-baseweb="popover"] li { color: var(--papel) !important; }
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li[aria-selected="true"] { background: var(--tinta-3) !important; }

[data-testid="stNumberInput"] div[data-baseweb="input"] {
  background: var(--tinta) !important;
  border: 2px solid var(--papel) !important;
  border-radius: 6px !important;
}
[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within { border-color: var(--ceu) !important; }
[data-testid="stNumberInput"] div[data-baseweb="base-input"] { background: transparent !important; }
[data-testid="stNumberInput"] input {
  color: var(--papel) !important;
  font-family: var(--display);
  font-weight: 800;
  font-size: 1.2rem;
}
[data-testid="stNumberInput"] button { background: var(--tinta-3) !important; color: var(--papel) !important; }

.rota {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  min-height: 50px;
  margin-top: 28px;
  padding: 6px 14px;
  border: 2px dashed var(--gelo);
  border-radius: 6px;
  background: rgba(92, 178, 255, .10);
  font-family: var(--display);
  font-weight: 900;
  font-size: 1.45rem;
  color: var(--papel);
}
.rota i { font-style: normal; color: var(--ceu); }

.stButton > button,
div[data-testid="stButton"] button {
  width: 100%;
  min-height: 58px;
  background: var(--ceu);
  color: var(--tinta);
  border: 3px solid var(--tinta);
  border-radius: 99px;
  box-shadow: 5px 5px 0 var(--royal);
  transition: transform .12s ease, box-shadow .12s ease;
}
.stButton > button p,
div[data-testid="stButton"] button p {
  color: var(--tinta) !important;
  font-family: var(--display);
  font-weight: 900;
  font-size: 1.3rem;
}
.stButton > button:hover,
div[data-testid="stButton"] button:hover {
  transform: translate(-2px, -2px);
  box-shadow: 8px 8px 0 var(--royal);
  background: #8CC8FF;
  border-color: var(--tinta);
}
.stButton > button:active,
div[data-testid="stButton"] button:active {
  transform: translate(3px, 3px);
  box-shadow: 1px 1px 0 var(--royal);
}

div[data-testid="stAlert"] {
  border-radius: 6px;
  border: 2px solid var(--papel);
}

.stSpinner p { color: var(--papel) !important; }

/* ---------- A nota (resultado) ---------- */

.nota {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto;
  grid-template-areas: "topo serie" "valor selo";
  gap: 22px 28px;
  margin: 6px 8px 28px;
  padding: 36px 40px;
  overflow: hidden;
  background: var(--nota-cor, #5CB2FF);
  color: var(--tinta);
  border: 3px solid var(--tinta);
  border-radius: 10px;
  box-shadow: 0 0 0 4px var(--papel), 0 0 0 7px var(--tinta), 14px 14px 0 7px rgba(0, 0, 0, .4);
  animation: imprimir 1s cubic-bezier(.2, .8, .2, 1) both;
}
.nota::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    repeating-radial-gradient(circle at 15% 120%, transparent 0 7px, rgba(3, 15, 43, .13) 7px 8px),
    repeating-radial-gradient(circle at 90% -20%, transparent 0 9px, rgba(3, 15, 43, .11) 9px 10px);
  pointer-events: none;
}
.nota::after {
  content: "";
  position: absolute;
  inset: 10px;
  border: 2px dashed rgba(3, 15, 43, .55);
  border-radius: 6px;
  pointer-events: none;
}
.nota > * { position: relative; z-index: 1; }
.nota .orn { position: absolute; z-index: 1; font-size: 1.1rem; color: var(--tinta); }
.nota .o1 { top: 14px; left: 18px; }
.nota .o2 { top: 14px; right: 18px; }
.nota .o3 { bottom: 14px; left: 18px; }
.nota .o4 { bottom: 14px; right: 18px; }

.nota-marca {
  position: absolute;
  right: -12px;
  bottom: -60px;
  z-index: 0;
  font-family: var(--display);
  font-weight: 900;
  font-size: 13rem;
  line-height: 1;
  color: rgba(3, 15, 43, .1);
  pointer-events: none;
}
.nota-topo { grid-area: topo; display: flex; align-items: center; gap: 16px; }
.nota-bandeira { font-size: 3.4rem; line-height: 1; }
.nota-tit { font-family: var(--display); font-weight: 900; font-size: 1.5rem; color: var(--tinta); }
.nota-sub { font-weight: 600; color: var(--tinta); }
.nota-serie {
  grid-area: serie;
  align-self: start;
  padding: 6px 12px;
  text-align: right;
  font-weight: 700;
  font-size: .9rem;
  line-height: 1.5;
  color: var(--tinta);
  border: 2px solid var(--tinta);
  border-radius: 4px;
}
.nota-valor-wrap { grid-area: valor; min-width: 0; }
.nota-rotulo { font-weight: 700; color: var(--tinta); }
.nota-valor {
  font-family: var(--display);
  font-weight: 900;
  font-size: clamp(2.8rem, 8vw, 6.4rem);
  line-height: 1.05;
  letter-spacing: -.03em;
  color: var(--tinta);
  font-variant-numeric: tabular-nums;
  overflow-wrap: anywhere;
  text-shadow: 3px 3px 0 rgba(234, 244, 255, .65);
}
.nota-valor small {
  margin-right: .35em;
  font-size: .38em;
  font-weight: 800;
  letter-spacing: 0;
  vertical-align: super;
  color: var(--tinta);
}
.nota-extenso { max-width: 52ch; margin-top: 10px; font-weight: 600; color: var(--tinta); }
.nota .nota-selo {
  grid-area: selo;
  align-self: end;
  justify-self: end;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 124px;
  height: 124px;
  background: var(--tinta);
  border: 4px double var(--ceu);
  border-radius: 50%;
  transform: rotate(8deg);
  box-shadow: 5px 5px 0 rgba(0, 0, 0, .35);
}
.nota .nota-selo, .nota .nota-selo * { color: var(--papel); }
.nota .nota-selo b { font-family: var(--display); font-weight: 900; font-size: 1.35rem; line-height: 1.1; }
.nota .nota-selo small { font-size: .8rem; }
.nota .nota-selo .alta { color: var(--claro); }
.nota .nota-selo .queda { color: #7FA0E8; }

@keyframes imprimir {
  from { clip-path: inset(-30px 100% -30px -30px); }
  to { clip-path: inset(-30px -30px -30px -30px); }
}

/* ---------- Painéis de preço ---------- */

.paineis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 8px 0 6px;
}
.painel {
  padding: 14px 18px;
  background: var(--tinta-2);
  border: 2px solid var(--cor);
  border-left-width: 12px;
  border-radius: 4px;
}
.painel-rotulo { font-weight: 700; color: var(--cor); }
.painel-valor {
  font-family: var(--display);
  font-weight: 800;
  font-size: 1.8rem;
  color: var(--papel);
  font-variant-numeric: tabular-nums;
}

/* ---------- Abas ---------- */

[data-baseweb="tab-list"] { gap: 8px; border-bottom: 3px solid var(--ceu); }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none; }
button[data-baseweb="tab"] {
  height: auto;
  padding: 10px 22px;
  background: var(--tinta-2);
  border: 2px solid var(--ceu);
  border-bottom: none;
  border-radius: 8px 8px 0 0;
}
button[data-baseweb="tab"] p {
  color: var(--papel) !important;
  font-family: var(--display);
  font-weight: 800;
  font-size: 1.05rem;
}
button[data-baseweb="tab"][aria-selected="true"] { background: var(--ceu); }
button[data-baseweb="tab"][aria-selected="true"] p { color: var(--tinta) !important; }

/* ---------- Faixa de negociação ---------- */

.faixa { padding: 54px 48px 8px; }
.faixa-barra {
  position: relative;
  height: 22px;
  border: 3px solid var(--papel);
  border-radius: 99px;
  background: linear-gradient(90deg, var(--royal), var(--ceu) 55%, var(--gelo));
}
.faixa-marca {
  position: absolute;
  top: -14px;
  width: 8px;
  height: 44px;
  transform: translateX(-50%);
  background: var(--papel);
  border: 2px solid var(--tinta);
  border-radius: 3px;
}
.faixa-marca em {
  position: absolute;
  bottom: 100%;
  left: 50%;
  margin-bottom: 8px;
  padding: 4px 12px;
  transform: translateX(-50%);
  white-space: nowrap;
  font-style: normal;
  font-weight: 800;
  color: var(--tinta);
  background: var(--ceu);
  border: 2px solid var(--tinta);
  border-radius: 4px;
}
.faixa-extremos {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 22px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
.faixa-extremos .min { color: #7FA6FF; }
.faixa-extremos .max { color: var(--claro); }

/* ---------- Recibo (aba Cálculo) ---------- */

.recibo {
  max-width: 580px;
  margin: 10px 0;
  padding: 22px 26px;
  background: var(--papel);
  color: var(--tinta);
  border: 3px solid var(--tinta);
  border-radius: 2px;
  box-shadow: 8px 8px 0 var(--royal);
  font-weight: 600;
}
.rec-linha { display: flex; align-items: baseline; gap: 8px; padding: 7px 0; color: var(--tinta); }
.rec-pontos { flex: 1; border-bottom: 2px dotted rgba(3, 15, 43, .5); transform: translateY(-4px); }
.rec-valor { font-family: var(--display); font-weight: 800; color: var(--tinta); font-variant-numeric: tabular-nums; }
.rec-formula { margin: 8px 0 4px; padding: 8px 12px; background: rgba(3, 15, 43, .08); border-radius: 3px; font-weight: 700; color: var(--tinta); }
.rec-total {
  margin-top: 8px;
  padding-top: 10px;
  border-top: 4px double var(--tinta);
  font-size: 1.2rem;
}

/* ---------- Passos (aba Aprenda) ---------- */

.passos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 18px;
  margin-top: 10px;
}
.passo {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px;
  background: rgba(15, 58, 158, .38);
  border: 2px solid rgba(234, 244, 255, .35);
  border-radius: 6px;
}
.passo-n {
  display: grid;
  place-items: center;
  flex: 0 0 46px;
  height: 46px;
  background: var(--ceu);
  color: var(--tinta);
  border: 3px solid var(--tinta);
  border-radius: 50%;
  box-shadow: 3px 3px 0 var(--royal);
  font-family: var(--display);
  font-weight: 900;
  font-size: 1.4rem;
}
.passo b { display: block; font-family: var(--display); font-size: 1.15rem; color: var(--papel); }
.passo span { font-size: .95rem; line-height: 1.45; color: var(--papel); }

/* ---------- Histórico ---------- */

.canhotos { display: grid; gap: 16px; padding: 4px 6px 8px; }
.canhoto {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 20px;
  padding: 14px 22px;
  background: var(--papel);
  color: var(--tinta);
  border: 2px solid var(--tinta);
  border-radius: 6px;
  box-shadow: 5px 5px 0 var(--gelo);
}
.canhoto-moeda { font-family: var(--display); font-weight: 900; font-size: 1.3rem; color: var(--tinta); }
.canhoto-nome { font-weight: 600; color: var(--tinta); }
.canhoto-valor {
  padding-left: 20px;
  border-left: 3px dashed rgba(3, 15, 43, .5);
  font-family: var(--display);
  font-weight: 800;
  color: var(--tinta);
  font-variant-numeric: tabular-nums;
  text-align: right;
}

/* ---------- Rodapé ---------- */

.rodape { margin: 64px 0 8px; text-align: center; color: var(--papel); }
.rodape .orns { margin-bottom: 8px; color: var(--ceu); font-size: 1.3rem; letter-spacing: .6em; }

/* ---------- Telas pequenas ---------- */

@media (max-width: 700px) {
  .nota {
    grid-template-columns: 1fr;
    grid-template-areas: "topo" "serie" "valor" "selo";
    padding: 38px 24px;
  }
  .nota-serie { text-align: left; }
  .nota .nota-selo { justify-self: start; }
  .faixa { padding-inline: 20px; }
  .canhoto { grid-template-columns: 1fr; gap: 6px; }
  .canhoto-valor { padding-left: 0; border-left: none; text-align: left; }
  .rota { margin-top: 0; }
}

/* ---------- Movimento reduzido ---------- */

@media (prefers-reduced-motion: reduce) {
  .ticker { overflow-x: auto; }
  .ticker-trilho, .nota { animation: none; }
  .stButton > button, div[data-testid="stButton"] button { transition: none; }
}
</style>
"""

mostrar(ESTILO)

# ==========================================================
# ESTADO
# ==========================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

vitrine = carregar_vitrine(VITRINE_PARES)

# ==========================================================
# TICKER
# ==========================================================

itens_ticker = []
for par in VITRINE_PARES:
    codigo_t = par.split("-")[1]
    bandeira_t = BANDEIRAS.get(codigo_t, "🌐")
    dado = vitrine.get(par)
    if dado:
        classe = "alta" if dado["variacao"] >= 0 else "queda"
        seta = "▲" if dado["variacao"] >= 0 else "▼"
        itens_ticker.append(
            f'<span class="tk"><b>{bandeira_t} {codigo_t}</b>'
            f'{br(dado["compra"], 4)}'
            f'<i class="{classe}">{seta} {br(abs(dado["variacao"]))}%</i></span>'
        )
    elif par in MENU_MOEDAS:
        itens_ticker.append(
            f'<span class="tk"><b>{bandeira_t} {codigo_t}</b>'
            f"{esc(MENU_MOEDAS[par])}</span>"
        )

trilho = "".join(itens_ticker) * 2  # duplicado para o loop ficar contínuo
mostrar(
    f'<div class="ticker" aria-hidden="true"><div class="ticker-trilho">{trilho}</div></div>'
)

# ==========================================================
# HERO
# ==========================================================

mostrar(
    f"""
    <div class="hero">
    <div class="hero-txt">
    <div class="hero-titulo" role="heading" aria-level="1">Seu real, em qualquer moeda do mundo.</div>
    <p class="hero-sub">Escolha o destino, digite quanto quer converter e veja na hora
    quanto vale. As cotações vêm ao vivo da AwesomeAPI.</p>
    </div>
    <svg class="selo" viewBox="0 0 200 200" aria-hidden="true">
    <defs><path id="anel" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
    <circle cx="100" cy="100" r="96" fill="#5CB2FF"/>
    <circle cx="100" cy="100" r="90" fill="none" stroke="#030F2B" stroke-width="2" stroke-dasharray="2 5"/>
    <circle cx="100" cy="100" r="58" fill="#1456E8"/>
    <circle cx="100" cy="100" r="52" fill="none" stroke="#EAF4FF" stroke-width="2"/>
    <text font-family="Fraunces, Georgia, serif" font-size="15" font-weight="800" fill="#030F2B">
    <textPath href="#anel" textLength="480">cotação ao vivo • {len(MENU_MOEDAS)} moedas • AwesomeAPI •</textPath>
    </text>
    <text x="100" y="118" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-weight="900" font-size="44" fill="#EAF4FF">{RS}</text>
    </svg>
    </div>
    """
)

# ==========================================================
# NÚMEROS
# ==========================================================

status_api = "Online" if vitrine else "Instável"

mostrar(
    f"""
    <div class="numeros">
    <div class="numero"><b>{len(MENU_MOEDAS)}</b><span>moedas disponíveis</span></div>
    <div class="numero"><b>BRL</b><span>moeda de origem</span></div>
    <div class="numero"><b>{status_api}</b><span>conexão com a AwesomeAPI</span></div>
    <div class="numero"><b>{len(st.session_state.historico)}</b><span>consultas nesta sessão</span></div>
    </div>
    """
)

# ==========================================================
# MOEDAS EM DESTAQUE
# ==========================================================

secao("Moedas em destaque")

cartas = []
for par in POPULARES:
    if par not in MENU_MOEDAS:
        continue
    codigo_p = par.split("-")[1]
    dado = vitrine.get(par)
    taxa = ""
    if dado:
        classe = "alta" if dado["variacao"] >= 0 else "queda"
        seta = "▲" if dado["variacao"] >= 0 else "▼"
        taxa = (
            f'<div class="cm-taxa">{br(dado["compra"], 4)}</div>'
            f'<div class="cm-var {classe}">{seta} {br(abs(dado["variacao"]))}%</div>'
        )
    cartas.append(
        f'<div class="cedula-mini" style="--cor:{cor_da_moeda(codigo_p)}">'
        f'<div class="cm-bandeira">{BANDEIRAS.get(codigo_p, "🌐")}</div>'
        f'<div class="cm-codigo">{codigo_p}</div>'
        f'<div class="cm-nome">{esc(MENU_MOEDAS[par])}</div>'
        f"{taxa}</div>"
    )

mostrar(f'<div class="carteira">{"".join(cartas)}</div>')

# ==========================================================
# CONVERSÃO
# ==========================================================

secao("Converta seu dinheiro")

try:
    guiche = st.container(border=True, key="guiche")
except TypeError:  # versões antigas do Streamlit não aceitam "key"
    guiche = st.container(border=True)

with guiche:
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

    regiao = st.selectbox("Região do mundo", regioes)

    moedas_filtradas = [
        codigo
        for codigo in MENU_MOEDAS
        if regiao == "Todas"
        or CATEGORIAS.get(codigo.split("-")[1], "Outras") == regiao
    ]

    moeda = st.selectbox(
        "Moeda de destino",
        moedas_filtradas,
        format_func=lambda codigo: (
            f"{BANDEIRAS.get(codigo.split('-')[1], '🌐')} "
            f"{codigo.split('-')[1]} • {MENU_MOEDAS[codigo]}"
        ),
    )

    col_valor, col_rota = st.columns([1.4, 1], gap="medium")

    with col_valor:
        valor = st.number_input(
            "Quanto você quer converter (R\\$)",
            min_value=0.01,
            value=100.00,
            step=10.00,
            format="%.2f",
        )

    with col_rota:
        destino = moeda.split("-")[1]
        mostrar(
            f'<div class="rota"><span>{BANDEIRAS["BRL"]} BRL</span><i>➜</i>'
            f'<span>{BANDEIRAS.get(destino, "🌐")} {destino}</span></div>'
        )

    consultar = st.button("Converter agora")

# ==========================================================
# RESULTADO
# ==========================================================

if consultar:
    try:
        with st.spinner("Buscando a cotação…"):
            cotacao = obter_cotacao(moeda)

        codigo_destino = moeda.split("-")[1]
        nome_moeda = MENU_MOEDAS[moeda]

        # --------------------------------------------------
        # CÁLCULO
        # --------------------------------------------------
        valor_convertido = valor / cotacao["compra"]

        # --------------------------------------------------
        # HISTÓRICO (mantém as 5 últimas)
        # --------------------------------------------------
        st.session_state.historico.insert(
            0,
            {
                "moeda": codigo_destino,
                "nome": nome_moeda,
                "valor_brl": valor,
                "resultado": valor_convertido,
            },
        )
        st.session_state.historico = st.session_state.historico[:5]

        # --------------------------------------------------
        # NOTA
        # --------------------------------------------------
        secao("Sua conversão")

        alta = cotacao["variacao"] >= 0
        classe_var = "alta" if alta else "queda"
        seta_var = "▲" if alta else "▼"
        data_txt = esc(formatar_data(cotacao["data"]))

        mostrar(
            f"""
            <div class="nota" style="--nota-cor:{cor_da_moeda(codigo_destino)}">
            <i class="orn o1">❖</i><i class="orn o2">❖</i><i class="orn o3">❖</i><i class="orn o4">❖</i>
            <div class="nota-marca" aria-hidden="true">{esc(codigo_destino)}</div>
            <div class="nota-topo">
            <span class="nota-bandeira">{BANDEIRAS.get(codigo_destino, "🌐")}</span>
            <div>
            <div class="nota-tit">Nota de conversão</div>
            <div class="nota-sub">Real brasileiro para {esc(nome_moeda)}</div>
            </div>
            </div>
            <div class="nota-serie">BRL/{esc(codigo_destino)}<br>{data_txt}</div>
            <div class="nota-valor-wrap">
            <div class="nota-rotulo">Você recebe</div>
            <div class="nota-valor"><small>{esc(codigo_destino)}</small>{br(valor_convertido)}</div>
            <div class="nota-extenso">{RS} {br(valor)} em reais equivalem a
            {br(valor_convertido)} em {esc(nome_moeda)}.</div>
            </div>
            <div class="nota-selo">
            <span class="{classe_var}">{seta_var}</span>
            <b>{br(abs(cotacao["variacao"]))}%</b>
            <small>variação hoje</small>
            </div>
            </div>
            """
        )

        # --------------------------------------------------
        # PAINEL
        # --------------------------------------------------
        secao("Cotação do dia")

        paineis_preco = [
            ("Compra", cotacao["compra"], "#5CB2FF"),
            ("Venda", cotacao["venda"], "#B9E0FF"),
            ("Máxima", cotacao["maxima"], "#8FD0FF"),
            ("Mínima", cotacao["minima"], "#4F8DFF"),
        ]
        mostrar(
            '<div class="paineis">'
            + "".join(
                f'<div class="painel" style="--cor:{cor}">'
                f'<div class="painel-rotulo">{rotulo}</div>'
                f'<div class="painel-valor">{RS} {br(v, 4)}</div></div>'
                for rotulo, v, cor in paineis_preco
            )
            + "</div>"
        )

        st.write("")

        aba_mercado, aba_calculo, aba_aprenda = st.tabs(
            ["Mercado", "Cálculo", "Aprenda"]
        )

        # ==================================================
        # MERCADO
        # ==================================================
        with aba_mercado:
            maxima = cotacao["maxima"]
            minima = cotacao["minima"]
            compra = cotacao["compra"]
            amplitude = maxima - minima

            if maxima > minima:
                posicao = max(0, min((compra - minima) / (maxima - minima), 1))
            else:
                posicao = 0

            mostrar(
                f"""
                <div class="faixa">
                <div class="faixa-barra">
                <span class="faixa-marca" style="left:{posicao * 100:.1f}%">
                <em>Agora {RS} {br(compra, 4)}</em></span>
                </div>
                <div class="faixa-extremos">
                <span class="min">Mínima {RS} {br(minima, 4)}</span>
                <span>{br(posicao * 100, 1)}% da faixa diária</span>
                <span class="max">Máxima {RS} {br(maxima, 4)}</span>
                </div>
                </div>
                """
            )
            mostrar(
                f'<div class="paineis"><div class="painel" style="--cor:#9DB4FF">'
                f'<div class="painel-rotulo">Amplitude do dia</div>'
                f'<div class="painel-valor">{RS} {br(amplitude, 4)}</div></div></div>'
            )

        # ==================================================
        # CÁLCULO
        # ==================================================
        with aba_calculo:
            mostrar(
                f"""
                <div class="recibo">
                <div class="rec-linha"><span>Valor informado</span><span class="rec-pontos"></span>
                <span class="rec-valor">{RS} {br(valor)}</span></div>
                <div class="rec-linha"><span>Cotação utilizada</span><span class="rec-pontos"></span>
                <span class="rec-valor">{RS} {br(cotacao["compra"], 4)}</span></div>
                <div class="rec-formula">Valor convertido = Valor em BRL ÷ Cotação</div>
                <div class="rec-linha"><span>{RS} {br(valor)} ÷ {br(cotacao["compra"], 4)}</span>
                <span class="rec-pontos"></span><span class="rec-valor">{br(valor_convertido)}</span></div>
                <div class="rec-linha rec-total"><span>Você recebe</span><span class="rec-pontos"></span>
                <span class="rec-valor">{esc(codigo_destino)} {br(valor_convertido)}</span></div>
                </div>
                """
            )

        # ==================================================
        # APRENDA
        # ==================================================
        with aba_aprenda:
            passos = [
                ("Seleção", "O usuário escolhe uma moeda disponível."),
                ("Requisição", "O Python envia uma requisição para a AwesomeAPI."),
                ("JSON", "A API retorna os dados da cotação."),
                (
                    "Tratamento",
                    "O programa extrai o valor de compra, venda, máxima, mínima e variação.",
                ),
                ("Conversão", "O valor em reais é dividido pela cotação."),
                ("Apresentação", "O resultado é exibido neste painel."),
            ]
            mostrar(
                '<div class="passos">'
                + "".join(
                    f'<div class="passo"><div class="passo-n">{i}</div>'
                    f"<div><b>{titulo}</b><span>{texto}</span></div></div>"
                    for i, (titulo, texto) in enumerate(passos, start=1)
                )
                + "</div>"
            )
            st.write("")
            st.info(
                "💡 Este projeto demonstra a integração entre uma aplicação "
                "Python, uma API externa e uma interface construída com Streamlit."
            )

    except Exception as erro:
        st.error(
            f"Não foi possível consultar {moeda.split('-')[1]}.\n\n"
            f"{erro}\n\n"
            "Confira sua conexão e tente de novo."
        )

# ==========================================================
# HISTÓRICO
# ==========================================================

if st.session_state.historico:
    secao("Últimas consultas")

    canhotos = "".join(
        f'<div class="canhoto">'
        f'<span class="canhoto-moeda">{BANDEIRAS.get(item["moeda"], "🌐")} {esc(item["moeda"])}</span>'
        f'<span class="canhoto-nome">{esc(item["nome"])}</span>'
        f'<span class="canhoto-valor">{RS} {br(item["valor_brl"])} ➜ '
        f'{esc(item["moeda"])} {br(item["resultado"])}</span>'
        f"</div>"
        for item in st.session_state.historico
    )
    mostrar(f'<div class="canhotos">{canhotos}</div>')

# ==========================================================
# RODAPÉ
# ==========================================================

mostrar(
    """
    <div class="rodape">
    <div class="orns" aria-hidden="true">❖ ✦ ❖ ✦ ❖</div>
    <div>Cotações fornecidas pela AwesomeAPI, apenas para referência.</div>
    </div>
    """
)