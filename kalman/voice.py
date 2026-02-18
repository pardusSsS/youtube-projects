import asyncio
import edge_tts
import os

# Narration Scripts for Kalman Filter Animation
SCRIPTS = {
    "Part1": """
Kalman Filter.
See through the noise.
""",

    "Part2": """
We live in a noisy world.
Every sensor, every measurement, carries some degree of error.
Look at this graph. The smooth cyan line is the true position of an object.
But what we actually measure are these scattered pink dots, noisy and unreliable.
The question is: how do we find the truth hidden inside all this noise?
""",

    "Part3": """
Every sensor lies, but each one lies differently.
GPS gives you position, but with three to five meters of uncertainty.
Accelerometers drift over time, slowly accumulating error.
Gyroscopes suffer from bias and jitter, adding random fluctuations.
Each sensor has its own unique noise profile, and none of them can be fully trusted alone.
""",

    "Part4": """
Now imagine a drone trying to navigate using these noisy sensors.
The smooth cyan line shows the ideal path it should follow.
But the pink line shows what the sensors actually report: a wobbly, uncertain trajectory.
Watch as the drone follows this noisy measured path. It jitters and deviates constantly.
Can we somehow combine these imperfect sensors to reconstruct a smooth and accurate path?
""",

    "Part5": """
What if we could predict where we'll be next?
This is the core idea behind the Kalman Filter.
On one side, we have a physical model that understands the laws of motion. It's smooth, but it drifts over time.
On the other side, we have sensor data. It's noisy, but it's grounded in reality.
The Kalman Filter combines both, producing the optimal estimate.
This fusion of model and measurement is what makes it so powerful.
""",

    "Part6": """
To use the Kalman Filter, we first need to define what we're tracking. This is called the State Vector.
For a simple example, our state vector x contains two things: position and velocity.
Think of a car on a number line. Its position tells us where it is, and its velocity tells us how fast it's moving.
Together, they form a complete description of the car's state.
In our example, position equals two and velocity equals three meters per second.
Watch as the car moves along the line, its state changing over time.
""",

    "Part7": """
The prediction step answers one question: where do I think I will be next?
The equation is straightforward. The predicted state x hat equals the transition matrix F times the current state, plus the control input matrix B times the control u.
F moves our state forward in time using the known physics.
B accounts for any external inputs, like pressing the throttle.
On the timeline, you can see how the filter projects from the current position to a predicted future position.
""",

    "Part8": """
But here's the catch: every prediction adds uncertainty.
The predicted covariance P grows with each step.
The equation shows how: the covariance propagates through the transition matrix F, and process noise Q gets added on top.
Q represents all the things our model doesn't perfectly capture, like wind gusts or road bumps.
Watch these ellipses grow larger with each time step. The further we predict without a measurement, the less certain we become.
This is why prediction alone is never enough.
""",

    "Part9": """
Then, a new sensor reading arrives. This is the measurement step.
The measurement z equals the observation matrix H times the true state, plus measurement noise v.
H maps our state into what the sensor actually sees.
And v represents the inherent noise in that sensor.
Now we have two pieces of information: our prediction, shown as the cyan ellipse, and the new measurement, shown in pink.
They don't agree perfectly. So which one should we trust more?
""",

    "Part10": """
This is where the Kalman Gain comes in. It's the trust balancer between model and sensor.
The formula calculates K based on the predicted covariance and the measurement noise R.
Think of it as a slider. When K is close to zero, we trust the model's prediction more.
When K is close to one, we trust the sensor measurement more.
The Kalman Gain automatically adjusts based on the relative uncertainties.
If the sensor is very accurate, K goes up. If the model is very reliable, K stays low.
This adaptive balancing is what makes the Kalman Filter optimal.
""",

    "Part11": """
Now comes the update step, where prediction and measurement are fused together.
The updated state equals the prediction plus the Kalman Gain times the innovation.
The innovation is the difference between what we measured and what we expected. It's the surprise.
The covariance also gets updated, shrinking as we incorporate new information.
Watch the visual below. The large cyan prediction ellipse and the pink measurement circle merge into a much smaller orange ellipse.
This is the key insight: by combining both sources, we get an estimate that's better than either one alone.
""",

    "Part12": """
The Kalman Filter operates as a continuous cycle.
First, we initialize with our best guess of the state and its uncertainty.
Then we predict, projecting the state forward using our model.
Next, a measurement arrives from the sensors.
Finally, we update, fusing the prediction with the measurement.
And then the cycle repeats, over and over.
With each iteration, the estimate gets refined. Predict, measure, update. Predict, measure, update.
This elegant loop is the heartbeat of the Kalman Filter.
""",

    "Part13": """
Let's see the filter in action.
The white line shows the true position of an object over time.
The pink dots are the noisy measurements from the sensor.
And the orange line is the Kalman Filter's estimate.
Notice how the estimate starts rough, but quickly converges toward the true position.
Even though the measurements are scattered and noisy, the filter smoothly tracks the underlying signal.
The estimate converges to the truth. This is the power of optimal estimation.
""",

    "Part14": """
Here are the complete Kalman Filter equations, all in one place.
The predict phase has two equations: one for the state, and one for the covariance.
The update phase has three: the Kalman Gain calculation, the state update, and the covariance update.
These five equations are everything you need. They are elegant, recursive, and computationally efficient.
This compact set of equations has been solving estimation problems for over sixty years.
""",

    "Part15": """
The original Kalman Filter, developed in nineteen sixty, is the Linear Kalman Filter.
It works perfectly when the system dynamics are linear, meaning the equation y equals A x plus b.
Its applications include constant velocity tracking, temperature estimation, and simple signal filtering.
There are two key conditions: the system must be linear, and the noise must be Gaussian.
When these conditions are met, the Linear Kalman Filter provides the mathematically optimal solution.
""",

    "Part16": """
But what happens when the system is nonlinear?
The Extended Kalman Filter, or EKF, handles this by linearizing the nonlinear function at the current operating point.
It computes the Jacobian, which is the partial derivative of the function, to create a local linear approximation.
The pink curve represents the true nonlinear dynamics, while the cyan tangent line is the linearization.
The EKF then applies the standard Kalman Filter equations to this linearized system.
It's an approximation, but it works remarkably well for mildly nonlinear problems.
""",

    "Part17": """
For highly nonlinear systems, there's an even better approach: the Unscented Kalman Filter, or UKF.
Instead of linearizing, it uses a clever trick called sigma points.
These carefully chosen points capture the mean and spread of the current distribution.
Each sigma point is passed through the nonlinear function individually.
After the transformation, the mean and covariance are recomputed from the transformed points.
No Jacobians are needed, and the UKF provides better accuracy than the EKF for strongly nonlinear systems.
""",

    "Part18": """
The Kalman Filter is everywhere in the real world.
GPS navigation fuses satellite signals with inertial sensors to give you a smooth location.
Self-driving cars use it to track pedestrians, vehicles, and lane markings.
The Apollo spacecraft relied on the Kalman Filter for lunar navigation.
In finance, it helps predict stock prices and market trends.
Robotics uses it for simultaneous localization and mapping, known as SLAM.
And weather forecasting depends on it to predict temperature, pressure, and wind patterns.
From your phone to outer space, the Kalman Filter is working behind the scenes.
""",

    "Part19": """
Let's recap the key ideas.
First, sensors are noisy. We can never fully trust raw data.
Second, the Kalman Filter combines a mathematical model with real measurements.
Third, the cycle is simple: predict where you'll be, then update with sensor data.
Fourth, the Kalman Gain automatically balances trust between model and sensor.
And fifth, the estimate converges to the true state over time.
There are three main types: the Linear KF for simple systems, the EKF for nonlinear dynamics using Jacobians, and the UKF using sigma points for the most challenging cases.
""",

    "Part20": """
Thank you for watching!
If you found this helpful, please like this video and subscribe for more deep dives into engineering and mathematics.
The Kalman Filter: optimal estimation from noisy data.
Share this with someone who wants to understand how modern technology sees through the noise.
""",

    "KalmanShort": """
Every sensor lies. GPS drifts. Accelerometers wobble. Gyroscopes jitter.
So how do self-driving cars, rockets, and your phone know exactly where they are?
The answer: the Kalman Filter.
It combines two things: a physical model that predicts the future, and sensor data that measures reality.
The cycle is simple. Predict where you'll be. Measure what the sensor says. Then update, fusing both into the best possible estimate.
The Kalman Gain decides how much to trust each source. Low gain? Trust the model. High gain? Trust the sensor.
Watch what happens. The noisy pink dots are raw sensor data. But the orange line, the Kalman estimate, smoothly tracks the truth.
That's the power of optimal estimation. From GPS to spacecraft to stock markets, the Kalman Filter sees through the noise.
Like and subscribe for more.
"""
}

VOICE = "en-US-GuyNeural"

async def generate_voiceover():
    if not os.path.exists("voiceovers"):
        os.makedirs("voiceovers")

    print(f"--- Seslendirme Başlıyor: {VOICE} ---")

    for part, text in SCRIPTS.items():
        filename = f"voiceovers/{part}.mp3"
        print(f"İşleniyor: {part}...")
        
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(filename)
    
    print("\n--- İŞLEM TAMAMLANDI! ---")
    print("'voiceovers' klasörünü kontrol et.")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())
