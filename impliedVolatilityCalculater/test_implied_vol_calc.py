from implied_vol_calc import ImpliedVolCalc


import matplotlib.pyplot as plt

broken = ImpliedVolCalc()

i = 0.01
strike = 145
current = 147.63
days = 6
years = days/365.25
call_price = 4.35
vols = []
error = []
while i<=4:
    d1, d2 = broken.get_ds(i, 147.63, 145, years, 0.05)
    price_at_vol = broken.get_call_price(d1, d2, current, strike, days, 0.05)
    error.append(price_at_vol - call_price)
    vols.append(i)
    i += 0.01

# Plotting
plt.plot(vols, error, marker='o')
plt.xlabel('Volatility')
plt.ylabel('Error')
plt.title('Error vs Volatility')
plt.grid(True)
plt.show()
exit()
class TestImpliedVolCalc:

    def setup_method(self):
        self.calc = ImpliedVolCalc()

    def test_simple_call(self):
        strike = 145
        current = 147.63
        days = 6
        call_price = 4.35
        result = self.calc.calc_implied_vol(call_price, current, strike, days)
        assert result is not None
    

    # def test_zero_call_price(self):
    #     strike = 145
    #     current = 147.63
    #     days = 6
    #     call_price = 0.0
    #     result = self.calc.get_implied_vol(call_price, current, strike, days)
    #     assert result is None

    # def test_high_call_price(self):
    #     strike = 145
    #     current = 147.63
    #     days = 6
    #     call_price = 100.0
    #     result = self.calc.get_implied_vol(call_price, current, strike, days)
    #     assert result is not None

    # def test_negative_call_price(self):
    #     strike = 145
    #     current = 147.63
    #     days = 6
    #     call_price = -4.35
    #     result = self.calc.get_implied_vol(call_price, current, strike, days)
    #     assert result is None
