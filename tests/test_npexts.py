import pandas as pd
import numpy as np
from npexts.c_trade_fsm import CTradeFSM
from npexts.py_trade_fsm import PyTradeFSM
# from rust_ext import axpy, mult, TradeFSM


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
) * 100000
df = pd.DataFrame(index=pd.date_range('1/1/2000', periods=len(pd_data), freq='1min'),
                  columns=('price', 'qty', 'should_enter_long', 'should_enter_short', 'should_exit_long', 'should_exit_short'),
                  data=pd_data)

def test_py_trade_fsm():
  py_fsm = PyTradeFSM()
  trade, state = py_fsm.trade(df)
  print(f"py trade = {trade}\nstate = {state}")


def test_c_trade_fsm():
  c_fsm = CTradeFSM()
  trade, state = c_fsm.trade(df)
  print(f"c trade = {trade}\nstate = {state}")


def test_rust_trade_fsm():
  rust_fsm = TradeFSM()
  v_fun = np.vectorize(rust_fsm.row_trade, cache=True)
  trade, state = v_fun(df.price, df.qty, df.should_enter_long, df.should_enter_short, df.should_exit_long, df.should_exit_short)
  print(f"trade = {trade}\nstate = {state}")
