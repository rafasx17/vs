#include <stdio.h>

typedef struct {
    float x, y;
} ponto;

void set_x_ponto(ponto *p, float _x) {
    p->x = _x;
}

void set_y_ponto(ponto *p, float _y) {
    p->y = _y;
}

void set_ponto(ponto *p, float _x, float _y) {
    p->x = _x;
    p->y = _y;
}

float getx_ponto(ponto *p) {
    return p->x;
}

float gety_ponto(ponto *p) {
    return p->y;
}

