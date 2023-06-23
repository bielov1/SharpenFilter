# Фільтр підвищення різкості для обробки зображень

## Demo

![alt text](C:\Users\Oleg\Downloads\rwq.png)

## Unsharp masking and highboost filtering
Subtracting an unsharp (smoothed) version of an image from the original image is 
process that has been used since the 1930s by the printing and publishing industry to 
sharpen images. This process, called unsharp masking, consists of the following steps:

1. Blur the original image
2. Subtract the blurred image from original(the resulting difference is called the <mark>mask</mark>) 
3. Add the mask to the original

## Smoothing or Blurring spatial filter

Smoothing (also called averaging) spatial filters are used to reduce sharp transitions in intensity. Because random noise typically consists of sharp transitions in intensity, an obvious application of smoothing is noise reduction

### Lowpass Gaussian filter kernel
Gaussian kernels of the form:

![alt text](C:\Users\Oleg\Downloads\Tex2Img_1687542221.jpg)

This equivalent form simplifies derivation of expressions later in this section. This 
form also reminds us that the function is circularly symmetric. Variable r is the distance from the center to any point on function G. Figure 3.0.1 shows values of r for 
several kernel sizes using integer values for s and t. Because we work generally with 
odd kernel sizes, the centers of such kernels fall on integer values, and it follows that 
all values of r^2
 are integers also. 

![alt text](C:\Users\Oleg\Downloads\Знімок екрана 2023-06-23 205051.png)


## Results

let's try to sharpen some images.


![alt text](G:\CourseWork\IPZ-coursework\Test images\moon.jpg)
![alt text](G:\CourseWork\IPZ-coursework\Test images\saved_moon.jpg)



![alt text](G:\CourseWork\IPZ-coursework\Test images\imoon.jpg)
![alt text](G:\CourseWork\IPZ-coursework\Test images\moon2_saved.jpg)