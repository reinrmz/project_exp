# Quarterly Tax Ledger

**Live app:** https://project-exp.onrender.com/

A simple web calculator for Philippine freelancers and self-employed
professionals on the **8% income tax rate option** (non-VAT). Enter your gross
income per quarter and it computes the taxable amount and tax payable, applying
the ₱250,000 annual deduction.

> This tool is for calculation and planning only. It does not file anything —
> file your taxes through **eBIRForms** accordingly.

## Tech stack

| Layer      | Choice                                  |
| ---------- | --------------------------------------- |
| Language   | Python 3.11                             |
| Framework  | [Streamlit](https://streamlit.io/)      |
| Data       | pandas, NumPy                           |
| Excel I/O  | openpyxl                                |
| UI         | `st.data_editor` grid + injected CSS (Space Grotesk / JetBrains Mono, dark theme) |
| Hosting    | [Render](https://render.com/)           |

## Project structure

```
main.py                   Entry point — sets page config, runs the calculator
constants.py              App config: version, period lookups, formatting
utility.py                Theme CSS injection and render helpers
tax_calculator/
  __init__.py
  tax.py                  Tax computation and the editable ledger UI
.streamlit/config.toml    Native dark theme
requirements.txt          Python dependencies
start.sh                  Render start command
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run main.py
```

App opens at `http://localhost:8501`.

## Deploy (Render)

Start command (see `start.sh`):

```bash
streamlit run main.py --server.port $PORT --server.address 0.0.0.0
```
