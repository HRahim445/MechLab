import math
import mathOps
import checks

# mass spring system 
def mass_spring(t):
    mass = checks.get_data("mass_spring", "mass")
    amplitude = checks.get_data("mass_spring", "amplitude")
    spring_k = checks.get_data("mass_spring", "spring_constant")
    # retrieve all required data
    
    if checks.range_check(0, 10, amplitude) and checks.range_check(0, 10000, mass): # perform range check and return values
        angular_velocity = math.sqrt(spring_k / mass)
        # calculate the angular velocity
        return {
            "Mass": mass,
            "Amplitude": amplitude,
            "Spring Constant": spring_k,
            "Angular Velocity": angular_velocity,
            "Period of Oscillation": (2 * math.pi) / angular_velocity,
            "Maximum Velocity": amplitude * angular_velocity,
            "Maximum Acceleration": amplitude * (angular_velocity ** 2),
            "Position": amplitude * math.cos(angular_velocity * t),
            "Velocity": - amplitude * angular_velocity * math.sin (angular_velocity * t),
            "Acceleration": - amplitude * (angular_velocity) ** 2 * math.cos(angular_velocity * t)
        }
    else:
        return {
                "Error": "Invalid Parameters"
        }

# simple pendulum system
def pendulum(t):
    length = checks.get_data("pendulum", "length")
    gravity = checks.get_data("pendulum", "acceleration_to_gravity")
    initial_angular_disp = math.radians(checks.get_data("pendulum", "initial_angular_displacement"))
    # retrieve all required data
        
    # perform range check and return as appropriate
    if checks.range_check(0, 100, length) and checks.range_check(0, 100000, gravity) and checks.range_check(0, 90, initial_angular_disp):
        
        angular_freq = math.sqrt(gravity / length)
        # calculate angular oscillation frequency
        return {
            "Length": length,
            "Acceleration to Gravity": gravity,
            "Initial Angular Displacement": math.degrees(initial_angular_disp),
            "Angular Oscillation Frequency": angular_freq,
            "Period of Oscillation": (2 * math.pi) / angular_freq,
            "Angular Displacement": initial_angular_disp * math.cos(angular_freq * t),
            "Distance Travelled from Equilibrium": abs(length * math.cos(angular_freq * t)),
            "Angular Rotation Velocity": - initial_angular_disp * angular_freq *  math.sin(angular_freq * t),
            "Linear Speed": length * (- initial_angular_disp * angular_freq *  math.sin(angular_freq * t)),
            "Angular Acceleration": - initial_angular_disp * (angular_freq ** 2) * math.cos(angular_freq * t),
        }
    else:
        return {
                "Error": "Invalid Parameters"
        }
    
# projectile motion system
def projectile(t):
    launch_speed = checks.get_data("projectile", "launch_speed")
    launch_angle = checks.get_data("projectile", "launch_angle")
    gravity = checks.get_data("projectile", "acceleration_to_gravity")
    # retrieve all required data

    # convert angle to radians
    angle_rad = math.radians(launch_angle)

    # resolve initial velocity components
    vx = launch_speed * math.cos(angle_rad)
    vy = launch_speed * math.sin(angle_rad)

    # calculated quantities
    time_of_flight = (2 * vy) / gravity
    maximum_height = (vy ** 2) / (2 * gravity)
    projectile_range = vx * time_of_flight

    # perform range checks
    if (checks.range_check(0, 100, launch_speed)
        and checks.range_check(0, 90, launch_angle)
        and checks.range_check(0, 50, gravity)):

        # dynamic quantities
        height = vy * t - 0.5 * gravity * (t ** 2)
        horizontal_distance = vx * t

        # prevent negative height after landing
        if height < 0:
            height = 0
            horizontal_distance = projectile_range

        return {
            "Launch Speed": launch_speed,
            "Launch Angle": launch_angle,
            "Acceleration to Gravity": gravity,
            "Maximum Height": maximum_height,
            "Range": projectile_range,
            "Height": height,
            "Horizontal Distance": horizontal_distance
        }
    else:
        return {
            "Error": "Invalid Parameters"
        }


# planetary orbit system
def orbit(t):
    star_mass = checks.get_data("orbit", "star_mass")
    object_mass = checks.get_data("orbit", "object_mass")
    angular_velocity = checks.get_data("orbit", "angular_velocity")
    # retrieve all required data

    G = 6.67 * (10 **-11)

    # calculated quantities
    orbital_radius = ((G * star_mass) / (angular_velocity ** 2)) ** (1 / 3)
    orbital_period = (2 * math.pi) / angular_velocity

    # dynamic quantity
    angular_position = angular_velocity * t

    # perform range checks
    if (checks.range_check(1, (10**100), star_mass)
        and checks.range_check(1, (10**50), object_mass)
        and checks.range_check(0, 1, angular_velocity)):

        return {
            "Star Mass": star_mass,
            "Object Mass": object_mass,
            "Angular Velocity": angular_velocity,
            "Orbital Radius": orbital_radius,
            "Orbital Time Period": orbital_period,
            "Angular Position in Cycle": angular_position
        }
    else:
        return {
            "Error": "Invalid Parameters"
        }
        
# 1D time-evolving collision system
def collision(t):
    mass_a = checks.get_data("collision", "object_a_mass")
    mass_b = checks.get_data("collision", "object_b_mass")
    u_a = checks.get_data("collision", "object_a_initial_speed")
    u_b = checks.get_data("collision", "object_b_initial_speed")
    restitution = checks.get_data("collision", "coefficient_of_restitution")

    if not (
        checks.range_check(0.001, 100, mass_a)
        and checks.range_check(0.001, 100, mass_b)
        and checks.range_check(-100, 100, u_a)
        and checks.range_check(-100, 100, u_b)
        and checks.range_check(0, 1, restitution)
    ):
        return {"Error": "Invalid Parameters"}

    # initial positions
    x_a0 = -2.0
    x_b0 = 2.0

    # check if collision is possible
    relative_speed = u_a - u_b
    if relative_speed <= 0:
        return {"Error": "Objects will not collide"}

    # exact collision time
    collision_time = (x_b0 - x_a0) / relative_speed

    # collision positions (same for both)
    x_collision = x_a0 + u_a * collision_time

    # final velocities
    v_a = (
        (mass_a * u_a + mass_b * u_b - mass_b * restitution * (u_a - u_b))
        / (mass_a + mass_b)
    )

    v_b = (
        (mass_a * u_a + mass_b * u_b + mass_a * restitution * (u_a - u_b))
        / (mass_a + mass_b)
    )

    # kinetic energy loss
    initial_ke = 0.5 * mass_a * u_a**2 + 0.5 * mass_b * u_b**2
    final_ke = 0.5 * mass_a * v_a**2 + 0.5 * mass_b * v_b**2
    ke_loss = initial_ke - final_ke

    # impulse
    if t >= collision_time:
        impulse = mass_a * (v_a - u_a)
    else:
        impulse = 0

    if t < collision_time:
        pos_a = x_a0 + u_a * t
        pos_b = x_b0 + u_b * t
        speed_a = u_a
        speed_b = u_b
        phase = "Before Collision"
    else:
        pos_a = x_collision + v_a * (t - collision_time)
        pos_b = x_collision + v_b * (t - collision_time)
        speed_a = v_a
        speed_b = v_b
        phase = "After Collision"

    return {
        "Object A Position": pos_a,
        "Object B Position": pos_b,
        "Object A Mass": mass_a,
        "Object B Mass": mass_b,
        "Object A Speed": speed_a,
        "Object B Speed": speed_b,
        "Total Kinetic Energy Loss": ke_loss,
        "Impulse A on B": -impulse,
        "Impulse B on A": impulse,
        "Collision Phase": phase,
        "Coefficient of Restitution": restitution
    }


# kinematics system
def kinematics(t):
    a = checks.get_data("kinematics", "a")
    b = checks.get_data("kinematics", "b")
    c = checks.get_data("kinematics", "c")
    d = checks.get_data("kinematics", "d")
    # retrieve all required data

    if not (
        checks.range_check(-1000, 1000, a)
        and checks.range_check(-1000, 1000, b)
        and checks.range_check(-1000, 1000, c)
        and checks.range_check(-1000, 1000, d)
    ):
        return {"Error": "Invalid Parameters"}

    # create displacement function
    displacement_func = mathOps.Function([a, b, c, d])

    # dynamic values
    displacement = displacement_func.evaluate(t)
    velocity = displacement_func.firstDerivative(t)
    acceleration = displacement_func.secondDerivative(t)
    
    function_str = (
        f"{a}x³ "
        f"+ {b}x² "
        f"+ {c}x "
        f"+ {d}"
    )

    return {
        "Displacement Function": function_str,
        "Displacement": displacement,
        "Velocity": velocity,
        "Acceleration": acceleration
    }



