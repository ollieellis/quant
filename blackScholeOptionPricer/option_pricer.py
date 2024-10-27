# lack of libries to learn from first principles
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
from scipy.stats import norm


class OptionPricer:

    def __init__(self):
        pass

    def euro_call_pricer(
        self,
        risk_free_rate: float,
        volatilities: np.array,
        strike_prices: np.array,
        expiration_date: datetime,
        current_price: float,
    ) -> np.array:
        """
        Using the black Scholes model; returns a matrix of option prices for all volality strike price combinations given.
        c = SN(d1) - N(d2)Ke^-rt
        d1 = ( ln(s/k) + t(r +0.5*v**2)) / ( v*t^0.5)
        d2 = d1 - v*t^0.5
        """
        time_to_maturity = self.get_time_to_maturity(expiration_date, "years")
        d1 = self.get_euro_d1(risk_free_rate, volatilities, strike_prices, current_price, time_to_maturity)
        d2 = d1 - self.get_euro_d1_denominator(volatilities, time_to_maturity, len(strike_prices))
        strikes_exp = self.get_strikes_exponent(risk_free_rate, volatilities, strike_prices, time_to_maturity)
        return current_price * norm.cdf(d1) - norm.cdf(d2) * strikes_exp

    def get_euro_d1(
        self,
        risk_free_rate: float,
        volatilities: np.array,
        strike_prices: np.array,
        current_price: float,
        years_to_maturity=float,
    ) -> np.array:
        # this may need to get renamed if d1 differs in puts ect
        d1_numerater = self.get_euro_d1_numerator(
            risk_free_rate,
            volatilities,
            strike_prices,
            current_price,
            years_to_maturity,
        )
        d1_denominator = self.get_euro_d1_denominator(volatilities, years_to_maturity, len(strike_prices))
        return d1_numerater / d1_denominator

    def get_strikes_exponent(
        self,
        risk_free_rate: float,
        volatilities: np.array,
        strike_prices: np.array,
        years_to_maturity=float,
    ) -> np.array:
        return self.get_strikes_matrix(strike_prices, len(volatilities)) * np.exp(-risk_free_rate * years_to_maturity)

    def get_euro_d1_numerator(
        self,
        risk_free_rate: float,
        volatilities: np.array,
        strike_prices: np.array,
        current_price: float,
        years_to_maturity=float,
        # this may need to get renamed if d1 differs in puts ect
    ) -> np.array:
        ratio_m = current_price / self.get_strikes_matrix(strike_prices, len(volatilities))
        v_matrix = self.get_vol_matrix(volatilities, len(strike_prices))
        time_risk_volatility_matrix = years_to_maturity * (risk_free_rate + 0.5 * np.power(v_matrix, 2))
        return np.log(ratio_m) + time_risk_volatility_matrix

    def get_euro_d1_denominator(
        self,
        volatilities: np.array,
        years_to_maturity: float,
        num_strikes: int,
    ):
        return self.get_vol_matrix(volatilities, num_strikes) * (years_to_maturity**0.5)

    def get_vol_matrix(self, volatilities: np.array, num_strikes: int):
        return np.tile(volatilities, (num_strikes, 1)).transpose()

    def get_strikes_matrix(self, strike_prices: np.array, num_volatilities: int):
        return np.tile(strike_prices, (num_volatilities, 1))

    def get_time_to_maturity(self, expiration_date: datetime, time_unit: str):
        if time_unit.lower() != "years":
            raise ValueError("Currently Only Years Supported")
        delta = expiration_date - datetime.now()
        return delta.total_seconds() / (365.25 * 24 * 60 * 60)
