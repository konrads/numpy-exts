import pandas as pd
import numpy as np
from npexts.c_trade_fsm import CTradeFSM
from npexts.py_trade_fsm import PyTradeFSM
from npexts.rust_trade_fsm import RustTradeFSM
import timeit


def gen_df(n):
  pd_data = (
    (10., 1., True, False, False, False),
    (15., 1., False, False, True, False),
    (10., 1., False, False, False, False),
    (10., 1., False, False, False, False),
    (10., 1., False, False, True, True),
    (20., 1., False, True, False, False),
    (10., 1., False, False, True, True),
    (10., 1., True, False, False, False),
    (10., 1., True, False, False, False),
    (10., 1., True, False, False, False),
  ) * n
  df = pd.DataFrame(index=pd.date_range('1/1/2000', periods=len(pd_data), freq='1min'),
                    columns=('price', 'qty', 'should_enter_long', 'should_enter_short', 'should_exit_long', 'should_exit_short'),
                    data=pd_data)
  return df

def test_compare_all():
  df = gen_df(100)
  py_fsm = PyTradeFSM()
  py_trade, py_state = py_fsm.trade(df)

  c_fsm = CTradeFSM()
  c_trade, c_state = c_fsm.trade(df)
  # FIXME: getting back bytes not str...
  c_state = np.array([x.decode('utf-8') for x in c_state])

  rust_fsm = RustTradeFSM()
  rust_v_fun = np.vectorize(rust_fsm.row_trade, cache=True)
  rust_trade, rust_state = rust_v_fun(df.price, df.qty, df.should_enter_long, df.should_enter_short, df.should_exit_long, df.should_exit_short)

  assert(py_trade.tolist() == c_trade.tolist())
  assert(c_trade.tolist() == rust_trade.tolist())
  assert(py_state.tolist() == c_state.tolist())
  assert(c_state.tolist() == rust_state.tolist())


def test_py_trade_fsm():
  df = gen_df(1000)
  py_fsm = PyTradeFSM()
  trade, state = py_fsm.trade(df)
  avg_exec_time = timeit.timeit(lambda: py_fsm.trade(df), number=10)
  print(f"\npy trade = {trade}\n   state = {state}\n   avg_exec_time = {avg_exec_time:.2f}")


def test_c_trade_fsm():
  df = gen_df(1000)
  c_fsm = CTradeFSM()
  trade, state = c_fsm.trade(df)
  # FIXME: getting back bytes not str...
  state = np.array([x.decode('utf-8') for x in state])
  avg_exec_time = timeit.timeit(lambda: c_fsm.trade(df), number=10)
  print(f"\nc trade = {trade}\n  state = {state}\n  avg_exec_time = {avg_exec_time:.2f}")


def test_rust_trade_fsm():
  df = gen_df(1000)
  rust_fsm = RustTradeFSM()
  v_fun = np.vectorize(rust_fsm.row_trade, cache=True)
  trade, state = v_fun(df.price, df.qty, df.should_enter_long, df.should_enter_short, df.should_exit_long, df.should_exit_short)
  avg_exec_time = timeit.timeit(lambda: v_fun(df.price, df.qty, df.should_enter_long, df.should_enter_short, df.should_exit_long, df.should_exit_short), number=10)
  print(f"\nrust trade = {trade}\n     state = {state}\n     avg_exec_time = {avg_exec_time:.2f}")
