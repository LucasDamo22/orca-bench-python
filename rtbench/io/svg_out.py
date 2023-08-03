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
from __future__ import annotations
from os.path import exists
from os.path import join
from os import remove
from rtbench.simulation.task_control_block import TaskControlBlock
import random

class SvgOut:
    colors = []
    SVG_TICK_CONST = 20
    SVG_TH_CONST = 30

    #def __init__(self: "SvgOut")

    def setColors(self: "SvgOut"):
            r = lambda: random.randint(0, 220)
            for t in range(0,len(self._blocked)):
                self.colors.append("#{:02x}{:02x}{:02x}".format(r(), r(), r()))
            return
    
    def svg_init(self:"SvgOut",time :int):
        #path to the svg file
        self.setColors()
        filename = 'rtbench/data_out/taskgraph.svg'
        #checking if it has already generated an svg
        #if it has it deletes the old one and generates a new one
        if exists(filename):
            remove(filename)
        
        #svg header
        svg_out = open(filename,'a')
        first_def =f'<svg width="{self.SVG_TICK_CONST * time+300}" height="{self.SVG_TICK_CONST * time+100}" viewBox="-50 -50 {self.SVG_TH_CONST*len(self._blocked)} {self.SVG_TICK_CONST * time}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet">\n'
        svg_out.write(first_def)
        #svg y axis
        yaxis = f'<rect x="0" y="-10" width="1" height="{self.SVG_TH_CONST*len(self._blocked)+20}" fill="black" />\n'
        yaxis+= f'<text x="15" y="{self.SVG_TH_CONST*len(self._blocked)+40}" font-size="14" text-anchor="end">Tasks</text>'#y do texto precisa ser o final do eixo +20
        svg_out.write(yaxis)
        #svg x axis
        xaxis = f'<rect x="-10" y="0" width="{self.SVG_TICK_CONST* time+20}" height="1" fill="black" />\n'
        xaxis+= f'<text x="{self.SVG_TICK_CONST* time+60}" y="3" font-size="14" text-anchor="end">Ticks</text>\n'#x do texto precisa ser o final do eixo +5
        svg_out.write(xaxis)

        #taskIds
        for t in self._blocked:
            taskId = f'<text x="-15" y="{(t._id*self.SVG_TH_CONST)-7}" font-size="12" text-anchor="end">{t._name}</text>\n'
            svg_out.write(taskId)

        
        count = 1
        # ticksX = '\n'
        # for i in range(0,time):
        #     ticksX += f'<text x="{sec+ 4 +i*self.SVG_TICK_CONST}" y="-8" font-size="11" text-anchor="end">{i+1}</text>\n'
        #     ticksX += f'<rect x="{sec+i*self.SVG_TICK_CONST}" y="-5" width="1" height="10" fill="black"/>\n'

        # svg_out.write(ticksX)


    def svg(self: "SvgOut"):

    


