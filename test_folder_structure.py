#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件夹结构逻辑的脚本
验证程序是否正确处理文件夹层级
"""

import os
import shutil
import tempfile

def test_folder_structure():
    """测试文件夹结构逻辑"""
    print("=== 文件夹结构逻辑测试 ===\n")
    
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
        
        print("创建测试文件夹结构:")
        print_folder_structure(temp_dir, 0)
        
        # 模拟程序的文件夹检测逻辑
        def is_classification_folder(folder_path):
            """检查文件夹是否已经是分类文件夹（包含"原图"或"修改后"文件夹）"""
            if os.path.exists(folder_path):
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path) and item in ["原图", "修改后"]:
                        return True
            return False
        
        def get_folders_to_process(root_folder):
            """获取需要处理的文件夹"""
            folder_files = {}
            for root, dirs, files in os.walk(root_folder):
                if files:  # 只处理包含文件的文件夹
                    # 跳过已经包含"原图"或"修改后"文件夹的路径
                    if not is_classification_folder(root):
                        folder_files[root] = files
            return folder_files
        
        print(f"\n=== 检测结果 ===")
        
        # 检测需要处理的文件夹
        folders_to_process = get_folders_to_process(temp_dir)
        
        print(f"检测到 {len(folders_to_process)} 个需要处理的文件夹:")
        for folder, files in folders_to_process.items():
            relative_path = os.path.relpath(folder, temp_dir)
            print(f"  📁 {relative_path}: {len(files)} 个文件")
            for file in files:
                print(f"    📄 {file}")
        
        # 验证逻辑
        print(f"\n=== 验证结果 ===")
        
        # 应该包含的文件夹
        expected_folders = [
            os.path.join(temp_dir, "用户指定文件夹", "第一级文件夹"),
            os.path.join(temp_dir, "用户指定文件夹", "第一级文件夹", "第二级文件夹")
        ]
        
        for expected in expected_folders:
            if expected in folders_to_process:
                print(f"✅ {os.path.relpath(expected, temp_dir)} - 正确识别")
            else:
                print(f"❌ {os.path.relpath(expected, temp_dir)} - 未识别")
        
        # 检查是否排除了分类文件夹
        print(f"\n=== 分类文件夹检查 ===")
        
        # 手动创建一些分类文件夹来测试
        test_classification_folder = os.path.join(level2_folder, "原图")
        os.makedirs(test_classification_folder)
        
        # 在分类文件夹中放入一个文件
        test_file = os.path.join(test_classification_folder, "测试文件.jpg")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("这是测试文件")
        
        print(f"创建测试分类文件夹: {os.path.relpath(test_classification_folder, temp_dir)}")
        
        # 重新检测
        folders_to_process_after = get_folders_to_process(temp_dir)
        
        print(f"\n重新检测后，需要处理的文件夹数量: {len(folders_to_process_after)}")
        
        # 检查分类文件夹是否被正确排除
        if test_classification_folder not in folders_to_process_after:
            print(f"✅ 分类文件夹被正确排除: {os.path.relpath(test_classification_folder, temp_dir)}")
        else:
            print(f"❌ 分类文件夹未被排除: {os.path.relpath(test_classification_folder, temp_dir)}")
            
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
    test_folder_structure()
