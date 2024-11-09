import math
from scipy.stats import norm
from typing import Optional
from loguru import logger


class ImpliedVolCalc:

    def __init__(self) -> None:
        pass

    def get_implied_vol(self, 
        call_price: float, 
        current_price: float,
        strike_price: float, 
        days: float, 
        risk_free_rate: float=0.05,
        tolerance: float=0.001,
        starting_vol: float=0.5,
        max_iterations: int=1000
    ) -> Optional[float]:
        years = days / 365.25
        vol = starting_vol
        error = 100000
        i = 0
        while error > tolerance:
            if i > max_iterations:
                logger.error(f"Failed to Calculate Volatility in {max_iterations} attempts")
                return None
            
            i += 1
            d1, d2 = self.get_ds(
                vol=vol,
                current_price=current_price,
                strike_price=strike_price,
                years=years,
                risk_free_rate=risk_free_rate,
            )
            price_at_vol = self.get_call_price(d1, d2, current_price, strike_price, years, risk_free_rate)
            vega = current_price * norm.pdf(d1) * years**0.5
            vol = -price_at_vol/vega + vol
            error = abs(price_at_vol - call_price)
        
        logger.info(f"Calculated Vol in {i} attempts")
        return vol

    def get_ds(vol: float, current_price: float, strike_price: float, years: float, risk_free_rate: float):
        sigma_t = vol * years
        d1 = (math.log(current_price / strike_price) + years * (risk_free_rate + 0.5 * vol**2)) / sigma_t
        d2 = d1 - sigma_t
        return d1, d2

    def get_call_price(self, d1: float, d2: float, current_price: float, strike_price: float, years: float, risk_free_rate: float):
        return current_price * norm.cdf(d1) - norm.cdf(d2) * strike_price * math.exp(-risk_free_rate * years)
