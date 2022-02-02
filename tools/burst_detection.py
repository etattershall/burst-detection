import pandas as pd
import numpy as np

def calc_significance(stacked_vectors, significance_threshold, n):
    # Must have been above the significance threshold for two consecutive timesteps
    a = stacked_vectors>significance_threshold
    b = a.rolling(window=n).sum()
    return stacked_vectors[stacked_vectors.axes[1][np.where(b.max()>=n)[0]]]


class BurstDetection:
    def __init__(self, short_ma_length, long_ma_length, significance_ma_length, signal_line_ma):
        self.short_ma_length = short_ma_length
        self.long_ma_length = long_ma_length
        self.significance_ma_length = significance_ma_length
        self.signal_line_ma = signal_line_ma
    
    def calc_macd(self, stacked_vectors, ema=True):
        if ema:
            long_ma = stacked_vectors.ewm(span=self.long_ma_length).mean()
            short_ma = stacked_vectors.ewm(span=self.short_ma_length).mean()
            significance_ma = stacked_vectors.ewm(span=self.significance_ma_length).mean()
            macd = short_ma - long_ma
            signal = macd.ewm(span=self.signal_line_ma).mean()
            hist = macd - signal
            return long_ma, short_ma, significance_ma, macd, signal, hist
        else:
            long_ma = stacked_vectors.rolling(self.long_ma_length).mean()
            short_ma = stacked_vectors.rolling(self.short_ma_length).mean()
            significance_ma = stacked_vectors.rolling(self.significance_ma_length).mean()
            macd = short_ma - long_ma
            signal = macd.rolling(self.signal_line_ma).mean()
            hist = macd - signal
            return long_ma, short_ma, significance_ma, macd, signal, hist        


    
    def calc_burstiness(self, hist, scaling_factor):
        return hist.iloc[self.long_ma_length-1:]/scaling_factor

    def calc_scaling(self, significance_ma, method):
        if method == "max":
            scaling = significance_ma.iloc[self.significance_ma_length-1:].max()
        elif method == "mean":
            scaling = significance_ma.iloc[self.significance_ma_length-1:].mean()
        elif method == "sqrt":
            scaling = np.sqrt(significance_ma.iloc[self.significance_ma_length-1:].max()  )      
        return scaling

    def max_burstiness(self, burstiness, absolute):
        if absolute:
            b = pd.concat([np.abs(burstiness).max(), np.abs(burstiness).idxmax()], axis=1)
        else:
            b = pd.concat([burstiness.max(), burstiness.idxmax()], axis=1)
        b.columns = ["max", "location"]
        return b
        
    def my_burstiness(self, stacked_vectors, absolute=True, method="sqrt"):
        long_ma, short_ma, significance_ma, macd, signal, hist = self.calc_macd(stacked_vectors)
        scaling_factor = self.calc_scaling(significance_ma, method)
        burstiness_over_time = self.calc_burstiness(hist, scaling_factor)
        burstiness = self.max_burstiness(burstiness_over_time, absolute=absolute)
        return(burstiness)
        
        
class Dataset:
    def __init__(self, name, years, stacked_vectors):
        self.name = name
        self.stacked_vectors = stacked_vectors
        self.years = years
    
    def get_sig_stacked_vectors(self, significance_threshold, years_above_significance):
        normalisation = self.stacked_vectors.sum(axis=1)
        self.sig_stacked_vectors = calc_significance(self.stacked_vectors.divide(normalisation, axis="index")*100, significance_threshold, years_above_significance)
    
    def get_burstiness(self, short_ma_length, long_ma_length, significance_ma_length, signal_line_ma_length, ema=True, scaling_type="sqrt", absolute=True):
        bd = BurstDetection(short_ma_length, long_ma_length, significance_ma_length, signal_line_ma_length)
        long_ma, short_ma, significance_ma, macd, signal, hist = bd.calc_macd(self.sig_stacked_vectors, ema=ema)
        self.scaling_factor = bd.calc_scaling(significance_ma, scaling_type)
        burstiness_over_time = bd.calc_burstiness(hist, self.scaling_factor)
        self.burstiness = bd.max_burstiness(burstiness_over_time, absolute=absolute)
    
    
    
    
    
        