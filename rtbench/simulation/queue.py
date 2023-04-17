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
from rtbench.simulation.system_event import SystemEvent
class PrioQueue:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def isEmpty(self):
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)

    def add(self, event):
        if not isinstance(event, SystemEvent):
            raise TypeError("Only SystemEvent objects can be added to the priority queue")
        self.queue.append(event)
        self._heapify_up(len(self.queue) - 1)

    def pop(self):
        if self.isEmpty():
            raise ValueError("Priority queue is empty")
        item = self.queue[0]
        last_item = self.queue.pop()
        if self.queue:
            self.queue[0] = last_item
            self._heapify_down(0)
        return item

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if parent_index < 0:
            return
        if self.queue[parent_index] > self.queue[index]:
            self._swap(parent_index, index)
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index
        if left_child_index < len(self.queue) and self.queue[left_child_index] < self.queue[smallest]:
            smallest = left_child_index
        if right_child_index < len(self.queue) and self.queue[right_child_index] < self.queue[smallest]:
            smallest = right_child_index
        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        self.queue[i], self.queue[j] = self.queue[j], self.queue[i]

