#!/usr/bin/env python
import subprocess
import os
import sys

#ensure matplotlib is
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Error: matplotlib is not installed. Please install it using: pip install matplotlib")
    sys.exit(1)

def run_simulation(bin_path):
    """run the rocket c simulation wi..."""
    if not os.path.exists(bin_path):
        print(f"Error: Binary '{bin_path}' not found. Did you run 'make'?")
        sys.exit(1)
        
    print(f"Running {bin_path} -r ...")
    result = subprocess.run([bin_path, "-r"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Simulation failed!")
        print(result.stderr)
        sys.exit(result.returncode)
        
    return result.stdout

def parse_csv(raw_output):
    """parse the csv output from the ..."""
    times = []
    velocities = []
    masses = []
    machs = []
    
    lines = raw_output.strip().split('\n')
    
    #process data lines (
    for line in lines[1:]:
        if not line or line.strip() == "":
            continue
            
        parts = line.split(',')
        if len(parts) >= 4:
            times.append(float(parts[0]))
            velocities.append(float(parts[1]))
            masses.append(float(parts[2]))
            machs.append(float(parts[3]))
            
    return times, velocities, masses, machs

def plot_results(t, v, m, mach):
    """create a 1x3 grid of plots usi..."""
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Rocket Trajectory Analysis (Velocity Only)', fontsize=16)
    
    #plot velocity
    axs[0].plot(t, v, 'r-', linewidth=2)
    axs[0].set_title('Velocity vs Time')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Velocity (m/s)')
    axs[0].grid(True)
    
    #plot mass
    axs[1].plot(t, m, 'g-', linewidth=2)
    axs[1].set_title('Mass vs Time')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Mass (kg)')
    axs[1].grid(True)
    
    #plot mach
    axs[2].plot(t, mach, 'm-', linewidth=2)
    axs[2].set_title('Mach Number vs Time')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Mach (#)')
    axs[2].grid(True)
    
    plt.tight_layout()
    
    #save the plot
    output_path = os.path.join(os.path.dirname(__file__), 'rocket_plot.png')
    plt.savefig(output_path, dpi=300)
    print(f"Plot successfully saved to: {output_path}")

def main():
    #set the expected pat
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    bin_path = os.path.join(project_root, 'bin', 'rocket_complex')
    
    #1. run simulation
    raw_output = run_simulation(bin_path)
    
    #2. parse results
    t, v, m, mach = parse_csv(raw_output)
    
    if not t:
        print("Error: No data was parsed from the simulation.")
        sys.exit(1)
        
    print(f"Successfully processed {len(t)} data points.")
    
    #3. create plots
    plot_results(t, v, m, mach)

if __name__ == "__main__":
    main()
