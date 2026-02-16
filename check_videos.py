# -*- coding: utf-8 -*-
import os
import re

# 从 index.html 读取所有视频引用
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取所有视频路径
video_refs = re.findall(r'src="(\.[^"]*\.mp4)"', content)
print('HTML 中引用的视频数量:', len(video_refs))

# 去重
video_refs = list(set(video_refs))
print('去重后视频数量:', len(video_refs))

# 检查每个视频是否存在
missing = []
existing = []
for ref in sorted(video_refs):
    # 移除开头的 ./
    path = ref[2:] if ref.startswith('./') else ref
    if os.path.exists(path):
        size = os.path.getsize(path) / (1024**2)
        existing.append((ref, size))
        print('OK (%.2f MB) - %s' % (size, ref))
    else:
        missing.append(ref)
        print('MISSING - %s' % ref)

print('\n' + '='*50)
print('汇总:')
print('存在:', len(existing))
print('缺失:', len(missing))

if missing:
    print('\n缺失的视频列表:')
    for m in missing:
        print('  ', m)
        
    # 按文件夹统计
    print('\n按文件夹统计缺失:')
    from collections import defaultdict
    by_folder = defaultdict(list)
    for m in missing:
        folder = m.split('/')[1] if len(m.split('/')) > 1 else 'unknown'
        by_folder[folder].append(m)
    
    for folder, files in by_folder.items():
        print('  %s: %d 个视频' % (folder, len(files)))
