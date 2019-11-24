#Steganography code to hide one image inside another image
#Works off of hiding the most significant bits (MSB) inside the
#least significant bits (LSB) of another image

#Merged photos should be image1.jpg and image2.jpg
#Outputs are PNG files since JPG compressions screws up the LSB while unmerging
#Files are automatically unmerged as well for verification.

#Code heavily borrowed/stolen from Kevin Salton do Prado
#Read more and visit his site here:
#https://towardsdatascience.com/steganography-hiding-an-image-inside-another-77ca66b2acb1

import PIL
from PIL import Image, ImageFilter


class Steg(object):
	@staticmethod
	#method to convert integer image RGB values to binary
	def __int_to_bin(rgb):
		r,g,b = rgb
		return('{0:08b}'.format(r),
			'{0:08b}'.format(g),
			'{0:08b}'.format(b))

	@staticmethod
	#method to convert binary image RGB values to integer
	def __bin_to_int(rgb):
		r,g,b = rgb
		return(int(r,2),
			int(g,2),
			int(b,2))
	#Combine MSB of image 1 with LSB of image 2
	@staticmethod
	def __merge_rgb(rgb1,rgb2):
		r1,g1,b1=rgb1
		r2,g2,b2=rgb2
		rgb = (r1[:4] + r2[:4],
			g1[:4] + g2[:4],
			b1[:4] + b2[:4])
		return rgb

	@staticmethod
	#Unmerge the images by separating MSB and LSB of the images in to two images
	def __unmerge_rgb(rgb):
		r,g,b = rgb
		rgb1 = (r[:4] + '0000',
			g[:4] + '0000',
			b[:4] + '0000')
		rgb2 = (r[4:] + '0000',
			g[4:] + '0000',
			b[4:] + '0000')
		return rgb1, rgb2

	@staticmethod
	#Meat of the merging, pass two images of the same size, get back the merged images
	def merge(img1, img2):
		#load images
		pix1 = img1.load()
		pix2 = img2.load()

		#New, merged image created with the same size and coding as the first image
		img_new = Image.new(img1.mode, img1.size)
		pix_new = img_new.load()

		#Pixel colors are normally integers, we need to convert to binary
		#Convert to binary pixelwise across the whole photo
		for i in range(img1.size[0]):
			for j in range(img1.size[1]):
				rgb1 = Steg.__int_to_bin(pix1[i,j])
				rgb2 = Steg.__int_to_bin(pix2[i,j])
				#Merge the pixels of the two images in to a new binary value
				rgb = Steg.__merge_rgb(rgb1,rgb2)
				#Write the new binary value to the picture and convert it to integer
				pix_new[i,j] = Steg.__bin_to_int(rgb)
			if i%100 == 0:
				print("image rows merged: {}".format(i))
		print("image merged")
		return img_new

	@staticmethod
	#Unmerge the file in to two separate files, pass 
	def unmerge(img):
		pix = img.load()
		#Create two blank images with the same dimensions and settings
		img_unmerge1 = Image.new(img.mode, img.size)
		pix_unmerge1 = img_unmerge1.load()
		img_unmerge2 = Image.new(img.mode, img.size)
		pix_unmerge2 = img_unmerge2.load()

		#Pixelwise get the binary values of each pixel
		for i in range(img.size[0]):
			for j in range(img.size[1]):
				rgb = Steg.__int_to_bin(pix[i,j])
				#Break the pixel in to two pixels
				rgb1, rgb2 = Steg.__unmerge_rgb(rgb)
				#Convert binary to integer and set it to a pixel value
				pix_unmerge1[i,j] = Steg.__bin_to_int(rgb1)
				pix_unmerge2[i,j] = Steg.__bin_to_int(rgb2)
			if i%100 == 0:
				print("image rows unmerged: {}".format(i))
		print("image unmerged")
		return img_unmerge1, img_unmerge2

#Unmerge the photo and save them
def unmerge(img):
	i1_name = "unmerged1.png"
	i2_name = "unmerged2.png"
	unmerge_img1, unmerge_img2 = Steg.unmerge(Image.open(img))
	print("images unmerged")
	unmerge_img1.save(i1_name)
	unmerge_img2.save(i2_name)

#Merge the photos in to a new photo and save it
def merge(i1, i2):
	img1 = Image.open(i1)
	img2 = Image.open(i2)
	image_name = 'merged_image.png'
	merged_image = Steg.merge(img1,img2)
	merged_image.save(image_name)
	print("images merged as {}".format(image_name))




#Set up the files, print out some basic details, check that files are the same size
#Then merge and unmerge the files
if __name__=='__main__':

	i2 = "1.jpg"
	i1 = "2.jpg"
	i3 = "merged_image.png"

	img1 = Image.open(i1)
	img2 = Image.open(i2)

	size1 = img1.size
	size2 = img2.size

	print("size of image is: " + str(img1.size))
	print("size of image is: " + str(img2.size))
	print("format of image is: " + str(img1.format))
	print("mode of image is: " + str(img1.mode))
	print(img1.size[0])
	print(img1.size[1])

	#Images must be the same size
	if size1 == size2:
		print("images are the same size")
	else:
		raise ValueError('ERROR: Images not the same size')

	merge(i1,i2)
	unmerge(i3)