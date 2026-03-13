#include <stdio.h>
typedef struct {
    int dia, mes, ano;
} data;

void set_dia_data(data *d, int dia) {
    d->dia = dia;
}

void set_mes_data(data *d, int mes) {
    d->mes = mes;
}

void set_ano_data(data *d, int ano) {
    d->ano = ano;
}

// Primeira forma de inicializar (acessando direto os membros da struct)
void init_data(data *d, int _d, int _m, int _a) {
    d->dia = _d; 
    d->mes = _m; 
    d->ano = _a;
}

// Segunda forma de inicializar (usando os métodos set que você criou).
// Como a linguagem C não permite "sobrecarga" (duas funções com o mesmo nome), 
// renomeei esta para init_data_v2 para evitar o erro de compilação.
void init_data_v2(data *d, int _d, int _m, int _a) {
    set_dia_data(d, _d);
    set_mes_data(d, _m); // Corrigido: adicionado 'set_'
    set_ano_data(d, _a); // Corrigido: adicionado 'set_'
}

void set_data(data *d, int valor) {
    d->dia = valor / 10000;
    d->mes = (valor % 10000) / 100;
    d->ano = (valor % 100);
    
    // Também poderia ser feito:
    // set_dia_data(d, (valor / 10000));
}

int get_dia_data(data *d) {
    return d->dia;
}

int get_mes_data(data *d) {
    return d->mes;
}

int get_ano_data(data *d) {
    return d->ano;
}
