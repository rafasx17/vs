n1 = int(input('Digite um número inteiro: '))
n2 = int(input('digite outro número inteiro: '))
s = n1 + n2
print('A soma entre {} e {} é igual a {}'.format(n1, n2, s))
# Este código solicita ao usuário que insira dois números inteiros, calcula a soma desses números e exibe o resultado. No entanto, há um erro na última linha. A função `format` deve ser chamada diretamente na string, e não após a função `print`. A correção seria: