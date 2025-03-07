from memoria_cache import MemoriaCache

cache = MemoriaCache()
cache.imprimir_cache()

with open(cache.arquivo_entrada, "rb") as f:
    while True:
        prox_byte = f.read(4) #lendo 4byte4s
        if not prox_byte:
            break  
        
        endereco = int.from_bytes(prox_byte, byteorder="big")
        hit_or_miss = cache.acessar_cache(endereco)
        cache.total_accesses += 1
        
        if cache.assoc == 1:
            cache_map = cache.acessar_cache_mapeamento_direto(endereco)
        elif cache.assoc == cache.nsets:
            cache_map = cache.acessar_cache_totalmente_associativa(endereco)
        else:
            cache_map = cache.acessar_cache_associativa(endereco)