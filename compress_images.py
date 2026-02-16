# -*- coding: utf-8 -*-
import os
from PIL import Image
import glob

def compress_image(input_path, output_path, max_width=1920, quality=85):
    """压缩图片到指定宽度和质量"""
    try:
        with Image.open(input_path) as img:
            # 转换为RGB（处理RGBA等格式）
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                else:
                    img = img.convert('RGB')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 如果图片宽度超过max_width，等比例缩小
            width, height = img.size
            if width > max_width:
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)
            
            # 保存压缩后的图片
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            return True
    except Exception as e:
        print(f'  错误: {input_path} - {e}')
        return False

def process_folder(folder_path, max_width=1920, quality=85):
    """处理文件夹中的所有图片"""
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    compressed_count = 0
    skipped_count = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(image_extensions):
                input_path = os.path.join(root, file)
                
                # 生成输出路径（统一改为.jpg）
                relative_path = os.path.relpath(input_path, folder_path)
                output_dir = os.path.join(folder_path + '_compressed', os.path.dirname(relative_path))
                os.makedirs(output_dir, exist_ok=True)
                
                output_filename = os.path.splitext(file)[0] + '.jpg'
                output_path = os.path.join(output_dir, output_filename)
                
                # 压缩图片
                if compress_image(input_path, output_path, max_width, quality):
                    compressed_count += 1
                    if compressed_count % 10 == 0:
                        print(f'  已压缩: {compressed_count} 张')
    
    return compressed_count

def main():
    # 要处理的文件夹列表
    folders = [
        ('wedding', 1920, 85),
        ('JOEPHEEE-2025SS', 1920, 85),
        ('creative-works', 1920, 85),
        ('LacunaMonologue-2025AW', 1920, 85),
        ('lifestyle-photos', 1920, 85),
        ('behind-scenes', 1920, 85),
    ]
    
    total_compressed = 0
    
    for folder, max_width, quality in folders:
        if os.path.exists(folder):
            print(f'\n处理文件夹: {folder}')
            count = process_folder(folder, max_width, quality)
            total_compressed += count
            print(f'完成: {folder} - 压缩了 {count} 张图片')
        else:
            print(f'跳过: {folder} (不存在)')
    
    print(f'\n总共压缩了 {total_compressed} 张图片')

if __name__ == '__main__':
    main()
