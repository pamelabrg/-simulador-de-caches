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

        input("Pressione Enter para continuar...")  # Aguarda a entrada do usuário
