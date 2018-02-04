# inconvenient_fluid_solver
Fully python based fluid solver.

Main purpose of this package is understanding the fluid solver.
For this purpose, this package does not use any 'convenient' extra module.
This package does not have any dependency, so there is no any external black box.
By same reason, this module was developed by python.
Of course and 'exactly' python is not good choice to develop fluid solver,
because fluid solver need to do heavy calculation.
But python is good for debugging and tracking the logic of simulation,
so development under python environment is intensional choice.

# Usage

One extra benefit of using python is jupyter-notebook.
Using jupyter-notebook and matplot at the same time, this environment is good to use for investigating navier-stroke process.
From jupyter-notebook, user can test fluid simulation with below process.

    import matplotlib.pyplot as plt
    %matplotlib inline

    from utils import NoiadUtils
    from solver import NoiadSolver, ParticleGenerator

    # full frame range
    frameNumber = 1200

    # generate particles
    pg = ParticleGenerator()
    pg.generateParticles()
    pg.generateGround()

    # prepare solver
    solver = NoiadSolver()

    # prepare figure
    fig = plt.figure()
    fig.set_figheight(5*int(frameNumber / 30))
    fig.set_figwidth(5)
    ax = fig.subplots(nrows=int(frameNumber / 30), ncols=1)

    # generate scene file per frame
    for t in range(1, frameNumber):
        
        for p in pg.particles:
            p.color.r = 0
            p.color.g = 0
            p.color.b = 0

        # add viscosity
        pg.particles = solver.addViscosityTerm(pg.particles)

        # add gravity
        pg.particles = solver.addGravityTerm(pg.particles)

        # move particles
        pg.particles = solver.moveParticle(pg.particles)

        # check collision
        pg.particles = solver.checkCollision(pg.particles)

        # calculate pressure value
        pg.particles = solver.calculateTemporaryPressure(pg.particles)

        # calculate pressure gradient
        pg.particles = solver.calculateModifiedAcceleration(pg.particles)

        # finalize particle position
        pg.particles = solver.finalizeParticlePosition(pg.particles)
        
        if t % 30 != 0:
            continue
        
        x = list()
        y = list()
        c = list()
        
        for p in pg.particles:
            x.append(p.position.x)
            y.append(p.position.y)
            if p.type == 1:
                c.append('b')
            else:
                c.append('r')

        row = ax[int(t / 30)]
        row.scatter(x, y, color=c)
                                                                                                                                
    plt.show()

# Jupyter-notebook sample
[notebok sample] jupyter_test.ipynb  

# Sample 

[Sample test clip1] https://www.youtube.com/watch?v=sW26bS7LHrg  

# License

* End User License Agreement (EULA)

# Changelog
