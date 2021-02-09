Python, Cython, Rust extension for pandas' vectorized apply function
====================================================================

In pandas, sometimes it's useful to apply a stateful vectorized function.

In this project, I compare pure Python, Cython, Rust-numpy (pyo3).


To setup
--------
```bash
mkvirtualenv numpy-exts
pip install -r requirements.txt
pip install -e .
poetry install
poetry run maturin develop
```




# rust-numpy example extension

Here, we use [`maturin`][maturin] for building Python wheel and
[`poetry`][poetry] for managing Python dependencies and virtualenvs.
Following commands creates a virtualenv, install Python-side
dependencies, and install the extension to the virtualenv.

```bash
poetry install
poetry run maturin develop
```

Once the extension installed, you can run the extension from
Python REPL started by `poetry run python`:

```python
>>> import numpy as np
>>> import rust_ext
>>> rust_ext.axpy(2.0, np.array([0.0, 1.0]), np.array([2.0, 3.0]))
array([2., 5.])
```

[maturin]: https://github.com/PyO3/maturin
[poetry]: https://python-poetry.org/
