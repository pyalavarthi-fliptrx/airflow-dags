from decimal import Decimal
import numbers as _numbers


class Money(Decimal):
    def __new__(cls, _value="0", context=None, precision='1.00'):
        # set precision to two decimal places and round
        value = Decimal(_value).quantize(Decimal(precision))
        return super(Money, cls).__new__(cls, value, context)

    def __mul__(self, _input):
        input = Decimal(str(_input))
        result = super().__mul__(input)
        return Money(result, precision=str(self))

    __rmul__ = __mul__

    # Todo: Make this work for more than 2 digit Money
    def __add__(self, _input):
        input = Money(str(_input))
        result = super().__add__(input)
        return Money(result)

    __radd__ = __add__

    def __repr__(self):
        return "Money('%s')" % str(self)

    # This is necessary for pydantic
    @classmethod
    def __get_validators__(cls):
        return [lambda value, values, config, field: cls(value)]


_numbers.Number.register(Money)
