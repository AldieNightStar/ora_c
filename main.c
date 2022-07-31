#include <stdlib.h>
#include <stdio.h>
#include "stacky.c"

typedef void (*sfunc)(t_stacky*);

void s_print(t_stacky* s) {
	printf("number %d\n", stacky_pop(s));
}

void main() {
	t_stacky* s = stacky_new(32);
	lbl:
	stacky_push(s, 32);
	s_print(s);
	s_print(s);
	s_print(s);
	s_print(s);
	s_print(s);
	goto lbl;
}