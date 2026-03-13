#condicoes simples e compostas, if, else, elif

n1 = float(input('digite a primeira nota: '))
n2 = float(input('digite a segunda nota: '))
m = (n1 + n2)/2
print('sua media foi {:.1f})'.format(m))
if m >= 6.0:
    print('sua media foi boa')
else:
    print('sua media foi ruim')
