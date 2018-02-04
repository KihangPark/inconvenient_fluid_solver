class NoiadUtils(object):

    @staticmethod
    def weight(distance, effect_radius):
        return (effect_radius / distance) - 1.0
