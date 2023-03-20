import turtle

screen = turtle.Screen()
screen.title("Robot Virtual DSL")
screen.setup(width=800, height=600)

class Robot:
    def __init__(self):
        self.robot = turtle.Turtle()
        self.robot.speed(1)

    def move_forward(self, steps):
        self.robot.forward(steps)

    def move_backward(self, steps):
        self.robot.backward(steps)

    def turn_left(self):
        self.robot.left(90)

    def turn_right(self):
        self.robot.right(90)

    def pen_up(self):
        self.robot.penup()

    def pen_down(self):
        self.robot.pendown()

    def change_color(self, color):
        self.robot.pencolor(color)

    def clear(self):
        self.robot.clear()

    def go_to_center(self):
        self.robot.penup()
        self.robot.home()
        self.robot.pendown()

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
            self.robot.turn_left()
        elif token_type == 'DERE':
            self.robot.turn_right()

      
