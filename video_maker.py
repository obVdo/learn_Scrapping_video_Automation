from moviepy.editor import *
import os
import random
from PIL import Image
from moviepy.video.fx import loop

def get_image_position(image_height, video_height):
    if image_height > video_height:
        return ("center", "top")
    else:
        return ("center", "center")

def create_reddit_comments_video():
    # Directory and file paths
    comment_images_dir = "comment_screenshots"  # Directory containing comment images
    audio_dir = "output_audio"  # Directory containing audio files
    intermediate_video_dir = "intermediate_videos"  # Directory for intermediate video files
    background_size = (1920, 1080)  # Size of the background video
    background_videos_dir = "../background_videos"  # Directory containing background videos
    output_video_file = "reddit_comments_video.mp4"  # Output video file name
    trans = '../trans.mp4'  # Transition video file
    comment_image_files = sorted(
        [
            os.path.join(comment_images_dir, f)
            for f in os.listdir(comment_images_dir)
            if f.endswith(".png")
        ]
    )
    audio_files = sorted(
        [
            os.path.join(audio_dir, f)
            for f in os.listdir(audio_dir)
            if f.endswith(".mp3")
        ]
    )

    os.makedirs(intermediate_video_dir, exist_ok=True)

    background_video_files = [
        os.path.join(background_videos_dir, f)
        for f in os.listdir(background_videos_dir)
        if f.endswith((".mp4", ".avi", ".mov"))
    ]

    # Function to calculate image position based on image height and video height
    def position_at_time(t):
        if t < scroll_start_time:
            return position
        else:
            # Calculate the scrolling position based on scrolling speed
            y = -scroll_speed * (t - scroll_start_time)
            return ("center", y)

    for image_file in comment_image_files:
        comment_number = os.path.splitext(os.path.basename(image_file))[0].split("_")[1]
        i = comment_number
        audio_file = os.path.join(audio_dir, f"comment_{comment_number}.mp3")

        if not os.path.isfile(audio_file):
            print(f"Audio file not found for comment {comment_number}. Skipping.")
            continue

        image = Image.open(image_file)
        image_width, image_height = image.size
        position = get_image_position(image_height, background_size[1])

        comment_video = ImageClip(image_file, duration=2)
        audio_clip = AudioFileClip(audio_file)
        audio_duration = audio_clip.duration

        scroll_start_time = 1 * 60 + 30  # 1 minute = 60 seconds

        # Calculate the scrolling duration (audio duration minus start time)
        scroll_duration = audio_duration - scroll_start_time

        # Calculate the scrolling speed so it takes 2 minutes to scroll 1080 pixels
        desired_scrolling_time = 2 * 60  # 2 minutes = 120 seconds
        scroll_speed = 1080 / desired_scrolling_time

        if image_height > background_size[1]:
            comment_video = comment_video.set_position(lambda t: position_at_time(t))
        else:
            comment_video = comment_video.set_position(position)
        comment_video = comment_video.set_duration(audio_clip.duration)
        video_with_audio = comment_video.set_audio(audio_clip)
        background_clip = VideoFileClip(random.choice(background_video_files))
        background_clip = background_clip.set_audio(None)
        background_clip = background_clip.loop(duration=video_with_audio.duration)

        final_video_clip = CompositeVideoClip([background_clip, video_with_audio])
        final_video_clip = concatenate_videoclips(
            [VideoFileClip(trans), final_video_clip], method="compose"
        )
        intermediate_video_file = os.path.join(
            intermediate_video_dir, f"intermediate_video_{i}.mp4"
        )
        final_video_clip.write_videofile(
            intermediate_video_file, codec="libx264", fps=24
        )

    intermediate_video_files = [
        os.path.join(intermediate_video_dir, f)
        for f in os.listdir(intermediate_video_dir)
        if f.endswith(".mp4")
    ]

    final_video_clips = [
        VideoFileClip(video_file) for video_file in intermediate_video_files
    ]
    final_video = concatenate_videoclips(
        final_video_clips, method="compose", bg_color=[11, 20, 22]
    )
    final_video.write_videofile(output_video_file, codec="libx264", fps=24)

if __name__ == "__main__":
    create_reddit_comments_video()
