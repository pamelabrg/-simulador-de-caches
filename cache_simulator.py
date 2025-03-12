from memoria_cache import MemoriaCache

cache = MemoriaCache()

with open(cache.arquivo_entrada, "rb") as f:
    while True:
        prox_byte = f.read(4)
        if not prox_byte:
            break  
        endereco = int.from_bytes(prox_byte, byteorder="big")
        
        if cache.assoc == 1:
            cache_map = cache.acessar_cache_mapeamento_direto(endereco)
        elif cache.nsets == 1:
            cache_map = cache.acessar_cache_totalmente_associativa(endereco)
        else:
            cache_map = cache.acessar_cache_associativa(endereco)

    total_acessos = cache.total_accesses    
    taxa_hit = (cache.hits / total_acessos) if total_acessos > 0 else 0
    taxa_miss = 1 - taxa_hit  
    total_misses = cache.compulsory_misses + cache.capacity_misses + cache.conflict_misses

    taxa_miss_compulsorio = (cache.compulsory_misses / total_misses) if total_misses > 0 else 0
    taxa_miss_capacidade = (cache.capacity_misses / total_misses) if total_misses > 0 else 0
    taxa_miss_conflito = (cache.conflict_misses / total_misses) if total_misses > 0 else 0

    if cache.flag_saida == 0:
        print(f"Total de acessos: {total_acessos}")
        print(f"Total de hits: {cache.hits}")
        print(f"Total de misses: {total_misses}")
        print(f"Taxa de hits = {taxa_hit:.2%}")
        print(f"Taxa de misses = {taxa_miss:.2%}")
        print(f"Misses compulsórios = {taxa_miss_compulsorio:.2%}")
        print(f"Misses de capacidade = {taxa_miss_capacidade:.2%}")
        print(f"Misses de conflito = {taxa_miss_conflito:.2%}")
    else:
        print(f"{total_acessos}, {taxa_hit:.4f}, {taxa_miss:.4f}, "
            f"{taxa_miss_compulsorio:.4f}, {taxa_miss_capacidade:.4f}, "
            f"{taxa_miss_conflito:.4f}")