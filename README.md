# 📦 CRUD de Pedidos com MySQL

Sistema CRUD de vendas desenvolvido em **Python + MySQL**, simulando funcionalidades básicas de um ERP comercial: cadastro de clientes, produtos e registro de pedidos com relacionamento entre entidades.

---

# 🚀 Funcionalidades

- Cadastro de clientes  
- Cadastro de produtos  
- Registro de pedidos  
- Listagem de dados  
- Atualização de registros  
- Exclusão de registros  
- Relacionamento entre clientes, produtos e pedidos  

---

# 🛠️ Tecnologias utilizadas

- Python  
- MySQL  
- SQL  
- Git e GitHub  

---

# 🗄️ Modelagem do Banco de Dados

O sistema utiliza banco relacional MySQL com três entidades principais:

- **clientes**
- **produtos**
- **pedidos**

---

# 🔗 Relacionamentos

- Um cliente pode realizar vários pedidos  
- Um produto pode aparecer em vários pedidos  
- Cada pedido pertence a um cliente e a um produto  

---

# 📊 Estrutura das Tabelas

## clientes
- id_cliente (PK)  
- nome  
- email  
- telefone  

## produtos
- id_produto (PK)  
- nome  
- preco  

## pedidos
- id_pedido (PK)  
- data  
- quantidade  
- id_cliente (FK)  
- id_produto (FK)  

---

# 🔑 Chaves Estrangeiras

- pedidos.id_cliente → clientes.id_cliente  
- pedidos.id_produto → produtos.id_produto  

---

# 📐 Cardinalidade

- clientes 1:N pedidos  
- produtos 1:N pedidos  

---

# 📁 Estrutura do Projeto
