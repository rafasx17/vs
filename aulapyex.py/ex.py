# comprimento de cateto oposto e adjacente de um triangulo retangulo, calcular  o comprimento da hipotenusa
import math 
co = float(input('digite o comprimento do cateto oposto: '))
ca = float(input('digite o comprimento do cateto adjacente: '))
hip = math.hypot(co, ca) # calcula a hipotenusa usando o teorema de pitagoras
print('a hipotenusa vai medir {:.2f}'.format(hip))
