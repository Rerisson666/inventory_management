from inventory import add_product, update_stock, get_product_location, generate_report
from database import initialize_db

def menu():
    print("1. Adicionar Produto")
    print("2. Atualizar Estoque")
    print("3. Rastrear Localização")
    print("4. Gerar Relatórios")
    print("5. Sair")

def main():
    initialize_db()

    while True:
        menu()
        choice = input("Escolha uma opção: ")

        if choice == '1':
            name = input("Nome do Produto: ")
            category = input("Categoria: ")
            quantity = int(input("Quantidade: "))
            price = float(input("Preço: "))
            location = input("Localização: ")
            add_product(name, category, quantity, price, location)
            print("Produto adicionado com sucesso!")

        elif choice == '2':
            product_id = int(input("ID do Produto: "))
            quantity_change = int(input("Alteração na Quantidade (+/-): "))
            update_stock(product_id, quantity_change)
            print("Estoque atualizado com sucesso!")

        elif choice == '3':
            product_id = int(input("ID do Produto: "))
            location = get_product_location(product_id)
            if location:
                print(f"Localização do produto: {location[0]}")
            else:
                print("Produto não encontrado.")

        elif choice == '4':
            low_stock, high_stock, all_products = generate_report()
            print("Produtos com Estoque Baixo:")
            for product in low_stock:
                print(f"Nome: {product[0]}, Quantidade: {product[1]}")
            
            print("\nProdutos com Excesso de Estoque:")
            for product in high_stock:
                print(f"Nome: {product[0]}, Quantidade: {product[1]}")
            
            print("\nTodos os Produtos:")
            for product in all_products:
                print(f"Nome: {product[0]}, Quantidade: {product[1]}")

        elif choice == '5':
            break

if __name__ == "__main__":
    main()
