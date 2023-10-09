import PyPDF2
import re

def Extrato(pdf_file, words_filter):
        
    phrase_filter = ''

    for i, item in enumerate(words_filter):
        word_value = item['word'].lower()
        if (i == len(words_filter)-1) : 
            phrase_filter = phrase_filter + ' ' + word_value + ' '
        else : 
            phrase_filter = phrase_filter +  ' ' + word_value + ' |'

    reader = PyPDF2.PdfReader(pdf_file)
    number_of_pages = len(reader.pages)

    # Eu recebo as palavras para filtrar e coloco numa string separadas por |

    text = []

    for i in range(number_of_pages):
        page = reader.pages[i]
        subtext = page.extract_text()
        subtext = subtext.replace("\n", " ")
        subtext = subtext.lower()
        padrao = re.compile('[ ]+')
        subtext = re.sub(padrao, ' ', subtext)
        text.append(subtext)

    # Jogo as paginas do pdf em uma array

    def nome (n):
        array = n.split(" ")
        array.pop(0)
        array.pop(-1)
        return (' '.join(array)).title()

    padrao = re.compile(r'^[a-z]+\s|nome:[a-z\s]+extrato|agência: [\d]+|conta: [\d-]+')
    banco = re.findall(padrao,text[0])

    perfil = {
        'banco': banco[0].title(),
        'nome': nome(banco[1]),
        'agencia': banco[2],
        'conta': banco[3]
    }

    # Separo as informaçoes do cliente

    for i in range(number_of_pages):
        padrao = re.compile('bradesco[\s\w\W]+saldo \(r\$\)')
        titulo = re.findall(padrao, text[i])
        text[i] = text[i].replace(titulo[0], '')

    texto = ''

    for txt in text:
        texto = texto + txt

    # Junto todas as paginas em uma so string

    padrao = re.compile('\d{2}/\d{2}/\d{4}')

    for data in re.finditer(padrao, texto):
        index = data.span()[0]
        texto = texto[:index-1] + '\n' + texto[index:]

    texto = texto.split('\n')

    # coloco \n antes de todas as datas e separo em uma array começando por elas

    padrao = re.compile('[a-z][0-9]|[0-9][a-z]')

    for i, txt in enumerate(texto):
        for j, x in enumerate(re.finditer(padrao, txt)):
            sep = x.group()[0]+' '+x.group()[1]
            posicao = x.span()[0] + j
            texto[i] = texto[i][:posicao] + sep + texto[i][posicao+2:]

    # Separo a letras e numeros que estao grudados

    filtro = []

    padrao = re.compile(phrase_filter)

    for txt in texto:
        tamanho = re.findall(padrao, txt)
        if (len(tamanho) > 0):
            filtro.append(txt)

    # Aplico as palavras filtro 

    filtro2 = []

    for txt in filtro:
        padraoData = re.compile(r'\d{2}/\d{2}/\d{4}')
        padrao = re.compile(r'\s?[a-z][0-9a-z\s\.]+[a-z0-9] [0-9]+ [0-9.,-]+ [0-9.,-]+\s?')
        data = re.findall(padraoData, txt)
        teste = re.findall(padrao, txt)
        for i in range(len(teste)):
            if (teste[i][0] == ' ') : filtro2.append(data[0]+teste[i])
            else : filtro2.append(data[0]+' '+teste[i])

    # Separo quem tiver mais de 1 historico no mesmo elemento

    filtro = []

    padrao = re.compile(phrase_filter)
    for txt in filtro2:
        tamanho = re.findall(padrao, txt)
        if (len(tamanho) > 0):
            filtro.append(txt)

    # Aplico mais uma vez as palavras filtro

    extrato = []
    nomes = []

    for item in filtro:
        padrao = re.compile(r'\d{2}/\d{2}/\d{4}|[a-z][a-z\s\.]+[a-z]|-[0-9.,]+\s')
        teste = re.findall(padrao, item)
        extrato.append({ 
            "nome": teste[1],
            "data": teste[0], 
            "valor": float(teste[2][1:].replace('.', '').replace(',', '.'))
        })
        nomes.append(teste[1])
    
    list_words = list(set(nomes))
        
    # Crio a array com [dia, historico, valor] para cada elemento restante

    return extrato, list_words, perfil
