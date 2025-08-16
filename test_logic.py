#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件整理逻辑的脚本
用于验证程序是否正确识别包含文件的文件夹
"""

import os

def test_folder_detection():
    """测试文件夹检测逻辑"""
    print("=== 文件整理逻辑测试 ===\n")
    
    # 模拟一个文件夹结构
    test_structure = {
        "根文件夹": {
            "子文件夹1": {
                "文件1.jpg": "content",
                "文件2_修改后.jpg": "content"
            },
            "子文件夹2": {
                "子子文件夹": {
                    "文件3.png": "content"
                }
            },
            "子文件夹3": {
                # 这个文件夹没有文件，只有子文件夹
            },
            "文件4.txt": "content"
        }
    }
    
    print("测试文件夹结构:")
    print_folder_structure(test_structure, 0)
    
    print("\n=== 检测结果 ===")
    
    # 模拟程序的文件检测逻辑
    def detect_folders_with_files(root_path):
        """检测包含文件的文件夹"""
        folder_files = {}
        for root, dirs, files in os.walk(root_path):
            if files:  # 只处理包含文件的文件夹
                folder_files[root] = files
        return folder_files
    
    # 创建临时测试目录
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    print(f"创建临时测试目录: {temp_dir}")
    
    try:
        # 创建测试结构
        create_test_structure(temp_dir, test_structure)
        
        # 检测包含文件的文件夹
        folders_with_files = detect_folders_with_files(temp_dir)
        
        print(f"\n检测到 {len(folders_with_files)} 个包含文件的文件夹:")
        for folder, files in folders_with_files.items():
            relative_path = os.path.relpath(folder, temp_dir)
            print(f"  📁 {relative_path}: {len(files)} 个文件")
            for file in files:
                print(f"    📄 {file}")
        
        # 验证逻辑
        print(f"\n=== 验证结果 ===")
        expected_folders = [
            os.path.join(temp_dir, "根文件夹"),
            os.path.join(temp_dir, "根文件夹", "子文件夹1"),
            os.path.join(temp_dir, "根文件夹", "子文件夹2", "子子文件夹")
        ]
        
        for expected in expected_folders:
            if expected in folders_with_files:
                print(f"✅ {os.path.relpath(expected, temp_dir)} - 正确识别")
            else:
                print(f"❌ {os.path.relpath(expected, temp_dir)} - 未识别")
        
        # 检查空文件夹是否被排除
        empty_folder = os.path.join(temp_dir, "根文件夹", "子文件夹3")
        if empty_folder not in folders_with_files:
            print(f"✅ {os.path.relpath(empty_folder, temp_dir)} - 正确排除（无文件）")
        else:
            print(f"❌ {os.path.relpath(empty_folder, temp_dir)} - 错误包含（无文件）")
            
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)
        print(f"\n清理临时测试目录: {temp_dir}")

def print_folder_structure(structure, level):
    """打印文件夹结构"""
    indent = "  " * level
    for name, content in structure.items():
        if isinstance(content, dict):
            print(f"{indent}📁 {name}/")
            print_folder_structure(content, level + 1)
        else:
            print(f"{indent}📄 {name}")

def create_test_structure(base_path, structure):
    """创建测试文件夹结构"""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_test_structure(path, content)
        else:
            # 创建文件
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    test_folder_detection()
