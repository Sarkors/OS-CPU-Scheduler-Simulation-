processes = [
    {"name": "P1", "bursts": [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4], 
    "burst_index": 0, 
    "time_remaining": 5,  
    "state": "ready", 
    "wait_time": 0,
    "response_time": -1,
    "turnaround_time": 0},
    {"name": "P2", "bursts": [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8],
    "burst_index": 0, 
    "time_remaining": 4,  
    "state": "ready", 
    "wait_time": 0,
    "response_time": -1,
    "turnaround_time": 0},
    {"name": "P3", "bursts": [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6],
    "burst_index": 0, 
    "time_remaining": 8,  
    "state": "ready", 
    "wait_time": 0,
    "response_time": -1,
    "turnaround_time": 0},
    {"name": "P4", "bursts": [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3], 
    "burst_index": 0, 
    "time_remaining": 3,  
    "state": "ready", 
    "wait_time": 0,
    "response_time": -1,
    "turnaround_time": 0},
    {"name": "P5", "bursts": [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4], 
    "burst_index": 0, 
    "time_remaining": 16,  
    "state": "ready", 
    "wait_time": 0,
    "response_time": -1,
    "turnaround_time": 0},
    {"name": "P6", "bursts": [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8], 
    "burst_index": 0,  
    "time_remaining": 11,  
    "state": "ready", 
    "wait_time": 0,
    "response_time": -1,
    "turnaround_time": 0},
    {"name": "P7", "bursts": [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10], 
    "burst_index": 0,  
    "time_remaining": 14,  
    "state": "ready", 
    "wait_time": 0,
    "response_time": -1,
    "turnaround_time": 0},
    {"name": "P8", "bursts": [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6], 
    "burst_index": 0,  
    "time_remaining": 4,  
    "state": "ready", 
    "wait_time": 0,
    "response_time": -1,
    "turnaround_time": 0}
]

def run_fcfs(processes):
    # reset all processes first so we start fresh
    for p in processes:
        p["burst_index"] = 0
        p["time_remaining"] = p["bursts"][0]
        p["state"] = "ready"
        p["wait_time"] = 0
        p["response_time"] = -1
        p["turnaround_time"] = 0

    # initialize simulation variables inside the function so they reset each run
    current_time = 0
    cpu = None          # holds whichever process is currently running
    io_queue = []       # processes currently doing I/O
    ready_queue = []    # processes waiting for CPU

    # start all processes in ready queue
    for p in processes:
        ready_queue.append(p)

    # while loop to check if any processes arent done
    while any(p["state"] != "done" for p in processes): # while loop to check if any processes we have are not done

        # if cpu is empty, pick next process based on algorithm
        if cpu is None and len(ready_queue) > 0: # if cpu is empty and if theres anything in our ready queue 
            cpu = ready_queue.pop(0)       # FCFS: just take the first one
            cpu["state"] = "running"       # change cpu state to running

            # print context switch info whenever a new process gets the CPU
            if cpu is not None:
                print(f"\n=== Context Switch at Time {current_time} ===")
                print(f"Running:     {cpu['name']} (burst remaining: {cpu['time_remaining']})")
                
                rq_info = ', '.join(f"{p['name']}({p['bursts'][p['burst_index']]})" for p in ready_queue)
                print(f"Ready Queue: {rq_info if rq_info else 'empty'}")
                
                io_info = ', '.join(f"{p['name']}(io remaining: {p['time_remaining']})" for p in io_queue)
                print(f"I/O:         {io_info if io_info else 'none'}")
            # response time = first time a process ever gets the CPU
            if cpu["response_time"] == -1: 
                cpu["response_time"] = current_time # update its response time for stats 

        #  figure out when the next event happens
        #  what if CPU is empty AND ready queue is empty?
        # that means everyone is doing I/O - we still need to advance time
        if cpu is not None:
            cpu_done = current_time + cpu["time_remaining"]
        else:
            cpu_done = float('inf')        # infinity - CPU has nothing to finish

        if len(io_queue) > 0: # if our io_queue has something in it 
            io_done_times = [current_time + p["time_remaining"] for p in io_queue]
            next_event = min([cpu_done] + io_done_times)
        else:
            next_event = cpu_done          # only the CPU to wait on

        # 3. advance time
        time_elapsed = next_event - current_time
        current_time = next_event

        # update cpu time remaining too
        if cpu is not None:
            cpu["time_remaining"] -= time_elapsed

        # 4. update wait time for everything sitting in ready queue
        for p in ready_queue:
            p["wait_time"] += time_elapsed

        # 5. update I/O countdowns, move finished processes to ready queue
        for p in io_queue:
            p["time_remaining"] -= time_elapsed

        # move finished I/O processes to ready queue
        # we loop over a copy so removing items doesn't mess up the loop
        for p in io_queue[:]: # create copy to iterate over                        
            if p["time_remaining"] <= 0:
                io_queue.remove(p)
                p["burst_index"] += 1      # move to next burst (next CPU burst)
                p["time_remaining"] = p["bursts"][p["burst_index"]]
                p["state"] = "ready"
                ready_queue.append(p)

        #  check if the running process finished its burst
        if cpu is not None and cpu["time_remaining"] <= 0:
            cpu["burst_index"] += 1        # move past the CPU burst we just finished

            # is there another burst after this one?
            if cpu["burst_index"] < len(cpu["bursts"]):
                # yes - next burst is I/O, send it there
                cpu["time_remaining"] = cpu["bursts"][cpu["burst_index"]]
                cpu["state"] = "io"
                io_queue.append(cpu)
            else:
                # no more bursts so process is done
                cpu["state"] = "done"
                cpu["turnaround_time"] = current_time  # finished at current time
                print(f"*** {cpu['name']} completed at time {current_time} ***")
            cpu = None                     # CPU is now free

    # print  results
    print(f"\n--- FCFS Results ---")
    for p in processes:
        print(f"{p['name']} | Wait: {p['wait_time']} | Response: {p['response_time']} | Turnaround: {p['turnaround_time']}")

    # calculate averages
    avg_wait = sum(p["wait_time"] for p in processes) / len(processes)
    avg_turnaround = sum(p["turnaround_time"] for p in processes) / len(processes)
    avg_response = sum(p["response_time"] for p in processes) / len(processes)

    # cpu utilization = total cpu burst time / total simulation time
    total_cpu_time = sum(sum(p["bursts"][i] for i in range(0, len(p["bursts"]), 2)) for p in processes)
    cpu_utilization = (total_cpu_time / current_time) * 100

    print(f"Total time: {current_time}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")
    print(f"Avg Waiting Time: {avg_wait:.2f}")
    print(f"Avg Turnaround Time: {avg_turnaround:.2f}")
    print(f"Avg Response Time: {avg_response:.2f}")

# run the simulation
run_fcfs(processes)

def run_sjf(processes):
    # reset all processes first so we start fresh
    for p in processes:
        p["burst_index"] = 0
        p["time_remaining"] = p["bursts"][0]
        p["state"] = "ready"
        p["wait_time"] = 0
        p["response_time"] = -1
        p["turnaround_time"] = 0

    # initialize simulation variables inside the function so they reset each run
    current_time = 0
    cpu = None          # holds whichever process is currently running
    io_queue = []       # processes currently doing I/O
    ready_queue = []    # processes waiting for CPU

    # start all processes in ready queue
    for p in processes:
        ready_queue.append(p)

    # while loop to check if any processes arent done
    while any(p["state"] != "done" for p in processes): # while loop to check if any processes we have are not done

        # if cpu is empty, pick next process based on algorithm
        if cpu is None and len(ready_queue) > 0: # if cpu is empty and if theres anything in our ready queue 
            # SJF  sort the ready queue by current burst length, then take the first
            ready_queue.sort(key=lambda p: p["bursts"][p["burst_index"]])
            cpu = ready_queue.pop(0)
            cpu["state"] = "running"       # change cpu state to running
            # response time = first time a process ever gets the CPU
            # print context switch info whenever a new process gets the CPU
            if cpu is not None:
                print(f"\n=== Context Switch at Time {current_time} ===")
                print(f"Running:     {cpu['name']} (burst remaining: {cpu['time_remaining']})")
                
                rq_info = ', '.join(f"{p['name']}({p['bursts'][p['burst_index']]})" for p in ready_queue)
                print(f"Ready Queue: {rq_info if rq_info else 'empty'}")
                
                io_info = ', '.join(f"{p['name']}(io remaining: {p['time_remaining']})" for p in io_queue)
                print(f"I/O:         {io_info if io_info else 'none'}")
                if cpu["response_time"] == -1: 
                    cpu["response_time"] = current_time # update its response time for stats 

        # figure out when the next event happens
        #  what if CPU is empty AND ready queue is empty?
        # that means everyone is doing I/O but still need to advance time
        if cpu is not None:
            cpu_done = current_time + cpu["time_remaining"]
        else:
            cpu_done = float('inf')        # infinity - CPU has nothing to finish

        if len(io_queue) > 0: # if our io_queue has something in it 
            io_done_times = [current_time + p["time_remaining"] for p in io_queue]
            next_event = min([cpu_done] + io_done_times)
        else:
            next_event = cpu_done          # only the CPU to wait on

        #  advance time
        time_elapsed = next_event - current_time
        current_time = next_event

        # update cpu time remaining too
        if cpu is not None:
            cpu["time_remaining"] -= time_elapsed

        # 4. update wait time for everything sitting in ready queue
        for p in ready_queue:
            p["wait_time"] += time_elapsed

        # 5. update I/O countdowns, move finished processes to ready queue
        for p in io_queue:
            p["time_remaining"] -= time_elapsed

        # move finished I/O processes to ready queue
        # we loop over a copy so removing items doesn't mess up the loop
        for p in io_queue[:]: # create copy to iterate over                        
            if p["time_remaining"] <= 0:
                io_queue.remove(p)
                p["burst_index"] += 1      # move to next burst (next CPU burst)
                p["time_remaining"] = p["bursts"][p["burst_index"]]
                p["state"] = "ready"
                ready_queue.append(p)

        # 6. check if the running process finished its burst
        if cpu is not None and cpu["time_remaining"] <= 0:
            cpu["burst_index"] += 1        # move past the CPU burst we just finished

            # is there another burst after this one?
            if cpu["burst_index"] < len(cpu["bursts"]):
                # yes next burst is I/O, send it there
                cpu["time_remaining"] = cpu["bursts"][cpu["burst_index"]]
                cpu["state"] = "io"
                io_queue.append(cpu)
            else:
                # no more bursts  process is done
                cpu["state"] = "done"
                cpu["turnaround_time"] = current_time  # finished at current time
                print(f"*** {cpu['name']} completed at time {current_time} ***")
            cpu = None                     # CPU is now free

    # print per-process results
    print(f"\n--- SJF Results ---")
    for p in processes:
        print(f"{p['name']} | Wait: {p['wait_time']} | Response: {p['response_time']} | Turnaround: {p['turnaround_time']}")

    # calculate averages
    avg_wait = sum(p["wait_time"] for p in processes) / len(processes)
    avg_turnaround = sum(p["turnaround_time"] for p in processes) / len(processes)
    avg_response = sum(p["response_time"] for p in processes) / len(processes)

    # cpu utilization = total cpu burst time / total simulation time
    total_cpu_time = sum(sum(p["bursts"][i] for i in range(0, len(p["bursts"]), 2)) for p in processes)
    cpu_utilization = (total_cpu_time / current_time) * 100

    print(f"Total time: {current_time}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")
    print(f"Avg Waiting Time: {avg_wait:.2f}")
    print(f"Avg Turnaround Time: {avg_turnaround:.2f}")
    print(f"Avg Response Time: {avg_response:.2f}")

run_sjf(processes)

def run_mlfq(processes):
    # reset all processes - same as FCFS but add two new fields
    for p in processes:
        p["burst_index"] = 0
        p["time_remaining"] = p["bursts"][0]
        p["state"] = "ready"
        p["wait_time"] = 0
        p["response_time"] = -1
        p["turnaround_time"] = 0
        p["queue_level"] = 1        # all processes start in queue 1
        p["time_on_cpu"] = 0        # tracks how long it's been running this turn

    current_time = 0
    cpu = None
    io_queue = []
    queue1 = []   # RR quantum 5
    queue2 = []   # RR quantum 10
    queue3 = []   # FCFS

    # all processes start in queue1
    for p in processes:
        queue1.append(p)

    while any(p["state"] != "done" for p in processes): 

        #  if cpu is empty, pick next process
        # check queue1 first, then queue2, then queue3
        if cpu is None and (len(queue1) > 0 or len(queue2) > 0 or len(queue3) > 0):
            if len(queue1) > 0:
                cpu = queue1.pop(0)
            elif len(queue2) > 0:
                cpu = queue2.pop(0)
            else:
                cpu = queue3.pop(0)

            cpu["state"] = "running"
            cpu["time_on_cpu"] = 0   # reset time on CPU for new turn

            if cpu["response_time"] == -1:
                cpu["response_time"] = current_time
                # print context switch info whenever a new process gets the CPU
            if cpu is not None:
                print(f"\n=== Context Switch at Time {current_time} ===")
                print(f"Running:     {cpu['name']} (burst remaining: {cpu['time_remaining']})")
                
                rq_info = ', '.join(f"{p['name']}(Q{p['queue_level']}, burst:{p['bursts'][p['burst_index']]})" for p in queue1 + queue2 + queue3)
                print(f"Ready Queue: {rq_info if rq_info else 'empty'}")
                
                io_info = ', '.join(f"{p['name']}(io remaining: {p['time_remaining']})" for p in io_queue)
                print(f"I/O:         {io_info if io_info else 'none'}")

                print(f"Running:     {cpu['name']} (Q{cpu['queue_level']}, burst remaining: {cpu['time_remaining']})")

        #  figure out next event
        
        if cpu is not None:
            cpu_done = current_time + cpu["time_remaining"]
            if cpu["queue_level"] == 1:
                quantum = 5
            elif cpu["queue_level"] == 2:
                quantum = 10
            else:
                quantum = float('inf')       # queue 3 has no quantum
            quantum_expires = current_time + quantum
        else:
            cpu_done = float('inf')
            quantum_expires = float('inf')

        # next event is smallest of cpu_done, quantum_expires, io completions
        if len(io_queue) > 0:
            io_done_times = [current_time + p["time_remaining"] for p in io_queue]
            next_event = min(cpu_done, quantum_expires, min(io_done_times))
        else:
            next_event = min(cpu_done, quantum_expires)

        # 3. advance time - same as before
        time_elapsed = next_event - current_time
        current_time = next_event

        # 4. update wait times - but now check all three queues
        for p in queue1 + queue2 + queue3:
            p["wait_time"] += time_elapsed

        # 5. update I/O - same as before
        # but when process returns from I/O, which queue does it go to?
        # update I/O countdowns
        for p in io_queue:
            p["time_remaining"] -= time_elapsed
        for p in io_queue[:]:
            if p["time_remaining"] <= 0:
                io_queue.remove(p)
                p["burst_index"] += 1
                p["time_remaining"] = p["bursts"][p["burst_index"]]
                p["state"] = "ready"
                # return to whichever queue level they belong to
                if p["queue_level"] == 1:
                    queue1.append(p)
                elif p["queue_level"] == 2:
                    queue2.append(p)
                else:
                    queue3.append(p)

        # 6. check what ended the current CPU turn
        if cpu is not None:
            cpu["time_remaining"] -= time_elapsed
            cpu["time_on_cpu"] += time_elapsed

            if cpu["time_remaining"] <= 0:
                # burst finished naturally - send to I/O or mark done
                cpu["burst_index"] += 1        # advance past finished burst

                if cpu["burst_index"] < len(cpu["bursts"]):
                    # more bursts remain - send to I/O
                    cpu["time_remaining"] = cpu["bursts"][cpu["burst_index"]]
                    cpu["state"] = "io"
                    io_queue.append(cpu)
                else:
                    # no more bursts - process is done
                    cpu["state"] = "done"
                    cpu["turnaround_time"] = current_time
                    print(f"*** {cpu['name']} completed at time {current_time} ***")
                cpu = None                     # free the CPU either way

            elif current_time >= quantum_expires:
                # quantum expired - demote and put back in lower queue
                if cpu["queue_level"] == 1:
                    cpu["queue_level"] = 2
                    queue2.append(cpu)
                elif cpu["queue_level"] == 2:
                    cpu["queue_level"] = 3
                    queue3.append(cpu)
                else:
                    queue3.append(cpu)         # already lowest, goes to back
                cpu["state"] = "ready"
                cpu = None                     # free the CPU

    # print results
    
    print(f"\n--- MLFQ Results ---")
    for p in processes:
        print(f"{p['name']} | Wait: {p['wait_time']} | Response: {p['response_time']} | Turnaround: {p['turnaround_time']}")

    # calculate averages
    avg_wait = sum(p["wait_time"] for p in processes) / len(processes)
    avg_turnaround = sum(p["turnaround_time"] for p in processes) / len(processes)
    avg_response = sum(p["response_time"] for p in processes) / len(processes)

    # cpu utilization = total cpu burst time / total simulation time
    total_cpu_time = sum(sum(p["bursts"][i] for i in range(0, len(p["bursts"]), 2)) for p in processes)
    cpu_utilization = (total_cpu_time / current_time) * 100

    print(f"Total time: {current_time}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")
    print(f"Avg Waiting Time: {avg_wait:.2f}")
    print(f"Avg Turnaround Time: {avg_turnaround:.2f}")
    print(f"Avg Response Time: {avg_response:.2f}")

run_mlfq(processes)