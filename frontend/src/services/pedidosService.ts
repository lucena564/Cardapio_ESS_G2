import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

export async function listarProdutosPorCategoria(categoria: string) {
  const res = await api.get(`/categorias/${categoria}`)
  return res.data
}

export async function fazerPedido(mesa: string, itens: any[]) {
  const payload = {
    mesa,
    itens: itens.map(item => ({
      produto_id: item.id,
      quantidade: item.quantidade
    }))
  }
  return await api.post('/pedidos', payload)
}

export async function editarPedido(mesa: string, itens: any[]) {
  return await api.put(`/pedidos/${mesa}`, {
    itens: itens.map(item => ({
      produto_id: item.id,
      quantidade: item.quantidade
    }))
  })
}

export async function fecharPedido(mesa: string) {
  return await api.post(`/pedidos/fechar/${mesa}`)
}
