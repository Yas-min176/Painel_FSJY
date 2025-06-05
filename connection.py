
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import pandas as pd

def autenticar_google():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = None

    # Usa token se existir
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)

    # Faz login se necessário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # "credentials.json" deve ser o arquivo da conta de projeto Google OAuth 2.0
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
            creds = flow.run_local_server(port=0)

        # Salva token
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return gspread.authorize(creds)

def carregar_dados_planilhas(links_codigos):
    gc = autenticar_google()
    dados_finais = []

    for codigo, link in links_codigos.items():
        try:
            sheet_id = link.split("/d/")[1].split("/")[0]
            planilha = gc.open_by_key(sheet_id)
            aba = planilha.worksheet("Respostas ao formulário 1")
            dados = aba.get_all_records()
            df = pd.DataFrame(dados)
            # Renomeia a coluna de quem lançou
            df = df.rename(columns={
                "Quem está Lançando:": "Funcionário"
            })

            # Garante que os valores são numéricos para soma
            df["Valor - Abastecimento"] = pd.to_numeric(df.get("Valor - Abastecimento", 0), errors="coerce").fillna(0)
            df["Valor - Manutenção"] = pd.to_numeric(df.get("Valor - Manutenção", 0), errors="coerce").fillna(0)
            df["Valor - Hospedagem"] = pd.to_numeric(df.get("Valor - Hospedagem", 0), errors="coerce").fillna(0)

            # Cria uma nova coluna com a soma de todos os valores
            df["Valor"] = (
                df["Valor - Abastecimento"] +
                df["Valor - Manutenção"] +
                df["Valor - Hospedagem"]
            )
            if df.empty:
                print(f"Planilha {codigo} está vazia.")
            else:
                print(f"{codigo} carregado com sucesso: {df.shape}")
                df["Veículo"] = codigo
                dados_finais.append(df)
        except Exception as e:
            print(f"Erro ao carregar {codigo}: {e}")

    if not dados_finais:
        print("Nenhuma planilha foi carregada com sucesso.")
        return pd.DataFrame()

    return pd.concat(dados_finais, ignore_index=True)
