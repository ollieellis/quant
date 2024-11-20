import math
from scipy.stats import norm
from typing import Optional
from loguru import logger
import inspect
import copy

class ImpliedVolCalc:

    def __init__(self) -> None:
        pass

    def calc_implied_vol(self, 
        call_price: float, 
        current_price: float,
        strike_price: float, 
        days: float, 
        risk_free_rate: float=0.05,
        tolerance: float=0.01,
        starting_vol: float=0.5,
        max_iterations: int=1000
    ) -> Optional[float]:
        years = days / 365.25
        vol = starting_vol
        error = 100000
        i = 0
        while abs(error) > abs(tolerance):
            if i > max_iterations:
                logger.error(f"Failed to Calculate Volatility in {max_iterations} attempts")
                return None
            print(vol, error)
            i += 1
            d1, d2 = self.get_ds(
                vol=vol,
                current_price=current_price,
                strike_price=strike_price,
                years=years,
                risk_free_rate=risk_free_rate,
            )
            price_at_vol = self.get_call_price(d1, d2, current_price, strike_price, years, risk_free_rate)
            vega = current_price * norm.pdf(d1) * (years**0.5)
            vol = -price_at_vol/vega + vol
            error = abs(price_at_vol - call_price)
        
        logger.info(f"Calculated Vol in {i} attempts")
        return vol
    
    def get_call_prices(self, vol, strike, current, years, risk_free_rate):
        #This is janky but I dont want to write this function 5 times to print a few graphs
        """Accepts calls where 1 param only is a list; will return black scholes call price for given params as list"""
        frame = inspect.currentframe()
        args_info = inspect.getargvalues(frame) #I dont support kwargs n args so wont be present
        is_list = [int(isinstance(v, list)) for k,v in args_info.items()]
        if sum(is_list) != 1:
            logger.error(f"Get Call Prices Called with {sum(is_list)} lists; Must use Only 1")
            raise ValueError(f"Call Prices Called with {sum(is_list)} lists")

        prices = []
        list_field = list(args_info.keys())[is_list.index(1)]
        for i, v in enumerate(args_info[list_field]):
            params = copy.deepcopy(args_info)
            params[list_field] = v 
            d1, d2 = self.get_ds()



    def get_call_price(self, d1: float, d2: float, current_price: float, strike_price: float, years: float, risk_free_rate: float):
        return current_price * norm.cdf(d1) - norm.cdf(d2) * strike_price * math.exp(-risk_free_rate * years)

    def get_ds(self, vol: float, current_price: float, strike_price: float, years: float, risk_free_rate: float):
        sigma_t = vol * years
        d1 = (math.log(current_price / strike_price) + years * (risk_free_rate + 0.5 * vol**2)) / sigma_t
        d2 = d1 - sigma_t
        return d1, d2