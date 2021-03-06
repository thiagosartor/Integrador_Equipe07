from bancoBD import Banco
from funcoes import Funcoes, LOG

class Cliente():
    def __init__(self, id_cliente=0, nome="", cpf="", telefone="", compra_fiado=0, senha="", dia_fiado=1):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.compra_fiado = compra_fiado
        self.senha = senha
        self.dia_fiado = dia_fiado

    def selectAll(self):
        try:
            banco = Banco()

            c = banco.conexao.cursor()
            c.execute('SELECT id_cliente, nome, telefone, compra_fiado FROM tb_cliente')

            result = c.fetchall()
            c.close()

            
            return result
           

        except Exception as e:
            return str(e)
           

    def selectOne(self):
        try:
            banco = Banco()

            c=banco.conexao.cursor()

            c.execute('SELECT id_cliente, nome,cpf, telefone, compra_fiado, dia_fiado FROM tb_cliente WHERE id_cliente = %s ', (self.id_cliente))

            for linha in c:
                self.id_cliente = linha[0]
                self.nome = linha[1]
                self.cpf = linha[2]
                self.telefone = linha[3]
                self.compra_fiado = linha[4]                
                self.dia_fiado = linha[5]

            c.close()

            return 'Busca feita com sucesso!'

        except:
            return 'Erro ao buscar cliente!'
                
    def insert(self):
        try:
            banco = Banco()
            c = banco.conexao.cursor()

            c.execute('INSERT INTO tb_cliente(nome,cpf,telefone,compra_fiado,senha,dia_fiado) VALUES(%s,%s,%s,%s,%s,%s)',(self.nome, self.cpf, self.telefone, self.compra_fiado, self.senha,self.dia_fiado))
            banco.conexao.commit()
            Funcoes.criaLOG(f'INSERT CLIENTE, id_cliente: {c.lastrowid}', LOG.info)
            c.close()

            return 'Cliente cadastrado com sucesso!'
        except Exception as e:
            Funcoes.criaLOG(str(e), LOG.error)
            raise Exception('Erro ao cadastrar cliente!', str(e))

    def update(self):
        try:
            banco = Banco()
            c = banco.conexao.cursor()

            c.execute('UPDATE tb_cliente SET nome=%s,cpf=%s,telefone=%s,compra_fiado=%s,dia_fiado=%s WHERE id_cliente = %s',(self.nome, self.cpf, self.telefone, self.compra_fiado, self.dia_fiado, self.id_cliente))
            banco.conexao.commit()
            Funcoes.criaLOG(f'UPDATE CLIENTE, id_cliente: {self.id_cliente}', LOG.info)
            c.close()

            return 'Cliente editado com sucesso!'

        except Exception as e:
            Funcoes.criaLOG(str(e), LOG.error)
            raise Exception('Erro ao editar cliente!', str(e))
             

    def delete(self):
        try:
            banco = Banco()
            c = banco.conexao.cursor()

            c.execute('DELETE FROM tb_cliente WHERE id_cliente = %s',(self.id_cliente))
            banco.conexao.commit()
            Funcoes.criaLOG(f'DELETE CLIENTE, id_cliente: {self.id_cliente}', LOG.info)
            c.close()

            return 'Cliente excluido com sucesso'
        
        except Exception as e:
            Funcoes.criaLOG(str(e), LOG.error)
            raise Exception('Erro ao tentar excluir cliente', str(e))
            
    def validaCPFExistente(self):
        try:
            banco = Banco()
            c = banco.conexao.cursor()

            c.execute('SELECT id_cliente FROM tb_cliente WHERE cpf=%s', (self.cpf))

            result = c.fetchall()
            c.close()
            return result

        except Exception as e:
            raise Exception('Erro ao tentar validar CPF', str(e))

    def validaClienteFiado(self):
        try:
            banco = Banco()
            c = banco.conexao.cursor()

            c.execute('SELECT id_cliente FROM tb_cliente where cpf = %s and compra_fiado = %s', (self.cpf, 1))

            result = c.fetchall()

            return result
        except Exception as e:
            raise Exception('Erro ao tentar validar cliente', str(e))

        finally:
            c.close()

    def validaSenhaCliente(self):
        try:
            banco = Banco()
            c = banco.conexao.cursor()

            c.execute('SELECT id_cliente FROM tb_cliente WHERE cpf = %s AND senha = %s', (self.cpf, self.senha))

            result = c.fetchall()

            return result
        except Exception as e:
            raise Exception('Erro ao tentar validar cliente', str(e))

        finally:
            c.close()

    def buscaClientePorCPF(self):
        banco = None
        c = None
        try:
            banco = Banco()

            c = banco.conexao.cursor()

            c.execute('SELECT id_cliente, nome, cpf, telefone, dia_fiado FROM tb_cliente WHERE cpf = %s', (self.cpf))
            result = c.fetchall()
            if len(result) > 0:
                for linha in result:
                    self.id_cliente = linha[0]
                    self.nome = linha[1]
                    self.cpf = linha[2]
                    self.telefone = linha[3]
                    self.dia_fiado = linha[4]
                return True
            else:
                return False

           

        except Exception as e:
            raise Exception('Erro ao tentar buscar cliente', str(e))

        finally:
            if c:
                c.close()
            if banco:
                banco.conexao.close()
        
    def selectLogin(self):
        banco = None
        c = None
        try:
            banco = Banco()
            c = banco.conexao.cursor()

            _sql = 'SELECT id_cliente, nome FROM tb_cliente WHERE nome = %s AND senha = %s'
            _sql_data = (self.nome, self.senha)

            c.execute(_sql, _sql_data)

            result = c.fetchall()
            if len(result) > 0:
                for linha in result:                    
                    self.id_cliente = linha[0]
                    self.nome = linha[1]                    
                
                return True

                         
            return False
        except Exception as e:
            raise Exception('Erro ao validar login de Cliente', str(e))
        finally:
            if c:
                c.close()
            if banco:
                banco.conexao.close()
