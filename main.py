import networkx as nx
import matplotlib.pyplot as plt
import csv

def read_books_data(filename):
    #Lee los datos del archivo CSV "books.csv" y muestra su contenido.
    books = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append(row)
    return books
    
def calculate_similarity(book1, book2):
    #Calcula la similitud entre dos libros basada en ciertos criterios.
    similarity_score = 0
    
    # Criterio 1: Mismo autor
    if book1['Author'] == book2['Author']:
        similarity_score += 1
        print("Se enconre una similitud entre: ", book1['Book'], "y", book2['Book'])
    
    # Criterio 2: Mismo género
    genres_book1 = set(book1['Genres'].strip("[]").replace("'", "").split(", "))
    genres_book2 = set(book2['Genres'].strip("[]").replace("'", "").split(", "))
    common_genres = genres_book1.intersection(genres_book2)
    similarity_score += len(common_genres)
    
    return similarity_score

def create_book_graph(books):
    #Crea un grafo de libros y asigna valores a las aristas basados en la similitud entre los libros.
    G = nx.Graph()

    # Agrega los nodos (libros) al grafo
    for book in books:
        G.add_node(book['Book'], author=book['Author'], genres=book['Genres'], description=book['Description'])

    # Agrega las aristas y asigna valores de similitud a las aristas
    for i, book1 in enumerate(books):
        for j, book2 in enumerate(books):
            if i != j:  # Evita comparar un libro consigo mismo
                similarity = calculate_similarity(book1, book2)
                if similarity > 4:
                    G.add_edge(book1['Book'], book2['Book'], weight=similarity)
    return G

# Nombre del archivo CSV
filename = "books.csv"

# Llama a la función para leer y mostrar los datos del archivo CSV
books = read_books_data(filename)

# Crea el grafo de libros y asigna valores a las aristas basados en la similitud entre los libros
book_graph = create_book_graph(books)


#config del grafo a mostrar
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(book_graph, k=2  )  # Determina la posición de los nodos
nx.draw(book_graph, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray', width=2)

# Añadir las aristas con los valores de  similitud
labels = nx.get_edge_attributes(book_graph, 'weight')
nx.draw_networkx_edge_labels(book_graph, pos, edge_labels=labels, font_color='red')

plt.title('Grafo de libros con similitud entre ellos')
plt.show()