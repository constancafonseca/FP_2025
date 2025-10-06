# 3.1 Representação e funções das letras
letras_validas = ('A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X','Z')
ordem_scrabble = {letra: i for i, letra in enumerate(letras_validas)}

def cria_conjunto (let,occ):
    if len(let) != len(occ):        
        raise ValueError('cria_conjunto: argumentos inválidos')
    for a in let:                   
        if a not in letras_validas :
            raise ValueError('cria_conjunto: argumentos inválidos')
    for b in occ:                  
        if type(b) != int or b < 0:
            raise ValueError('cria_conjunto: argumentos inválidos')
    dicionario = {}
    for i in range(len(let)):
        dicionario[let[i]] = occ[i]
    return dicionario

def gera_numero_aleatorio(estado):    
    estado ^= ( estado << 13) & 0xFFFFFFFF
    estado ^= ( estado >> 17) & 0xFFFFFFFF
    estado ^= ( estado << 5) & 0xFFFFFFFF
    return estado                                               

def gera_num_indice(estado, i):
    estado = gera_numero_aleatorio(estado)
    n = estado % (i + 1)
    return n, estado

def permuta_letras(letras, estado):
    for i in range(len(letras)-1, -1, -1):
        a, estado = gera_num_indice(estado, i)
        letras[i], letras[a] = letras[a], letras[i]

def baralha_conjunto(conj, estado):
    letras = []
    for letra in conj.keys():          
        letras.extend([letra] * conj[letra])
    permuta_letras(letras, estado)
    return letras

def testa_palavra_padrao(palavra, padrao, conj):
    if type(palavra) != str or type(padrao) != str or type(conj) != dict:
        raise ValueError('testa_palavra_padrao: argumentos inválidos')
    
    if len(palavra) != len(padrao):
        return False
    
    conj_temp = conj.copy()
    for p_char, w_char in zip(padrao, palavra):
        if p_char == '.':
            if w_char not in conj_temp or conj_temp[w_char] == 0:
                return False
            conj_temp[w_char] -= 1
        else:
            if p_char != w_char:
                return False
    return True

# 3.2 Representação e funções do tabuleiro
def cria_tabuleiro():
    tabuleiro = []
    for _ in range(15):
        linha = []
        for j in range(15):
            linha.append('.')
        tabuleiro.append(linha)
    return tabuleiro

def cria_casa(l, c):
    if type(l) != int or type(c) != int or not (0 <= l < 15) or not (0 <= c < 15):
        raise ValueError('cria_casa: argumentos inválidos')
    return (l, c)

def obtem_valor(tab, casa):
    if type(tab) != list or len(tab) != 15 or any(type(linha) != list or len(linha) != 15 for linha in tab):
        raise ValueError('obtem_valor: argumentos inválidos')
    if type(casa) != tuple or len(casa) != 2:
        raise ValueError('obtem_valor: argumentos inválidos')
    l, c = casa
    if type(l) != int or type(c) != int or not (0 <= l < 15) or not (0 <= c < 15):
        raise ValueError('obtem_valor: argumentos inválidos')
    return tab[l][c]

def insere_letra(tab, casa, letra):
    if type(tab) != list or len(tab) != 15 or any(type(linha) != list or len(linha) != 15 for linha in tab):
        raise ValueError('insere_letra: argumentos inválidos')
    if type(casa) != tuple or len(casa) != 2:
        raise ValueError('insere_letra: argumentos inválidos')
    l, c = casa
    if type(l) != int or type(c) != int or not (0 <= l < 15) or not (0 <= c < 15):
        raise ValueError('insere_letra: argumentos inválidos')
    if type(letra) != str or len(letra) != 1 or letra not in letras_validas:
        raise ValueError('insere_letra: argumentos inválidos')
    if tab[l][c] != '.':
        raise ValueError('insere_letra: casa já ocupada')
    tab[l][c] = letra
    return tab

def obtem_sequencia(tab, casa, direcao, tamanho):
    if type(tab) != list or len(tab) != 15 or any(type(linha) != list or len(linha) != 15 for linha in tab):
        raise ValueError('obtem_sequencia: argumentos inválidos')
    if type(casa) != tuple or len(casa) != 2:
        raise ValueError('obtem_sequencia: argumentos inválidos')
    l, c = casa
    l -= 1
    c -= 1
    if type(l) != int or type(c) != int or not (0 <= l < 15) or not (0 <= c < 15):
        raise ValueError('obtem_sequencia: argumentos inválidos')
    if direcao not in ('H', 'V'):
        raise ValueError('obtem_sequencia: argumentos inválidos')
    if type(tamanho) != int or tamanho <= 0 or tamanho > 15:
        raise ValueError('obtem_sequencia: argumentos inválidos')
    
    sequencia = ''
    for i in range(tamanho):
        if direcao == 'H':
            nova_c = c + i
            if nova_c >= 15:
                break
            sequencia += tab[l][nova_c]
        else:  # direcao == 'V'
            nova_l = l + i
            if nova_l >= 15:
                break
            sequencia += tab[nova_l][c]
    return sequencia

def insere_palavra(tab, casa, direcao, palavra):
    if type(tab) != list or len(tab) != 15 or any(type(linha) != list or len(linha) != 15 for linha in tab):
        raise ValueError('insere_palavra: argumentos inválidos')
    if type(casa) != tuple or len(casa) != 2:
        raise ValueError('insere_palavra: argumentos inválidos')
    l, c = casa
    l -= 1
    c -= 1
    if type(l) != int or type(c) != int or not (0 <= l < 15) or not (0 <= c < 15):
        raise ValueError('insere_palavra: argumentos inválidos')
    if direcao not in ('H', 'V'):
        raise ValueError('insere_palavra: argumentos inválidos')
    if type(palavra) != str or any(char not in letras_validas for char in palavra):
        raise ValueError('insere_palavra: argumentos inválidos')
    
    tamanho = len(palavra)
    if direcao == 'H':
        if c + tamanho > 15:
            raise ValueError('insere_palavra: palavra não cabe no tabuleiro')
        for i in range(tamanho):
            if tab[l][c + i] != '.' and tab[l][c + i] != palavra[i]:
                raise ValueError('insere_palavra: conflito com letra existente')
        for i in range(tamanho):
            tab[l][c + i] = palavra[i]
    else:  # direcao == 'V'
        if l + tamanho > 15:
            raise ValueError('insere_palavra: palavra não cabe no tabuleiro')
        for i in range(tamanho):
            if tab[l + i][c] != '.' and tab[l + i][c] != palavra[i]:
                raise ValueError('insere_palavra: conflito com letra existente')
        for i in range(tamanho):
            tab[l + i][c] = palavra[i]
    return tab

def tabuleiro_para_str(tab):
    if type(tab) != list or len(tab) != 15 or any(type(linha) != list or len(linha) != 15 for linha in tab):
        raise ValueError('tabuleiro_para_str: argumento inválido')
    
    header_top = "     " + " ".join("1" if i >= 10 else " " for i in range(1, 16))
    header_bottom = " " * 5 + " ".join(str(i % 10) for i in range(1, 16))
    
    separador = "   +-" + "--" * 15 + "+"
    linhas_str = [header_top, header_bottom, separador]

    for i, linha in enumerate(tab, start=1):
        num_linha = f'{i:2d}'  # 1 a 15 alinhado
        conteudo = ' '.join(linha)
        linhas_str.append(f'{num_linha} | {conteudo} |')

    linhas_str.append(separador)
    return '\n'.join(linhas_str)

# 3.3 Representação e funções do dicionário
def cria_jogador(ordem, pontos, conj_letras):
    if type(ordem) != int or ordem < 0 or ordem > 4:
        raise ValueError('cria_jogador: argumentos inválidos')
    if type(pontos) != int:
        raise ValueError('cria_jogador: argumentos inválidos')
    if type(conj_letras) != dict:
        raise ValueError('cria_jogador: argumentos inválidos')
    for letra, occ in conj_letras.items():
        if letra not in letras_validas or type(occ) != int or occ < 0:
            raise ValueError('cria_jogador: argumentos inválidos')
    
    return {
        'id': ordem,
        'pontos': pontos,
        'letras': conj_letras.copy()
    }

def jogador_para_str(jog):
    if type(jog) != dict:
        raise ValueError('jogador_para_str: argumento inválido')
    ordem, pontos, conj_letras = jog.get('id'), jog.get('pontos'), jog.get('letras')
    if type(ordem) != int or ordem < 0 or ordem > 4:
        raise ValueError('jogador_para_str: argumento inválido')
    if type(pontos) != int:
        raise ValueError('jogador_para_str: argumento inválido')
    if type(conj_letras) != dict:
        raise ValueError('jogador_para_str: argumento inválido')
    for letra, occ in conj_letras.items():
        if letra not in letras_validas or type(occ) != int or occ < 0:
            raise ValueError('jogador_para_str: argumento inválido')
    
    letras_str = ' '.join(letra for letra, occ in sorted(conj_letras.items(), key=lambda x: ordem_scrabble[x[0]]) for _ in range(occ))   
    return f'#{ordem} ({pontos:>3}): {letras_str}'

def distribui_letra(letras, jogador):
    if type(letras) != list or any(type(l) != str or len(l) != 1 or l not in letras_validas for l in letras):
        raise ValueError('distribui_letra: argumentos inválidos')
    if type(jogador) != dict:
        raise ValueError('distribui_letra: argumentos inválidos')
    ordem, pontos, conj_letras = jogador.get('id'), jogador.get('pontos'), jogador.get('letras')
    if type(ordem) != int or ordem < 0 or ordem > 4:
        raise ValueError('distribui_letra: argumentos inválidos')
    if type(pontos) != int:
        raise ValueError('distribui_letra: argumentos inválidos')
    if type(conj_letras) != dict:
        raise ValueError('distribui_letra: argumentos inválidos')
    for letra, occ in conj_letras.items():
        if letra not in letras_validas or type(occ) != int or occ < 0:
            raise ValueError('distribui_letra: argumentos inválidos')   
        
    if not letras:  # lista vazia
        return False
    
    letra = letras.pop()  # retira a última letra
    if letra in jogador['letras']:
        jogador['letras'][letra] += 1
    else:
        jogador['letras'][letra] = 1

    return True

# 3.4 Funções do jogo
def joga_palavra(tab, palavra, casa, direcao, conj_letras, primeira):
    if type(tab) != list or len(tab) != 15 or any(len(linha) != 15 for linha in tab):
        raise ValueError('joga_palavra: tabuleiro inválido')
    if type(palavra) != str or len(palavra) < 2:
        return ()
    if type(casa) != tuple or len(casa) != 2:
        raise ValueError('joga_palavra: casa inválida')
    if direcao not in ('H', 'V'):
        return ()
    if type(conj_letras) != dict:
        raise ValueError('joga_palavra: conjunto de letras inválido')

    l, c = casa
    l -= 1
    c -= 1
    tamanho = len(palavra)

    if direcao == 'H' and c + tamanho > 15:
        return ()
    if direcao == 'V' and l + tamanho > 15:
        return ()

    letras_jogador = conj_letras.copy()
    letras_usadas_temp = []
    intersecta_tabuleiro = False

    for i, letra in enumerate(palavra):
        li, ci = (l, c+i) if direcao=='H' else (l+i, c)
        tab_letra = tab[li][ci]

        if tab_letra == '.':
            if letras_jogador.get(letra, 0) > 0:
                letras_usadas_temp.append(letra)
                letras_jogador[letra] -= 1
            else:
                return ()
        else:
            if tab_letra != letra:
                return ()
            intersecta_tabuleiro = True

    meio_l, meio_c = 7, 7  # casa central 0-based
    if primeira:
        cobre_casa_central = False
        for i in range(tamanho):
            li, ci = (l, c+i) if direcao=='H' else (l+i, c)
            if (li, ci) == (meio_l, meio_c):
                cobre_casa_central = True
                break
        if not cobre_casa_central or len(letras_usadas_temp) < 2:
            return ()
    else:
        if not letras_usadas_temp:
            return ()
        if not intersecta_tabuleiro:
            return ()

    for i, letra in enumerate(palavra):
        li, ci = (l, c+i) if direcao=='H' else (l+i, c)
        tab[li][ci] = letra

    letras_usadas_final = sorted(letras_usadas_temp)
    return tuple(letras_usadas_final)

def processa_jogada(tab, jog, pilha, pontos, primeira):
    if type(tab) != list or len(tab) != 15 or any(len(linha) != 15 for linha in tab):
        raise ValueError('processa_jogada: tabuleiro inválido')
    if type(jog) != dict:
        raise ValueError('processa_jogada: jogador inválido')
    if type(pilha) != list or any(type(l) != str or len(l) != 1 or l not in letras_validas for l in pilha):
        raise ValueError('processa_jogada: pilha inválida')
    if all(valor < 1 for valor in pontos.values()):
        raise ValueError('processa_jogada: pontos inválidos')
    if type(primeira) != bool:
        raise ValueError('processa_jogada: valor de primeira inválido')

    ordem, pontos_jogador, conj_letras = jog.get('id'), jog.get('pontos'), jog.get('letras')
    if type(ordem) != int or ordem < 0 or ordem > 4:
        raise ValueError('processa_jogada: jogador inválido')
    if type(pontos_jogador) != int:
        raise ValueError('processa_jogada: jogador inválido')
    if type(conj_letras) != dict:
        raise ValueError('processa_jogada: jogador inválido')
    for letra, occ in conj_letras.items():
        if letra not in letras_validas or type(occ) != int or occ < 0:
            raise ValueError('processa_jogada: jogador inválido')

    while True:
        jogada = input(f"Jogada J{jog['id']}: ").strip().upper()
        if jogada == 'P':
            return False

        elif jogada.startswith('T '):
            letras_troca = jogada[2:].split()
            conj = jog['letras']
            if all(letras_troca.count(l) <= conj.get(l,0) for l in letras_troca):
                for l in letras_troca:
                    conj[l] -= 1
                    if conj[l] == 0:
                        del conj[l]
                for l in letras_troca:
                    if pilha:
                        nova = pilha.pop()
                        conj[nova] = conj.get(nova,0) + 1
                return True

        elif jogada.startswith('J '):
            partes = jogada.split()
            if len(partes) != 5:
                continue
            _, linha, col, direcao, palavra = partes
            try:
                linha = int(linha)
                col = int(col)
            except:
                continue

            usadas = joga_palavra(tab, palavra, (linha,col), direcao, jog['letras'], primeira)
            if usadas:
                pontos_palavra = 0
                for i, letra in enumerate(palavra):
                    li, ci = (linha-1, col-1+i) if direcao=='H' else (linha-1+i, col-1)
                    pontos_palavra += pontos[letra]

                jog['pontos'] += pontos_palavra

                for l in usadas:
                    jog['letras'][l] -= 1
                    if jog['letras'][l] == 0:
                        del jog['letras'][l]
                for _ in usadas:
                    if pilha:
                        nova = pilha.pop()
                        jog['letras'][nova] = jog['letras'].get(nova,0)+1
                return True

def scrabble(num_jogadores, saco, pontos, seed):
    if type(num_jogadores) != int or not (2 <= num_jogadores <= 4):
        raise ValueError('scrabble: argumentos inválidos')

    # Validar saco
    if type(saco) != dict:
        raise ValueError('scrabble: argumentos inválidos')
    for letra, occ in saco.items():
        if letra not in letras_validas or type(occ) != int or occ < 0:
            raise ValueError('scrabble: argumentos inválidos')

    # Validar pontos
    if type(pontos) != dict:
        raise ValueError('scrabble: argumentos inválidos')
    for letra, val in pontos.items():
        if letra not in letras_validas or type(val) != int or val < 1:
            raise ValueError('scrabble: argumentos inválidos')
    
    for letra in saco:
        if letra not in pontos:
            raise ValueError('scrabble: argumentos inválidos')
    # Inicializações
    if type(seed) != int or seed < 0:
        raise ValueError('scrabble: argumentos inválidos')

    print("Bem-vindo ao SCRABBLE.")
    tab = cria_tabuleiro()
    pilha = baralha_conjunto(saco, seed)
    primeira = True

    # Criar jogadores
    jogadores = [cria_jogador(i+1, 0, {}) for i in range(num_jogadores)]

    # Distribui 7 letras
    for jog in jogadores:
        for _ in range(7):
            distribui_letra(pilha, jog)

    while True:
        for jog in jogadores:
            print(tabuleiro_para_str(tab))
            for j in jogadores:
                print(jogador_para_str(j))
            
            jogou = processa_jogada(tab, jog, pilha, pontos, primeira)
            
            if primeira and jogou:
                primeira = False

            if jogou:
                passadas_consecutivas = 0
            else:
                passadas_consecutivas += 1

            if all(v == 0 for v in jog['letras'].values()) and not pilha:
                pontos = tuple(j["pontos"] for j in jogadores)
                return pontos

            if passadas_consecutivas >= num_jogadores:
                pontos = tuple(j["pontos"] for j in jogadores)
                return pontos
