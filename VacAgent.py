class VacAgent:
    def __init__(self):
        self.pos_x = 1  # Starting X position
        self.pos_y = 1  # Starting Y position
        self.facing = 'NORTH'  # Initial facing direction
        self.visited_locations = set([(1, 1)])  # Track visited locations
        self.dirt_locations = set()  # Track known dirt locations
        self.obstacle_locations = set()  # Track known obstacle locations
        self.path = [(1, 1)]  # Path stack for backtracking
        self.task_complete = False

    def see(self, percept):
        current_location = (self.pos_x, self.pos_y)

        # Check for dirt
        if percept.see_dirt():
            self.dirt_locations.add(current_location)

        # Check for obstacles and add to obstacle map if found
        if percept.see_obstacle():
            front_location = self.next_location()
            self.obstacle_locations.add(front_location)

        # Handle bump by reverting position
        if percept.feel_bump():
            self.move_back()

    def select_action(self):
        # Check if all dirt is cleaned
        if not self.dirt_locations and self.pos_x == 1 and self.pos_y == 1 and self.task_complete:
            return 'SHUT_OFF'

        current_location = (self.pos_x, self.pos_y)

        # Prioritize cleaning dirt if present
        if current_location in self.dirt_locations:
            self.dirt_locations.remove(current_location)
            return 'SUCK_DIRT'

        # Explore unvisited, accessible locations
        next_location = self.next_location()
        if next_location not in self.visited_locations and next_location not in self.obstacle_locations:
            self.visited_locations.add(next_location)
            self.path.append(current_location)  # Remember path for backtracking
            return 'GO_FORWARD'
        else:
            # Turn left if forward is blocked or already visited
            self.update_direction(turn_right=False)
            return 'TURN_LEFT'

    def next_location(self):
        if self.facing == 'NORTH':
            return (self.pos_x, self.pos_y - 1)
        elif self.facing == 'SOUTH':
            return (self.pos_x, self.pos_y + 1)
        elif self.facing == 'EAST':
            return (self.pos_x + 1, self.pos_y)
        elif self.facing == 'WEST':
            return (self.pos_x - 1, self.pos_y)

    def move_back(self):
        # Reset position if bump occurred and update location tracking
        if self.path:
            last_location = self.path.pop()
            self.pos_x, self.pos_y = last_location

    def update_direction(self, turn_right):
        # Update direction based on turn action
        if turn_right:
            if self.facing == 'NORTH':
                self.facing = 'EAST'
            elif self.facing == 'EAST':
                self.facing = 'SOUTH'
            elif self.facing == 'SOUTH':
                self.facing = 'WEST'
            elif self.facing == 'WEST':
                self.facing = 'NORTH'
        else:
            if self.facing == 'NORTH':
                self.facing = 'WEST'
            elif self.facing == 'WEST':
                self.facing = 'SOUTH'
            elif self.facing == 'SOUTH':
                self.facing = 'EAST'
            elif self.facing == 'EAST':
                self.facing = 'NORTH'

# Mocking percept for demonstration purposes
class VacPercept:
    def __init__(self, dirt=False, obstacle=False, bump=False):
        self.dirt = dirt
        self.obstacle = obstacle
        self.bump = bump

    def see_dirt(self):
        return self.dirt

    def see_obstacle(self):
        return self.obstacle

    def feel_bump(self):
        return self.bump

# Example usage
if __name__ == "__main__":
    agent = VacAgent()

    # Simulating percepts (replace with actual percept input)
    percepts = [
        VacPercept(dirt=True),
        VacPercept(obstacle=True),
        VacPercept(bump=True)
    ]

    for percept in percepts:
        agent.see(percept)
        action = agent.select_action()
        print(f"Action: {action}")
