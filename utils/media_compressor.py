import io
import subprocess
import os
import tempfile
import shutil
import ffmpeg

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


class MediaCompressor:
    SUPPORTED_FORMATS = {
        'JPEG': {'ext': '.jpg', 'save_kwargs': {'quality': 85, 'optimize': True}},
        'PNG': {'ext': '.png', 'save_kwargs': {'optimize': True}},
        'GIF': {'ext': '.gif', 'save_kwargs': {'optimize': True}},
        'WEBP': {'ext': '.webp', 'save_kwargs': {'quality': 85, 'method': 6}},
    }

    @staticmethod
    def compress_image(image, output_path=None, quality=85, max_width=1200, max_height=1200):
        """
        Compress an image while preserving its original format when possible.
        Supports JPEG, PNG, GIF, and WebP formats.

        Parameters:
        - image: Image file (InMemoryUploadedFile, path, or file-like object)
        - output_path: Optional custom output path/filename
        - quality: Quality setting for lossy formats (1-100)
        - max_width: Maximum width after compression
        - max_height: Maximum height after compression

        Returns:
        - ContentFile object containing the compressed image
        """
        try:
            # Handle InMemoryUploadedFile case (Django file upload)
            if isinstance(image, InMemoryUploadedFile):
                image_data = io.BytesIO(image.read())
                image.seek(0)  # Reset file pointer for future reads
                original_filename = image.name
            elif isinstance(image, str):
                image_data = image
                original_filename = os.path.basename(image)
            else:
                image_data = image
                original_filename = getattr(image, 'name', 'image')

            # Open and process the image
            img = Image.open(image_data)
            original_format = img.format or 'JPEG'  # Default to JPEG if format is None

            # Handle animated GIFs specially
            is_animated = hasattr(img, 'is_animated') and img.is_animated

            if is_animated:
                # For animated GIFs, we need to handle frames
                frames = []
                try:
                    while True:
                        # Copy the current frame
                        frame = img.copy()
                        
                        # Resize frame if needed
                        if frame.size[0] > max_width or frame.size[1] > max_height:
                            frame.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                        
                        frames.append(frame)
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass  # We've reached the last frame

                # Save animated GIF
                output_buffer = io.BytesIO()
                frames[0].save(
                    output_buffer,
                    format='GIF',
                    save_all=True,
                    append_images=frames[1:],
                    optimize=True,
                    duration=img.info.get('duration', 100),
                    loop=img.info.get('loop', 0)
                )
            else:
                # Process single image
                # Preserve transparency for PNG and non-animated GIF
                if img.mode in ('RGBA', 'LA') and original_format in ('PNG', 'GIF'):
                    # Keep alpha channel
                    pass
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # Resize if the image is larger than max dimensions
                if img.size[0] > max_width or img.size[1] > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                # Get format-specific save parameters
                format_info = MediaCompressor.SUPPORTED_FORMATS.get(
                    original_format,
                    MediaCompressor.SUPPORTED_FORMATS['JPEG']
                )
                
                # Update quality for lossy formats
                if original_format in ('JPEG', 'WEBP'):
                    format_info['save_kwargs']['quality'] = quality

                # Create output buffer
                output_buffer = io.BytesIO()
                img.save(
                    output_buffer,
                    format=original_format,
                    **format_info['save_kwargs']
                )

            output_buffer.seek(0)

            # Determine output filename
            if output_path:
                output_filename = output_path
            else:
                # Preserve original extension if it matches the format
                original_ext = os.path.splitext(original_filename)[1].lower()
                format_info = MediaCompressor.SUPPORTED_FORMATS.get(original_format)
                if format_info and original_ext == format_info['ext']:
                    output_filename = original_filename
                else:
                    output_filename = f"{os.path.splitext(original_filename)[0]}{format_info['ext']}"

            # Create ContentFile
            compressed_image = ContentFile(output_buffer.getvalue(), name=output_filename)
            
            return compressed_image
            
        except Exception as e:
            raise ValidationError(f"Error compressing image: {str(e)}")
        
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
            # Create a temporary directory to handle the files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Generate temporary file paths
                temp_input = os.path.join(temp_dir, 'input' + os.path.splitext(video.name)[1])
                temp_output = os.path.join(temp_dir, 'output' + os.path.splitext(video.name)[1])
                
                # Handle Django UploadedFile objects
                if hasattr(video, 'temporary_file_path'):
                    # For TemporaryUploadedFile
                    input_path = video.temporary_file_path()
                else:
                    # For InMemoryUploadedFile or other file-like objects
                    with open(temp_input, 'wb') as f:
                        if hasattr(video, 'chunks'):
                            for chunk in video.chunks():
                                f.write(chunk)
                        else:
                            f.write(video.read())
                    input_path = temp_input
    
                # Compress the video using ffmpeg
                try:
                    stream = ffmpeg.input(input_path)
                    stream = ffmpeg.output(stream, temp_output, video_bitrate=target_bitrate)
                    ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
                except ffmpeg.Error as e:
                    raise ValidationError(f"FFmpeg error: {e.stderr.decode()}")
    
                # Read the compressed file
                with open(temp_output, 'rb') as f:
                    compressed_content = f.read()
    
                # Create a ContentFile with the compressed video
                output_filename = output_path if output_path else video.name
                return ContentFile(compressed_content, name=output_filename)
    
        except Exception as e:
            raise ValidationError(f"Error compressing video: {str(e)}")

    @staticmethod
    def extract_image_metadata(image_file):
        """Helper function to extract image metadata."""
        try:
            if isinstance(image_file, ContentFile):
                image = Image.open(io.BytesIO(image_file.read()))
                file_size = image_file.size
            else:
                image = Image.open(image_file)
                file_size = getattr(image_file, 'size', 0)
                
            width, height = image.size
            file_type = image.format if image.format is not None else None
            
            return {
                'width': width,
                'height': height,
                'file_size': file_size,
                'file_type': file_type
            }
        except Exception as e:
            raise ValidationError(f"Error extracting image metadata: {str(e)}")

    @staticmethod
    def extract_video_metadata(video_file):
        """Helper function to extract video metadata."""
        try:
            # Create a temporary file to analyze with ffmpeg
            with tempfile.NamedTemporaryFile(suffix=os.path.splitext(video_file.name)[1], delete=False) as temp_file:
                if isinstance(video_file, ContentFile):
                    temp_file.write(video_file.read())
                    video_file.seek(0)  # Reset the file pointer
                else:
                    shutil.copyfileobj(video_file, temp_file)
                
                temp_file_path = temp_file.name
    
            try:
                # Probe the temporary file
                probe = ffmpeg.probe(temp_file_path, v='error', select_streams='v:0', show_entries='stream=width,height,duration')
                stream_info = probe.get('streams', [{}])[0]
                
                metadata = {
                    'width': int(stream_info.get('width', 0)),
                    'height': int(stream_info.get('height', 0)),
                    'duration': float(stream_info.get('duration', 0)),
                    'file_size': video_file.size if hasattr(video_file, 'size') else os.path.getsize(temp_file_path),
                }
    
                return metadata
    
            finally:
                # Clean up the temporary file
                os.unlink(temp_file_path)
    
        except Exception as e:
            raise ValidationError(f"Error extracting video metadata: {str(e)}")

