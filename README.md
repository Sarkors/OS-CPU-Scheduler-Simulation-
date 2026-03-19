# CPU Scheduler Simulation
### COP 4610 — Operating Systems | Florida Atlantic University

A Python simulation comparing three CPU scheduling algorithms — **FCFS**, **SJF**, and **MLFQ** — across 8 processes with mixed CPU and I/O bursts.

---

## Algorithms Implemented

| Algorithm | Type | Description |
|---|---|---|
| **FCFS** — First Come First Served | Non-preemptive | Processes are served in arrival order |
| **SJF** — Shortest Job First | Non-preemptive | Always picks the process with the shortest current CPU burst |
| **MLFQ** — Multilevel Feedback Queue | Preemptive | Three queues with priority and time quantum demotion |

### MLFQ Queue Structure
- **Queue 1** — Round Robin, quantum = 5 (all processes start here)
- **Queue 2** — Round Robin, quantum = 10
- **Queue 3** — FCFS, no quantum (lowest priority)

Processes are demoted down when their quantum expires. They are never promoted back up. When returning from I/O, a process goes back to whichever queue it was in before.

---

## Results Summary

| Metric | FCFS | SJF | MLFQ |
|---|---|---|---|
| Total Time | 648 | 668 | 596 |
| CPU Utilization | 85.34% | 82.78% | **92.79%** |
| Avg Waiting Time | 185.25 | **133.50** | 140.12 |
| Avg Turnaround Time | 521.38 | **469.62** | 476.25 |
| Avg Response Time | 24.38 | 27.12 | **15.75** |

- **SJF** wins on waiting time and turnaround time
- **MLFQ** wins on CPU utilization and response time
- **FCFS** is simplest but performs worst across all metrics

---

## How to Run

**Requirements:** Python 3.x (no external libraries needed)

```bash
python CPUscheduler.py
```

The program will run all three algorithms in sequence and print:
- A context switch log showing the simulation state at each scheduling decision
- Per-process stats (waiting time, response time, turnaround time)
- Summary averages and CPU utilization for each algorithm

---

## Project Structure

```
├── CPUscheduler.py        # Main simulation — all three algorithms
├── README.md              # This file
└── report/
    └── ComputerOS_Report_Final.docx   # Full written report with flowcharts and analysis
```

---

## How It Works

The simulation is **event-driven** — instead of ticking second by second, time jumps forward to the next meaningful event:
- A CPU burst finishes
- An I/O burst finishes  
- A time quantum expires (MLFQ only)

Each process stores its full list of alternating CPU and I/O burst times. Even indices are CPU bursts, odd indices are I/O bursts. All 8 processes are activated at time 0.

### Process Data Format
```python
{"name": "P1", "bursts": [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4]}
#                          ^  IO  ^ IO  ^ IO  ^ IO  ^ IO  ^ IO  ^ IO  ^
#                         CPU    CPU    CPU    CPU    CPU    CPU    CPU   CPU
```

---

## Sample Output

```
=== Context Switch at Time 0 ===
Running:     P1 (burst remaining: 5)
Ready Queue: P2(4), P3(8), P4(3), P5(16), P6(11), P7(14), P8(4)
I/O:         none

=== Context Switch at Time 5 ===
Running:     P2 (burst remaining: 4)
Ready Queue: P3(8), P4(3), P5(16), P6(11), P7(14), P8(4)
I/O:         P1(io remaining: 27)

--- FCFS Results ---
P1 | Wait: 170 | Response: 0  | Turnaround: 395
P2 | Wait: 164 | Response: 5  | Turnaround: 591
...
CPU Utilization: 85.34%
Avg Waiting Time: 185.25
Avg Turnaround Time: 521.38
Avg Response Time: 24.38
```

---

## Key Takeaways

- No single algorithm dominates every metric — the best choice depends on what the system prioritizes
- **MLFQ** is the most practical for general-purpose scheduling because it adapts to process behavior without needing prior knowledge of burst lengths
- **SJF** minimizes waiting time but requires knowing burst lengths in advance and starves long processes
- **FCFS** guarantees fairness but is inefficient when short and long processes are mixed
