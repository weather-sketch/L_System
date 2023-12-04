import turtle as t
import random
import importlib


class LSystemGenerator:
    def __init__(self, axiom, rules, angle, distance, iterations):
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.distance = distance
        self.iterations = iterations
        self.branch_size = 1
        self.leaf_size = 1

    def generate(self):
        self.context_sensitive_rules = (
            {('F', 'F', 'F'): ']', 
             ('X', 'F', 'F'): ']',
             ('F', 'X', 'F'): ']'}
            )
        self.stochastic_rules = {
            'F': [('F', 0.3), ('[+F]F', 0.5)],
            'X': [('F', 0.3), ('[+X]F', 0.7)]
            }
        sequence = self.axiom
        for _ in range(self.iterations):
            sequence = list(sequence)
            new_sequence = []
            for i in range(len(sequence)):
                char = sequence[i]
                # Apply predefined rules first
                if char in self.rules:
                    char = self.rules[char]

                # Check if the character with its context matches any context sensitive rule
                left_context = sequence[i-1] if i > 0 else None
                right_context = sequence[i+1] if i < len(sequence) - 1 else None
                rule_key = (left_context, char, right_context)

                if rule_key in self.context_sensitive_rules:
                     char = self.context_sensitive_rules[rule_key]
                
                     # apply stochastic rules
                if char in self.stochastic_rules:
                    replacements, probabilities = zip(*self.stochastic_rules[char])
                    char = random.choices(replacements, probabilities)[0]

                new_sequence.append(char)

            sequence = ''.join(new_sequence)
            yield sequence
    
    # reset everything when need to load a new model
    def reset(self):
        t.clear()
        self.generator = self.generate()
        print("Reset.")
    
    # hot key for reset
    def registered_hotkey_(self):
        t.listen()
        t.onkey(self.reset, 'r')
            
           
class LSystemRenderer:
    def __init__(self, generator): 
        self.generator = generator
        self.generator_iteration = generator.generate()
    
    # click through the generation process    
    def click_through(self, x, y):
        try:
            save_string = next(self.generator_iteration) # use a generator not a string
            t.clear()
            self.draw(save_string)
            print(save_string)
            # stop when finish iteration 
        except StopIteration:
            print("Done")
            print(f"Iterations: {self.generator.iterations}")
        
    def draw(self, sequence):
        t.setheading(90)
        t.speed(0)
        save_position =(t.position(),t.heading())
        t.width(self.generator.branch_size)      
        stack = []
        
        colors = ["red", "orange", "yellow", "green", "blue", "violet"]
        leaf_shapes = [self.draw_circle, self.draw_triangle, self.draw_square]
        for element in sequence:
            if element == 'F':
               t.forward(self.generator.distance)
            elif element == '+':
               t.left(self.generator.angle)
            elif element == '-':
               t.right(self.generator.angle)
            elif element == '[':
               position = t.position()
               heading = t.heading()
               stack.append((position,heading))
            elif element == ']':
               if stack:
                   position,heading = stack.pop()
                   # draw leaf
                   t.penup()
                   t.goto(position)
                   t.setheading(heading)
                   # randomise the color used
                   t.color(random.choice(colors))
                   t.begin_fill()
                   # randomise the leaf shape
                   random.choice(leaf_shapes)()
                   t.end_fill()
                   t.penup()
                   # draw branch
                   t.color("green")
                   t.width(self.generator.branch_size)
                   t.goto(position) 
                   t.setheading(heading) 
                   t.pendown()
        t.penup()
        t.goto(save_position[0])
        t.setheading(save_position[1])
        t.pendown()
        
    def draw_circle(self):
            t.circle(self.generator.leaf_size)

    def draw_triangle(self):
        for _ in range(3):
            t.forward(self.generator.leaf_size)
            t.right(120)

    def draw_square(self):
        for _ in range(4):
            t.forward(self.generator.leaf_size)
            t.right(90) 
 
            
class ParameterManager:
    def __init__(self, generator):
        self.generator = generator
        self.distance = generator.distance
        self.angle = generator.angle
        self.leaf_size = generator.leaf_size
        self.branch_size = generator.branch_size
    
    def change_param(self, param, delta, min_val = None):
        """Change the parameter by a delta value."""
        current_val = getattr(self, param)
        new_val = current_val + delta
        # if the new value is below min value
        if (min_val != None and new_val > min_val):
            # print error message
            print(f"The {param} cannot be decreased further.")
        else:
            # else, set a new value
            setattr(self, param, new_val)
            setattr(self.generator, param, new_val) 
            print(f"The {param} is changed by {delta} and is now: {new_val}")
  
    def increase_distance(self):
        self.change_param("distance", 1)
        
    def decrease_distance(self):
        self.change_param("distance", -1, 1)
        
    def increase_angle(self):
        self.change_param("angle", 10)

    def decrease_angle(self):
        self.change_param("angle", -10, 10)
            
    def increase_leaf(self):
        self.change_param("leaf_size", 1)
    
    def decrease_leaf(self):
        self.change_param("leaf_size", -1, 1)
        
    def increase_branch(self):
        self.change_param("branch_size", 1)
        
    def decrease_branch(self):
        self.change_param("branch_size", -1, 1)
        
    def registered_hotkey(self):
        t.listen()
        t.onkey(self.increase_distance, '1')
        t.onkey(self.decrease_distance, '2')
        t.onkey(self.increase_angle, '3')
        t.onkey(self.decrease_angle, '4')
        t.onkey(self.increase_leaf, '5')
        t.onkey(self.decrease_leaf, '6')        
        t.onkey(self.increase_branch, '7')
        t.onkey(self.decrease_branch, '8')    

        
class LSystemController:
    def __init__(self):
        self.generator = None
        self.renderer = None
        self.parameter_manager = None
        # load a model using a key 
        self.model_dict = {
            'a': 'model_a',
            'b': 'model_b',
            'c': 'model_c',
            'd': 'model_d',
            'e': 'model_e',
            'f': 'model_f',
            'g': 'model_g',
            'h': 'model_h',
        }
       
    def registered_hotkeys(self):
        t.listen()
        t.onkey(self.instructions, 'i')
        t.onkey(lambda: self.load_model_with_input(), 'space')
          
    def instructions(self):
        instructions = {
            '1': 'increase distance',
            '2': 'decrease distance',
            '3': 'increase angle',
            '4': 'decrease angle',
            '5': 'increase leaf size',
            '6': 'decrease leaf size',
            '7': 'increase branch size',
            '8': 'decrease branch size',
            'r' :'reset the screen',
            'space': 'choose a new model',
            'i': 'see this instruction again.'
            }
        text = ',\n'.join(f"Press '{k}' to {v} "for k, v in instructions.items())
        t.write(text, move=False, align="center", font=("Arial", 20, "normal"))
        t.pendown()
        
    def load_model_with_input(self):
        # prompt the user to choose a model
        user_input = input("Enter the name of the model to load, type the index: ")
        try:
            model_name = self.model_dict[user_input]
            self.load_model(model_name)
        except KeyError:
            print(f"Not Valid. Please choose from the available models.")
        
    def load_model(self, model_name):
        # load the .py files
        model = importlib.import_module(model_name)
        self.generator =  LSystemGenerator(
            model.axiom,
            model.rules,
            model.angle,
            model.distance,
            model.iterations,
        )
        self.generator.registered_hotkey_()
        if self.renderer:
                self.renderer.generator = self.generator
                self.renderer.generator_iteration = self.generator.generate()
        else:
            self.renderer = LSystemRenderer(self.generator)

        self.parameter_manager = ParameterManager(self.generator)
        self.parameter_manager.registered_hotkey()
          
    def main(self):
        print("Available models:", ", ".join(self.model_dict.keys()))
        while True:
            try:
                user_input = input("Choose a model from a - h, type the index:")
                self.load_model(self.model_dict[user_input])
                break
            except KeyError:
                print(f"Not Valid. Please choose from the available models.")
                
        t.setup(width = 960, height = 720)
        t.title("L system Generator")
        t.penup()
        t.goto(0,-300)
        t.tracer(False)
        t.hideturtle()
        self.instructions()    
        t.onscreenclick(self.renderer.click_through)      
        screen = t.Screen()
        self.registered_hotkeys()
        screen.mainloop()
 
        
if __name__ == "__main__":
    controller = LSystemController()
    controller.main()