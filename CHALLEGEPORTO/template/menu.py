import click
import oracledb

connection = oracledb.connect("rm552539/130701@oracle.fiap.com.br/orcl")
cursor = connection.cursor()


def print_menu():
    print("1. Criar registro")
    print("2. Ler registros")
    print("3. Atualizar registro")
    print("4. Excluir registro")
    print("5. Sair")

@click.command()
def main():
    while True:
        print_menu()
        choice = input("Escolha uma opção (1-5): ")

        if choice == '1':
            create()
        elif choice == '2':
            read()
        elif choice == '3':
            update()
        elif choice == '4':
            delete()
        elif choice == '5':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

def create():
    """Cria um novo registro."""
    id_segurado = input("ID do segurado: ")  
    cpf = input("CPF do segurado: ")
    nr_apolice = input("Número da apólice: ")
    dt_cadastro = input("Data de cadastro (YYYY-MM-DD): ")
    nm_usuario = input("Nome do usuário: ")

    cursor.execute("""
        INSERT INTO T_GUISR_SEGURADO (ID_SEGURADO, CPF_SEGURADO, NR_APOLICE, DT_CADASTRO, NM_USUARIO)
        VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5)
    """, (id_segurado, cpf, nr_apolice, dt_cadastro, nm_usuario))

    connection.commit()
    print("Registro criado com sucesso.")


def read():
    """Lê todos os registros."""
    cursor.execute("SELECT * FROM t_guisr_segurado")
    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row[0]}, CPF: {row[1]}, Apólice: {row[2]}")

def update():
    """Atualiza um registro."""
    id_segurado = input("ID do segurado para atualizar: ")

    cursor.execute("SELECT * FROM t_guisr_segurado WHERE id_segurado = :1", (id_segurado,))
    row = cursor.fetchone()

    if row:
        new_cpf = input(f"Novo CPF ({row[1]}): ")
        new_nr_apolice = input(f"Novo número da apólice ({row[2]}): ")
        new_dt_cadastro = input(f"Nova data de cadastro ({row[3]}): ")
        new_nm_usuario = input(f"Novo nome do usuário ({row[4]}): ")

        cursor.execute("""
            UPDATE t_guisr_segurado
            SET cpf_segurado = :1, nr_apolice = :2, dt_cadastro = TO_DATE(:3, 'YYYY-MM-DD'),
                nm_usuario = :4
            WHERE id_segurado = :5
        """, (new_cpf, new_nr_apolice, new_dt_cadastro, new_nm_usuario, id_segurado))

        connection.commit()
        print("Registro atualizado com sucesso.")
    else:
        print("Segurado não encontrado.")

def delete():
    """Exclui um registro."""
    id_segurado = input("ID do segurado para excluir: ")

    cursor.execute("DELETE FROM t_guisr_segurado WHERE id_segurado = :1", (id_segurado,))
    connection.commit()
    print("Registro excluído com sucesso.")

if __name__ == '__main__':
    main()

cursor.close()
connection.close()
print("Operações no banco de dados concluídas.")
