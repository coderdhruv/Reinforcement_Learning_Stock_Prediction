class candlestick:
    def __init__(self, upper_shadow_length, lower_shadow_length, body_length, color):
        self.upper_shadow_length = upper_shadow_length
        self.lower_shadow_length = lower_shadow_length
        self.body_length = body_length
        self.color = color


class actionspace:
    def __init__(self):
        self.hold = 'Hold'
        self.long = 'Long'
        self.short = 'Short'


class memorybufferstate:
    def __init__(self, candlestickstate, action, reward):
        self.candlestickstate = candlestickstate
        self.action = action
        self.reward = reward


class candlestickState:
    def __init__(self, centreofut, centreoflt, centreofbl, centreofcolor):
        self.centreofut = centreofut
        self.centreoflt = centreoflt
        self.centreofbl = centreofbl
        self.centreofcolor = centreofcolor


# class onlineclusteringdatapoint:
#     def __init__(self, xi, density_xi):
#         self.xi = xi
#         self.density_xi = density_xi


# class onlineclusteringenv:
#     def __init__(self, prev_mean_x, prev_mean_X):
#         self.prev_mean_x = prev_mean_x
#         self.prev_mean_X = prev_mean_X


memorybuffer = []
onlineclusteringxiarray = []
onlineclusteringclustercentres = []
