import os
import base64
import requests

def define_path(folder_path):
    return folder_path

def list_image_files(path):
    """
    List all image files in the given folder based on common image file extensions.
    
    :param path: str - The path to the folder.
    :return: list - A list containing the full paths of all image files in the folder.
    """
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.avif')
    image_files = [] 
    
    try:
        for file in os.listdir(path):
            if file.lower().endswith(valid_extensions):
                full_path = os.path.join(path, file)
                image_files.append(full_path)
        return image_files
    except FileNotFoundError:
        return "The folder path does not exist."

def encode_image_to_base64(image_path):
    """
    Encode an image file to Base64.
    
    :param image_path: str - The path to the image file.
    :return: str - The Base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_image_captions(image_files):
    """
    Send image files to the local Ollama Llava model and get captions for each image.
    
    :param image_files: list - A list of full paths to image files.
    :return: dict - A dictionary with image file names as keys and their captions as values.
    """
    url = "http://localhost:11434/api/generate"  
    headers = {"Content-Type": "application/json"}
    captions = {}

    for image_path in image_files:
        image_base64 = encode_image_to_base64(image_path)
        payload = {
            "model": "llava:latest", 
            "prompt": "Describe in as many details as possible What is shown in this image, including the style of the image.",
            "stream": False,
            "images": [image_base64]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            captions[os.path.basename(image_path)] = result.get('response', 'No caption generated')
        else:
            captions[os.path.basename(image_path)] = "Failed to generate caption"

    return captions

def save_captions_to_text(captions, folder_path):
    for image_name, caption in captions.items():
        base_name = os.path.splitext(image_name)[0]
        text_file_name = f"{base_name}.txt"
        text_file_path = os.path.join(folder_path, text_file_name)
        
        with open(text_file_path, 'w', encoding='utf-8') as file:
            file.write(caption)
        print(f"Saved caption to {text_file_path}")

def refine_caption(caption):
    """
    Refine the generated caption by removing stop words and limiting its length.
    
    :param caption: str - The original caption.
    :return: str - The refined caption.
    """
    stop_words = {'a', 'an', 'the', 'are', 'is', 'in', 'of', 'to', 'with', 'on'}
    words = [word for word in caption.split() if word not in stop_words][:3]
    return '_'.join(words)

def rename_images_based_on_captions(folder_path):
    """
    Reads descriptions from .txt files, generates short captions using an API,
    and renames image files and their corresponding .txt files to these captions.
    
    :param folder_path: str - The path to the folder containing image and text files.
    """
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.avif')
    existing_names = set()  
    
    all_files = os.listdir(folder_path)
    print(f"Listing all files: {all_files}")

    for file in all_files:
        if file.endswith('.txt'):
            base_name = file[:-4]
            image_path = None
            for ext in valid_extensions:
                potential_path = os.path.join(folder_path, base_name + ext)
                matched_files = [f for f in all_files if f.lower() == base_name.lower() + ext]
                if matched_files:
                    image_path = os.path.join(folder_path, matched_files[0])
                    break
            
            if not image_path:
                print(f"No matching image file found for {file}")
                continue
            
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as txt_file:
                description = txt_file.read().strip()
            
            payload = {
                "model": "llama3.1:latest",
                "prompt": f"Summarize the main subject in 2-3 words based on this description: {description}. just provide the 2-3 words, do not write anything except to the 2-3 words caption! e.g: an apple, wolverine, etc.",
                "stream": False
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                result = response.json()
                raw_caption = result.get('response', 'caption')
                short_caption = refine_caption(raw_caption)
                short_caption = ''.join(char for char in short_caption if char.isalnum() or char in ['_', '-'])[:15]

                counter = 1
                unique_caption = short_caption
                while unique_caption in existing_names:
                    unique_caption = f"{short_caption}_{counter}"
                    counter += 1
                existing_names.add(unique_caption)
                
                new_image_path = os.path.join(folder_path, unique_caption + os.path.splitext(image_path)[1])
                new_txt_path = os.path.join(folder_path, unique_caption + '.txt')
                
                os.rename(image_path, new_image_path)
                os.rename(os.path.join(folder_path, file), new_txt_path)
                print(f"Renamed {base_name} to {unique_caption}")
            else:
                print(f"Failed to generate caption for {base_name}")

images_folder_path = '<REPLACE THIS WITH THE PATH TO YOUR IMAGES FOLDER>'
folder = define_path(images_folder_path)
contents = list_image_files(folder)
captions = generate_image_captions(contents)
save_captions_to_text(captions, folder)
rename_images_based_on_captions(images_folder_path)
