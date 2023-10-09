import xlsxwriter
import io

def Excel (extrato, list_words, infos):

    def Mes (mes) :
        match(mes):
            case '01' : return 'Jan '
            case '02' : return 'Fev '
            case '03' : return 'Mar '
            case '04' : return 'Abr '
            case '05' : return 'Mai '
            case '06' : return 'Jun '
            case '07' : return 'Jul '
            case '08' : return 'Ago '
            case '09' : return 'Set '
            case '10' : return 'Out '
            case '11' : return 'Nov '
            case '12' : return 'Dez '
        
    dados = {}
    firstYear = int(extrato[0]['data'][6:])
    lastYear = int(extrato[-1]['data'][6:])
    qtdAnos = lastYear - firstYear  + 1
    for i in range(len(list_words)):
        anos = {}
        for j in range(qtdAnos):
            anos[str(firstYear + j)] = {
                    "01": 0.00,
                    "02": 0.00,
                    "03": 0.00,
                    "04": 0.00,
                    "05": 0.00,
                    "06": 0.00,
                    "07": 0.00,
                    "08": 0.00,
                    "09": 0.00,
                    "10": 0.00,
                    "11": 0.00,
                    "12": 0.00
                }
        dados[list_words[i].lower()] = [anos]

    for item in extrato:
        nome = item['nome']
        ano = item['data'][6:]
        mes = item['data'][3:5]
        valor = item['valor']
        dados[nome][0][ano][mes] += valor

    excel_file = io.BytesIO()

    workbook = xlsxwriter.Workbook(excel_file)
    
    worksheet = workbook.add_worksheet()
    
    row = 0
    col = 0

    for value in infos.values():
        worksheet.write(row, col, value)
        row += 1

    row += 1

    for i, (nome, anos) in enumerate(dados.items()): # Quantidade de palavras filtro
        worksheet.merge_range(row,col,row,(2*qtdAnos)-1,nome)
        row += 1
        for c,(ano,meses) in enumerate(anos[0].items()): # Quantidade de anos
            worksheet.merge_range(row,col + (c*2),row,col + 1 + (c*2), ano)
            total = 0
            for r,(mes,valor) in enumerate(meses.items()): # Quantidade de meses
                worksheet.write(row + 1 + r, col + (c*2), Mes(mes))
                worksheet.write(row + 1 + r, col + 1 + (c*2), valor)
                total += valor
                if (mes == '12'): 
                    worksheet.write(row + 2 + r, col + (c*2), 'Total')
                    worksheet.write(row + 2 + r, col + 1 + (c*2), total)
        row += 15


    workbook.close()

    return excel_file.getvalue()
