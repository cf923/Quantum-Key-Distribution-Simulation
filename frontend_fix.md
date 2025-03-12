Problems/bad syntax (pretty much ranked by importance):

6 Quiz has multiple choice questions that only allow one input.

7 Don't use text fields as quiz inputs.

11 Don't do `if x in y` for checking if y is x (`if y==x`).

10 Comments should say why not what.

13 use st.markdown instead of st.write, especially for single variables as it doesn't return the output in separate text.

14 You can use static variables if you don't want a variable to change, e.g. error_bound.

Fixed:

~~1 Don't AI generate the description.~~

~~12 Use LaTeX not UTF-8 for symbols, possibly don't use them at all.~~

~~2 Don't use QKDSim.py. Use the newer, more optimized versions.~~

~~15 don't import in a conditional~~

~~9 Don't import libraries twice.~~

~~3 Import files, don't copy+paste them.~~

~~5 Don't return the results as columns of values. Plot them.~~

~~4 Increase max_value of nbits slider, and max_value of error_trsh slider objects.~~

~~8 Don't import everything form a library to only use it once.~~
