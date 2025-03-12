
import sys
import os
import math
import random

DEBUG = False

class MemoriaCache:

    def __init__(self):

        parametros = self.verificar_parametros()
        self.nsets, self.bsize, self.assoc, self.substituicao, self.flag_saida, self.arquivo_entrada = parametros

        size_cache = self.nsets * self.bsize * self.assoc
        self.cache = self.inicializar_cache()

        self.n_bits_offset = int(math.log2(self.bsize))
        self.n_bits_index = int(math.log2(self.nsets))
        self.n_bits_tag = 32 - self.n_bits_offset - self.n_bits_index
        
        if DEBUG:        
            print(f"Bits de offset: {self.n_bits_offset}")
            print(f"Bits de índice: {self.n_bits_index}")
            print(f"Bits de tag: {self.n_bits_tag}")
        
        self.total_accesses = 0
        self.hits = 0
        self.compulsory_misses = 0
        self.capacity_misses = 0
        self.conflict_misses = 0
        self.tempo_global = 0

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
            if not os.path.exists(arquivo_entrada):
                raise FileNotFoundError(f"Arquivo '{arquivo_entrada}' não encontrado.")

            #print("Tudo OK")
            return nsets, bsize, assoc, substituicao, flag_saida, arquivo_entrada

        except ValueError as e:
            print(f"Erro: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)

    def inicializar_cache(self, ):
        cache = []

        if self.assoc == 1:  # para mapeamento direto
            for _ in range(self.nsets):
                bloco = {
                    "validade": 0,
                    "tag": 0,
                    "data": [0] * self.bsize
                }
                cache.append(bloco)  # um bloco a cada set

        elif self.nsets == 1:  # totalmente associativa
            for _ in range(self.assoc):
                bloco = {
                    "validade": 0,
                    "tag": 0,
                    "data": [0] * self.bsize,
                    "tempo_insercao": 0,  # para FIFO
                    "tempo_uso": 0        # para LRU
                }
                cache.append(bloco)  # todos os blocos em uma lista
        else:  # associativa por conjunto
            for _ in range(self.nsets):
                conjunto = []
                for _ in range(self.assoc):
                    bloco = {
                        "validade": 0,
                        "tag": 0,
                        "data": [0] * self.bsize,
                        "tempo_insercao": 0,  # para FIFO
                        "tempo_uso": 0        # para LRU
                    }
                    conjunto.append(bloco)
                cache.append(conjunto)  # lista de sets(conjuntos) com os blocos

        return cache
    
    def acessar_cache_mapeamento_direto(self, endereco):
        self.tempo_global += 1
        self.total_accesses += 1

        index = (endereco >> self.n_bits_offset) & (2**self.n_bits_index - 1)
        tag = endereco >> (self.n_bits_offset + self.n_bits_index)
        if DEBUG: 
            print(f"Endereço: {endereco}, Tag: {tag}, Índice: {index}")
            print("----------------------------------------------------------------------")

        bloco = self.cache[index]
        if bloco["validade"]:
            if bloco["tag"] == tag:
                if DEBUG: 
                    print("\n----------------------------------------------------------------------")
                    print(f"Hit!")
                self.hits += 1
                bloco["tempo_uso"] = self.tempo_global
                return
            else:
                if DEBUG: 
                    print("\n----------------------------------------------------------------------")
                    print(f"Miss de Conflito!")
                self.preencher_bloco(bloco, endereco)
                self.conflict_misses += 1
                bloco["validade"] = 1
                bloco["tag"] = tag
                bloco["tempo_insercao"] = self.tempo_global
                bloco["tempo_uso"] = self.tempo_global
                return
        else:
            if DEBUG: 
                print("\n----------------------------------------------------------------------")
                print(f"Miss Compulsório!")
            self.preencher_bloco(bloco, endereco)
            self.compulsory_misses += 1
            bloco["validade"] = 1
            bloco["tag"] = tag
            bloco["tempo_insercao"] = self.tempo_global
            bloco["tempo_uso"] = self.tempo_global
            return
        
    def acessar_cache_associativa(self, endereco):
        self.tempo_global += 1
        self.total_accesses += 1
        index = (endereco >> self.n_bits_offset) & (2**self.n_bits_index - 1)
        tag = endereco >> (self.n_bits_offset + self.n_bits_index)

        conjunto = self.cache[index]
        if DEBUG: 
            print(f"Endereço: {endereco}, Tag: {tag}, Índice: {index}")
            print("----------------------------------------------------------------------")
       
        for bloco in conjunto:
            if bloco["validade"] and bloco["tag"] == tag:
                if DEBUG:
                    print("\n----------------------------------------------------------------------")
                    print(f"Hit! Endereço {endereco} encontrado no bloco {bloco}.")
                self.hits += 1
                bloco["tempo_uso"] = self.tempo_global
                return
                
        #miss, agora descobrir qual tipo de miss:
        for bloco in conjunto:
            if not bloco["validade"]:
                if DEBUG:
                    print("\n----------------------------------------------------------------------")
                    print(f"Miss compulsorio")
                self.preencher_bloco(bloco, endereco)
                self.compulsory_misses += 1
                bloco["validade"] = 1
                bloco["tag"] = tag
                bloco["tempo_uso"] = self.tempo_global
                bloco["tempo_insercao"] = self.tempo_global
                return
        
        #sem espaço livre, verifica conflito ou capacidade
        set_full = all(bloco["validade"] for bloco in conjunto)
        cache_full = all(all(bloco["validade"] for bloco in conj) for conj in self.cache)
        
        if set_full and not cache_full:
            if DEBUG:
                print("\n----------------------------------------------------------------------")
                print(f"Miss de Conflito!")
            self.conflict_misses += 1
        elif cache_full:
            if DEBUG:
                print("\n----------------------------------------------------------------------")
                print(f"Miss de Capacidade!")
            self.capacity_misses += 1
    
        bloco_substituido = self.substituir_bloco(conjunto)
        self.preencher_bloco(bloco_substituido, endereco)
        bloco_substituido["validade"] = 1
        bloco_substituido["tag"] = tag
        bloco_substituido["tempo_uso"] = self.tempo_global
        bloco_substituido["tempo_insercao"] = self.tempo_global    
        return

    def acessar_cache_totalmente_associativa(self, endereco):
        self.tempo_global += 1
        self.total_accesses += 1
        tag = endereco >> self.n_bits_offset

        if DEBUG:
            print("\n----------------------------------------------------------------------")
            print(f"Endereço: {endereco}, Tag: {tag}")
        
        for bloco in self.cache:
            if bloco["validade"] and bloco["tag"] == tag:
                if DEBUG:
                    print("\n----------------------------------------------------------------------")
                    print(f"Hit!")
                self.hits += 1
                bloco["tempo_uso"] = self.tempo_global 
                return

        for bloco in self.cache:
            if bloco["validade"] == 0:
                if DEBUG:
                    print("\n----------------------------------------------------------------------")
                    print("Miss Compulsório")
                self.compulsory_misses += 1
                bloco["validade"] = 1
                bloco["tag"] = tag
                bloco["tempo_uso"] = self.tempo_global
                bloco["tempo_insercao"] = self.tempo_global
                self.preencher_bloco(bloco, endereco)
                return
        if DEBUG:
            print("\n----------------------------------------------------------------------")
            print("Miss Capacidade")
        bloco_substituido = self.substituir_bloco(self.cache) 

        self.capacity_misses += 1
        bloco_substituido["validade"] = 1
        bloco_substituido["tag"] = tag
        bloco_substituido["tempo_insercao"] = self.tempo_global
        bloco_substituido["tempo_uso"] = self.tempo_global
        self.preencher_bloco(bloco_substituido, endereco)
        return

    def substituir_bloco(self, conjunto):
        if self.substituicao == "R":
            bloco_ant = random.choice(conjunto)
        elif self.substituicao == "F": 
            bloco_ant = min(conjunto, key=lambda bloco: bloco["tempo_insercao"])
        elif self.substituicao == "L": 
            bloco_ant = min(conjunto, key=lambda bloco: bloco["tempo_uso"])
        return bloco_ant

    def preencher_bloco(self, bloco, endereco):
        base = int(endereco//self.bsize)
        first = base * self.bsize
        for i in range(self.bsize):
            bloco["data"][i] = first + i
        return