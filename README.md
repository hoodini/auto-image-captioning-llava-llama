![YUV.AI AUTO CAPTIONING](https://github.com/hoodini/auto-image-captioning-llava-llama/blob/main/colorful-phoenix-made-of-neural-networks-flying-ov-LmOfJkIFTUGdbiCqxYoBSA-oK_jb_CfSua1QFoOR4pc4w.jpeg?raw=true)

# Image Captioning and Renaming Script

This script is designed to automate the process of generating detailed captions for images, saving them to text files, and renaming the image files based on the generated captions. The script uses a local model API to generate captions and refine them to create descriptive and concise filenames.

## Features

- **List Image Files**: Identifies and lists image files in a specified directory based on common image file extensions.
- **Encode Images to Base64**: Converts image files to Base64 encoding for easy transmission.
- **Generate Image Captions**: Sends the Base64-encoded images to a local model API and generates detailed captions.
- **Save Captions to Text Files**: Saves the generated captions in text files with the same name as the corresponding image.
- **Refine and Rename Images**: Refines the captions to 2-3 word summaries and renames the image files and text files based on these summaries.

## Requirements

- Python 3.x
- Required Python libraries:
  - `os`
  - `base64`
  - `requests`
- [Ollama](https://ollama.com) installed and configured.

## Setup

1. **Install Ollama**: Make sure you have Ollama installed on your machine.

2. **Start the Required Models**:
   - Open a terminal and run the following command to start the Llava model:
     ```bash
     ollama run llava:latest
     ```
   - In a separate terminal, run the following command to start the Llama model:
     ```bash
     ollama run llama:latest
     ```

3. **Set the Image Folder Path**: Before running the script, change the path to your image folder.
   
   Replace this line:
    ```python
    images_folder_path = '/Users/yuval.avidani/Downloads/test'
    ```
   with the path to your images:
    ```python
    images_folder_path = '/path/to/your/images'
    ```

4. **Run the Script**: Once the models are running and the path is set, run the script.

   The script will:
   - List all image files in the folder.
   - Generate captions using the local model API.
   - Save the captions in text files.
   - Rename the image files and text files based on the refined captions.

## Functions in the Script

- `define_path(folder_path)`: Returns the folder path.
- `list_image_files(path)`: Lists all image files in the given folder.
- `encode_image_to_base64(image_path)`: Encodes an image file to Base64.
- `generate_image_captions(image_files)`: Sends image files to the local model API and gets captions.
- `save_captions_to_text(captions, folder_path)`: Saves the generated captions to text files.
- `refine_caption(caption)`: Refines the generated caption by removing stop words and limiting its length.
- `rename_images_based_on_captions(folder_path)`: Renames images based on refined captions.

## Example

```python
images_folder_path = '/Users/yourname/Downloads/test'
folder = define_path(images_folder_path)
contents = list_image_files(folder)
captions = generate_image_captions(contents)
save_captions_to_text(captions, folder)
rename_images_based_on_captions(images_folder_path)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

This project was created by **Yuval Avidani (YUV.AI)**. If you find this code useful, please give credit to Yuval by mentioning **YUV.AI** and tagging **@yuvalav** on X (formerly Twitter).

## Disclaimer

This script requires a local model API to function. Ensure that the API is correctly configured and accessible on your local machine before running the script.
