import os
import sys
from PIL import Image, ImageOps
from moviepy.editor import VideoFileClip
from PIL import Image, ImageSequence
import math
import shutil
        
def rename_and_replace_images(directory):
    # Browse all files in the directory
    for counter, filename in enumerate(sorted(os.listdir(directory), key=lambda x: os.path.getmtime(os.path.join(directory, x)))):
        if filename.endswith(".gif"):
            file_path = os.path.join(directory, filename)
            new_filename = f"gif_{counter + 1}.gif"
            new_file_path = os.path.join(directory, new_filename)

            # Rename file with new name (replacement)
            os.rename(file_path, new_file_path)

def image_to_1d_array(image_path):
    # Load image
    img = Image.open(image_path)

    # Convert image to black & white (1 bit per pixel)
    img_bw = img.convert("1")

    # Invert image colors
    img_bw = ImageOps.invert(img_bw)

    # Get image dimensions
    width, height = img.size

    # Initialize a list to store image pixels
    pixels = []

    # Browse each image pixel
    for y in range(height):
        for x in range(0, width, 8):  # Group by bytes
            byte = 0
            for i in range(8):
                if x + i < width:
                    # Get pixel value (0 for black, 255 for white)
                    pixel_value = img_bw.getpixel((x + i, y))
                    # Convert pixel value to 0 or 1
                    pixel_value = 0 if pixel_value == 0 else 1
                    # Shift and add pixel value to byte
                    byte |= pixel_value << (7 - i)
            # Add byte to list
            pixels.append(byte)

    # Return pixel list
    return pixels

def process_images_in_directory(directory, output_file, decimation):
    # Open file in write mode
    with open(output_file, 'w') as f_out:
        # Redirect output to file
        original_stdout = sys.stdout
        sys.stdout = f_out

        # Initialize a list to store the pixels of all images
        all_image_pixels = []

        # Browse all files in directory
        for filename in os.listdir(directory):
            if filename.endswith(".gif"):
                file_path = os.path.join(directory, filename)

                # Call function to obtain image pixels
                image_pixels = image_to_1d_array(file_path)

                # Add image pixels to list
                all_image_pixels.append(image_pixels)
         
        # Calculate array size
        d1 = len(all_image_pixels[0])
        d1 = math.ceil(d1 / 16)
        d1 = math.ceil(d1 / decimation)
        d1 = d1 + 1
        d2 = len(all_image_pixels[0])
                
        # Display the array in the output file
        print("const unsigned char gif_array[{}][{}] = {{".format(d1, d2), file=f_out)
        for idx, image_pixels in enumerate(all_image_pixels):
            # test for decimation
            if idx%decimation==0:
                row_content = "    {"
                for i, pixel in enumerate(image_pixels):
                    if i > 0 and i % 16 == 0:
                        row_content += "\n     "
                    row_content += f"0x{pixel:02X}"
                    if i != len(image_pixels) - 1:
                        row_content += ", "
                row_content += "}"
                if idx != len(all_image_pixels) - 1:
                    row_content += ","
                row_content += "\n"
                print(row_content, end="", file=f_out)
            
        print("};", file=f_out)

        # Restore standard output
        sys.stdout = original_stdout
        
def movie_convertor(mp4_file_path, gif_path, folder_gif_path):
    clip = VideoFileClip(mp4_file_path)
    # Resize video
    new_clip = clip.resize(newsize=(128, 64))
    # Save resized video
    new_clip.write_gif(gif_path, fps=30)

    # Open GIF file
    with Image.open(input_gif_path) as gif:
        # Browse each frame of the GIF file
        for i, frame in enumerate(ImageSequence.Iterator(gif)):
            # Create a file name for each frame
            output_image_path  = f"{folder_gif_path}/frame_{i}.gif"
            # Save frame as image
            frame.save(output_image_path )
    

if __name__ == "__main__":
    # Test input arguments
    if len(sys.argv) != 4:
        print("Need 3 arguments: 1=video path, 2=project name, 3=decimation factor (int)")
        sys.exit(1)
    
    # retrieve arguments 
    mp4_file_path = sys.argv[1]
    project_name = sys.argv[2]
    
    # Create directory paths
    actual_path = os.path.dirname(mp4_file_path)
    directory_path = os.path.join(actual_path, project_name)
    
    # Creation of working paths 
    gif_path = directory_path + "\\" + project_name + ".gif"
    folder_gif_path = directory_path + "\\" + sys.argv[2] + "_gif"
    input_video_path = sys.argv[1]
    input_gif_path = gif_path
    
    # Path to image directory and C output file
    output_file = directory_path + "\\" + sys.argv[2] + "_tab.c" 
    decimation = int(sys.argv[3])
    
    # Create new working directory
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        
    # Delete gif image backup directory
    try:
        shutil.rmtree(folder_gif_path)
        print(f"Directory '{folder_gif_path}' has been successfully deleted.")
    except Exception as e:
        print(f"Error deleting directory '{folder_gif_path}': {e}")
    # Create new directory for saving gif images
    os.makedirs(folder_gif_path)
    
    # Convert video to gif image
    movie_convertor(mp4_file_path, gif_path, folder_gif_path)

    # Rename and replace images in folder
    rename_and_replace_images(folder_gif_path)

    # Call function to process all renamed images in directory and write to C file
    process_images_in_directory(folder_gif_path, output_file, decimation)

    print(f"Data written to the C file : {output_file}")
    
