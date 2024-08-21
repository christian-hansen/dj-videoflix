from videoflix.admin import VideoResource
dataset = VideoResource().export()

# Write the JSON data to a file
if dataset:
    with open('./backups/exported_video_data.txt', 'w') as file:
        file.write(dataset.json)  # Assuming datase
        print('Video data exported')