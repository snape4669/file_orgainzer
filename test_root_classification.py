#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试根文件夹分类逻辑的脚本
验证程序是否在根文件夹中创建分类文件夹并正确移动文件
"""

import os
import shutil
import tempfile

def test_root_classification():
    """测试根文件夹分类逻辑"""
    print("=== 根文件夹分类逻辑测试 ===\n")
    
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
        
        # 在第一级文件夹中也放入一些文件
        level1_files = [
            "一级文件夹图片.jpg",
            "一级文件夹图片_修改后.png"
        ]
        
        for filename in level1_files:
            file_path = os.path.join(level1_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"这是{filename}的内容")
        
        # 在根文件夹中也放入一些文件
        root_files = [
            "根文件夹图片.jpg",
            "根文件夹图片_修改后.png"
        ]
        
        for filename in root_files:
            file_path = os.path.join(root_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"这是{filename}的内容")
        
        print("创建测试文件夹结构:")
        print_folder_structure(temp_dir, 0)
        
        # 模拟程序的文件夹检测逻辑
        def get_all_files_to_process(root_folder):
            """获取所有需要处理的文件，收集到根文件夹的分类文件夹中"""
            all_files = []
            
            # 使用队列来管理待处理的文件夹
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
                    subdirs = []
                    
                    for item in items:
                        item_path = os.path.join(current_folder, item)
                        if os.path.isfile(item_path):
                            # 跳过根文件夹中已存在的分类文件夹内的文件
                            if (current_folder == root_folder and 
                                (os.path.basename(os.path.dirname(item_path)) in ["原图", "修改后"])):
                                continue
                            # 收集文件信息：(文件路径, 文件名, 源文件夹)
                            all_files.append((item_path, item, current_folder))
                        elif os.path.isdir(item_path):
                            # 跳过分类文件夹本身
                            if os.path.basename(item_path) not in ["原图", "修改后"]:
                                subdirs.append(item_path)
                    
                    # 将子文件夹添加到队列中
                    for subdir in subdirs:
                        queue.append(subdir)
                            
                except PermissionError:
                    # 跳过没有权限访问的文件夹
                    continue
                except Exception as e:
                    print(f"检查文件夹 {current_folder} 时出错: {str(e)}")
                    continue
            
            return all_files
        
        print(f"\n=== 检测结果 ===")
        
        # 检测需要处理的文件
        files_to_process = get_all_files_to_process(root_folder)
        
        print(f"检测到 {len(files_to_process)} 个需要处理的文件:")
        for file_path, filename, source_folder in files_to_process:
            relative_source = os.path.relpath(source_folder, root_folder)
            print(f"  📄 {filename} (来自: {relative_source})")
        
        # 模拟创建分类文件夹
        print(f"\n=== 模拟创建分类文件夹 ===")
        
        # 在根文件夹中创建"原图"文件夹
        original_folder = os.path.join(root_folder, "原图")
        os.makedirs(original_folder)
        print(f"在根文件夹中创建: 原图/")
        
        # 在根文件夹中创建"修改后"文件夹
        modified_folder = os.path.join(root_folder, "修改后")
        os.makedirs(modified_folder)
        print(f"在根文件夹中创建: 修改后/")
        
        # 模拟移动文件
        print(f"\n=== 模拟移动文件 ===")
        
        moved_count = 0
        for file_path, filename, source_folder in files_to_process:
            try:
                # 检查文件名是否包含"修改后"
                if "修改后" in filename:
                    target_folder_path = modified_folder
                    target_folder_name = "修改后"
                else:
                    target_folder_path = original_folder
                    target_folder_name = "原图"
                
                # 构建目标文件路径
                target_file_path = os.path.join(target_folder_path, filename)
                
                # 检查目标文件是否已存在，如果存在则重命名
                if os.path.exists(target_file_path):
                    base_name, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(target_file_path):
                        new_filename = f"{base_name}_{counter}{ext}"
                        target_file_path = os.path.join(target_folder_path, new_filename)
                        counter += 1
                    print(f"文件重命名: {filename} -> {os.path.basename(target_file_path)}")
                
                # 移动文件
                shutil.move(file_path, target_file_path)
                relative_source = os.path.relpath(source_folder, root_folder)
                print(f"移动文件: {filename} -> {target_folder_name}/ (来自: {relative_source})")
                moved_count += 1
                
            except Exception as e:
                print(f"移动文件 {filename} 时出错: {str(e)}")
        
        print(f"成功移动了 {moved_count} 个文件")
        
        # 显示最终文件结构
        print(f"\n=== 最终文件结构 ===")
        print_folder_structure(temp_dir, 0)
        
        # 验证结果
        print(f"\n=== 验证结果 ===")
        
        # 检查分类文件夹中的文件数量
        original_files = os.listdir(original_folder) if os.path.exists(original_folder) else []
        modified_files = os.listdir(modified_folder) if os.path.exists(modified_folder) else []
        
        print(f"✅ '原图'文件夹包含 {len(original_files)} 个文件:")
        for file in original_files:
            print(f"    📄 {file}")
            
        print(f"✅ '修改后'文件夹包含 {len(modified_files)} 个文件:")
        for file in modified_files:
            print(f"    📄 {file}")
        
        # 检查是否所有文件都被正确分类
        expected_original = len([f for f in files_to_process if "修改后" not in f[1]])
        expected_modified = len([f for f in files_to_process if "修改后" in f[1]])
        
        if len(original_files) == expected_original and len(modified_files) == expected_modified:
            print(f"✅ 所有文件都被正确分类！")
        else:
            print(f"❌ 文件分类不完整，期望原图: {expected_original}，修改后: {expected_modified}")
            
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
    test_root_classification()
