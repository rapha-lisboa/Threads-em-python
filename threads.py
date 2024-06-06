# Importação de bibliotecas
from threading import Thread, Lock


def separate_numbers(numbers, num_batches):
    """
    Função que pega uma array de números com tamanho indefinido e separa em um numero determinado de lotes,
    o intuito é que cada thread futuramente seja responsável por um lote

    Args:
        numbers (array): lista de números para ser dividida
        num_batches (int): numero de lotes que serão destinados aos threads

    Return:
        array: lista com os batches já separados
    """
    batches = []
    for batch in range(num_batches):
        batches.append(numbers[batch::num_batches])

    return batches

total_sum = 0
lock = Lock()

def sum_numbers(numbers):
    """
    Função que atualiza a variável global total_sum com a soma dos números da lista dada pelos parâmetros.

    Args:
        numbers (array): lista de números a serem somados
    """
    global total_sum
    lock.acquire()
    total_sum += sum(numbers)
    lock.release()

def sum_with_threads(numbers, num_threads):
    """
    Função que dado uma lista de números, separa essa lista em vários lotes dependendo do número de threads que
    serão usados, cria vários threads, faz com que cada thread realize a soma de um lote e ao fim a soma de todos 
    os threads sejam reunidos para concluir a soma de todos os números da lista inicial

    Args:
        numbers (array): lista de números
        num_threads (int): número de threads que deseja ser utilizado

    Return:
        int: soma de todos os números da lista numbers dada nos parametros
    """

    threads = []

    # Instancia as threads
    for batch in separate_numbers(numbers, num_threads):
        threads.append(Thread(target=sum_numbers, args=(batch,)))
    
    # Inicia as threads
    for thread in threads:
        thread.start()

    #Interrompe as threads e reune os resultados
    for thread in threads:
        thread.join()
    
    return total_sum
    

# 3 somas diferentes realizadas por threads
soma1 = sum_with_threads(range(11), num_threads=2)
soma2 = sum_with_threads(range(1001), num_threads=2)
soma3 = sum_with_threads(range(1_000_001), num_threads=2)

# Resultado das 3 somas anteriores
print('A soma dos numeros de 0 a 10 é: ' + str(soma1))
print('A soma dos numeros de 0 a 1000 é: ' + str(soma2))
print('A soma dos numeros de 0 a 1 milhão é: ' + str(soma3))