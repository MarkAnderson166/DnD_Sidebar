import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import math
import cv2

video_capture = None

# Load images and videos from nested directories
def load_media_from_nested_folders(base_directory):
    media_dict = {}
    for root, dirs, files in os.walk(base_directory):
        folder_name = os.path.basename(root)
        media_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg', '.mp4'))]
        if media_files:
            media_dict[folder_name] = media_files
    return media_dict

# Function to display the media
def show_media(folder_name, index):
    global current_media, current_rotation
    if folder_name in media_dict:
        media_file = media_dict[folder_name][index]
        media_path = os.path.join(media_directory, folder_name, media_file)

        # Stop video if it was playing
        if isinstance(current_media, str) and current_media.endswith('.mp4'):
            stop_video()

        # Check if it's a video or an image
        if media_file.endswith(('.png', '.jpg', '.jpeg')):
            current_media = Image.open(media_path)
            current_rotation = 0
            display_image()
        elif media_file.endswith('.mp4'):
            current_media = media_path
            stop_video()  # Ensure the previous video is stopped
            play_video()

# Function to display the current image with rotation and grid
def display_image():
    global current_media, current_rotation
    if isinstance(current_media, Image.Image):
        rotated_image = current_media.rotate(current_rotation, expand=True)
        photo = ImageTk.PhotoImage(rotated_image)
        image_window.image_label.config(image=photo)
        image_window.image_label.image = photo
        if show_grid_var.get():
            draw_grid(rotated_image)

# Play video in a loop
def play_video():
    global video_capture
    video_capture = cv2.VideoCapture(current_media)

    def update_video():
        ret, frame = video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((image_window.winfo_width(), image_window.winfo_height()), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            image_window.image_label.config(image=photo)
            image_window.image_label.image = photo
            if show_grid_var.get():
                draw_grid(img)  # Draw grid over the video
            image_window.after(30, update_video)  # Update every 30 ms
        else:
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            update_video()

    update_video()

# Stop the currently playing video
def stop_video():
    global video_capture
    if video_capture is not None:
        video_capture.release()
        video_capture = None

# Toggle fullscreen and windowed mode
def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        image_window.attributes("-fullscreen", True)
    else:
        image_window.attributes("-fullscreen", False)
        image_window.geometry("800x600")

# Rotate the image by 90 degrees
def rotate_image():
    global current_rotation
    current_rotation = (current_rotation + 90) % 360
    display_image()

# Draw grid overlay based on selected grid type
def draw_grid(image):
    grid_image = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(grid_image)
    width, height = image.size
    grid_type = grid_type_var.get()
    x_offset = x_offset_var.get()
    y_offset = y_offset_var.get()
    grid_size = grid_size_var.get()

    # Clear previous grid
    draw.rectangle((0, 0, width, height), fill=(0, 0, 0, 0))

    # Set thickness and color
    thickness = thickness_var.get()
    color = color_var.get()

    if grid_type == 'Hexagonal':
        hex_height = int(math.sqrt(3) * grid_size)

        for row in range(int(height / hex_height) + 1):
            for col in range(int(width / (grid_size * 3 / 2)) + 1):
                x = col * grid_size * 3 / 2 + x_offset
                y = row * hex_height + (hex_height // 2 if col % 2 else 0) + y_offset
                points = [
                    (x + grid_size * math.cos(math.radians(angle)), y + grid_size * math.sin(math.radians(angle)))
                    for angle in range(0, 360, 60)
                ]
                draw.line(points + [points[0]], fill=color, width=thickness)

    elif grid_type == 'Square':
        grid_size = int(grid_size * 1.5)
        for x in range(0, width + grid_size, grid_size):
            draw.line([(x + x_offset, 0), (x + x_offset, height)], fill=color, width=thickness)
        for y in range(0, height + grid_size, grid_size):
            draw.line([(0, y + y_offset), (width, y + y_offset)], fill=color, width=thickness)

    overlay_image = Image.alpha_composite(image.convert("RGBA"), grid_image)
    photo = ImageTk.PhotoImage(overlay_image)
    image_window.image_label.config(image=photo)
    image_window.image_label.image = photo

# Create a fullscreen window for displaying media
def create_image_window():
    global image_window, fullscreen, current_media, current_rotation
    fullscreen = False
    current_media = None
    current_rotation = 0

    image_window = tk.Toplevel()
    image_window.title("Media Display")
    image_window.geometry("800x600")

    image_window.image_label = tk.Label(image_window)
    image_window.image_label.pack(expand=True)

    image_window.image_label.bind("<Double-Button-1>", toggle_fullscreen)

# Set up the controller window
controller_window = tk.Tk()
controller_window.title("Media Controller")

# Load media from nested directories
media_directory = r"D:\DnD_Sidebar"  # Change this to your media directory
media_dict = load_media_from_nested_folders(media_directory)

# Create dropdowns for each folder
for folder in media_dict.keys():
    label = tk.Label(controller_window, text=folder)
    label.pack(pady=5)

    combo = ttk.Combobox(controller_window, values=media_dict[folder], state="readonly")
    combo.current(0)
    combo.bind("<<ComboboxSelected>>", lambda e, f=folder, c=combo: show_media(f, c.current()))
    combo.pack(pady=5)

# Rotation button on the controller
rotate_button = tk.Button(controller_window, text="Rotate 90°", command=rotate_image)
rotate_button.pack(side=tk.LEFT, padx=5, pady=5)

# Grid toggle button
show_grid_var = tk.BooleanVar(value=False)
toggle_grid_button = tk.Checkbutton(controller_window, text="Show Grid", variable=show_grid_var, command=display_image)
toggle_grid_button.pack(side=tk.LEFT, padx=5, pady=5)

# Grid type selection
grid_type_var = tk.StringVar(value='Hexagonal')
grid_type_frame = tk.Frame(controller_window)
grid_type_frame.pack(pady=5)

hex_radio = tk.Radiobutton(grid_type_frame, text='Hexagonal', variable=grid_type_var, value='Hexagonal', command=display_image)
hex_radio.pack(side=tk.LEFT)

square_radio = tk.Radiobutton(grid_type_frame, text='Square', variable=grid_type_var, value='Square', command=display_image)
square_radio.pack(side=tk.LEFT)

# Slider for grid X offset
x_offset_var = tk.IntVar(value=0)
x_offset_slider = tk.Scale(controller_window, from_=0, to=100, variable=x_offset_var, label="X Offset", orient=tk.HORIZONTAL, command=lambda x: display_image())
x_offset_slider.pack(fill=tk.X, padx=5, pady=5)

# Slider for grid Y offset
y_offset_var = tk.IntVar(value=0)
y_offset_slider = tk.Scale(controller_window, from_=0, to=100, variable=y_offset_var, label="Y Offset", orient=tk.HORIZONTAL, command=lambda x: display_image())
y_offset_slider.pack(fill=tk.X, padx=5, pady=5)

# Slider for grid size
grid_size_var = tk.IntVar(value=40)
grid_size_slider = tk.Scale(controller_window, from_=40, to=100, variable=grid_size_var, label="Grid Size", orient=tk.HORIZONTAL, command=lambda x: display_image())
grid_size_slider.pack(fill=tk.X, padx=5, pady=5)

# Thickness selection
thickness_var = tk.IntVar(value=2)
thickness_frame = tk.Frame(controller_window)
thickness_frame.pack(pady=5)

thickness_label = tk.Label(thickness_frame, text="Line Thickness:")
thickness_label.pack(side=tk.LEFT)

for thickness in [1, 2, 3]:
    thickness_radio = tk.Radiobutton(thickness_frame, text=str(thickness), variable=thickness_var, value=thickness, command=display_image)
    thickness_radio.pack(side=tk.LEFT)

# Color selection
color_var = tk.StringVar(value='grey')
color_frame = tk.Frame(controller_window)
color_frame.pack(pady=5)

color_label = tk.Label(color_frame, text="Line Color:")
color_label.pack(side=tk.LEFT)

for color in ['black', 'grey', 'white', 'red']:
    color_radio = tk.Radiobutton(color_frame, text=color.capitalize(), variable=color_var, value=color, command=display_image)
    color_radio.pack(side=tk.LEFT)

# Create the image window
create_image_window()

# Show the initial media from the first folder
if media_dict:
    initial_folder = next(iter(media_dict))
    show_media(initial_folder, 0)

controller_window.mainloop()
