Python, Cython, Rust extension for pandas' vectorized apply function
====================================================================

In pandas, sometimes it's useful to apply a stateful vectorized function.

In this project, I compare pure Python, Cython, Rust-numpy (pyo3).


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

Which suggests Cython is tiny bit faster than pure Python, yet Rust is 9x slower!
