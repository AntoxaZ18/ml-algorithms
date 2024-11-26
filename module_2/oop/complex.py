import cmath


class ComplexNumber(complex):
    """class for representing complex number based on python mplementation. Added polar representation"""

    def __new__(cls, real: float, imag: float, form="rect") -> complex:
        """form = "rect" for algebraic (rect) form or "polar" for polar form"""

        forms = {"rect", "polar"}

        if form not in forms:
            raise ValueError(f'form: "{form}" not in availables forms: {forms}')

        if not (isinstance(real, (int, float)) and isinstance(imag, (int, float))):
            raise ValueError("real and imag args must be integers or floats")

        if form == "polar":
            rect_form = cmath.rect(real, imag)
            real = rect_form.real
            imag = rect_form.imag

        number = super().__new__(cls, real, imag)
        return number

    def polar(self):
        """return complex number in polar form as tuple (module, angle(in rad))"""
        return cmath.polar(self)
    