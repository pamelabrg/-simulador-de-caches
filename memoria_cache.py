
import sys
import os
import math

class MemoriaCache:

    def __init__(self):

        parametros = self.verificar_parametros()
        self.nsets, self.bsize, self.assoc, self.substituicao, self.flag_saida, self.arquivo_entrada = parametros

        size_cache = self.nsets * self.bsize * self.assoc
        self.cache = self.inicializar_cache(size_cache)

        #for i in range(0, size_cache):
        #    print(f"cache[{i}] = {cache[i]}")

        self.n_bits_offset = int(math.log2(self.bsize))
        self.n_bits_index = int(math.log2(self.nsets))
        self.n_bits_tag = 32 - self.n_bits_offset - self.n_bits_index

        self.total_accesses = 0
        self.hits = 0
        self.compulsory_misses = 0
        self.capacity_misses = 0
        self.conflict_misses = 0


    def is_power_of_two(self, x):
        return x > 0 and (x & (x - 1)) == 0

    def verificar_parametros(self):
        if len(sys.argv) != 7:
            print("Uso: cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada>")
            sys.exit(1)

        try:
            nsets = int(sys.argv[1])
            if not self.is_power_of_two(nsets):
                raise ValueError("nsets deve ser uma potência de 2.")

            bsize = int(sys.argv[2])
            if not self.is_power_of_two(bsize):
                raise ValueError("bsize deve ser uma potência de 2.")

            assoc = int(sys.argv[3])
            if not self.is_power_of_two(assoc):
                raise ValueError("assoc deve ser uma potência de 2.")

            substituicao = sys.argv[4]
            if not substituicao in ("R", "F", "L"):
                raise ValueError("substituicao deve ser 'R', 'F' ou 'L'.")

            flag_saida = int(sys.argv[5])
            if flag_saida not in (0, 1):
                raise ValueError("flag_saida deve ser 0 ou 1.")

            arquivo_entrada = sys.argv[6]
            #if not os.path.exists(arquivo_entrada):
            #    raise FileNotFoundError(f"Arquivo '{arquivo_entrada}' não encontrado.")

            print("Tudo OK")
            return nsets, bsize, assoc, substituicao, flag_saida, arquivo_entrada

        except ValueError as e:
            print(f"Erro: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)

    def inicializar_cache(self, size_cache):
        cache = []
        for _ in range(self.nsets):
            conjunto = []
            for _ in range(self.assoc):
                bloco = {"validade": 0, "tag": 0, "data": [] * self.bsize}
                conjunto.append(bloco)
            cache.append(conjunto)
        return cache

    def imprimir_cache(self):
        print("\n=== Estado Atual da Cache ===")
        for i, conjunto in enumerate(self.cache):
            print(f"Conjunto {i}:")
            for j, bloco in enumerate(conjunto):
                validade = "V" if bloco["validade"] else "I"  # V = Válido, I = Inválido
                tag = bloco["tag"] if bloco["tag"] is not None else "None"
                dados = bloco["data"]
                print(f"  Bloco {j}: [Validade: {validade}, Tag: {tag}, Dados: {dados}]")
            print("-" * 40)
    
    def acessar_cache_mapeamento_direto(self, endereco):
        index = (endereco >> self.n_bits_offset) & (2**self.n_bits_index - 1)
        tag = endereco >> (self.n_bits_offset + self.n_bits_index)

        bloco = self.cache[index]
        if bloco["validade"]:
            if bloco["tag"] == tag:
                print(f"Hit! Endereço {endereco} encontrado no bloco {bloco}.")
                #hit
                self.hits += 1
                return
            else:
                print(f"Miss! Endereço {endereco} não encontrado no bloco {bloco}.")
                #miss
                self.conflict_misses += 1
                bloco["validade"] = 1
                bloco["tag"] = tag
                return
        else:
            print(f"Miss! Endereço {endereco} não encontrado no bloco {bloco}.")
            #miss
            self.compulsory_misses += 1
            bloco["validade"] = 1
            bloco["tag"] = tag
            return
        
    def acessar_cache_associativa(self, endereco):
        index = (endereco >> self.n_bits_offset) & (2**self.n_bits_index - 1)
        tag = endereco >> (self.n_bits_offset + self.n_bits_index)

        conjunto = self.cache[index]
        for bloco in conjunto:
            if bloco["validade"] and bloco["tag"] == tag:
                print(f"Hit! Endereço {endereco} encontrado no bloco {bloco}.")
                #hit
                self.hits += 1
                return
                
        #miss, agora descobrir qual tipo de miss:
        for bloco in conjunto:
            if bloco["validade"] == 0:
                print(f"Miss compulsorio Endereço {endereco} não encontrado no bloco {bloco}.")
                #miss
                self.compulsory_misses += 1
                bloco["validade"] = 1
                bloco["tag"] = tag
                return
        
        #sem espaço livre, verifica conflito ou capacidade
        for bloco in conjunto:
            if bloco["tag"] != tag and bloco["validade"]:
                print(f"Miss de Conflito! Substituindo bloco com tag {bloco['tag']} por {tag}.")
                #miss
                self.conflict_misses += 1
                bloco["tag"] = tag
                #talvez limpar o bloco?
                return
            
        print(f"Miss capacidade susbtituir bloco em conjunto {index}.")
        #miss
        self.capacity_misses += 1
        #implementar politica de substituição

    def acessar_cache_totalmente_associativa(self, endereco):
        tag = endereco >> (self.n_bits_offset + self.n_bits_index)

        for bloco in self.cache:
            if bloco["validade"] and bloco["tag"] == tag:
                print(f"Hit! Endereço {endereco} encontrado no bloco {bloco}.")
                #hit
                self.hits += 1
                return
        print(f"Miss! Endereço {endereco} não encontrado no bloco {bloco}.")
        #miss, verificar tipo

        for bloco in self.cache:
            if bloco["validade"] == 0:
                print(f"Miss compulsorio Endereço {endereco} não encontrado no bloco {bloco}.")
                #miss
                self.compulsory_misses += 1
                bloco["validade"] = 1
                bloco["tag"] = tag
                return
        
        #sem espaço livre, só ppode ser capacidade
        print(f"Miss capacidade susbtituir bloco.")
        #miss
        self.capacity_misses += 1
        #implementar politica de substituição