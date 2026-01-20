# fixed-income-carry-trade-brazil

Quantitative analysis of BR-US fixed income carry trade using Nelson-Siegel-Svensson models, bond options valuation, and portfolio optimization. Includes live yield curve fitting, spread analysis, and risk metrics.

---

## Overview

Este proyecto implementa un framework cuantitativo para analizar el **carry trade** entre curvas de tipos de interés de Brasil y Estados Unidos usando modelos Nelson-Siegel-Svensson (NSS). El objetivo es medir el spread BR-US, la rentabilidad real ajustada por inflación y la contribución de opciones sobre bonos al perfil riesgo-retorno de la cartera.

Se incluyen módulos para:
- Ajustar curvas de rendimiento BR y US con NSS.
- Analizar el carry real (nominal – inflación) y el rolldown a lo largo de la curva.
- Valorar opciones sobre bonos y swaptions con el framework Black-76.
- Construir una estrategia con theta harvesting y duración casi neutral en bonos del Tesouro Direto.

---

## Features

- NSS curve fitting para curvas US y Brasil (nivel, pendiente, curvatura y segundo hump).
- Cálculo de spreads BR-US por maturidad, carry real y estadísticas (media, rango, volatilidad simple).
- Valuación de opciones sobre bonos (calls/puts) y estructuras tipo collar con Black-76.
- Métricas de portafolio: duración aproximada, carry esperado, Sharpe ratio simplificado.
- Resumen JSON reproducible con parámetros NSS, spreads y resultados de la estrategia (results/summary_20jan2026.json).
- Notebooks separados para fitting, análisis de carry, opciones y optimización de portafolio.

---

## Quickstart

### 1. Clonar repositorio

```bash
git clone https://github.com/lorenlorenloren/fixed-income-carry-trade-brazil.git
cd fixed-income-carry-trade-brazil
```

### 2. Crear entorno e instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ejecutar script principal

```bash
python nss_carry_trade.py
```

Esto generará:
- Gráficos de curvas ajustadas (si se activan).
- Estadísticas de spread y carry.
- Un archivo `results/summary_20jan2026.json` con el resumen ejecutivo.

### 4. Ejecutar en Google Colab

1. Sube el repositorio (o haz fork) a tu cuenta de GitHub.
2. Abre [https://colab.research.google.com](https://colab.research.google.com).
3. Pestaña **GitHub** → pega la URL del repo `fixed-income-carry-trade-brazil`.
4. Abre el notebook deseado, por ejemplo `notebooks/01_nss_fitting.ipynb`.
5. En la primera celda ejecuta:

```python
!git clone https://github.com/lorenlorenloren/fixed-income-carry-trade-brazil.git
%cd fixed-income-carry-trade-brazil
!pip install -r requirements.txt
```

6. Ejecuta las celdas del notebook para reproducir el análisis NSS, carry y opciones.

---

## Data

La carpeta `data/` contiene ejemplos de datos históricos (formato CSV):

- `yields_us_jan2026.csv`: maturities en años y yields de Treasuries de EE. UU. (spot o par).
- `yields_br_jan2026.csv`: maturities en años y yields de bonos del Tesouro Direto (LTN/NTN-F, etc.).

Formato típico:

```text
maturity,yield
0.25,4.50
0.50,4.60
1.00,4.20
...
```

Puedes actualizar estos ficheros con datos reales diarios desde Tesouro Direto, Bloomberg u otras fuentes equivalentes.

---

## Project structure

```text
.
├── README.md                # Descripción del proyecto y guía de uso
├── requirements.txt         # Dependencias Python
├── nss_carry_trade.py       # Script principal (NSS + carry + opciones + resumen)
├── data/
│   ├── yields_us_jan2026.csv
│   └── yields_br_jan2026.csv
├── notebooks/
│   ├── 01_nss_fitting.ipynb           # Fitting NSS BR/US
│   ├── 02_carry_analysis.ipynb        # Spreads, carry real, rolldown
│   ├── 03_bond_options.ipynb          # Black-76 sobre bonos y swaptions
│   └── 04_portfolio_optimization.ipynb# Construcción y optimización de cartera
├── src/
│   ├── nss_model.py          # Funciones de curva NSS reutilizables
│   ├── options.py            # Black-76 para opciones sobre bonos
│   ├── carry.py              # Lógica de carry trade BR-US
│   └── utils.py              # Helpers (lectura datos, plots, métricas)
├── tests/
│   └── test_nss_fitting.py   # Tests básicos de fitting NSS
├── results/
│   └── summary_20jan2026.json# Resumen del run del 20/01/2026
└── LICENSE                   # MIT License
```

---

## Model limitations

El modelo es útil para ilustrar conceptos de term structure y carry trade, pero tiene varias **limitaciones** importantes:

1. **Supuestos del modelo NSS**  
   NSS resume la curva con pocos parámetros y supone una estructura relativamente suave; en episodios de estrés (crisis fiscal, shocks de liquidez) puede fallar capturando quiebres y cambios de régimen.

2. **Estacionariedad de la prima a plazo**  
   Se asume prima de término estable en el tiempo; en mercados emergentes como Brasil la term premium puede cambiar abruptamente con noticias fiscales, políticas o de inflación.

3. **Volatilidad y colas en mercados EM**  
   El uso de volatilidad histórica moderada subestima colas gruesas típicas de mercados emergentes; shocks de tasas o FX pueden ser > 2–3 desviaciones estándar en ventanas cortas.

4. **Supuestos del framework Black-76**  
   Black-76 asume distribución lognormal de forwards, costos de transacción nulos y volatilidad bien comportada; en realidad existen spreads bid-ask relevantes y smiles/skirts de volatilidad marcados en curvas de tasas.

5. **Riesgo cambiario BRL/USD**  
   La estrategia asume cierto grado de cobertura vía forwards, pero la correlación BRL-activos de riesgo global puede subir fuertemente en drawdowns, generando pérdidas por basis y gaps de liquidez.

6. **Datos y parametrización hardcoded**  
   Los ejemplos usan datos estáticos de enero 2026 y parámetros calibrados en una fecha; extrapolar resultados a otros entornos de tasas sin recalibrar puede producir señales engañosas.

---

## References

- Nelson, C. R., & Siegel, A. F. (1987). *Parsimonious Modeling of Yield Curves*.
- Svensson, L. E. O. (1994). *Estimating and Interpreting Forward Interest Rates*.
- Tesouro Direto – Brazilian government bond data and technical documentation.
- Bloomberg – Market data for US Treasuries and Brazilian fixed income spreads.
- Black, F. (1976). *The Pricing of Commodity Contracts*. (Black-76 framework for options on forwards/futures).

> Inspired by *Option Volatility & Pricing* (Sheldon Natenberg).

---

## License

This project is licensed under the MIT License – see the `LICENSE` file for details.

---

## Social

Author – Quantitative Finance Student, Brazil 🇧🇷
