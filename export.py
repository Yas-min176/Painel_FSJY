from xhtml2pdf import pisa
import pandas as pd
import datetime

def gerar_html(df, filtros_aplicados, caminho_saida="relatorio.pdf"):
    data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #333;
                padding: 5px;
                font-size: 12px;
            }}
            th {{
                background-color: #eee;
            }}
            h1 {{
                font-size: 18px;
                text-align: center;
            }}
            .meta {{
                margin-top: 10px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <h1>Relatório de Gastos - Painel_FSJY</h1>
        <p class="meta">Gerado em: {data}</p>
        <p class="meta">Filtros: {filtros_aplicados}</p>
        <table>
            <tr>{"".join(f"<th>{col}</th>" for col in df.columns)}</tr>
            {"".join("".join(f"<td>{cell}</td>" for cell in row) for row in df.values.tolist())}
        </table>
    </body>
    </html>
    """

    with open("temp_relatorio.html", "w", encoding="utf-8") as f:
        f.write(html)

    with open("temp_relatorio.html", "r", encoding="utf-8") as source_file:
        with open(caminho_saida, "wb") as output_file:
            pisa.CreatePDF(source_file.read(), dest=output_file)
