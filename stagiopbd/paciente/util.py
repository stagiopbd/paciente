

def formatar_paciente_model(item):
    return {
        'cpf': item.cpf,
        'nome_completo': item.nome_completo,
        'data_nascimento': item.data_nascimento.strftime(
            '%d/%m/%Y'),
        'sexo': item.sexo,
        'tipo_sanguineo': item.tipo_sanguineo,
        'inativo': item.inativo
    }


def formatar_paciente_dict(item):
    return {
        'cpf': item['cpf'],
        'nome_completo': item['nome_completo'],
        'data_nascimento': item['data_nascimento'].strftime(
            '%d/%m/%Y'),
        'sexo': item['sexo'],
        'tipo_sanguineo': item['tipo_sanguineo'],
        'inativo': item['inativo']
    }
