import pygame
import math
from behavior_tree import ExecutionStatus, BehaviorTree, SequenceNode, LeafNode

# Pygame setup
pygame.init()

# Adjusted screen size for better fit
WIDTH, HEIGHT = 1200, 800  # Screen resolution
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sisyphean Myth Simulation")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Hill class
class Hill:
    def __init__(self):
        self.base_x = 0
        self.base_y = 700
        self.length = 1440
        self.angle = 33.69

    def draw(self):
        top_x = self.base_x + self.length * math.cos(math.radians(self.angle))
        top_y = self.base_y - self.length * math.sin(math.radians(self.angle))
        pygame.draw.polygon(screen, GREEN, [
            (self.base_x, self.base_y),
            (top_x, top_y),
            (top_x + 100, top_y),
            (self.base_x + 100, self.base_y)
        ])

# Boulder class
class Boulder:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 30
        self.speed = 5

    def move_up(self):
        self.y -= self.speed * math.sin(math.radians(33.69))
        self.x += self.speed * math.cos(math.radians(33.69))

    def move_down(self):
        self.y += 2 * self.speed * math.sin(math.radians(33.69))
        self.x -= 2 * self.speed * math.cos(math.radians(33.69))

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

# Sisyphus class
class Sisyphus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.image.load("sisyphe.png")
        self.image = pygame.transform.scale(self.image, (100, 200))

    def move_up(self):
        self.y -= self.speed * math.sin(math.radians(33.69))
        self.x += self.speed * math.cos(math.radians(33.69))

    def move_down(self):
        self.y += self.speed * math.sin(math.radians(33.69))
        self.x -= self.speed * math.cos(math.radians(33.69))

    def draw(self):
        screen.blit(self.image, (int(self.x - 50), int(self.y - 100)))

# Behavior tree nodes
class PushBoulderNode(LeafNode):
    def __init__(self, node_name, boulder, sisyphus, hill):
        super().__init__(node_name)
        self.boulder = boulder
        self.sisyphus = sisyphus
        self.hill = hill

    def enter(self, agent):
        self.top_y = self.hill.base_y - self.hill.length * math.sin(math.radians(self.hill.angle))

    def execute(self, agent):
        margin = 1.0
        if (self.boulder.y <= 600  and self.sisyphus.y <= 700 and self.boulder.y > 50 and (self.boulder.y < self.sisyphus.y and self.boulder.x > self.sisyphus.x)):     
            self.boulder.move_up()
            self.sisyphus.move_up()
            return ExecutionStatus.RUNNING
        return ExecutionStatus.SUCCESS

class BoulderRollBackNode(LeafNode):
    def __init__(self, node_name, boulder, sisyphus, hill):
        super().__init__(node_name)
        self.boulder = boulder
        self.sisyphus = sisyphus
        self.hill = hill

    def enter(self, agent):
        self.base_y = self.hill.base_y

    def execute(self, agent):
        margin = 1.0
        if self.boulder.y < 600:
            self.boulder.move_down()
            self.sisyphus.move_down()
            return ExecutionStatus.RUNNING
        return ExecutionStatus.SUCCESS

class CheckBoulderAtBaseNode(LeafNode):
    def __init__(self, node_name, boulder, sisyphus):
        super().__init__(node_name)
        self.boulder = boulder
        self.sisyphus = sisyphus

    def enter(self, agent):
        self.base_y = self.boulder.y  # Set base Y where the boulder should be

    def execute(self, agent):
        margin = 1.0
        if  self.sisyphus.y < 700:
            self.boulder.y = self.base_y
            self.sisyphus.move_down()
            if self.sisyphus.y >= 700:
                self.sisyphus.y = 700
                self.boulder.y = 600
            return ExecutionStatus.SUCCESS
        return ExecutionStatus.RUNNING
    
# Create the behavior tree
def create_behavior_tree(boulder, hill, sisyphus):
    root = SequenceNode("Sisyphean Cycle")
    
    # Sequência de ações: primeiro, empurrar a bola para cima, depois verificar se a bola desceu completamente e depois parar
    push_boulder = PushBoulderNode("Push Boulder", boulder, sisyphus, hill)
    roll_back = BoulderRollBackNode("Boulder Rolls Back", boulder, sisyphus, hill)
    check_boulder_at_base = CheckBoulderAtBaseNode("Check Boulder At Base", boulder, sisyphus=sisyphus)

    root.add_child(push_boulder)
    root.add_child(roll_back)
    root.add_child(check_boulder_at_base)

    return BehaviorTree(root=root)

# Main function
def main():
    boulder = Boulder(x=100, y=HEIGHT - 200)
    hill = Hill()
    sisyphus = Sisyphus(x=50, y=HEIGHT - 100)
    behavior_tree = create_behavior_tree(boulder, hill, sisyphus)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        behavior_tree.update(None)

        screen.fill(BLACK)
        hill.draw()
        boulder.draw()
        sisyphus.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
