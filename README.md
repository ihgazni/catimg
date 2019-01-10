# catimg
show image on server without X display  installed 


## Usage

        1. on a server without X-display installed

![](doc/images/catimg.0.png)


        2. adjust the terminal size,
           more small, more clear, more slow
           
 ![](doc/images/catimg.1.png)


        3. python3 catimg.py xxxxx.png
 
  ![](doc/images/catimg.2.png)
        
        4. cat _xxxxx.png.txt 
  
  ![](doc/images/catimg.4.png)
  
  
        5. the result generated in a very 7-point fontsize terminal
        
  ![](doc/images/catimg.3.png)
  
  
## Others

just map the bgr color-space to ansi-256 color-space
handled pixel-by-pixel, so its slow................
