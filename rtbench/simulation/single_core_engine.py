"""
This file is part of project ORCA. More information on the project
can be found at the following repositories at GitHub's website.

http://https://github.com/andersondomingues/orca-sim
http://https://github.com/andersondomingues/orca-software
http://https://github.com/andersondomingues/orca-mpsoc
http://https://github.com/andersondomingues/orca-tools
http://https://github.com/andersondomingues/orca-modeling

Copyright (C) 2018-2020 Anderson Domingues, <ti.andersondomingues@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
from queue import PriorityQueue

from rtbench.io.terminal import warn, error, info  # debug, header
from rtbench.modeling.graph import Graph
from rtbench.scheduling.scheduling_algorithm import SchedulingAlgorithm
from rtbench.simulation.task_control_block import TaskControlBlock
from rtbench.simulation.system_event import SystemEvent, SystemEventType
from rtbench.simulation.queue import PrioQueue


class SingleCoreEngine:
    SCHED_IRQ_PERIOD = 4

    def __init__(
        self: "SingleCoreEngine", task_graph: Graph, algorithm: SchedulingAlgorithm
    ):
        self._system_time: int = 0
        self._queue = PrioQueue()
        self._running = []
        self._blocked = []
        self._ready = []

        # populate blocked list with tasks from the graph
        for n in task_graph.get_nodes():
            tlb = TaskControlBlock(
                n.get_data()["id"],
                n.get_data()["name"],
                n.get_data()["period"],
                n.get_data()["capacity"],
                n.get_data()["deadline"],
            )
            self._blocked.append(tlb)
            
        self._algorithm = algorithm


    def printrunning(self: "SingleCoreEngine"):
        for t in self._running:
            print(f"RUNNING - id {t._id} current {t._current_capacity} capa {t._capacity}")
    def printready(self: "SingleCoreEngine"):
        for t in self._ready:
            print(f"READY - id {t._id} current {t._current_capacity} capa {t._capacity}")
    def printblocked(self: "SingleCoreEngine"):
        for t in self._blocked:
            print(f"BLOCKED - id {t._id} current {t._current_capacity} capa {t._capacity}")


    def simulate(self: "SingleCoreEngine", time: int):
        irq_event: SystemEvent = SystemEvent(0, SystemEventType.SCHEDULER_IRQ)
        self._queue.add(irq_event)

        iterations = 0
        start_time = 0

        '''
        print("--------------------------------------------------------")
        print("types")
        print(type(self._system_time))
        print(type(self._queue))
        print(type(self._running))
        print(type(self._blocked))
        print(type(self._ready))
        print(type(time))
        print(type(time))

        print("--------------------------------------------------------")
        '''
        
        while self._system_time < time:
            #print("--------------------------------------------------------")
            #self.printready()
            #self.printrunning()
            #self.printblocked()
            
            top_event: SystemEvent = self._queue.pop()

            
            #print("''''")
            #print(top_event.__str__())
            
            
            self._elapsed_time = top_event._time - self._system_time
            self._system_time += self._elapsed_time
            
            
            #print(f"{top_event._time}<-top event time")
            #print(f"{self._system_time}<-system time")
            #print(f"{self._elapsed_time}<-elapsed time")
            # warning
            if top_event._type == SystemEventType.TASK_FINISHED_IRQ:
                warn(str(self._system_time) + ": task finished")
            else:
                warn(str(self._system_time) + ": scheduled irq")

            # If the top of the queue is a task finish syscall, we must
            # put the finished task into the blocked queue and process
            # a new task to take its place
            self.schedule(self._algorithm)
            '''
            print(f"{top_event.get_time}<-topeventGetTime")
            print(f"{top_event.get_type}<-topeventGetType")
            print(f"{SystemEventType.SCHEDULER_IRQ}<-systemSchedulerIRQ")
            
            if top_event.get_type() == SystemEventType.SCHEDULER_IRQ:
                print("yes")
            else:
                print("NO")
            '''
            # Next event is the scheduler interruption
            if top_event.get_type() == SystemEventType.SCHEDULER_IRQ:
                # remove all events from the simulation queue; since the
                # scheduler_irq has been removed, only the event for the
                # running task remains
                while self._queue.__len__() > 0:
                    self._queue.pop()
                    #print(f"{self._queue.get()}")

                # register the interruption
                irq_event._time = self._system_time + self.SCHED_IRQ_PERIOD
                self._queue.add(irq_event)

            # register next task finish within the simulation
            next_task = self._running[0]

            #aaa=666
            info(iterations, start_time, self._system_time, self._system_time)
            start_time = self._system_time
            iterations += 1
            
            #print(f"{next_task._current_capacity}<-next task capacity")
            
            # slack time
            if next_task is not None:
                top_event._time = self._system_time + (
                    next_task._capacity - next_task._current_capacity
                )
                top_event.type = SystemEventType.TASK_FINISHED_IRQ
                self._queue.add(top_event)
                warn("running task")

                info(
                    iterations,
                    next_task._period,
                    next_task._capacity,
                    next_task._deadline,
                )
            else:
                warn("slack time")
            
            info("sistem time", self._system_time)
            self.print_task_list()
            
        
        return self._system_time

    def schedule(self: "SingleCoreEngine", algorithm: SchedulingAlgorithm):
        for t in self._running:
            # add elapsed time to current capacity of the task

            t._current_capacity += self._elapsed_time
            
            #print("current")
            #print(t._current_capacity)
            #print("capa")
            #print(t._capacity)
            #print(f"{t._id}<-ID")
            #print(f"{t._capacity}<-capacity")
            #print(f"{self._elapsed_time} <-elapsed time schedule")
            #self.printrunning()
            
            # case A: task has timed out, preempted
            if t._current_capacity < t._capacity:
                #print("foi pro ready")
                self._ready.append(t)

            # case B: task has finished succeffuly
            else:
                #print("foi pro blocked")
                t._release_time += t._period
                t._current_capacity = 0
                t._next_deadline += t._deadline
                self._blocked.append(t)

        # clear running list as tasks were added to other lists
        self._running.clear()

        freed = []

        # move tasks from blocked to the ready queue
        for t in self._blocked:
            if t._release_time <= self._system_time:
                self._ready.append(t)
                freed.append(t)

        # remove freed tasks from blocked list
        for t in freed:
            self._blocked.remove(t)

        # sort ready list (using sort algorithm)
        self._algorithm.schedule(self._ready)

        # get first element and push it to the executing queue (if any)
        if len(self._ready) != 0:
            task = self._ready[0]
            self._ready.remove(task)
            self._running.append(task)

            if task._next_deadline < self._system_time:
                error("missed deadline!")
               # print(f"task{self._ready[0]}")

        return self._system_time

    def print_task_list(self: "SingleCoreEngine"):
        # print lists
        info("==============================================")
        #print(f"{self._system_time}<-SYSTEM TIME ON PTKLS")
        info("----- running")
        for t in self._running:
            info(str(t))

        info("----- ready")
        for t in self._ready:
            info(str(t))

        info("----- blocked")
        for t in self._blocked:
            info(str(t))

        info("==============================================")
