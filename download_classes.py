# download_classes.py
import json
import urllib.request
import os

def main():
    url = 'https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt'
    dest_txt = 'imagenet_classes.txt'
    dest_json = 'imagenet_classes.json'
    
    print('Downloading ImageNet class list...')
    try:
        urllib.request.urlretrieve(url, dest_txt)
        print('ImageNet classes txt downloaded!')
        
        with open(dest_txt, 'r', encoding='utf-8') as f:
            classes = [line.strip() for line in f]
        
        # Build dictionary
        class_dict = {i: name for i, name in enumerate(classes)}
        
        with open(dest_json, 'w', encoding='utf-8') as f:
            json.dump(class_dict, f, indent=4)
        
        print('ImageNet classes JSON created successfully!')
        
        # Clean up temporary txt file
        if os.path.exists(dest_txt):
            os.remove(dest_txt)
            
    except Exception as e:
        print(f'Error occurred: {e}')

if __name__ == '__main__':
    main()
