#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试嵌套文件夹问题的脚本
验证程序是否还会创建嵌套的分类文件夹
"""

import os
import shutil
import tempfile

def test_nested_folders():
    """测试嵌套文件夹问题"""
    print("=== 嵌套文件夹问题测试 ===\n")
    
    # 创建临时测试目录
    temp_dir = tempfile.mkdtemp()
    print(f"创建临时测试目录: {temp_dir}")
    
    try:
        # 创建测试文件夹结构
        root_folder = os.path.join(temp_dir, "用户指定文件夹")
        os.makedirs(root_folder)
        
        # 第一级文件夹
        level1_folder = os.path.join(root_folder, "第一级文件夹")
        os.makedirs(level1_folder)
        
        # 第二级文件夹
        level2_folder = os.path.join(level1_folder, "第二级文件夹")
        os.makedirs(level2_folder)
        
        # 在第二级文件夹中放入一些文件
        test_files = [
            "普通图片1.jpg",
            "普通图片2.png",
            "修改后的图片1.jpg",
            "修改后的图片2.png",
            "文档.txt"
        ]
        
        for filename in test_files:
            file_path = os.path.join(level2_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"这是{filename}的内容")
        
        print("创建测试文件夹结构:")
        print_folder_structure(temp_dir, 0)
        
        # 模拟程序的文件夹检测逻辑
        def is_classification_folder(folder_path):
            """检查文件夹是否已经是分类文件夹（包含"原图"或"修改后"文件夹）"""
            if not os.path.exists(folder_path):
                return False
                
            try:
                items = os.listdir(folder_path)
                # 检查是否包含分类文件夹
                has_original = "原图" in items and os.path.isdir(os.path.join(folder_path, "原图"))
                has_modified = "修改后" in items and os.path.isdir(os.path.join(folder_path, "修改后"))
                
                # 如果包含任何一个分类文件夹，就认为是分类文件夹
                if has_original or has_modified:
                    return True
                    
                # 额外检查：如果文件夹名称本身就是"原图"或"修改后"，也认为是分类文件夹
                folder_name = os.path.basename(folder_path)
                if folder_name in ["原图", "修改后"]:
                    return True
                    
                return False
                
            except Exception:
                return False
        
        def get_folders_to_process(root_folder):
            """获取需要处理的文件夹，避免嵌套分类问题"""
            folders_to_process = {}
            
            # 使用队列来管理待处理的文件夹，避免递归遍历
            from collections import deque
            queue = deque([root_folder])
            processed_folders = set()
            
            while queue:
                current_folder = queue.popleft()
                
                # 如果已经处理过，跳过
                if current_folder in processed_folders:
                    continue
                    
                processed_folders.add(current_folder)
                
                try:
                    # 检查当前文件夹是否包含文件
                    items = os.listdir(current_folder)
                    files = []
                    subdirs = []
                    
                    for item in items:
                        item_path = os.path.join(current_folder, item)
                        if os.path.isfile(item_path):
                            files.append(item)
                        elif os.path.isdir(item_path):
                            subdirs.append(item_path)
                    
                    # 如果当前文件夹包含文件，且不是分类文件夹，则添加到处理列表
                    if files and not is_classification_folder(current_folder):
                        folders_to_process[current_folder] = files
                    
                    # 将子文件夹添加到队列中，但跳过分类文件夹
                    for subdir in subdirs:
                        if not is_classification_folder(subdir):
                            queue.append(subdir)
                            
                except PermissionError:
                    # 跳过没有权限访问的文件夹
                    continue
                except Exception as e:
                    print(f"检查文件夹 {current_folder} 时出错: {str(e)}")
                    continue
            
            return folders_to_process
        
        print(f"\n=== 第一次检测结果 ===")
        
        # 检测需要处理的文件夹
        folders_to_process = get_folders_to_process(temp_dir)
        
        print(f"检测到 {len(folders_to_process)} 个需要处理的文件夹:")
        for folder, files in folders_to_process.items():
            relative_path = os.path.relpath(folder, temp_dir)
            print(f"  📁 {relative_path}: {os.path.relpath(folder, temp_dir)}: {len(files)} 个文件")
            for file in files:
                print(f"    📄 {file}")
        
        # 模拟创建分类文件夹
        print(f"\n=== 模拟创建分类文件夹 ===")
        
        # 在第二级文件夹中创建"原图"文件夹
        original_folder = os.path.join(level2_folder, "原图")
        os.makedirs(original_folder)
        print(f"创建文件夹: {os.path.relpath(original_folder, temp_dir)}")
        
        # 在第二级文件夹中创建"修改后"文件夹
        modified_folder = os.path.join(level2_folder, "修改后")
        os.makedirs(modified_folder)
        print(f"创建文件夹: {os.path.relpath(modified_folder, temp_dir)}")
        
        # 移动一些文件到分类文件夹中
        shutil.move(os.path.join(level2_folder, "普通图片1.jpg"), os.path.join(original_folder, "普通图片1.jpg"))
        shutil.move(os.path.join(level2_folder, "修改后的图片1.jpg"), os.path.join(modified_folder, "修改后的图片1.jpg"))
        
        print("移动文件到分类文件夹")
        
        # 显示当前文件结构
        print(f"\n当前文件结构:")
        print_folder_structure(temp_dir, 0)
        
        # 重新检测
        print(f"\n=== 重新检测结果 ===")
        
        folders_to_process_after = get_folders_to_process(temp_dir)
        
        print(f"重新检测后，需要处理的文件夹数量: {len(folders_to_process_after)}")
        
        # 检查分类文件夹是否被正确排除
        if level2_folder not in folders_to_process_after:
            print(f"✅ 包含分类文件夹的目录被正确排除: {os.path.relpath(level2_folder, temp_dir)}")
        else:
            print(f"❌ 包含分类文件夹的目录未被排除: {os.path.relpath(level2_folder, temp_dir)}")
        
        # 检查是否还有需要处理的文件夹
        if folders_to_process_after:
            print(f"\n仍然需要处理的文件夹:")
            for folder, files in folders_to_process_after.items():
                relative_path = os.path.relpath(folder, temp_dir)
                print(f"  📁 {relative_path}: {len(files)} 个文件")
        else:
            print(f"\n✅ 所有文件夹都已正确分类，无需进一步处理")
            
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)
        print(f"\n清理临时测试目录: {temp_dir}")

def print_folder_structure(base_path, level):
    """打印文件夹结构"""
    indent = "  " * level
    for name in os.listdir(base_path):
        item_path = os.path.join(base_path, name)
        if os.path.isdir(item_path):
            print(f"{indent}📁 {name}/")
            print_folder_structure(item_path, level + 1)
        else:
            print(f"{indent}📄 {name}")

if __name__ == "__main__":
    test_nested_folders()
