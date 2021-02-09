import numpy as np


class PyTradeFSM:
  long_pos = 0.
  short_pos = 0.

  def __init__(self, price='price', qty='qty',
               should_enter_long='should_enter_long', should_enter_short='should_enter_short',
               should_exit_long='should_exit_long', should_exit_short='should_exit_short'):
    self.price = price
    self.qty = qty
    self.should_enter_long = should_enter_long
    self.should_enter_short = should_enter_short
    self.should_exit_long = should_exit_long
    self.should_exit_short = should_exit_short

  def _trade(self, price, qty, should_enter_long, should_enter_short, should_exit_long, should_exit_short):
    if should_enter_long and self.long_pos == 0.:
      self.long_pos = price * qty
      return self.long_pos, 'enter_long'
    elif should_exit_long and self.long_pos != 0.:
      res = self.long_pos
      self.long_pos = 0.
      return res, 'exit_long'
    elif should_enter_short and self.short_pos == 0.:
      self.short_pos = price * qty
      return self.short_pos, 'enter_short'
    elif should_exit_short and self.short_pos != 0.:
      res = self.short_pos
      self.short_pos = 0.
      return res, 'exit_short'
    else:
      return 0., 'na'

  def trade(self, df):
    self.long_pos = 0.
    self.short_pos = 0.
    v_fun = np.vectorize(self._trade, cache=True)
    trade_val, state_val = v_fun(df[self.price], df[self.qty], df[self.should_enter_long], df[self.should_enter_short], df[self.should_exit_long], df[self.should_exit_short])
    return [trade_val, state_val]

