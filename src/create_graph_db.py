from neo4j import GraphDatabase
import simba_db as simba
import entidade_relacionamento
from dotenv import load_dotenv
import os

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
load_dotenv()
URI = os.getenv("URI")
AUTH_BASE = os.getenv("AUTH_BASE")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")
PATH_DATABASE_SIMBA = os.getenv("PATH_DATABASE_SIMBA")

AUTH = (AUTH_BASE, AUTH_PASSWORD)

driver = GraphDatabase.driver(URI, auth=AUTH)

def record_graph_to_neo4j (driver, query:str) -> None:
    driver.execute_query(query_ = query)

def main(driver):
    dados_simba = simba.Simba(simba_csv_path=PATH_DATABASE_SIMBA)
    df = dados_simba.get_dataframe()

    print(df.describe())

    print(df.columns)

    count = 1

   
    for _, row in df.iterrows():
        print(f"****** Entidade-Relacionamento nº {count}")
        entidade = entidade_relacionamento.Entidade()
        entidade.get_dados_simba(dados=row)
        cypher_conta_tit, id_1 = entidade.sintaxe_cypher_conta_titular()
        cypher_conta_od, id_2 = entidade.sintaxe_cypher_conta_od()
        cypher_transacao, natur_trans = entidade.sintaxe_cypher_transacao()

        cypher_pessoa_titular = entidade.sintaxe_cypher_pessoa_titular()
        cypher_pessoa_od = entidade.sintaxe_cypher_pessoa_od()


        relacionamento = entidade_relacionamento.Relacionamento()
        cypher_relacionamento_transacao = relacionamento.create_relacionamento_transacao(natureza_lancamento=natur_trans)
        cypher_relacionamento_pessoa_titular_conta = relacionamento.create_relacionamento_pessoa_titular_conta()
        cypher_relacionamento_pessoa_od_conta = relacionamento.create_relacionamento_pessoa_od_conta()

        sintaxe = f"""
                    {cypher_conta_tit}
                    {cypher_conta_od}
                    {cypher_transacao}
                    {cypher_pessoa_titular}
                    {cypher_pessoa_od}
                    {cypher_relacionamento_transacao}
                    {cypher_relacionamento_pessoa_titular_conta}
                    {cypher_relacionamento_pessoa_od_conta}
                    """

        print(sintaxe)
        print("*************")
        count += 1

        try:
            record_graph_to_neo4j(driver=driver,
                                  query=sintaxe)
        except Exception as e:
            print(f"Erro de execução no NEO4J: {e}")

if __name__ == "__main__":
    main(driver)
