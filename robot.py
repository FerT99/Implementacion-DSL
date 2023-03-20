import math
import turtle
import re

class LogoParser:
    def __init__(self, input_str):
        self.input_str = input_str
        self.tokens = []
        self.current_token = 0

    def parse(self):
        self.tokenize()
        self.program()

    def tokenize(self):
        # regex para cada token
        token_specs = [
            ('REPT', r'REPT\(\d+\)'),
            ('DELA', r'DELA\(\d+\)'),
            ('ATRA', r'ATRA\(\d+\)'),
            ('IZQD', r'IZQD\(\d+\)'),
            ('DERE', r'DERE\(\d+\)'),
            ('LPLM', r'LPLM'),
            ('BPLM', r'BPLM'),
            ('CNTR', r'CNTR'),
            ('LIMP', r'LIMP'),
            ('COLP', r'COLP\(\d+\)'),
            ('LBRACKET', r'\{'),
            ('RBRACKET', r'\}'),
            ('SEMICOLON', r';'),
            ('WHITESPACE', r'\s+'),
        ]

        token_re = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
        get_token = re.compile(token_re).match
        pos = 0

        while True:
            match = get_token(self.input_str, pos)
            if not match:
                break

            pos = match.end()
            token_type = match.lastgroup
            token_value = match.group(token_type)

            if token_type != 'WHITESPACE':
                self.tokens.append((token_type, token_value))

    def expect(self, expected_token_type):
        token_type, token_value = self.tokens[self.current_token]
        if token_type != expected_token_type:
            raise SyntaxError(f"Se esperaba {expected_token_type}, pero se encontró {token_type}")
        self.current_token += 1
        return token_value

    def program(self):
        while self.current_token < len(self.tokens):
            token_type, token_value = self.tokens[self.current_token]
            self.command(token_type, token_value)
            self.current_token += 1    

screen = turtle.Screen()
screen.title("Robot Virtual DSL")
screen.setup(width=800, height=600)
screen.tracer(0)
turtle.colormode(255)

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.pen_down_state = False
        self.pen_color = "red" # Inicializar el color del lápiz como rojo
        self.colors = ["black", "red", "blue", "green", "yellow", "purple"]

    def set_pen_color(self, color_index):
        if 0 <= color_index < len(self.colors):  
            self.pen_color = self.colors[color_index]
        else:
            raise ValueError(f"Índice de color inválido: {color_index}")

    def move_forward(self, steps):
        self.x += steps * math.cos(math.radians(self.angle))
        self.y += steps * math.sin(math.radians(self.angle))
        self.draw_line()

    def move_backward(self, steps):
        self.x -= steps * math.cos(math.radians(self.angle))
        self.y -= steps * math.sin(math.radians(self.angle))
        self.draw_line()

    def turn_left(self):
        self.angle = (self.angle + 90) % 360

    def turn_right(self):
        self.angle = (self.angle - 90) % 360

    def pen_up(self):
        self.pen_down_state = False

    def pen_down(self):
        self.pen_down_state = True

    def set_pen_color(self, color):
        self.pen_color = color

    def clear_screen(self):
        turtle.clear()

    def go_to_center(self):
        self.x = 0
        self.y = 0

    def draw_line(self):
        if self.pen_down_state:
            turtle.pencolor(self.pen_color) # Usar self.pen_color en lugar de self.set_pen_color
            turtle.pen(pencolor=self.pen_color, pendown=True)
            turtle.setpos(self.x, self.y)
        else:
            turtle.pen(pendown=False)
            turtle.setpos(self.x, self.y)
        turtle.update()


class LogoExecutor(LogoParser):
    def __init__(self, input_str):
        super().__init__(input_str)
        self.robot = Robot()

    def command(self, token_type, token_value):
        if token_type == 'REPT':
            repetitions = int(token_value[5:-1]) # Extraer el número de repeticiones
            self.expect("LBRACKET")
            for _ in range(repetitions):
                self.program()
            self.expect("RBRACKET")
        elif token_type == 'DELA':
            steps = int(token_value[5:-1]) # Extraer el número de pasos
            self.robot.move_forward(steps)
        elif token_type == 'ATRA':
            steps = int(token_value[5:-1]) # Extraer el número de pasos
            self.robot.move_backward(steps)
        elif token_type == 'IZQD':
            angle = int(token_value[5:-1])  # Extraer el ángulo
            for _ in range(angle // 90):
                self.robot.turn_left()
        elif token_type == 'DERE':
            angle = int(token_value[5:-1])  # Extraer el ángulo
            for _ in range(angle // 90):
                self.robot.turn_right()
        elif token_type == 'LPLM':
            self.robot.pen_up()
        elif token_type == 'BPLM':
            self.robot.pen_down()
        elif token_type == 'CNTR':
            self.robot.go_to_center()
        elif token_type == 'LIMP':
            self.robot.clear_screen()
        elif token_type == 'COLP':
            color = int(token_value[5:-1])  # Extraer el número del color
            self.robot.set_pen_color(color)

dsl_code = "BPLM; DELA(10); IZQD(90); DELA(10); IZQD(90); DELA(15); IZQD(90); DELA(15); LPLM;"
executor = LogoExecutor(dsl_code)
executor.parse()

turtle.mainloop()