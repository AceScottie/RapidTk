from .errors import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Event
import time
class Chart:
	def __init__(self, master, labels=[], data=[], ticks=[]):
		self.master = master
		self.labels = labels
		self.data = data
		self.ticks = ticks
		self.fig = None
		self.ax = None
		self.annot = None
		self.prev_ind = [-1, -1]

	def draw(self, bg="white", fg="black"):
		self.fig, self.ax = plt.subplots()
		self.ax.set_facecolor(bg) 
		self.fig.patch.set_facecolor(bg)
		self.ax.spines['bottom'].set_color(fg)
		self.ax.spines['top'].set_color(fg)
		self.ax.spines['left'].set_color(fg)
		self.ax.spines['right'].set_color(fg)
		self.ax.tick_params(axis='y', colors=fg)
		self.ax.tick_params(axis='x', colors=fg)
		self.fig.subplots_adjust(left=0.03, bottom=0.15, right=0.80, top=0.90, wspace=0.2, hspace=0.2)
		self.ax.set_ylim([0, 5.5])
		self.ax.set_xticks(np.arange(len(self.ticks)))
		self.ax.set_xticklabels(self.ticks)
		line = [None] * len(self.labels)
		i = 0
		for v in self.data:
			line[i], = plt.plot(self.ticks, v, label=self.labels[i], linestyle=['-','--','-.',':',][i%4],  marker='o',alpha=1-(i/10))
			i+=1
		for tick in self.ax.xaxis.get_major_ticks():
			tick.label.set_fontsize(8)
			tick.label.set_rotation(60)
		plt.grid()
		if len(self.labels) > 0:
			plt.legend(loc=3,bbox_to_anchor=(1,0))
		self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points", bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->", color=fg, lw=2))
		self.annot.set_visible(False)
		chart = FigureCanvasTkAgg(self.fig, self.master)
		chart.draw()
		widget = chart.get_tk_widget()
		chart.mpl_connect("motion_notify_event", lambda e=Event(), l=line, :self._hover2(e, l))
		return widget

	def _update(self, ind, line, l):
		x,y = line.get_data()
		self.annot.xy = (x[ind], y[ind])
		self.annot.set_text("{}:{}\nDate:{}".format(self.labels[l], self.data[l][ind], self.ticks[ind]))
		self.annot.get_bbox_patch().set_alpha(0.4)

	def _hover2(self, event, line):
		vis = False
		if not self.annot.get_visible():
			for i in range(len(line)):
				x = line[i].contains(event)
				if x[0]:
					vis = True
					self._update(x[1]['ind'][0], line[i], i)
					self.annot.set_visible(True)
					self.fig.canvas.draw_idle()
					break
		if not vis:
			self.annot.set_visible(False)