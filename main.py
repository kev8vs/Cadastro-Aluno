import sqlite3
import os


def conectar_banco_dados():
    conexao = sqlite3.connect("alunos_notas.db")
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        nota REAL CHECK(nota BETWEEN 0 AND 10)
    )
""")
    conexao.commit()
    conexao.close()

def imprimir_título(titulo=str):
    print('---' * 10)
    print(titulo.center(30))
    print('---' * 10)


def pressione_enter():
    input('\nAperte ENTER para continuar...')


def imprimir_menu():
    imprimir_título('Menu')
    print("""
1 - Adicionar aluno
2 - Listar todos os alunos
3 - Buscar aluno pelo ID
4 - Atualizar aluno
5 - Remover aluno 
6 - Mostrar Média geral das notas
7 - Sair
    """)


def main():
    while True:
        os.system('cls')
        imprimir_menu()
        escolha = input("\n- Escolha de 1 a 7: ")
        if escolha == '1':
            adicionar_aluno()
        elif escolha == '2':
            listar_todos_alunos()
        elif escolha == '3':
            buscar_aluno_pelo_id()
        elif escolha == '4':
            atualizar_cadastro_aluno()
        elif escolha == '5':
            remover_aluno()
        elif escolha == '6':
            media_geral_turmas()
        elif escolha == '7': 
            print('\n- Desligando Sistema...')
            break
        else:
            print('\nERRO! Digite apenas números de 1 a 6.')
            pressione_enter()


def adicionar_aluno():
    while True:
        try:
            os.system('cls')
            imprimir_título('Adicionar Aluno')
            nome = str(input('Nome do aluno: ').capitalize())
            idade = int(input('Qual idade do aluno: '))
            nota = float(input('Qual a nota do aluno: '))
            # Verifica e adiciona no banco de dados
            if nota >= 0 and nota <= 10 and idade > 0 and nome is not None:
                conexao = sqlite3.connect("alunos_notas.db")
                cursor = conexao.cursor()
                cursor.execute('''
                    INSERT INTO alunos (nome, idade, nota)
                    VALUES (?, ?, ?)
                ''', (nome, idade, nota))
                conexao.commit()
                conexao.close()
                break
            else:
                print('\nErro! Digite valores válidos. ')
                pressione_enter()

        except Exception:
            print('\nERRO! Digite valores Válidos')
            pressione_enter()


def listar_todos_alunos():
    imprimir_título('Listar Alunos')
    conexao = sqlite3.connect("alunos_notas.db")
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM alunos')
    alunos = cursor.fetchall()
    print('\n' + '---' * 10)
    for aluno in alunos:
        print(f'- ID: {aluno[0]} \n- Nome: {aluno[1]} \n- Idade: {aluno[2]} \n- Nota: {aluno[3]}')
        print('---' * 10)
    conexao.commit()
    conexao.close()
    pressione_enter()
    

def buscar_aluno_pelo_id():
    os.system('cls')
    imprimir_título('Buscar ALuno')
    while True:
        try:
            buscar_id = int(input("Digite o ID do aluno: "))
            conexao = sqlite3.connect("alunos_notas.db")
            cursor = conexao.cursor()
            cursor.execute('SELECT * FROM alunos WHERE id = ?', (buscar_id,))
            aluno = cursor.fetchone()
            if aluno:
                print(f'- ID: {aluno[0]} \n- Nome: {aluno[1]} \n- Idade: {aluno[2]} \n- Nota: {aluno[3]}')
                conexao.commit()
                conexao.close()
                pressione_enter()
                break
            else:
                print('Aluno não encontrado!')
            conexao.close()
            pressione_enter()
        except Exception:
            print('\nERRO! Digite apenas números inteiros.')


def remover_aluno():
    os.system('cls')
    imprimir_título('Remover Aluno')    
    while True:
        try:
            id_aluno = int(input("Digite o ID do aluno: "))
            conexao = sqlite3.connect("alunos_notas.db")
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
            
            if cursor.rowcount > 0: # verifica se foi deletado, 1 quer dizer que sim, 0 que dizer que não
                conexao.commit()
                print("\n- Cadastro do aluno deletado com sucesso!")
                conexao.close()
                break
            else:
                print("\n- Cadastro do aluno não encontrado!")
            conexao.close()
        except Exception:
            print('\nERRO! Digite apenas números inteiros.')
    pressione_enter()


def atualizar_cadastro_aluno():
    os.system('cls')
    imprimir_título('Atualizar o Cadastro do ALuno')
    while True:
            try:
                id_aluno = int(input("Digite o ID do aluno: "))
                conexao = sqlite3.connect("alunos_notas.db")
                cursor = conexao.cursor()
                cursor.execute('SELECT * FROM alunos WHERE id = ?', (id_aluno,))
                aluno = cursor.fetchone()
                if aluno:
                    nome = str(input('\nQual o nome do aluno: ').capitalize())
                    idade = int(input('Qual a idade do aluno: '))
                    nota = float(input('Qual a nota do aluno: '))

                    if nota >= 0 and nota <= 10 and idade > 0:
                        cursor.execute("UPDATE alunos SET nome = ?, idade = ?, nota = ? WHERE id = ?", (nome, idade, nota, id_aluno))
                        conexao.commit()
                        conexao.close()
                        print('\n- Aluno atualizado com sucesso! ')
                        break
                    else:
                        print('\nErro! Digite Valores Válidos.')
                        pressione_enter()
                else:
                    print('\nAluno não encontrado.')
                    pressione_enter()
                conexao.close()
            except Exception:
                print('\nERRO! Digite valores válidos.')
    pressione_enter()


def media_geral_turmas():
    os.system('cls')
    imprimir_título("Média Geral da Turma")
    conexao = sqlite3.connect("alunos_notas.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT AVG(nota) FROM alunos")
    resultado = cursor.fetchone()
    print('\n' + '---' * 10)
    if resultado is None:
        print("\nNão existem alunos cadastrados!")
    else:
        print(f"\n - Média geral da turma: {resultado[0]:.2f}")

    conexao.close()
    pressione_enter()  


if __name__ == "__main__":
    conectar_banco_dados()
    main()
