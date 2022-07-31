/* ==============================
	STD LIB FOR STACK
 ============================== */

#define __std_def_size 8192

char* __std_str_get(int id);

typedef struct {
	int ptr;
	int max;
	int* data;
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

int stacky_push_str(t_stacky* st, char* str) {
	return stacky_push(st, __std_reg_str(str));
}

int stacky_pop(t_stacky* st) {
	if (st->ptr < 1) {
		return 0;
	}
	return st->data[--st->ptr];
}

char* stacky_pop_str(t_stacky* st) {
	int id = stacky_pop(st);
	return __std_str_get(id);
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

void s_drop(t_stacky* st) {
	stacky_pop(st);
}

// ========= STRINGS (INT) ============

char** __std_strings;
int __std_strings_ptr = 0;

void __std_init_strings() {
	__std_strings = malloc(sizeof(char*) * __std_def_size);
}

int __std_reg_str(char* str) {
	__std_strings[__std_strings_ptr] = str;
	return __std_strings_ptr++;
}

char* __std_str_get(int id) {
	if (id < 0 || id >= __std_def_size) return "{STRING_OUT_RANGE}";
	return __std_strings[id];
}