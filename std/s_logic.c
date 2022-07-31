void s_eq(t_stacky *s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a==b);
}

void s_less(t_stacky *s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a < b);
}

void s_less_eq(t_stacky *s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a <= b);
}

void s_greater(t_stacky *s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a > b);
}

void s_greater_eq(t_stacky *s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a >= b);
}

void s_neq(t_stacky *s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a != b);
}

void s_not(t_stacky *s) {
	stacky_push(s, !stacky_pop(s));
}

void s_and(t_stacky *s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a && b);
}

void s_or(t_stacky *s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a || b);
}