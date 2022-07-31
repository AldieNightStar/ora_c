void s_dump(t_stacky* s) {
	int size = stacky_pop(s);
	if (size < 1) return;
	int buf[size];
	for (int i = 0; i < size; i++) {
		buf[i] = stacky_pop(s);
	}
	for (int i = size-1; i >= 0; i--) {
		stacky_push(s, buf[i]);
		printf("DUMP %d -> %d\n", size-i, buf[i]);
	}
}