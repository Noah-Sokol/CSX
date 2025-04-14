class planet:

        
    def __init__(self, mass, posX, posY, veloX, veloY, accelX, accelY):
        self.mass = mass
        self.posX = posX
        self.posY = posY
        self.veloX = veloX
        self.veloY = veloY
        self.accelX = accelX
        self.accelY = accelY


    def step(self, dt, planets):
        '''
        Updates all non-static instance variables of planet with next step of dt

        args:
            self - planet - planet object
            dt - int - time passed in iteration
            planets - planets[] - list of all planets
        
        
        
        '''
        #reset accels so they can be calculated by the action from each planet
        self.accelX = 0
        self.accelY = 0

        #calc accels for each planet
        for planet in planets:
            if planet != self:
                #calc horizontal distance
                x_dist = planet.posX - self.posX
                #calc vertical distance
                y_dist = planet.posY - self.posY

                #calc overall distance
                r = (x_dist ** 2 + y_dist ** 2) ** .5
            
                #use inverse square law to calculate force
                force = 6.67E-11 * self.mass * planet.mass / r ** 2

                diag_accel = force/self.mass
                #add horizontal component of acceleration
                self.accelX += diag_accel * x_dist / r
                #add vertical component of acceleration
                self.accelY += diag_accel * y_dist / r

        #add velo which is accel times time passed
        self.veloX += self.accelX*dt
        self.veloY += self.accelY*dt

        #add to position 
        self.posX += self.veloX * dt
        self.posY += self.veloY * dt


    def __str__(self):
        #to string to print all instance variables
        return f"PosX: {self.posX} PosY: {self.posY} VeloX: {self.veloX} VeloY: {self.veloY} AccelX: {self.accelX} AccelY: {self.accelY}"



    
