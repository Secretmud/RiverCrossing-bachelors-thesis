#include <math.h>
#include <stdio.h>
#include <time.h>


float S(float x);
float trapez(float (*f)(float), float a, float b, int slices);
float midpoint(float (*f)(float), float a, float b, int slices);
float T1(float x);

int a = 0;
int D = 20;
int N = 1e6;
float v = 1, smax = 0.9;


int main(int argc, char **argv) {
    printf("Midpoint:\n");

    clock_t start = clock();
    float ans = midpoint(T1, a, D, N);
    printf("\tAlg time> %.8f\n", (clock() - start)/1e6);
    printf("%.8f seconds\n", ans);

    printf("\n\nTrapez:\n");
    start = clock();
    ans = trapez(T1, a, D, N);
    printf("\tAlg time> %.8f\n", (clock() - start)/1e6);
    printf("%.8f seconds\n", ans);
    return 0;
}

float S(float x) {
    float col = smax*exp(-pow(pow(x, 1.2)-D/1.5, 4)/200);
    return col;
}

float T1(float x) {
    float sum = 1/sqrt(pow(v, 2) - pow(S(x), 2));
    return sum;
}

float trapez(float (*f)(float), float a, float b, int slices) {
    float h = fabs((b - a) / slices);
    float sum = .0f;
    sum +=  (*f)(a)/2;
    for (int i = 1; i < slices; i++)
        sum += (*f)(a + i*h);
    sum +=  (*f)(b)/2;
    return sum*h;
}

float midpoint(float (*f)(float), float a, float b, int slices) {
    float h = fabs((b - a) / slices);
    float sum = .0;
    float x[slices];
    float start = a + h/2;
    for (int i = 0; i < slices; i++)
        x[i] = start + i*h;
    for (int i = 0; i < slices; i++)
        sum += (*f)(x[i]);
    return sum*h;
}