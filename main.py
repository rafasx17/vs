from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
import yfinance as yf

# --- 1. CONFIGURAÇÃO DO BANCO (PERSISTÊNCIA) ---
DATABASE_URL = "sqlite:///./investimentos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. MODELO DE BANCO DE DATOS (ORMs) ---
class OrdemDB(Base):
    __tablename__ = "ordens"
    id = Column(Integer, primary_key=True, index=True)
    ativo = Column(String)
    quantidade = Column(Integer)
    preco = Column(Float)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(bind=engine)

# --- 3. MODELOS DE ENTRADA (SCHEMAS) ---
class Ordem(BaseModel):
    ativo: str
    quantidade: int
    preco: float

app = FastAPI(title="Sitema de Investimentos Ultra Completo")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 4. ROTAS (O CORAÇÃO DO SISTEMA) ---

@app.get("/")
def home():
    return {"msg": "Carteira Profissional do Rafael Online"}

# [C]REATE: Adicionar nova compra
@app.post("/comprar", tags=["Operações"])
def registrar_compra(nova_ordem: Ordem, db: Session = Depends(get_db)):
    db_ordem = OrdemDB(
        ativo=nova_ordem.ativo.upper(),
        quantidade=nova_ordem.quantidade,
        preco=nova_ordem.preco
    )
    db.add(db_ordem)
    db.commit()
    db.refresh(db_ordem)
    return {"status": "Sucesso", "id": db_ordem.id, "horario": db_ordem.data_criacao}

# [R]EAD: Listar toda a carteira (Preço Médio)
@app.get("/carteira", tags=["Consultas"])
def listar_carteira(db: Session = Depends(get_db)):
    ordens = db.query(OrdemDB).all()
    resumo = {}
    for o in ordens:
        ticker = o.ativo.upper()
        if ticker not in resumo:
            resumo[ticker] = {"pago": 0.0, "qtd": 0}
        resumo[ticker]["pago"] += (o.quantidade * o.preco)
        resumo[ticker]["qtd"] += o.quantidade
    
    lista = []
    for t, d in resumo.items():
        lista.append({"ativo": t, "qtd": d["qtd"], "pm": f"R$ {d['pago']/d['qtd']:.2f}"})
    return lista

# [R]EAD: Filtrar por Ticker
@app.get("/carteira/{ticker}", tags=["Consultas"])
def filtrar_por_ativo(ticker: str, db: Session = Depends(get_db)):
    historico = db.query(OrdemDB).filter(OrdemDB.ativo == ticker.upper()).all()
    return {"ativo": ticker.upper(), "historico": historico}

# [U]PDATE: Editar uma ordem errada
@app.put("/carteira/{id_ordem}", tags=["Operações"])
def atualizar_ordem(id_ordem: int, atualizada: Ordem, db: Session = Depends(get_db)):
    db_ordem = db.query(OrdemDB).filter(OrdemDB.id == id_ordem).first()
    if not db_ordem:
        raise HTTPException(status_code=404, detail="ID não encontrado")
    db_ordem.ativo = atualizada.ativo.upper()
    db_ordem.quantidade = atualizada.quantidade
    db_ordem.preco = atualizada.preco
    db.commit()
    return {"msg": "Atualizado com sucesso"}

# [D]ELETE: Apagar uma ordem
@app.delete("/carteira/{id_ordem}", tags=["Operações"])
def apagar_ordem(id_ordem: int, db: Session = Depends(get_db)):
    db_ordem = db.query(OrdemDB).filter(OrdemDB.id == id_ordem).first()
    if not db_ordem:
        raise HTTPException(status_code=404, detail="ID não encontrado")
    db.delete(db_ordem)
    db.commit()
    return {"msg": "Removido do banco"}

# --- 5. LÓGICA DE MERCADO (INTELIGÊNCIA) ---

# LUCRO REAL INDIVIDUAL
@app.get("/carteira/{ticker}/lucro-real", tags=["Mercado Financeiro"])
def lucro_real_ativo(ticker: str, db: Session = Depends(get_db)):
    ordens = db.query(OrdemDB).filter(OrdemDB.ativo == ticker.upper()).all()
    if not ordens:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    
    acao = yf.Ticker(f"{ticker.upper()}.SA")
    preco_agora = acao.fast_info['last_price']
    
    total_qtd = sum(o.quantidade for o in ordens)
    total_pago = sum(o.quantidade * o.preco for o in ordens)
    lucro = (total_qtd * preco_agora) - total_pago
    
    return {
        "ativo": ticker.upper(),
        "preco_bolsa": f"R$ {preco_agora:.2f}",
        "seu_lucro": f"R$ {lucro:.2f}",
        "status": "🚀" if lucro >= 0 else "📉"
    }

# RELATÓRIO GERAL DA CARTEIRA
@app.get("/carteira/relatorio/geral", tags=["Mercado Financeiro"])
def relatorio_geral(db: Session = Depends(get_db)):
    ordens = db.query(OrdemDB).all()
    if not ordens:
        return {"msg": "Carteira vazia"}
    
    agrupado = {}
    for o in ordens:
        t = o.ativo.upper()
        if t not in agrupado: agrupado[t] = {"q": 0, "p": 0.0}
        agrupado[t]["q"] += o.quantidade
        agrupado[t]["p"] += (o.quantidade * o.preco)
    
    total_inv = 0.0
    total_atua = 0.0
    
    for t, info in agrupado.items():
        try:
            p_agora = yf.Ticker(f"{t}.SA").fast_info['last_price']
        except: p_agora = 0.0
        total_inv += info["p"]
        total_atua += (info["q"] * p_agora)
        
    return {
        "investimento_total": f"R$ {total_inv:.2f}",
        "valor_atual": f"R$ {total_atua:.2f}",
        "lucro_total": f"R$ {total_atua - total_inv:.2f}"
    }