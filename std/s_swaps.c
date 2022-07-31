void s_swap2(t_stacky* s) {
	int a = stacky_pop(s);
	int b = stacky_pop(s);
	int c = stacky_pop(s);
	stacky_push(s, a);
	stacky_push(s, b);
	stacky_push(s, c);
}

void s_swap3(t_stacky* s) {
	int a = stacky_pop(s);
	int b = stacky_pop(s);
	int c = stacky_pop(s);
	int d = stacky_pop(s);
	stacky_push(s, d);
	stacky_push(s, b);
	stacky_push(s, c);
	stacky_push(s, a);
}

void s_swap4(t_stacky* s) {
	int a = stacky_pop(s);
	int b = stacky_pop(s);
	int c = stacky_pop(s);
	int d = stacky_pop(s);
	int e = stacky_pop(s);
	stacky_push(s, e);
	stacky_push(s, b);
	stacky_push(s, c);
	stacky_push(s, d);
	stacky_push(s, a);
}

void s_swap5(t_stacky* s) {
	int a = stacky_pop(s);
	int b = stacky_pop(s);
	int c = stacky_pop(s);
	int d = stacky_pop(s);
	int e = stacky_pop(s);
	int f = stacky_pop(s);
	stacky_push(s, f);
	stacky_push(s, b);
	stacky_push(s, c);
	stacky_push(s, d);
	stacky_push(s, e);
	stacky_push(s, a);
}

void s_swap6(t_stacky* s) {
	int a = stacky_pop(s);
	int b = stacky_pop(s);
	int c = stacky_pop(s);
	int d = stacky_pop(s);
	int e = stacky_pop(s);
	int f = stacky_pop(s);
	int g = stacky_pop(s);
	stacky_push(s, g);
	stacky_push(s, b);
	stacky_push(s, c);
	stacky_push(s, d);
	stacky_push(s, e);
	stacky_push(s, f);
	stacky_push(s, a);
}