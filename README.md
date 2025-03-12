# Simulador de Cache

Este simulador de cache foi desenvolvido para a cadeira de Arquitetura e Organização de Computadores 2 por Pâmela Braga e Gabriela Aguiar. Ele suporta diferentes tipos de mapeamento de cache e calcula estatísticas como taxa de hit, miss compulsório, miss de capacidade e miss de conflito.

## Configuração de Depuração

No arquivo `memoria_cache.py`, a variável `DEBUG` controla a exibição de mensagens detalhadas:

```python
DEBUG = False  # Para desativar prints (padrão)
DEBUG = True   # Para ativar mensagens detalhadas
```

## Como Executar

Execute o simulador no terminal com o seguinte comando:

```bash
python cache_simulator.py <tamanho_cache> <tamanho_bloco> <associatividade> <politica_substituicao> <flag_saida> <arquivo_entrada>
```

### Exemplo:
```bash
python cache_simulator.py 256 4 1 L 1 bin_100.bin
```

### Parâmetros:
- **tamanho_cache**: Tamanho total da cache em bytes (ex.: 256).
- **tamanho_bloco**: Tamanho de cada bloco em bytes (ex.: 4).
- **associatividade**: Define o tipo de mapeamento
- **politica_substituicao**: Política de substituição:
  - `F` para FIFO (First In, First Out).
  - `L` para LRU (Least Recently Used).
  - `R` para aleatória (Random).
- **flag_saida**: Formato da saída:
  - `0` para um relatório legível com labels.
  - `1` para uma linha de valores separados por vírgula.
- **arquivo_entrada**: Arquivo contendo os endereços a serem simulados (ex.: `bin_100.bin`).

### Arquivos de Teste:
- **bin_100.bin**
- **bin_1000.bin**
- **bin_10000.bin**
- **vortex.in.sem.persons.bin**
