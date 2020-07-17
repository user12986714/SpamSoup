# Executable types (and their contract)
As this project is intended to be a mix of machine learning algorithms
rather than a specific one, there can be many executables with different
input/output contracts and different functionalities, chained together
to form complete classification routes.  
These executables are grouped into types by their contracts.

> Note: Any executable should assume and provide output
under `utf-8` encoding.

# Type 0
Type 0 executables are stateless; for a given input, they will *always*
generate same outputs. They are usually vectorizers turning list of
phrases into list of unsigned integers more suitable for classification;
however, it is entirely possible to have a type 0 executable whom itself
is a complete classification route.  
Type 0 executables take no command line argument, receives input from
`stdin` and will be signaled `EOF` when input ends; they output through
`stdout` and shall exit when output ends.

# Type 1
Type 1 executables are usually one-pass learning algorithms; they
receive 2 command line arguments - the first is a single character
indicating whether the input is true positive, `T`; false positive,
`F`; or undecided and needs classification, any other character;
the second is a string indicating an absolute or relative path to
a file that should be used as the place of state data storage. The file
can be directly accessed with `fopen` by the provided path, with no
processing of path needed, regardless the path is absolute or relative.  
Type 1 executables receives input from` stdin` and will be signaled `EOF`
when input ends; they output through `stdout` and shall exit when
output ends.

# Type 2
Type 2 executables are usually two-pass learning algorithms; they
receive 2 command line arguments, similar to that of type 1. The
difference is that the first argument now not only indicates the class
the input belongs to, but also indicates the stage of learning.  
If the argument is `t` or `f`, it indicates that this is the first
pass of learning; `t` indicates true positive and `f` indicates
false positive. The executable should output exactly `LEARN\n`
if it decides to move on to the second pass, or output any other strings,
including empty ones, otherwise.  
If the argument is `T` or `F`, it indicates that this is the second
pass of learning; this will only occur if the executable decided to
learn in the first pass. `T` indicates true positive and `F` indicates
false positive.  
If the argument is any other character, the class the input belongs to
is undecided and needs classification by the executable.  
Type 1 executables receives input from` stdin` and will be signaled `EOF`
when input ends; they output through `stdout` and shall exit when
output ends.
