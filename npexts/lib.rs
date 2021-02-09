use pyo3::prelude::{pyclass, pymodule, pymethods, PyModule, PyResult, Python};
use std::os::raw::c_uchar;


#[pyclass]
struct RustTradeFSM {
  long_pos: f64,
  short_pos: f64,
}

#[pymethods]
impl RustTradeFSM {
  #[new]
  fn new() -> Self {
    RustTradeFSM {
      long_pos: 0.0,
      short_pos: 0.0,
    }
  }

  fn row_trade(&mut self, price: f64, qty: f64, should_enter_long: c_uchar, should_enter_short: c_uchar, should_exit_long: c_uchar, should_exit_short: c_uchar) -> (f64, &'static str) {
    if should_enter_long != 0 && self.long_pos == 0.0 {
      self.long_pos = price * qty;
      (self.long_pos, "enter_long")
    } else if should_exit_long != 0 && self.long_pos != 0.0 {
      let res = self.long_pos;
      self.long_pos = 0.;
      (res, "exit_long")
    }
    else if should_enter_short != 0 && self.short_pos == 0.0 {
      self.short_pos = price * qty;
      (self.short_pos, "enter_short")
    }
    else if should_exit_short != 0 && self.short_pos != 0.0 {
      let res = self.short_pos;
      self.short_pos = 0.;
      (res, "exit_short")
    }
    else {
      (0., "na")
    }
  }
}



#[pymodule]
fn rust_trade_fsm(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
  m.add_class::<RustTradeFSM>()?;
  Ok(())
}
