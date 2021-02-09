import numpy as np

cdef char* NOOP = 'noop'
cdef char* ENTER_LONG = 'enter_long'
cdef char* ENTER_SHORT = 'enter_short'
cdef char* EXIT_LONG = 'exit_long'
cdef char* EXIT_SHORT = 'exit_short'


cdef class CTradeFSM(object):
  cdef double long_pos, short_pos
  cdef str price_col, qty_col, should_enter_long_col, should_enter_short_col, should_exit_long_col, should_exit_short_col

  def __cinit__(self, str price_col='price', str qty_col='qty',
                str should_enter_long_col='should_enter_long', str should_enter_short_col='should_enter_short',
                str should_exit_long_col='should_exit_long', str should_exit_short_col='should_exit_short'):
    self.long_pos = 0.
    self.short_pos = 0.
    self.price_col = price_col
    self.qty_col = qty_col
    self.should_enter_long_col = should_enter_long_col
    self.should_enter_short_col = should_enter_short_col
    self.should_exit_long_col = should_exit_long_col
    self.should_exit_short_col = should_exit_short_col

  cpdef (double, char*) _trade(self, double price, double qty, double should_enter_long, double should_enter_short, double should_exit_long, double should_exit_short):
    if should_enter_long and self.long_pos == 0.:
      self.long_pos = price * qty
      return self.long_pos, ENTER_LONG
    elif should_exit_long and self.long_pos != 0.:
      res = self.long_pos
      self.long_pos = 0.
      return res, EXIT_LONG
    elif should_enter_short and self.short_pos == 0.:
      self.short_pos = price * qty
      return self.short_pos, ENTER_SHORT
    elif should_exit_short and self.short_pos != 0.:
      res = self.short_pos
      self.short_pos = 0.
      return res, EXIT_SHORT
    else:
      return 0., NOOP

  # not the most efficient...
  cpdef trade(self, df):
    v_fun = np.vectorize(self._trade, cache=True)
    trade_val, state_val = v_fun(df[self.price_col], df[self.qty_col], df[self.should_enter_long_col], df[self.should_enter_short_col], df[self.should_exit_long_col], df[self.should_exit_short_col])
    return (trade_val, state_val)
