void s_printn(t_stacky* s) {
	printf("%d\n", stacky_pop(s));
}

void s_prints(t_stacky* s) {
	printf("%s\n", stacky_pop_str(s));
}