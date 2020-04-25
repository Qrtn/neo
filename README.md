# Neo (R3)

> *"What are you trying to tell me? That I can dodge bullets?"*
>
> *"No, Neo. I'm trying to tell you that when you're ready, you won't have to."*

![Neo](https://github.com/yousefa00/SPIMBOT/blob/r3/plan/logo.png?raw=true)

### *A new era of SPIMbot*

- Geometric accuracy
- Economic efficiency
- Spatial awareness
- Concurrency
- Instruction set virtualization
- Source code generation

## Strategy

**Geometric accuracy:** Neo is built on the fundamental premise that it is possible to navigate to and shoot all 16 hosts on the map without deviating from a fixed path. This eliminates the need for scanning. Instead, Neo relies on a sequence of repeating instructions that set the bot's angle and velocity at precisely-timed intervals.

**Economic efficiency:** Neo knows when to shoot and when not to shoot. By checking the arena map before attempting to capture a host, Neo can determine the exact number of UDP packets to send, depending on whether the host is neutral or hostile.

**Spatial awareness:** Whenever Neo is hit by an enemy UDP packet and reboots, he immediately identifies which host he has respawned at. Based on the host's location, Neo moves back into its designated path without missing a beat.

## Implementation

**Concurrency:** Neo multitasks seamlessly between solving puzzles and operating the bot. This is done by placing all movement, shooting, and odometry-related code into kernel space. Whenever the bot must wait while it is traveling, control is given back to user space code, which is constantly requesting and solving puzzles. *This means that no cycles are wasted waiting for any event to occur.*

**Instruction set virtualization:** At the core of Neo's precise movements is a custom instruction set called the *Intermediate Movement Language* (IML). The IML consists of 4-byte wide integer instructions that tell the bot to set its angle or velocity, shoot UDP packets, check the status of hosts, or delay a certain number of cycles (handing control back to the puzzle solver) before executing the next instruction. Instructions in IML are stored in the data segment of the SPIMbot, and can be expressed much more concisely than they would be in MIPS assembly. IML is also simple enough that its interpreter can be implemented fairly easily in MIPS.

**Source code generation:** Designing an entire movement plan in IML is better than writing in MIPS, but it is still far too tedious for designing the bot's path. Neo's initial movement plans were written in the *Advanced Movement Language* (AML), which is translated by a Python program into IML. AML features versatile commands like `goto` and `chkshoot`, which compile into a series of angle, velocity, and other IML instructions. The AML compiler also has the advantage of being able to do precise geometric calculations while storing the bot's actual position at each step in full precision. This is critical because SPIMbots can only move at angles that are integer degrees.

While finalizing Neo's movement plan, one final abstraction on top of AML came into place: *Path Schema*, a high-level sequence of the positions Neo will be in and the targets it will shoot during one orbit around the map. Path Schema was primarily useful because it automatically generated the AML that executes when Neo needs to restart its path at a particular host. In addition, Path Schema had useful utilities that could reflect and manipulate sequences of locations. Since the map is symmetric across two axes, and Neo's ultimate movement path had point symmetry, this proved useful in saving time and eliminating human error.
