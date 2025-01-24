import pytest
from JuliaSetSecond import calculate_z_serial_purepython

class TestJuliaSet:
    @pytest.mark.parametrize(
        "max_iterations, desired_width, expected_sum",
        [
            (300, 1000, 33219980),  # Example: original test case
            (200, 500, 8309980)   # Example: idk what to put to make it work
        ]
    )
    def test_sum(self, max_iterations, desired_width, expected_sum):
        cs, zs = self.gen_var(desired_width)
        output = calculate_z_serial_purepython(max_iterations, zs, cs)
        assert sum(output) == expected_sum

    def gen_var(self, desired_width):
        x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
        c_real, c_imag = -0.62772, -0.42193

        x_step = (x2 - x1) / desired_width
        y_step = (y1 - y2) / desired_width

        x = []
        y = []

        ycoord = y2
        while ycoord > y1:
            y.append(ycoord)
            ycoord += y_step

        xcoord = x1
        while xcoord < x2:
            x.append(xcoord)
            xcoord += x_step

        zs = []
        cs = []

        for ycoord in y:
            for xcoord in x:
                zs.append(complex(xcoord, ycoord))
                cs.append(complex(c_real, c_imag))

        return cs, zs
