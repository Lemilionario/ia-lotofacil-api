
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TOKEN_VALIDO = "lotofacil_mestre_2025"

dezenas_frequentes = [1, 3, 4, 6, 10, 11, 12, 13, 14, 19, 23, 24, 25]
zona_quente = [10, 13, 14, 16, 19, 22, 23, 25]
clusters = [[2, 12, 22], [5, 10, 15], [4, 9, 14, 19]]
todas = list(range(1, 26))

def gerar_apostas_fidedignas():
    apostas = []
    for _ in range(3):
        aposta = set()
        aposta.update(random.sample(dezenas_frequentes, 7))
        cluster_escolhido = random.choice(clusters)
        aposta.update(random.sample(cluster_escolhido, min(4, len(cluster_escolhido))))
        aposta.update(random.sample(zona_quente, 2))
        while len(aposta) < 15:
            dez = random.choice(todas)
            aposta.add(dez)
        apostas.append(sorted(aposta))
    return apostas

@app.get("/")
def home():
    return {"mensagem": "API da IA Lotofacil ativa."}

@app.get("/gerar")
def gerar(token: str):
    if token != TOKEN_VALIDO:
        raise HTTPException(status_code=403, detail="Token inválido.")
    apostas = gerar_apostas_fidedignas()
    return {"apostas": apostas}

@app.get("/bonus")
def bonus(token: str):
    if token != TOKEN_VALIDO:
        raise HTTPException(status_code=403, detail="Token inválido.")
    aposta = sorted(random.sample(zona_quente, 8) + random.sample(dezenas_frequentes, 7))
    return {"aposta": aposta}

@app.get("/resumo")
def resumo(token: str):
    if token != TOKEN_VALIDO:
        raise HTTPException(status_code=403, detail="Token inválido.")
    return {
        "zonas_quentes": zona_quente,
        "clusters_ativos": clusters,
        "frequentes": dezenas_frequentes,
        "observação": "Versão simplificada com base estatística real"
    }

class ApostaInput(BaseModel):
    dezenas: List[int]

@app.post("/analisar")
def analisar(aposta: ApostaInput, token: str):
    if token != TOKEN_VALIDO:
        raise HTTPException(status_code=403, detail="Token inválido.")
    dezenas = aposta.dezenas
    analise = {
        "zona_quente": [d for d in dezenas if d in zona_quente],
        "frequentes": [d for d in dezenas if d in dezenas_frequentes],
        "clusters": [d for d in dezenas if any(d in c for c in clusters)],
        "pares": len([d for d in dezenas if d % 2 == 0]),
        "ímpares": len([d for d in dezenas if d % 2 != 0]),
    }
    return analise

@app.post("/validar")
def validar(aposta: ApostaInput, token: str):
    if token != TOKEN_VALIDO:
        raise HTTPException(status_code=403, detail="Token inválido.")
    dezenas = aposta.dezenas
    score = 0
    score += sum(1 for d in dezenas if d in dezenas_frequentes)
    score += sum(1 for d in dezenas if d in zona_quente)
    score += sum(1 for d in dezenas if any(d in c for c in clusters))
    return {"score_estimado": score, "mensagem": "Quanto maior o score, mais coerente é a aposta."}
