# Presentation Report: Numerical Methods for Solving Differential Equations

This report describes the contents, structure, and pedagogical flow of the Manim presentation defined in `presentation/main.py` and its companion scenes. The presentation is a guided comparison of Euler-based methods and Runge-Kutta methods, starting from a concrete rocket-physics motivation, moving through a simple test ODE, and ending with an application example that uses the same ideas on a hobby rocket model.

## High-Level Purpose

The presentation is built to answer a single question: how do different numerical methods behave when solving differential equations, and why is RK4 usually preferred over simpler Euler methods?

The narrative is intentionally progressive:

1. Introduce the topic and the comparison between methods.
2. Motivate the differential equation with a rocket mass and momentum problem.
3. Show how Euler methods approximate a smooth solution and why they drift.
4. Present RK4 as a much more accurate explicit method.
5. Derive RK4 from a general four-stage method and matching conditions.
6. Visualize the space of RK4-like methods and the error landscape.
7. Apply the methods to a hobby rocket velocity model and compare numerical error.

## Shared Visual Language

The presentation uses a consistent color scheme defined in `presentation/theme.py`:

- `exact_solution`: white
- `forward_euler`: blue
- `backward_euler`: red
- `rk4`: green
- `highlight`: yellow
- `k1`: orange
- `k2`: teal
- `k3`: purple
- `k4`: maroon

Headers are placed in the upper-left corner through a helper named `create_header`, and most slides use a single dominant title line with stepwise reveals beneath it. The presentation relies heavily on `next_slide()` pauses, so many scenes are designed as animated lecture segments rather than static slides.

## Slide-by-Slide Content

### 1. Title Card

The opening slide presents the title:

- **Numerical Methods for solving differential equations**

It is accompanied by the subtitle:

- **Comparison of Euler and Runge-Kutta Methods in theoretical cases and practical applications**

The author line reads:

- **Jakub Kowal, 2026**

This slide establishes the topic and frames the talk as both theoretical and applied.

### 2. Problem: Rocket Trajectory

This section introduces the physical motivation for the rest of the presentation: a rocket with changing mass during fuel burn.

The slide builds a stylized rocket diagram from basic geometric shapes:

- body rectangle
- nose cone triangle
- side fins
- engine trapezoid
- orange exhaust flare
- velocity vector upward from the rocket
- exhaust velocity vector downward from the nozzle

The math content starts with the rocket mass model:

- $M(t) = M_{dry} + M_{fuel}(t)$
- $M(t)$ is described as a non-increasing function, so $dM(t)/dt \le 0$
- initial conditions are shown as $M(0) = M_{dry} + M_{fuel_0}$, $v(0) = 0$, and $P|_{t=0} = 0$

The fuel mass is then specified as a piecewise function:

- $M_{fuel}(t) = M_{fuel_0} (1 - t/t_{burn})^2$ for $0 \le t \le t_{burn}$
- $M_{fuel}(t) = 0$ for $t > t_{burn}$
- burn time is defined as $t_{burn} = M_{fuel_0} / q$
- a concrete burn rate is given as $q = 0.3$

The slide then transitions from initial conditions to the general momentum expression at time $t$:

- $P|_t = M(t) \cdot \vec{v}(t)$

It continues to the next instant $t + dt$ and expands the mass update in a differential form, highlighting the change in mass as the exhausted fuel term.

Several annotations appear during this derivation:

- the numerator of the mass change is labeled as the mass of exhausted fuel
- $dM(t)/dt$ is isolated as the derivative term
- the rocket velocity vector and exhaust velocity vector are distinguished visually
- the exhaust velocity is explicitly shown relative to the rocket

The momentum equation is then expanded into a more complete expression for $P|_{t+dt}$, combining the rocket body velocity and exhaust contribution.

This section is the physical anchor for the entire presentation: it explains why differential equations arise naturally in the rocket problem and why numerical methods are needed.

### 3. Euler’s Method

This section switches to a simple 1D test equation so the behavior of numerical integration can be seen without the complexity of rocket dynamics.

The slide begins with a smooth test curve defined by:

- exact solution: $y(t) = \sin(t) + 0.5t + 1$
- derivative: $dy/dt = f(t,y) = \cos(t) + 0.5$

The axes are labeled $t$ and $y(t)$, and a starting point $(t_0, y_0)$ is marked on the curve.

#### Euler approximation

The forward Euler update is shown as:

- $y_{n+1} = y_n + \Delta t \cdot f(t_n, y_n)$

The animation steps through several iterations with a relatively large time step. For the first few steps, the presentation slows down to explain what is happening geometrically:

- the local tangent line is drawn at the current point
- the current point is emphasized
- a dashed extension of the tangent is shown
- $\Delta t$ and $\Delta y$ are highlighted as the step geometry
- the next Euler point is placed at the end of the tangent-based update

This creates the standard picture of Euler’s method as repeated tangent-line extrapolation.

#### Error accumulation

After several steps, the presentation overlays the numerical polygon against the exact curve and emphasizes that the approximation diverges significantly from the analytical solution.

This is followed by a short explanation of why the error occurs:

- Euler assumes the rate of change is constant across the whole step
- the true slope changes inside the interval

A moving tangent illustration reinforces the idea that slope variation is the core reason Euler drifts.

#### Forward Euler and Backward Euler

The slide then explicitly separates the two Euler variants.

Forward Euler is shown first with the formula and a completed path of step segments.

Backward Euler is then introduced with the implicit update:

- $y_{n+1} = y_n + \Delta t \cdot f(t_{n+1}, y_{n+1})$

The animation for backward Euler mirrors the forward Euler visual structure, but the slope is evaluated at the next time point. The presentation also shows a comparison polygon and notes that backward Euler is better than forward Euler, but still not precise.

This section’s main teaching point is that Euler methods are simple and intuitive, but step-size sensitivity and slope variation limit their accuracy.

### 4. Runge-Kutta 4th Order (RK4)

This section uses the same test equation as the Euler section, but now demonstrates a much more accurate explicit method.

The ODE is repeated in the corner, and the RK4 formula is built stage by stage:

- $k_1 = f(t_n, y_n)$
- $k_2 = f(t_n + \Delta t/2, y_n + (\Delta t/2)k_1)$
- $k_3 = f(t_n + \Delta t/2, y_n + (\Delta t/2)k_2)$
- $k_4 = f(t_n + \Delta t, y_n + \Delta t k_3)$
- $y_{n+1} = y_n + (\Delta t/6)(k_1 + 2k_2 + 2k_3 + k_4)$

The method is visualized as a sequence of stage evaluations:

- a first slope at the starting point
- a midpoint estimate using $k_1$
- a second midpoint estimate using $k_2$
- an endpoint estimate using $k_3$
- a weighted combination of the four stages

Colored arrows and intermediate dots show where each stage is evaluated. The animation deliberately exposes the geometry behind the method rather than presenting the formula as a black box.

#### Accuracy emphasis

After several steps, the presentation overlays the RK4 path with the exact solution and stresses that the approximation closely follows the analytical curve.

The filled area between the RK4 approximation and the exact curve is used to give a visual sense of the error magnitude, which is much smaller than in the Euler sections.

#### Weight question

The slide then isolates the weighted sum in the RK4 formula and asks:

- Why we use these weights?

This question drives the transition into the derivation section.

### 5. RK4 Derivation

This is the most mathematically detailed section of the presentation. It explains where the classic RK4 coefficients come from instead of treating them as magic constants.

#### The classic RK4 form

The derivation begins by restating the canonical method and highlighting the role of the fractional coefficients in the stage formulas and in the final weighted sum.

#### General four-stage method

The presentation then replaces the fixed RK4 coefficients with a general 4-stage Runge-Kutta template:

- stage locations $c_2$, $c_3$, $c_4$
- internal weights $a_{ij}$
- output weights $b_1$, $b_2$, $b_3$, $b_4$

The goal is stated explicitly:

- solve for $a$, $b$, and $c$

#### Taylor expansion and coefficient matching

Next, the method is compared against the Taylor expansion of the true solution:

- $y_{true} = y_n + \Delta t y' + \dots + \Delta t^4/24 \; y^{(4)} + O(\Delta t^5)$
- $y_{RK} = y_n + \Delta t(b_1k_1 + b_2k_2 + b_3k_3 + b_4k_4)$

The audience is told that the coefficients must be matched up to fourth order.

#### Order conditions

The presentation then displays the classic fourth-order conditions, grouped by order and consistency constraints. These include equations such as:

- $\sum_i b_i = 1$
- $\sum_i b_i c_i = 1/2$
- $\sum_i b_i c_i^2 = 1/3$
- $\sum_{i,j} b_i a_{ij} c_j = 1/6$
- and the higher-order fourth-order conditions

Additional consistency conditions are shown for the stage sums.

The key conclusion is that there are 11 equations but 13 unknowns, meaning the system is underdetermined and has degrees of freedom.

#### Classical choice and weight collapse

The presentation then explains that the classic RK4 method is a particular choice inside this family:

- $c_2 = 1/2$
- $c_3 = 1/2$

This leads to the standard weights:

- $b_1 = 1/6$
- $b_2 = 1/3$
- $b_3 = 1/3$
- $b_4 = 1/6$

The slide explicitly connects these weights to Simpson’s 1/3 rule:

- Simpson’s weights: 1 - 4 - 1
- RK4 weights: 1 - 2 - 2 - 1

#### PLTE

The last part of the derivation introduces the Principal Local Truncation Error (PLTE):

- the remaining $O(\Delta t^5)$ term is the PLTE
- it measures the inherent error introduced in a single step
- different $(c_2, c_3)$ pairs change the magnitude of this error

This section establishes that RK4 is not just one formula, but one member of a wider design space.

### 6. Mapping the Landscape (log10 Error)

This section visualizes how different RK4-like coefficient choices affect error.

The slide shows a heatmap over the $(c_2, c_3)$ plane with axes labeled:

- $c_2$
- $c_3$

The background image is a precomputed heatmap, and a colorbar is added with the label:

- log10(Error)

The slide marks several notable points and curves:

- Classic RK4
- Kutta 3/8
- Ralston’s method
- RK3 residuals on a hyperbola-like curve

The presentation narrates these points with brief annotations:

- classic RK4 is the reference point
- Kutta 3/8 is described as minimizing error for the average ODE case
- Ralston’s method is described as good for edge-case ODEs

The curve and the highlighted points suggest that method choice is not arbitrary; different coefficient sets lead to different error behavior.

### 7. Application to Hobby Rocket

The final major section returns to the original rocket motivation and applies the numerical methods to a practical model.

#### Problem setup

The slide lists the rocket parameters:

- $M_{dry} = 1.0$ kg
- $M_{fuel_0} = 0.9$ kg
- $q = 0.3$ kg/s
- $t_{burn} = 3.0$ s
- $v_e = 300$ m/s

It then defines the working equations:

- $M(t) = 1.0 + 0.9(1 - t/3)^2$
- $M'(t) = -0.6(1 - t/3)$
- $a(t) = -(M'(t)/M(t))v_e - g$
- $g = 9.81$ m/s$^2$

#### Velocity comparison

The graph compares velocity over time using a step size of $h = 2.0$ s.

The exact velocity is defined using the rocket mass and gravity term, and the graph overlays numerical solutions for:

- Forward Euler
- Backward Euler
- RK4

A legend is shown on the right, and each method’s accumulated error is displayed as an error label.

The animation builds each numerical solution step by step and shades the area between the exact and approximate curves.

#### Interpretation

The point of this section is twofold:

1. Show that the same numerical methods used earlier can be applied to a realistic physical model.
2. Demonstrate that error differences remain visible even in a practical engineering context.

The presentation computes the approximate area under each numerical curve and compares it to the exact area, reporting the difference as an error metric.

## Overall Narrative Structure

The presentation is designed as a teaching sequence rather than a catalog of formulas. Its structure is cumulative:

- It starts with a real physical system that naturally leads to differential equations.
- It then reduces to a simple test problem so the audience can inspect numerical behavior clearly.
- It contrasts Euler methods with RK4 on the same ODE.
- It derives RK4 from first principles and shows that the standard coefficients are not arbitrary.
- It visualizes the method family and the error landscape.
- It ends with a real application where method choice affects practical results.

## Summary of Main Messages

- Differential equations arise naturally in rocket motion and variable-mass systems.
- Euler methods are easy to understand but accumulate noticeable error.
- Backward Euler improves behavior, but it still does not match RK4 precision.
- RK4 works by sampling the slope at four carefully chosen stage points.
- The standard RK4 coefficients are one valid solution in a larger coefficient family.
- Different stage choices affect local truncation error.
- The final rocket example shows why high-order methods matter in practice.

## File-Level Scope

The presentation is assembled from the following scene modules:

- `presentation/title.py`
- `presentation/problem.py`
- `presentation/euler.py`
- `presentation/rk4.py`
- `presentation/rk4_explain.py`
- `presentation/rk4_landscape.py`
- `presentation/application.py`

The entry point `presentation/main.py` runs these scenes in order, using slide wipes between major sections.
