from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid

app = FastAPI(title="Cardápio Virtual - Histórico de Pedidos", version="1.0.0")

# Enums
class StatusPedido(str, Enum):
    EMANDAMENTO = "em andamento"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"

# Models
class ItemPedido(BaseModel):
    id: str
    nome: str
    quantidade: int
    preco_unitario: float
    observacoes: Optional[str] = None

class Order(BaseModel):
    idOrder: str
    numero_pedido: int  # 4 dígitos
    data: str  # formato YYYY-MM-DD
    hora: str  # formato HH:MM
    valor: float
    itens: List[ItemPedido]
    mesa: Optional[int] = None
    status: StatusPedido

class OrderCreate(BaseModel):
    itens: List[ItemPedido]
    mesa: Optional[int] = None

class OrderUpdate(BaseModel):
    status: StatusPedido

# Dados simulados
def gerar_dados_simulados():
    orders = []
    
    # Itens do cardápio para simulação
    itens_cardapio = [
        {"nome": "Pizza Margherita", "preco": 35.90},
        {"nome": "Hambúrguer Artesanal", "preco": 28.50},
        {"nome": "Lasanha Bolonhesa", "preco": 32.00},
        {"nome": "Salada Caesar", "preco": 22.90},
        {"nome": "Risotto de Camarão", "preco": 45.00},
        {"nome": "Coca-Cola 350ml", "preco": 6.50},
        {"nome": "Suco Natural Laranja", "preco": 8.90},
        {"nome": "Cerveja Heineken", "preco": 12.00},
        {"nome": "Brigadeiro (3 unid)", "preco": 15.90},
        {"nome": "Petit Gateau", "preco": 18.50}
    ]
    
    status_opcoes = [StatusPedido.EMANDAMENTO, StatusPedido.CONCLUIDO, StatusPedido.CANCELADO]
    
    # Gerar 12 pedidos dos últimos 5 dias para o usuário
    base_date = datetime.now()
    
    for i in range(12):
        data_pedido = base_date - timedelta(days=i//3, hours=(i*2)%24, minutes=(i*15)%60)
        
        # Selecionar itens aleatórios
        import random
        num_itens = random.randint(1, 4)
        itens_selecionados = random.sample(itens_cardapio, num_itens)
        
        itens_pedido = []
        valor_total = 0
        
        for item in itens_selecionados:
            quantidade = random.randint(1, 2)
            item_pedido = ItemPedido(
                id=str(uuid.uuid4()),
                nome=item["nome"],
                quantidade=quantidade,
                preco_unitario=item["preco"],
                observacoes="Sem cebola" if random.random() > 0.8 else None
            )
            itens_pedido.append(item_pedido)
            valor_total += item["preco"] * quantidade
    
        status = random.choice([StatusPedido.EMANDAMENTO, StatusPedido.CONCLUIDO])        
        # Número do pedido de 4 dígitos
        numero_pedido = 1000 + i
        
        order = Order(
            idOrder=str(uuid.uuid4()),
            numero_pedido=numero_pedido,
            data=data_pedido.strftime("%Y-%m-%d"),
            hora=data_pedido.strftime("%H:%M"),
            valor=round(valor_total, 2),
            itens=itens_pedido,
            mesa=random.randint(1, 15) if random.random() > 0.3 else None,
            status=status
        )
        orders.append(order)
    
    return sorted(orders, key=lambda x: f"{x.data} {x.hora}", reverse=True)

# Base de dados simulada
orders_db = gerar_dados_simulados()

# Endpoints
@app.get("/")
def root():
    return {"message": "API do Histórico de Pedidos - Cardápio Virtual"}

@app.get("/orders/history", response_model=List[Order])
def listar_historico_pedidos(
    status: Optional[StatusPedido] = Query(None, description="Filtrar por status"),
    mesa: Optional[int] = Query(None, description="Filtrar por mesa"),
    dias: Optional[int] = Query(None, ge=1, le=30, description="Pedidos dos últimos X dias"),
    limit: int = Query(10, ge=1, le=50, description="Limite de resultados")
):
    """Listar histórico de pedidos com filtros opcionais"""
    orders_filtrados = orders_db.copy()
    
    if status:
        orders_filtrados = [o for o in orders_filtrados if o.status == status]
    
    if mesa:
        orders_filtrados = [o for o in orders_filtrados if o.mesa == mesa]
    
    if dias:
        data_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
        orders_filtrados = [o for o in orders_filtrados if o.data >= data_limite]
    
    return orders_filtrados[:limit]

@app.get("/orders/{idOrder}", response_model=Order)
def obter_pedido(idOrder: str):
    """Obter detalhes de um pedido específico"""
    for order in orders_db:
        if order.idOrder == idOrder:
            return order
    raise HTTPException(status_code=404, detail="Pedido não encontrado")

@app.post("/orders", response_model=Order)
def criar_pedido(order_data: OrderCreate):
    """Criar um novo pedido"""
    valor_total = sum(item.preco_unitario * item.quantidade for item in order_data.itens)
    
    # Gerar número de pedido sequencial (simulado)
    ultimo_numero = max([o.numero_pedido for o in orders_db], default=999)
    novo_numero = ultimo_numero + 1
    
    agora = datetime.now()
    novo_order = Order(
        idOrder=str(uuid.uuid4()),
        numero_pedido=novo_numero,
        data=agora.strftime("%Y-%m-%d"),
        hora=agora.strftime("%H:%M"),
        valor=round(valor_total, 2),
        itens=order_data.itens,
        mesa=order_data.mesa,
        status=StatusPedido.EMANDAMENTO
    )
    
    orders_db.insert(0, novo_order)  # Adicionar no início da lista
    return novo_order

@app.put("/orders/{idOrder}", response_model=Order)
def atualizar_pedido(idOrder: str, order_update: OrderUpdate):
    """Atualizar status de um pedido"""
    for i, order in enumerate(orders_db):
        if order.idOrder == idOrder:
            orders_db[i].status = order_update.status
            return orders_db[i]
    raise HTTPException(status_code=404, detail="Pedido não encontrado")

@app.get("/estatisticas")
def obter_estatisticas():
    """Obter estatísticas do histórico de pedidos"""
    total_orders = len(orders_db)
    total_vendas = sum(order.valor for order in orders_db)
    
    # Contar por status
    status_count = {}
    for status in StatusPedido:
        status_count[status.value] = len([o for o in orders_db if o.status == status])
    
    # Item mais vendido
    item_vendas = {}
    for order in orders_db:
        for item in order.itens:
            if item.nome in item_vendas:
                item_vendas[item.nome] += item.quantidade
            else:
                item_vendas[item.nome] = item.quantidade
    
    item_mais_vendido = max(item_vendas.items(), key=lambda x: x[1]) if item_vendas else ("Nenhum", 0)
    
    return {
        "total_pedidos": total_orders,
        "total_vendas": round(total_vendas, 2),
        "ticket_medio": round(total_vendas / total_orders if total_orders > 0 else 0, 2),
        "pedidos_por_status": status_count,
        "item_mais_vendido": {
            "nome": item_mais_vendido[0],
            "quantidade": item_mais_vendido[1]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)