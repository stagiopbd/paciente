import numpy as np


def calc_imc(peso, altura):
    imc = np.divide(peso, np.power(altura, 2))

    if imc < 18.5:
        imc_classe = "Abaixo do peso"
    elif imc < 25:
        imc_classe = "Peso ideal (parabéns)"
    elif imc < 30:
        imc_classe = "Levemente acima do peso"
    elif imc < 35:
        imc_classe = "Obesidade Grau I"
    elif imc < 40:
        imc_classe = "Obesidade Grau II (severa)"
    else:
        imc_classe = "Obesidade Grau III (mórbida)"
    return imc_classe
