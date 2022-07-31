/* ==============================
	STD LIB FOR STACK
 ============================== */

typedef struct {
	int* data;
	int ptr;
	int max;
} t_stacky;

t_stacky* stacky_new(int size) {
	t_stacky* st = malloc(sizeof(t_stacky));
	st->data = malloc(sizeof(int)*size);
	st->ptr = 0;
	st->max = size;
	return st;
}

void stacky_free(t_stacky* st) {
	free(st->data);
	free(st);
}

int stacky_push(t_stacky* st, int dat) {
	if (st->max <= st->ptr) {
		return 0;
	}
	st->data[st->ptr++] = dat;
	return 1;
}

int stacky_pop(t_stacky* st) {
	if (st->ptr < 1) {
		return 0;
	}
	return st->data[--st->ptr];
}

void s_swap(t_stacky* st) {
	int a = stacky_pop(st);
	int b = stacky_pop(st);
	stacky_push(st, a);
	stacky_push(st, b);
}

void s_dup(t_stacky* st) {
	int a = stacky_pop(st);
	stacky_push(st, a);
	stacky_push(st, a);
}