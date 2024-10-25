#lack of libries to learn from first principles
from typing import Optional, List, Dict
from scipy.stats import norm
from datetime import datetime
import numpy as np

class OptionPricer:


    def __init__(self):
        pass

    def euro_call_pricer(self, risk_free_rate: float, volatilities: np.array, strike_prices: np.array, expiration_date: datetime, current_price: float):
        """
        returns a matrix of option prices for all volality strike price combinations given

        No dividends are paid out during the life of the option.
        There are no transaction costs in buying the option.
        The returns of the underlying asset are normally distributed.
        Volitility (and risk free rate) will be assumed Constant
        """
        #c = SN(d1) - N(d2)Ke^-rt
        #d1 = ( ln(s/k) + t(r +0.5*v**2)) / ( v*t^0.5)
        #d2 = d1 - v*t^0.5
        time_to_maturity = self.get_time_to_maturity(expiration_date, "years")
        # vol_time_sqrd = self.get_vol_time_sqrd(volatilities, time_to_maturity, len(strike_prices))
        d1 = self.get_euro_d1_numerator(risk_free_rate, volatilities, strike_prices, current_price, time_to_maturity)
        # d1 = np.dot(d1, 1/vol_time_sqrd)
        print(d1)
        expected_return = norm.cdf(d1)
        print(expected_return)
        # d2 = d1 - vol_time_sqrd

    def get_euro_drift_term(self, 
            risk_free_rate: float, 
            volatilities: np.array,
            strike_prices: np.array,
            current_price: float,
            years_to_maturity=float,
        ):
        #this may need to get renamed if d1 differs in puts ect
        d1_numerater = self.get_euro_d1_numerator(risk_free_rate, volatilities, strike_prices, current_price, years_to_maturity)
        # d1_denominator = 

    def get_euro_d1_numerator(self, 
            risk_free_rate: float, 
            volatilities: np.array,
            strike_prices: np.array,
            current_price: float,
            years_to_maturity=float,
        ):
        #this may need to get renamed if d1 differs in puts ect
        ratio_m = current_price/self.get_strikes_matrix(strike_prices, len(volatilities))
        ln_ratio_m = np.log(ratio_m)

        v_matrix = self.get_vol_matrix(volatilities, len(strike_prices))
        time_risk_volatility_matrix = years_to_maturity*(risk_free_rate + 0.5*np.power(v_matrix, 2))
        # time_risk_volatility_matrix = np.tile(time_risk_volatility_matrix, (len(strike_prices), 1)).transpose()
        
        return ln_ratio_m + time_risk_volatility_matrix
    
    def get_vol_matrix(self, volatilities: np.array, num_strikes: int):
        return np.tile(volatilities, (num_strikes, 1)).transpose()
    
    def get_strikes_matrix(self, strike_prices: np.array, num_volatilities: int):
        return np.tile(strike_prices, (num_volatilities, 1))


    def get_time_to_maturity(self, expiration_date: datetime, time_unit: str):
        if time_unit.lower() != "years":
            raise ValueError("Currently Only Years Supported")
        delta = expiration_date - datetime.now()
        return delta.total_seconds() / (365.25 * 24 * 60 * 60)