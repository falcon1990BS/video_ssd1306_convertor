Description:

The video_ssd1306_convertor converts a .mp4 video into a two dimensional C-language array.
This array can then be copied to an .h file and used by a ssd1306.c library.
This script is free, provided that the libraries used are also free.

Usage:

- The python script must be run with python 3
- Some libraries may need to be installed. Just use "pip" to use them. 
- The python script needs 3 arguments:
    1. Video path
    2. the project name
    3. decimation rate
      -> Allows you to reduce the number of images converted
- The ssd1306 C library come from this github
    -> https://github.com/guiguitz/STM32-Display-OLED-128x64-API/tree/main
- Create a project directory
- Copy .mp4 video to project directory
       
Steps:

1. Create a directory with the project name
2. Copy the python script
3. Copy the video in .mp4 format
4. Run a command prompt
5. Execute command:
    -> python VideoToSSD1306Convertor.py <path to video> <project name> <decimation rate>
6. The .c file is created in the project directory.

Example (windows):

```ssh
python VideoToSSD1306Convertor.py C:\<user>\Documents\<myproject>\<myvideo.mp4> <myprojectname> 1
```

Tutorial:

1. Create an animated logo with powerpoint 
![mylogo_01](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/144198be-14a7-4a86-b012-8f443942c93e)
![mylogo_02](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/8e15d62b-ea83-4c35-afa2-c3e671db1526)
![mylogo_03](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/fe1e623d-d06c-40ac-ba3c-07f543280e3f)
![mylogo_04](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/1d062b4a-4997-470a-966f-d39c45347165)

2. Export as .mp4 with a slightly longer duration than the animation
![mylogo_05](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/b4a05492-d53c-401c-92cf-2c41447cd8c0)
![mylogo_06](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/601f6dd9-abb3-45d0-b7ae-db0ae96f65ed)

3. Create a directory with the python script and video 
![mylogo_07](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/128a2d95-630d-4bb1-914f-a3c629835b36)

4. Run the python script from the directory
![mylogo_09](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/27474fe0-1664-4fc0-a70f-b35ac2565e83)
![mylogo_10](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/49b30ae3-0a92-4a51-8a80-2e5e3199a361)

5. Go to the generated directory <mylogossd1306_gif>.
![mylogo_11](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/247b295f-3173-4579-af95-f8f21ab78612)
The directory contains another directory with the images of the cut video, the gif of the video in 128x64 format and the C file of the table corresponding to the frames of the video.

The .gif is like this:

![mylogossd1306](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/7444841a-3811-4b21-80a2-2922266c6d20)

6. The C file is composed as follows
![mylogo_12](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/56671bb6-1007-4447-9504-309f74714d5f)

7. Used a function in the C program that calls the "SSD1306_DrawBitmap()" function.

Example (pseudo code):

```python
uint8_t display_logo()
{
	static uint8_t cpt = 0;
	SSD1306_Clear();
	SSD1306_DrawBitmap(0, 0, gif_array[cpt], 128, 64, 1);
	if(cpt++ >= 56)
	{
		SSD1306_Clear();
		cpt =0;
	}
	SSD1306_UpdateScreen();
	return 0;
}
```

8. the result is like this

![MYLOGO](https://github.com/falcon1990BS/video_ssd1306_convertor/assets/37402726/944f90bf-64cf-461f-9af8-326b2f2c23f8)






