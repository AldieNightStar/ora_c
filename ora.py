#!/bin/env python

from lex import lex, T_STR, T_SPC, T_NUM, Token
import os
import sys
import subprocess

scriptDirectory = os.path.dirname(os.path.realpath(__file__))

def main(args):
	if len(args) < 2:
		print("usage: ora.py [name] [out]")
		print("\t[name] is a name of source file")
		print("\t[out] is a name out program (no extension)")
		return
	inname = args[0]
	outname = args[1]
	with open(inname) as f:
		src = c_compile(f.read())
		with open(outname + ".c", 'w') as o:
			o.write(src)
	subprocess.Popen(["gcc", "-w", "-O3", "-I", scriptDirectory+"/std", "-o", outname, outname+".c"]).wait()
	subprocess.Popen(["strip", outname]).wait()

# ==========================================
# Compiler
# ==========================================

C_PUSH = "push"
C_PUSH_STRING = "pushs"
C_CALL = "call"
C_GOTO = "goto"
C_LABEL = "label"
C_LOGIC_GOTO = "goto?"
C_RETURN = "ret"

def c_lex(src):
	return lex(src)

def c_proc_make_calls(toks):
	arr = []
	for tok in toks:
		if tok.type == T_NUM:
			arr.append((C_PUSH, int(tok.value)))
		elif tok.type == T_SPC:
			name = tok.value
			if name == "ret":
				arr.append((C_RETURN, 0))
			elif name.endswith(":"):
				name = name[0:-1]
				arr.append((C_LABEL, name))
			elif name.startswith("!"):
				name = name[1:]
				arr.append((C_GOTO, name))
			elif name.startswith("?"):
				name = name[1:]
				arr.append((C_LOGIC_GOTO, name))
			else:
				arr.append((C_CALL, tok.value))
		elif tok.type == T_STR:
			arr.append((C_PUSH_STRING, tok.value))
	return arr

def c_proc_analyze_string_pool(toks):
	strings = []
	arr = []
	for tok in toks:
		if tok.type == T_STR:
			if tok.value in strings:
				arr.append(Token(T_NUM, strings.index(tok.value), 0))
			else:
				strings.append(tok.value)
				arr.append(Token(T_NUM, len(strings)-1, 0))
			continue
		arr.append(tok)
	return arr, strings

def c_proc_analyze_includes(toks):
	it = iter(toks)
	arr = []
	incs = []
	while True:
		tok = next(it, None)
		if tok == None:
			break
		if tok.type == T_SPC and tok.value == "use":
			name = next(it, None)
			if name == None or name.type != T_SPC: break
			name = name.value
			incs.append(name)
			continue
		arr.append(tok)
	return arr, incs

def c_proc_analyze_funcs(toks):
	it = iter(toks)
	funcs = {}
	arr = []
	curname = "main"
	for tok in it:
		# func name ret
		if tok.type == T_SPC and tok.value == "func":
			name = next(it, None)
			if name == None or name.type != T_SPC: break
			name = name.value
			if len(arr) > 1:
				funcs[curname] = arr
			arr = []
			curname = name
			continue
		arr.append(tok)
	if len(arr) > 1:
		funcs[curname] = arr
	return funcs

def c_compile_toks(toks):
	"Processing logic. Returns tokens, includes"

	# Import c files
	toks, includes = c_proc_analyze_includes(toks)

	toks, stringpool = c_proc_analyze_string_pool(toks)

	# funcs: {"main": [tokens...]}
	funcs = c_proc_analyze_funcs(toks)

	# Make calls and labels from tokens
	for name, toks in funcs.items():
		funcs[name] = c_proc_make_calls(toks)

	return includes, funcs, stringpool

def c_compile_func_to_src(name, toks):
	sb = []
	for tok in toks:
		if type(tok) != tuple or len(tok) < 2:
			continue
		tp, arg = tok
		if tp == C_CALL:
			sb.append(g_call(arg))
			continue
		elif tp == C_PUSH:
			sb.append(g_push(arg))
			continue
		elif tp == C_GOTO:
			sb.append(g_goto(arg))
			continue
		elif tp == C_LOGIC_GOTO:
			sb.append(g_if_goto(arg))
			continue
		elif tp == C_LABEL:
			sb.append(g_label(arg))
			continue
		elif tp == C_PUSH_STRING:
			sb.append(g_push_string(arg))
			continue
		elif tp == C_RETURN:
			sb.append("return;\n")
			continue
	return g_func(name, "".join(sb))

def c_compile_to_src(includes, funcs, stringpool):
	sb = []
	for name, toks in funcs.items():
		sb.append(c_compile_func_to_src(name, toks))
	src = "".join(sb)
	sb = []
	sb.append(g_include("stdlib.h"))
	sb.append(g_include("__std.c"))
	for inc in includes:
		sb.append(g_include("s_" + inc + ".c"))
	sb.append("\n")
	sb.append(src);

	strings_sb = []
	for id in range(len(stringpool)):
		strings_sb.append(g_set_string(id, stringpool[id]))
	strings_pool_register = ''.join(strings_sb)

	sb.append(g_main(f"__std_init_strings({len(stringpool)});\n{strings_pool_register}\ns_main(s);"))
	return "".join(sb)

def c_compile(src):
	toks = c_lex(src)
	includes, funcs, stringpool = c_compile_toks(toks)
	new_src = c_compile_to_src(includes, funcs, stringpool)
	return new_src


# ==========================================
# File generator
# ==========================================

g_callback_def = "typedef void (*sfunc)(t_stacky*);\n"

def g_include(name):
	return f"#include <{name}>\n"

def g_call(name):
	return f"s_{name}(s);\n"

def g_label(name):
	return f"{name}:\n"

def g_goto(name):
	return f"goto {name};\n"

def g_main(instructions_str):
	s1 = "t_stacky* s = stacky_new(8192);\n"
	inner = g_tab(f"{s1}{instructions_str}")
	return f"void main(){{\n{inner}\n}}\n"

def g_push(arg):
	return f"stacky_push(s, {arg});\n"

def g_if_goto(arg):
	return f"if (stacky_pop(s) == 1) goto {arg};\n"

def g_func(name, inner):
	return f"void s_{name}(t_stacky* s){{\n{g_tab(inner)}}}\n"

def g_push_string(arg):
	return f"stacky_push_str(s, \"{g_esc_string(arg)}\");\n"

def g_esc_string(s):
	return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\0", "\\0").replace("\"", "\\\"")

def g_set_string(id, str):
	return f"__std_str_set({id}, \"{g_esc_string(str)}\");\n"

def g_tab(str):
	arr = str.split("\n")
	arr2 = []
	for a in arr:
		s = a.strip()
		if len(s) < 1:
			arr2.append(s)
			continue
		arr2.append("\t" + s)
	return "\n".join(arr2)

# ==========================================
# Main launcher
# ==========================================

if __name__ == "__main__":
	main(sys.argv[1:])