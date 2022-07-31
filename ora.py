#!/bin/env python

from lex import lex, T_STR, T_SPC, T_NUM
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
	subprocess.Popen(["gcc", "-O3", "-I", scriptDirectory+"/std", "-o", outname, outname+".c"]).wait()
	subprocess.Popen(["strip", outname]).wait()

# ==========================================
# Compiler
# ==========================================

C_PUSH = "push"
C_CALL = "call"
C_GOTO = "goto"
C_LABEL = "label"
C_LOGIC_GOTO = "goto?"

def c_lex(src):
	return lex(src)

def c_proc_remove_strings(toks):
	arr = []
	for tok in toks:
		if tok.type == T_STR: continue
		arr.append(tok)
	return arr

def c_proc_make_calls(toks):
	arr = []
	for tok in toks:
		if tok.type == T_NUM:
			arr.append((C_PUSH, int(tok.value)))
		elif tok.type == T_SPC:
			name = tok.value
			if name.endswith(":"):
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
	return arr

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
			if name == None or name.type != T_STR: break
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

	# funcs: {"main": [tokens...]}
	funcs = c_proc_analyze_funcs(toks)

	# Remove string tokens
	for name, toks in funcs.items():
		funcs[name] = c_proc_remove_strings(toks)

	# Make calls and labels from tokens
	for name, toks in funcs.items():
		funcs[name] = c_proc_make_calls(toks)

	return includes, funcs

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
	return g_func(name, "".join(sb))

def c_compile_to_src(includes, funcs):
	sb = []
	for name, toks in funcs.items():
		sb.append(c_compile_func_to_src(name, toks))
	src = "".join(sb)
	sb = []
	sb.append(g_include("stdlib.h"))
	sb.append(g_include("stacky.c"))
	sb.append("// Imports\n")
	for inc in includes:
		sb.append(g_include("s_" + inc + ".c"))
	sb.append("// " + ("="*16) + "\n\n")
	sb.append(src);
	sb.append(g_main("s_main(s);\n"))
	return "".join(sb)

def c_compile(src):
	toks = c_lex(src)
	includes, funcs = c_compile_toks(toks)
	new_src = c_compile_to_src(includes, funcs)
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
	s = "t_stacky* s = stacky_new(8192);"
	return f"void main(){{\n{s}\n{instructions_str}\n}}\n"

def g_push(arg):
	return f"stacky_push(s, {arg});\n"

def g_if_goto(arg):
	sb = []
	sb.append("int exnum = stacky_pop(s); ")
	sb.append(f"if (exnum == 1) goto {arg};\n")
	return "".join(sb)

def g_func(name, inner):
	return f"void s_{name}(t_stacky* s){{\n{inner}}}\n"

# ==========================================
# Main launcher
# ==========================================

if __name__ == "__main__":
	main(sys.argv[1:])