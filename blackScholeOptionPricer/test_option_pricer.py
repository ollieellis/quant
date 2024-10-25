import numpy as np
from scipy.stats import norm
from datetime import datetime, timedelta

from option_pricer import OptionPricer


class TestEuroCall:

    def test_d1_numerator_simple(self):
        pricer = OptionPricer()
        expected = self.get_expected_matrix(self.euro_call_d1_numerator)
        print(expected)
        result = pricer.get_euro_d1_numerator(**self.simple_call_params())
        print(result)
        assert abs(np.max(result - expected)) < 0.01

    def test_euro_call_pricer_simple(self):
        pricer = OptionPricer()
        expected = None
        expiration_date = datetime.now() + timedelta(seconds=365.25*24*60*60)
        result = pricer.euro_call_pricer(
            risk_free_rate=1.04, 
            volatilities=np.array([0.1, 0.2, 0.3]),
            strike_prices=np.array([100, 105, 110, 120]),
            current_price=95,
            expiration_date=expiration_date
        )
        print(result)

    def test_get_strikes_matrix(self):
        vols = 5
        strikes = np.arange(1,4)
        pricer = OptionPricer()
        assert pricer.get_strikes_matrix(strikes, vols).shape == (5,3)

    def test_get_vol_matrix(self):
        strikes = 3
        vols = np.arange(1,6)
        pricer = OptionPricer()
        assert pricer.get_vol_matrix(vols, strikes).shape == (5,3)

    def get_expected_matrix(self, desired_matrix_func):
        simple_params = self.simple_call_params()
        expected = np.zeros((len(simple_params["volatilities"]), len(simple_params["strike_prices"])))
        for i, v in enumerate(simple_params["volatilities"]):
            for j, strike in enumerate(simple_params["strike_prices"]):
                call_price = desired_matrix_func(
                    S=simple_params["current_price"],
                    K=strike,
                    T=simple_params["years_to_maturity"],
                    r=simple_params["risk_free_rate"],
                    sigma=v
                )
                expected[i][j] = call_price
        return expected

    def euro_call_d1_numerator(self, S, K, T, r, sigma):
        d1 = (np.log(S/K) + (r + sigma**2/2)*T)
        return d1
    
    def euro_call_d1(self, S, K, T, r, sigma):
        d1 = (np.log(S/K) + (r + sigma**2/2)*T)/ (sigma*np.sqrt(T))
        return d1
        
    def euro_call(self, S, K, T, r, sigma):
        N = norm.cdf
        d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return S * N(d1) - K * np.exp(-r*T)* N(d2)
    
    def simple_call_params(self):
        return { 
            "risk_free_rate": 1.04, 
            "volatilities": np.array([0.1, 0.2, 0.3]),
            "strike_prices": np.array([100, 105, 110, 120]),
            "current_price": 95,
            "years_to_maturity": 1,
        }