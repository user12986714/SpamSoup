# Endpoint executables
Each classification route must be ended with an endpoint executable,
whose output will be used for display for further polling analysis by
the framework.  

# Output specifiation of classification
An endpoint executable shall output a string with the following format:
```
%c (%Lf)\n
```
where `%c` shall be replaced by a single character that is either `T`
or `F`, with `T` indicating true positive and `F` otherwise; and `%Lf`
shall be replaced by a C99 `long double` type value formated by `printf()`
in the standard library with format specifier `%Lf`, whose absolute value
indicates the confidence of classification, and shall be positive if the
classification is true positive and negative otherwise.

> Note: There is no output specifiation when learning, and the output
when learning is not used for any purpose other than logging.