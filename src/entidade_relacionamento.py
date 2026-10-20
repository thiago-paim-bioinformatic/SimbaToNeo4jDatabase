class Entidade:
    def __init__(self):
        pass

    def get_dados_simba(self, dados) -> None:
        df = dados
        self.NUMERO_CASO = df['ï»¿NUMERO_CASO'] 
        self.NUMERO_BANCO = df['NUMERO_BANCO'] 
        self.NOME_BANCO = df['NOME_BANCO'] 
        self.NUMERO_AGENCIA = df['NUMERO_AGENCIA']
        self.NUMERO_CONTA = df['NUMERO_CONTA'] 
        self.TIPO = df['TIPO'] 
        self.NOME_TITULAR = df['NOME_TITULAR'] 
        self.CPF_CNPJ_TITULAR = df['CPF_CNPJ_TITULAR']
        self.DESCRICAO_LANCAMENTO = df['DESCRICAO_LANCAMENTO'] 
        self.CNAB = df['CNAB'] 
        self.DATA_LANCAMENTO = df['DATA_LANCAMENTO'] 
        self.NUMERO_DOCUMENTO = df['NUMERO_DOCUMENTO']
        self.NUMERO_DOCUMENTO_TRANSACAO = df['NUMERO_DOCUMENTO_TRANSACAO'] 
        self.LOCAL_TRANSACAO = df['LOCAL_TRANSACAO'] 
        self.VALOR_TRANSACAO = df['VALOR_TRANSACAO']
        self.NATUREZA_LANCAMENTO = df['NATUREZA_LANCAMENTO']
        self.VALOR_SALDO = df['VALOR_SALDO'] 
        self.NATUREZA_SALDO = df['NATUREZA_SALDO'] 
        self.CPF_CNPJ_OD = df['CPF_CNPJ_OD']
        self.NOME_PESSOA_OD = df['NOME_PESSOA_OD'] 
        self.TIPO_PESSOA_OD = df['TIPO_PESSOA_OD'] 
        self.NUMERO_BANCO_OD = df['NUMERO_BANCO_OD']
        self.NUMERO_AGENCIA_OD = df['NUMERO_AGENCIA_OD'] 
        self.NUMERO_CONTA_OD = df['NUMERO_CONTA_OD'] 
        self.OBSERVACAO = df['OBSERVACAO']
        self.NOME_ENDOSSANTE_CHEQUE = df['NOME_ENDOSSANTE_CHEQUE'] 
        self.DOC_ENDOSSANTE_CHEQUE = df['DOC_ENDOSSANTE_CHEQUE']


    def sintaxe_cypher_conta_titular(self) -> str:

        ID = f"{str(self.NUMERO_BANCO).strip().zfill(3)}-{str(self.NUMERO_AGENCIA).strip().zfill(9)}-{str(self.NUMERO_CONTA).strip().zfill(14)}"

        sintaxe_cypher = f"""
            MERGE (titular:CONTA {{id:'{ID}'}})
            ON CREATE SET
                titular.numero_banco = '{self.NUMERO_BANCO}',
                titular.nome_banco ='{self.NOME_BANCO}',
                titular.numero_agencia = '{self.NUMERO_AGENCIA}',
                titular.numero_conta = '{self.NUMERO_CONTA}',
                titular.numero_caso = '{self.NUMERO_CASO}'
            """
        return sintaxe_cypher, ID
    
    
    def sintaxe_cypher_conta_od(self) -> str:
    
        ID = f"{str(self.NUMERO_BANCO_OD).strip().zfill(3)}-{str(self.NUMERO_AGENCIA_OD).strip().zfill(9)}-{str(self.NUMERO_CONTA_OD).strip().zfill(14)}"

        sintaxe_cypher = f"""
            MERGE (od:CONTA {{id:'{ID}'}})
            ON CREATE SET
                od.numero_banco ='{self.NUMERO_BANCO_OD}',
                od.nome_banco = '',
                od.numero_agencia = '{self.NUMERO_AGENCIA_OD}',
                od.numero_conta = '{self.NUMERO_CONTA_OD}',
                od.numero_caso = '{self.NUMERO_CASO}'
            """
        return sintaxe_cypher, ID

    def sintaxe_cypher_transacao(self) -> str:
        
        ID = f"{self.CNAB}-{str(self.DATA_LANCAMENTO).strip().replace(" ","").replace(":","")}-{str(self.VALOR_TRANSACAO).replace(".","")}-{self.NATUREZA_LANCAMENTO}-{str(self.VALOR_SALDO).replace(".","")}-{self.NATUREZA_SALDO}"

        sintaxe_cypher = f"""
            MERGE (t:TRANSACAO {{id:'{ID}'}})
            ON CREATE SET
                t.cnab = '{self.CNAB}',
                t.data_lancamento = datetime('{self.DATA_LANCAMENTO.strftime('%Y-%m-%dT%H:%M:%S')}'),
                t.valor_transacao = toFloat({self.VALOR_TRANSACAO}),
                t.natureza_lancamento = '{self.NATUREZA_LANCAMENTO}',
                t.valor_saldo = toFloat({self.VALOR_SALDO}),
                t.natureza_saldo = '{self.NATUREZA_SALDO}',
                t.descricao_lancamento = '{self.DESCRICAO_LANCAMENTO}',
                t.numero_documento = '{self.NUMERO_DOCUMENTO}',
                t.numero_documento_transacao =  '{self.NUMERO_DOCUMENTO_TRANSACAO}',
                t.nome_endossante_cheque = '{self.NOME_ENDOSSANTE_CHEQUE}',
                t.doc_endossante_cheque = '{self.DOC_ENDOSSANTE_CHEQUE}',
                t.numero_caso = '{self.NUMERO_CASO}'
            """
        return sintaxe_cypher, str(self.NATUREZA_LANCAMENTO)


    def sintaxe_cypher_pessoa_titular(self) -> str:

        ID = str(self.CPF_CNPJ_TITULAR).strip().replace(".0","").zfill(14)
        sintaxe_cypher = f"""
            MERGE (pt:PESSOA {{id:'{ID}'}})
            ON CREATE SET
                pt.nome_pessoa ='{self.NOME_TITULAR}',
                pt.cpf_cnpj = '{ID}',
                pt.tipo_pessoa = '{self.TIPO}',
                pt.numero_caso = '{self.NUMERO_CASO}'
            """
        return sintaxe_cypher
        
    def sintaxe_cypher_pessoa_od(self) -> str:
        ID = str(self.CPF_CNPJ_OD).strip().replace(".0","").zfill(14)
        sintaxe_cypher = f"""
            MERGE (pod:PESSOA {{id:'{ID}'}})
            ON CREATE SET
                pod.nome_pessoa ='{self.NOME_PESSOA_OD}',
                pod.cpf_cnpj = '{ID}',
                pod.tipo_pessoa = '{self.TIPO_PESSOA_OD}',
                pod.numero_caso = '{self.NUMERO_CASO}'
            """
        return sintaxe_cypher

class Relacionamento:
    def __init__(self):
        pass

    def create_relacionamento_transacao(self, natureza_lancamento:str) -> str:

        if natureza_lancamento == "D":
            
            sintaxe_cypher = f"""
                MERGE (titular)-[:ENVIOU]->(t)
                MERGE (t)-[:RECEBEU]->(od)
                """
            return sintaxe_cypher
        
        elif natureza_lancamento == "C":
            sintaxe_cypher = f"""
                MERGE (titular)<-[:RECEBEU]-(t)
                MERGE (t)<-[:ENVIOU]-(od)
                """
            return sintaxe_cypher
        else:
            sintaxe_cypher = f"""
                MERGE (titular)-[:TRANSACIONOU]-(t)
                MERGE (t)-[:TRANSACIONOU]-(od)
                """
            return sintaxe_cypher

    def create_relacionamento_pessoa_titular_conta(self) -> str:
        sintaxe_cypher = "MERGE (pt)<-[:PERTENCE]-(titular)"
        return sintaxe_cypher

    def create_relacionamento_pessoa_od_conta(self) -> str:
        sintaxe_cypher = "MERGE (pod)<-[:PERTENCE]-(od)"
        return sintaxe_cypher
    
