class Elevator:
    def __init__(self, numFloors):
        self.currentFloor = 1
        self.direction = "idle"  # "up", "down", "idle"
        self.doorsOpen = False
        self.requests = set()  # Set of floor numbers requested
        self.numFloors = numFloors
        
    def addRequest(self, floor):
        """Add a floor request to the elevator"""
        if 1 <= floor <= self.numFloors:
            self.requests.add(floor)
            print(f"Floor {floor} requested")
        else:
            print(f"Invalid floor: {floor}")
    
    def openDoors(self):
        """Open elevator doors"""
        self.doorsOpen = True
        print(f"Doors opening at floor {self.currentFloor}")
    
    def closeDoors(self):
        """Close elevator doors"""
        self.doorsOpen = False
        print(f"Doors closing at floor {self.currentFloor}")
    
    def moveUp(self):
        """Move elevator up one floor"""
        if self.currentFloor < self.numFloors:
            self.currentFloor += 1
            print(f"Moving up to floor {self.currentFloor}")
        
    def moveDown(self):
        """Move elevator down one floor"""
        if self.currentFloor > 1:
            self.currentFloor -= 1
            print(f"Moving down to floor {self.currentFloor}")
    
    def decideDirectionLook(self):
        """LOOK Algorithm: Continue in current direction until no more requests, then reverse"""
        if not self.requests:
            self.direction = "idle"
            return
            
        # Find requests above and below current floor
        above = [floor for floor in self.requests if floor > self.currentFloor]
        below = [floor for floor in self.requests if floor < self.currentFloor]
        
        if self.direction == "up":
            # Continue going up if there are requests above
            if above:
                self.direction = "up"
                print(f"Continuing UP, serving floors: {sorted(above)}")
            elif below:
                # No more requests above, reverse direction
                self.direction = "down"
                print(f"Reversing to DOWN, will serve floors: {sorted(below, reverse=True)}")
            else:
                self.direction = "idle"
                
        elif self.direction == "down":
            # Continue going down if there are requests below
            if below:
                self.direction = "down"
                print(f"Continuing DOWN, serving floors: {sorted(below, reverse=True)}")
            elif above:
                # No more requests below, reverse direction
                self.direction = "up"
                print(f"Reversing to UP, will serve floors: {sorted(above)}")
            else:
                self.direction = "idle"
                
        else:  # direction == "idle"
            # Choose initial direction based on closest request
            if above and below:
                # Choose direction with closer request
                closestAbove = min(above)
                closestBelow = max(below)
                if (closestAbove - self.currentFloor) <= (self.currentFloor - closestBelow):
                    self.direction = "up"
                    print(f"Starting UP (closer request at {closestAbove})")
                else:
                    self.direction = "down"
                    print(f"Starting DOWN (closer request at {closestBelow})")
            elif above:
                self.direction = "up"
                print(f"Starting UP, serving floors: {sorted(above)}")
            elif below:
                self.direction = "down"
                print(f"Starting DOWN, serving floors: {sorted(below, reverse=True)}")
    
    def step(self):
        """Execute one step of elevator simulation using LOOK algorithm"""
        # If we're at a requested floor, stop and open doors
        if self.currentFloor in self.requests:
            self.requests.remove(self.currentFloor)
            print(f"✓ Arrived at requested floor {self.currentFloor}")
            self.openDoors()
            # In real simulation, doors would stay open for a bit
            self.closeDoors()
            
        # Decide direction for next move using LOOK algorithm
        self.decideDirectionLook()
        
        # Move in the decided direction
        if self.direction == "up":
            self.moveUp()
        elif self.direction == "down":
            self.moveDown()
        elif self.direction == "idle":
            print("Elevator is idle")
    
    def status(self):
        """Print current elevator status"""
        requestsAbove = [f for f in self.requests if f > self.currentFloor]
        requestsBelow = [f for f in self.requests if f < self.currentFloor]
        
        print(f"Floor: {self.currentFloor}, Direction: {self.direction}, "
              f"Doors: {'Open' if self.doorsOpen else 'Closed'}")
        print(f"  Requests above: {sorted(requestsAbove)}")
        print(f"  Requests below: {sorted(requestsBelow, reverse=True)}")
        print(f"  All requests: {sorted(self.requests)}")


class Building:
    def __init__(self, numFloors):
        self.numFloors = numFloors
        self.elevator = Elevator(numFloors)
    
    def callElevator(self, floor):
        """Call elevator to a specific floor"""
        self.elevator.addRequest(floor)
    
    def getUserInput(self):
        """Get floor requests from user when elevator is idle"""
        print("\n" + "="*60)
        print(f"🛗 Elevator is idle on floor {self.elevator.currentFloor}. What would you like to do?")
        print("1. Request a floor (enter floor number)")
        print("2. Add multiple requests (e.g., '3,7,2,9')")
        print("3. Show elevator status")
        print("4. Exit simulation")
        print("="*60)
        
        while True:
            try:
                userInput = input("Enter your choice: ").strip()
                
                if userInput == "4":
                    return "exit"
                elif userInput == "3":
                    self.elevator.status()
                    continue
                elif userInput == "1":
                    floor = int(input(f"Enter floor number (1-{self.numFloors}): ").strip())
                    if 1 <= floor <= self.numFloors:
                        self.callElevator(floor)
                        return "continue"
                    else:
                        print(f"Please enter a floor between 1 and {self.numFloors}")
                
                elif userInput == "2":
                    floorsInput = input(f"Enter floor numbers separated by commas (1-{self.numFloors}): ").strip()
                    floors = [int(f.strip()) for f in floorsInput.split(",")]
                    validFloors = []
                    for floor in floors:
                        if 1 <= floor <= self.numFloors:
                            self.callElevator(floor)
                            validFloors.append(floor)
                        else:
                            print(f"Invalid floor: {floor}")
                    if validFloors:
                        print(f"Added requests for floors: {validFloors}")
                        return "continue"   
                # elif "," in userInput:
                #     # Multiple floor requests
                #     floors = [int(f.strip()) for f in userInput.split(",")]
                #     validFloors = []
                #     for floor in floors:
                #         if 1 <= floor <= self.numFloors:
                #             self.callElevator(floor)
                #             validFloors.append(floor)
                #         else:
                #             print(f"Invalid floor: {floor}")
                #     if validFloors:
                #         print(f"Added requests for floors: {validFloors}")
                #         return "continue"
                # else:
                #     floor = int(userInput)
                #     if 1 <= floor <= self.numFloors:
                #         self.callElevator(floor)
                #         return "continue"
                #     else:
                #         print(f"Please enter a floor between 1 and {self.numFloors}")
            except ValueError:
                print("Please enter a valid number, comma-separated numbers, or choice")
    
    def simulateInteractive(self):
        """Run interactive simulation that waits for user input when idle"""
        print(f"🏢 Starting LOOK Algorithm Elevator Simulation!")
        print(f"Building has {self.numFloors} floors")
        print("The LOOK algorithm continues in one direction until no more requests,")
        print("then reverses direction (like looking back and forth)")
        print("=" * 60)
        
        stepCount = 0
        
        while True:
            stepCount += 1
            print(f"\n--- Step {stepCount} ---")
            self.elevator.status()
            
            # Check if elevator is idle and has no requests
            if self.elevator.direction == "idle" and not self.elevator.requests:
                result = self.getUserInput()
                if result == "exit":
                    print("👋 Simulation ended by user")
                    break
                elif result == "continue":
                    continue  # Process the new request
            
            self.elevator.step()
    
    def simulateSteps(self, steps):
        """Run simulation for a number of steps (non-interactive)"""
        print(f"Starting LOOK algorithm simulation for {steps} steps")
        print("=" * 50)
        
        for step in range(steps):
            print(f"\n--- Step {step + 1} ---")
            self.elevator.status()
            self.elevator.step()
            
            # Stop if elevator is idle and no requests
            if self.elevator.direction == "idle" and not self.elevator.requests:
                print("\n✅ Elevator has completed all requests!")
                break


# Example usage and testing
if __name__ == "__main__":
    print("🛗 LOOK Algorithm Elevator Simulation")
    print("Choose simulation mode:")
    print("1. Interactive mode (user input when idle)")
    print("2. Pre-programmed demo showing LOOK algorithm")
    
    while True:
        try:
            choice = input("Enter 1 or 2: ").strip()
            if choice in ["1", "2"]:
                break
            print("Please enter 1 or 2")
        except KeyboardInterrupt:
            print("\nExiting...")
            exit()
    
    # Create a 10-floor building
    building = Building(10)
    
    if choice == "1":
        # Interactive mode
        building.simulateInteractive()
    
    else:
        # Pre-programmed demo to show LOOK algorithm behavior
        print("\n🎯 Running LOOK algorithm demo...")
        print("This will show how LOOK handles requests in both directions")
        
        # Add requests that demonstrate LOOK behavior
        print("\n📝 Adding requests: floors 8, 3, 6, 2, 9, 4")
        building.callElevator(8)  # up
        building.callElevator(3)  # down  
        building.callElevator(6)  # up
        building.callElevator(2)  # down
        building.callElevator(9)  # up
        building.callElevator(4)  # up
        
        # Run simulation
        building.simulateSteps(20)
        
        print(f"\n{'='*50}")
        print("🔄 Adding more requests to show direction reversal:")
        
        # Add more requests to show reversal
        building.callElevator(7)
        building.callElevator(1)
        building.callElevator(5)
        
        # Continue simulation
        building.simulateSteps(15)