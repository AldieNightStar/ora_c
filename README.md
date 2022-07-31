# Ora - Perfomant language
### Transpiles to `C`

# Usage
```r
use out
use math
use swaps
use debug
use logic

func main
	10000 loop:
		dup 0 eq ?end
		dec
		inner
		dup 1000 mod 0 neq ?next
		dup printn
	next:
		!loop
	end:
		"DONE!" prints

func inner
	10000 loop:
		dup 0 eq ?end
		dec
		!loop
	end:
		drop
```

# Install
* Install `python 3.7+` version
* Install `gcc` compiler (For Windows it's `MinGW`)

# Usage
```sh
# Compile file
python ora.py file.txt out.exe
```

# Syntax
```r
# Line of comment

# Go to label
!label

# Define new label "label"
label:

# Go to label if top element in stack is 1
?label

# Push elements to the stack and then call the command
# In fact it will call `s_command_name(stack)` in c
1 2 3 "string" command_name

# Duplicate last element
# will: 1 2 2
1 2 dup

# Swaps last elements
# will: 3 1 2
3 2 1 swap

# Drop last element
# will: 1 2
1 2 3 drop

# Include std c files
# Will add `s_math.c` from std directory
use math

```

# Writing API
* Go to `std` directory
* Create file `s_your_awesome_library.c`
```c
// Let's say you want to add some math function
// All you need to get value from stack: stacky_pop(s);
// And put some value back:              stacky_push(s, value);
// Supported type is ONLY 'int'
void s_my_add(t_stacky* s) {
	int b = stacky_pop(s);
	int a = stacky_pop(s);
	stacky_push(s, a+b);
}
```
* Then import in your program
```r
use out
use your_awesome_library

# Here are you function is callen
3 2 my_add printn
```