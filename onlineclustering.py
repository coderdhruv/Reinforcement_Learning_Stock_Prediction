from classdefs import onlineclusteringxiarray
import investpy


class onlineclustering:
    def __init__(self, pie_dictionary, muN, XN):
        self.pie_dictionary = pie_dictionary
        self.muN = muN
        self.XN = XN

    def distance_candle_stockobj(self, x1, x2):
        diff_upper_shadow = abs(
            x1.upper_shadow_length - x2.upper_shadow_length)
        diff_lower_shadow = abs(
            x1.lower_shadow_length - x2.lower_shadow_length)
        diff_body_length = abs(x1.body_length - x2.body_length)
        diff_color = abs(x1.color - x2.color)
        return diff_upper_shadow**2 + diff_lower_shadow**2 + diff_body_length**2 + diff_color**2

    
    def distance_sum(self, xn, onlineclusteringxiarray):
        sum = 0
        for i in range(0, len(onlineclusteringxiarray)):
            sum += self.distance_candle_stockobj(
                onlineclusteringxiarray[i] - xn)
        return sum

    def xi_squared(self, xi):
        return abs(xi.upper_shadow_length)**2 + abs(xi.lower_shadow_length)**2 + abs(xi.body_length)**2 + abs(xi.color)**2

    def calc_pieN_xn(self, xn):
        return (len(onlineclusteringxiarray)+1)*(abs(self.distance_candle_stockobj(xn, self.muN)) + self.XN - self.xi_squared(self.muN))

    def calc_pieN_xi(self, xi):
        return self.pie_dictionary[xi] - self.distance_candle_stockobj(xi, self.muN)

    def multiply_xi(self, xi, t):
        return candlestick(t*(xi.upper_shadow_length), t*(xi.lower_shadow_length), t*(xi.body_length), t*(xi.color))

    def add_xi(self, x1, x2):
        diff_upper_shadow = abs(
            x1.upper_shadow_length + x2.upper_shadow_length)
        diff_lower_shadow = abs(
            x1.lower_shadow_length + x2.lower_shadow_length)
        diff_body_length = abs(x1.body_length + x2.body_length)
        diff_color = abs(x1.color + x2.color)
        return diff_upper_shadow + diff_lower_shadow + diff_body_length + diff_color

    def sum_pien(self,xn):
        sum_of_pien=0
        for i in range (1,n):
            sum_of_pien+=self.pie_dictionary[xi]
        sum_of_pien+=2*calc_pieN_xn(xn)
        return sum_of_pien

    def update_muN(self, xn):
        n = len(onlineclusteringxiarray)+1
        self.muN = self.add_xi(self.multiply_xi(self.muN,(n-1)/n),self.multiply_xi(xn,1/n))
        self.XN = self.add_xi(self.multiply_xi(self.XN,(n-1)/n),self.multiply_xi(self.xi_squared(xn),1/n))
        


        # print(df)
preprocess_obj = preprocess()
candlestick_daily = preprocess_obj.get_daily_candlestick_data(df, '2000-01-03')
