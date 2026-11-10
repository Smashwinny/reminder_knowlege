# Experiment results (machine-written)
- Python 3.13.5, elapsed 0.055s
## Step 1 Geometry and timing
- 6 inch diameter = 0.1524 m. At 20,000 RPM, 1/rev = 333.3333 Hz, period = 3.0000 ms.
- Tip speed = 159.59 m/s = 357.0 mph = 574.5 km/h, Mach 0.465 (a=343 m/s assumed).
- 300 acc/dec per s at 20,000 RPM is 0.900 events/rev, not exactly 1. Exactly once-per-rev at 300 Hz would be 18000 RPM.
- 0.2 ms → 24.00°. 2 ms → 240.00°. Exactly 20° → 0.1667 ms.
- moteus 15–30 kHz ISR: 45.0–90.0 updates/rev. MCOUT 400 Hz: 1.20 packets/rev.
## Step 2 Kinematics
- θ = ζ tan(α). At 45°, coupling = 1. At 30° 0.5774, at 60° 1.7321.
- An assumed 8° lag becomes 8.00° pitch at 45°, 4.62° at 30°, 13.86° at 60°.
## Step 3 Dynamics (ASSUMED model)
- I=6.400e-06 kg m², wn=1.4 Ω (466.7 Hz), ζ_damp=0.25, δΩ/Ω=4%.
- Lag / pitch amplitude = 1.929°, phase vs acceleration = 143.9°.
- Mean thrust Fz = 16.978 N. Side force = 1.3646 N, tilt = 4.595°. Baseline side force (no cyclic) = 5.24e-17 N.
## Step 4 160 Hz
- Ω = 333.33 Hz, Ω/2 = 166.67 Hz, |160−Ω/2| = 6.67 Hz.
- Doubling EI moves a 160 Hz flap mode to 226.3 Hz (scaling only).
## Step 5 MCOUT protocol
- CRC test vector '123456789' → 0x31C3 (expected 0x31C3): PASS.
- 84-byte round-trip CRC_ok=True, output_allowed=True; corrupted CRC_ok=False; missing INTERLOCK output_allowed=False; ESTOP output_allowed=False.
- Docs inconsistency: moteus guide SERIALx_PROTOCOL=50 vs ArduPilot README =51 at pinned SHAs.
## Step 6 Comparisons
- Disk area 6 inch = 0.01824 m², PULSAR 37.6 cm = 0.11104 m², ratio = 6.087 (supports the 'over six times less area' claim).
- Paulos 2013 38.6 cm area ratio vs Bird = 6.42×; that vehicle used two motors.
