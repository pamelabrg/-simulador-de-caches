from memoria_cache import MemoriaCache

cache = MemoriaCache()
#cache.imprimir_cache()

with open(cache.arquivo_entrada, "rb") as f:
    while True:
        prox_byte = f.read(4)  # Lendo 4 bytes
        if not prox_byte:
            break  
        #print(f"Próximo byte: {prox_byte}")
        endereco = int.from_bytes(prox_byte, byteorder="big")
        #print(f"Endereço: {endereco}")
        
        if cache.assoc == 1:
            cache_map = cache.acessar_cache_mapeamento_direto(endereco)
        elif cache.assoc == cache.nsets:
            cache_map = cache.acessar_cache_totalmente_associativa(endereco)
        else:
            cache_map = cache.acessar_cache_associativa(endereco)
        #print("\n\n\n")
        #input("Pressione Enter para continuar...") 
    


    total_acessos = cache.total_accesses

    # Evita divisão por zero
    taxa_hit = (cache.hits / total_acessos) if total_acessos > 0 else 0
    taxa_miss = 1 - taxa_hit  # Taxa de miss = 100% - Taxa de hit
    total_misses = cache.compulsory_misses + cache.capacity_misses + cache.conflict_misses

    taxa_miss_compulsorio = (cache.compulsory_misses / total_misses)  if total_misses > 0 else 0
    taxa_miss_capacidade = (cache.capacity_misses / total_misses)  if total_misses > 0 else 0
    taxa_miss_conflito = (cache.conflict_misses / total_misses)  if total_misses > 0 else 0

    # Exibir os resultados formatados  Total de acessos, Taxa de hit, Taxa de miss, Taxa de miss compulsório, Taxa de miss de capacidade, Taxa de miss de conflito 
    print(f"{total_acessos}, {taxa_hit:.4f}, {taxa_miss:.4f}, {taxa_miss_compulsorio:.4f}, {taxa_miss_capacidade:.4f}, {taxa_miss_conflito:.4f}")
    '''print(f"Total de acessos: {total_acessos}")
    print(f"Total de hits: {cache.hits}")
    print(f"Total de misses compulsórios: {cache.compulsory_misses}")
    print(f"Total de misses de capacidade: {cache.capacity_misses}")
    print(f"Total de misses de conflito: {cache.conflict_misses}")

    print(f"Taxa de hit: {taxa_hit:.2f}%")
    print(f"Taxa de miss: {taxa_miss:.2f}%")
    print(f"Taxa de miss compulsório: {taxa_miss_compulsorio:.2f}%")
    print(f"Taxa de miss de capacidade: {taxa_miss_capacidade:.2f}%")
    print(f"Taxa de miss de conflito: {taxa_miss_conflito:.2f}%")'''


