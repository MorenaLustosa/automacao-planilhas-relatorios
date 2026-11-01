# Automação de planilhas e relatórios — processamento de dados

**Status:** MVP local funcional; sem agendamento ou integração automática com sistemas externos. **Dados:** fictícios. **Tecnologias:** Python, pandas, openpyxl, Streamlit.

## Objetivo
Receber uma planilha, validar campos obrigatórios, detectar linhas com dados ausentes ou inválidos e duplicatas exatas, consolidar indicadores por setor e exportar um Excel com três abas: **Dados tratados**, **Inconsistencias** e **Resumo**.

## Como usar
Instale Python 3.10+. Nesta pasta execute `python -m pip install -r requirements.txt` e `python -m streamlit run app.py` (ou `INICIAR_WINDOWS.bat` no Windows). Use `dados_exemplo/indicadores.csv` (padrão) ou importe `.csv`/`.xlsx`. Clique em **Baixar relatório Excel (3 abas)**.

## Modelo de entrada
Colunas obrigatórias: `data,setor,indicador,valor,meta`. Data ISO `AAAA-MM-DD`, valores numéricos com ponto como separador decimal. Exemplo: `2026-10-01,Vendas,Qualidade,92,85`. Linhas idênticas nas cinco colunas são consideradas duplicatas (a primeira é mantida). Datas inválidas ou valores faltantes não entram no resumo. A comparação `valor >= meta` pressupõe que **quanto maior, melhor** para todos os indicadores; adapte se isso não for verdade.

## Cálculos
Agrupa por setor e indicador e mostra número de registros, média dos valores, média das metas e proporção de registros que atingiram a meta. A aba de inconsistências aponta número da linha do CSV (inclui cabeçalho), não a linha real de planilhas com cabeçalhos deslocados.

## Estrutura
- `core.py`: validações, agregação e exportação.
- `app.py`: interface web local.
- `dados_exemplo/indicadores.csv`: registros simulados.
- `tests/test_core.py`: testes unitários.

## Limitações e evolução
Ainda não agenda execuções, não envia e-mails e não se conecta a Google Sheets/ERP. Melhorias: configuração de regras por indicador, histórico de processamento, permissões, agendamento e notificações. Não publique dados sensíveis em repositórios públicos.
