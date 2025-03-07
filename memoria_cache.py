
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
            if not substituicao in ("r", "f", "l"):
                raise ValueError("substituicao deve ser 'r', 'f' ou 'l'.")

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
