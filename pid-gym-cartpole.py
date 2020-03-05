#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 08:50:31 2020

@author: Tarik Hoshan
"""

from simple_pid import PID
import gym

X_LIMIT = 0.2 # Define boundary within which the cart is allowed to roam
              # freely. Decreasing this value too much will cause instability
              # as the cart will keep bumping on this invisible boundary
              # and cause the cart to be pushed in a way that overrides the
              # PID controller.

def run_cart():
    env = gym.make("CartPole-v1")
    
    # Let this thing run forever. This is a hack as the _max_episode_steps
    # class variable is meant to be private.
    env._max_episode_steps = 2 ** 63
    
    # Instantiate the PID controller. The setpoint represents an angle of zero
    # meaning that the pole is vertical.
    pid = PID(1, 0.2, 0.1, setpoint=0)
    
    observation = env.reset()
    while True:
        env.render()
      
        # Get the angle and x coordinate
        angle = observation[2]
        x = observation[0]
         
        # Use the angle as the control variable.
        control = pid(angle)
      
        # Translate the control returned by the PID controller to a
        # left / right action on the cart.
        action = control_to_action(control, angle, x)
      
        # Simulation step, returning the new state of the cart-pole.
        observation, reward, done, info = env.step(action)
         
        # print state on the screen
        print((observation, reward, done, info))
    
        # Either failed or you have died waiting for this thing to finish    
        if done:
            env.close()
            break

def control_to_action(control, angle, x):
    # The PID ensures the pole does not fall. However, the cart could drift
    # too much towards the left or the right. When a certain limit is
    # exceeded, overwrite the PID control by doing the following:   
    # - if the cart is too much to the right and the pole is leaning towards
    #   the right, push the cart towards the right to tilt the pole back to
    #   the left. This will have the side effect of the PID moving the cart
    #   towards the left to keep the pole from falling.
    if x > X_LIMIT and angle > 0:
        return 1
    # - if the cart is too much to the left and the pole is leaning towards
    #   the left, push the cart towards the left to tilt the pole back to
    #   the right. This will have the side effect of the PID moving the cart
    #   towards the right to keep the pole from falling.
    elif x < -X_LIMIT and angle < 0:
        return 0

    # The cart is within the acceptable x boundaries. Apply the PID control.
    
    # If the control is positive, the angle needs to be increased, i.e. the
    # pole has to be pushed towards the right by pushing the cart towards the
    # left with an action = 0; and vice verca.
    action = 0 if control > 0 else 1 
    return action
    
if __name__ == '__main__':
    run_cart()




