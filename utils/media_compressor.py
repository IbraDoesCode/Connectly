import os
from PIL import Image
import ffmpeg
from io import BytesIO
from django.core.exceptions import ValidationError

class MediaCompressor:
    @staticmethod
    def compress_image(image, output_path=None, quality=85, max_width=1200, max_height=1200):
        """
        Compress an image to reduce its size.
        
        Parameters:
        - image: Image file to compress
        - output_path: Output file path to save the compressed image (if None, will overwrite original file)
        - quality: Quality of the output image (1-100)
        - max_width: Maximum width of the image
        - max_height: Maximum height of the image
        
        Returns:
        - Compressed image (either saved to the file system or returned as a BytesIO object)
        """
        try:
            # Open the image file
            img = Image.open(image)
            
            # Resize if the image is larger than max dimensions
            img.thumbnail((max_width, max_height), Image.ANTIALIAS)

            # Prepare the output path or use the original file
            if output_path is None:
                output_path = image.name  
            
            # Save the compressed image with the specified quality
            img.save(output_path, quality=quality, optimize=True, format="JPEG")

            return output_path
        except Exception as e:
            raise ValidationError(f"Error compressing image: {e}")

    @staticmethod
    def compress_video(video, output_path=None, target_bitrate="1000k"):
        """
        Compress a video file using ffmpeg.
        
        Parameters:
        - video: Video file to compress
        - output_path: Output file path to save the compressed video (if None, will overwrite original file)
        - target_bitrate: Bitrate to set for the compressed video (e.g., '1000k' for 1000 kbps)
        
        Returns:
        - Compressed video (either saved to the file system or returned as a file path)
        """
        try:
            # Check if the output path is specified, or use the input file name
            if output_path is None:
                output_path = video.name

            # Compress the video using ffmpeg
            ffmpeg.input(video).output(output_path, video_bitrate=target_bitrate).run()

            return output_path
        except ffmpeg.Error as e:
            raise ValidationError(f"Error compressing video: {e}")

