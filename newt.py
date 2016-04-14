from PIL import Image as img
from numpy import random, size, array, max, ones, double, arange, meshgrid, sqrt, median, std, where, min, exp, sort, arctan2, abs, sin, cos, log, pi, maximum, minimum, real, imag, mod
from scipy.ndimage.filters import convolve as vconv

class newt:
	pic = array([0])
	pic = pic

	def __init__(self, pic):
		self.max = max(pic)
		self.pic = pic
		
	def siz(self,pic2):
		pic = 255*self.pic/max(self.pic)
		sizzle = [0, 0]
		sizzle[0] = size(self.pic[:,:][:,0,0])
		sizzle[1] = size(self.pic[:,:][0,:,0])
		for row in range(sizzle[0]):
			for col in range(sizzle[1]):
				r = 5*random.randint(2)
				for color in range(3): 
					pic[:,:][row,col,color] = pic[:,:][row,col,color] + r
		im = img.fromarray(pic.astype('uint8'))
		im.show()
		
	def shw(self):
		pic = 255*self.pic/max(self.pic)
		im = img.fromarray(pic.astype('uint8'))
		im.show()
		
	def srt(self):
		pic = 255*self.pic/max(self.pic)
		for color in range(3):
			pic[:,:][:,:,color] = sort(sort(pic[:,:][:,:,color],(color+1)%2),color%2)
		im = img.fromarray(pic.astype('uint8'))
		im.show()
		
	def nwyr(self):
		pic = 255*self.pic/max(self.pic)
		for color in range(3):
			pic[:,:][:,:,color] = (pic[:,:][:,:,0]+pic[:,:][:,:,1]+pic[:,:][:,:,2])/3
		im = img.fromarray(pic.astype('uint8'))
		im.show()
		
	def conv(self,kernel='lap 3'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):		
			self.pic[:,:][:,:,color] = vconv(self.pic[:,:][:,:,color],\
													kernel,mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)
		return self
		
	def highboost(self,kernel='d 17'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):
			m = median(self.pic[:,:][:,:,color])
			self.pic[:,:][:,:,color] = self.pic[:,:][:,:,color] - vconv(self.pic[:,:][:,:,color],\
													kernel,mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)\
													+m
		return self
		
	def varfilt(self,kernel='g 7'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):
			m = median(self.pic[:,:][:,:,color])
			self.pic[:,:][:,:,color] = vconv(self.pic[:,:][:,:,color]**2, kernel, mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)	- \
													(vconv(self.pic[:,:][:,:,color], kernel, mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0))**2								
		return self
		
	def srtfilt(self):
		
		for color in range(3):
			self.pic[:,:][:,:,color] = sort(sort(self.pic[:,:][:,:,color]),0)
											
		return self
		
	def dhat(self,kernel='d 3'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):
			pic = self.pic[:,:][:,:,color]
			m = median(pic)
			st = std(pic)
			pic -= m
			filt = vconv(self.pic[:,:][:,:,color],kernel,mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)
			diff = pic - filt
			dex = where(diff == min(diff))
			scl = pic[dex]/filt[dex]
			
			self.pic[:,:][:,:,color] = (pic - scl*filt) >max([st,10])
			
		return self
		
	def dline(self,kernel='g 3'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):
			pic = self.pic[:,:][:,:,color]
			m = median(pic)
			st = std(pic)
			pic -= m
			filt = vconv(self.pic[:,:][:,:,color],kernel,mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)
			diff = pic - filt
			dex = where(diff == min(diff))
			scl = pic[dex]/filt[dex]
			for step in range(25):
				self.pic[:,:][:,:,color] += (pic - step*scl*filt/25)>max([st,10])
			self.pic[:,:][:,:,color]=self.pic[:,:][:,:,color]>75
		return self
	
	def kernelmaker(self,kernel):	
		type, n = kernel.split(' ')
		n = double(n)
		n = n + 1 - n%2
		if (type=='d'):
			x = arange(-n//2+1,n//2+1,1)
			x, y = meshgrid(x,x)
			kernel = sqrt(x**2+y**2)<=n/2
		elif (type=='g'):
			x = arange(-n//2+1,n//2+1,1)
			x, y = meshgrid(x,x)
			kernel = sqrt(x**2+y**2)
			kernel = exp(-kernel*9/n**2)*(kernel<=n/2)
		elif (type=='lap'):
			kernel = array([[-1., -1., -1.],[-1., 9., -1.],[-1., -1., -1.]])
		return array(kernel, dtype=double)