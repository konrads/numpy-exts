Python, Cython, Rust extension for pandas vectorized apply()
============================================================

In pandas, sometimes it's useful to apply a stateful vectorized function. Example of such is a trade simulator that chooses to enter/exit long/short position based on a pandas DF.

In this project, I compare implementations of pure Python, Cython, Rust-numpy (pyo3).


To setup
--------
```bash
mkvirtualenv numpy-exts
pip install -r requirements.txt
python ./setup.py develop
# NOTE, following doesn't seem to work for required extensions: pip install -e .
```

To run comparisons
------------------
```bash
pytest -s  # for verbose, to see exec times
```
 
Expected output:
```
tests/test_npexts.py .
py trade = [10. 10.  0. ... 10.  0.  0.]
   state = ['enter_long' 'exit_long' 'noop' ... 'enter_long' 'noop' 'noop']
   avg_exec_time = 0.09
.
c trade = [10. 10.  0. ... 10.  0.  0.]
  state = ['enter_long' 'exit_long' 'noop' ... 'enter_long' 'noop' 'noop']
  avg_exec_time = 0.08
.
rust trade = [10. 10.  0. ... 10.  0.  0.]
     state = ['enter_long' 'exit_long' 'noop' ... 'enter_long' 'noop' 'noop']
     avg_exec_time = 0.73
```

This suggests Cython is slightly faster pure Python, but Rust is ~10x slower!  Surprising, needs an investigation... 
