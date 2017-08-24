import sys
import os
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.autograd import Function
from torch.nn.modules.module import Module
import matplotlib.pylab as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import seaborn as sea
import torch.optim as optim
from coords2RMSD import Coords2RMSD

def test_gradient():
	maxL=2
	L=3
	x0 = Variable(torch.FloatTensor([2,0,0, 3,0.1,1, 3,0.1,0 ]).cuda(), requires_grad=True)
	x1 = Variable(torch.randn(x0.size(0)).cuda())
	length = Variable(torch.IntTensor(1).fill_(L-1))
	target = Variable(torch.FloatTensor([0,0,0, 1,1,0, 3,0,0]).cuda())
	loss = Coords2RMSD(maxL)
	rmsd_x0 = loss(x0, target, length)
	rmsd_x0.backward()
	float_rmsd_x0 = np.sqrt(rmsd_x0.data[0])
	back_grad_x0 = torch.FloatTensor(x0.grad.size()).copy_(x0.grad.data)
	
	aligned_x0 = torch.zeros(3*maxL)
	aligned_target = torch.zeros(3*maxL)
	
	grads = []
	for i in range(0,3*L):
		dx = 0.0001
		x1.data.copy_(x0.data)
		x1.data[i]+=dx
		rmsd_x1 = loss(x1, target, length)
		float_rmsd_x1 = np.sqrt(rmsd_x1.data[0])
		drmsd_dx = (float_rmsd_x1-float_rmsd_x0)/(dx)
		grads.append(drmsd_dx)
	
	fig = plt.figure()
	plt.plot(grads,'-r', label = 'num grad')
	plt.plot(back_grad_x0[:3*L].numpy(),'bo', label = 'an grad')
	plt.legend()
	plt.savefig('TestFig/rmsd_gradients_CUDA.png')

if __name__=='__main__':
	test_gradient()