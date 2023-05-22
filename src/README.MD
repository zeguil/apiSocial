
# Salvar mudanças no banco
alembic revision --autogenerate -m "descrição"

# Atualizar banco
alembic upgrade head

# Voltar alterações no banco
alembic downgrade -1