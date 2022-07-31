void s_add(t_stacky* s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a+b);
}

void s_sub(t_stacky* s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a-b);
}

void s_div(t_stacky* s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a/b);
}

void s_mul(t_stacky* s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a*b);
}

void s_mod(t_stacky* s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a%b);
}

void s_inc(t_stacky* s) {
	stacky_push(s, stacky_pop(s)+1);
}

void s_dec(t_stacky* s) {
	stacky_push(s, stacky_pop(s)-1);
}
