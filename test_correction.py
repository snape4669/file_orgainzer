#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件分类修正功能的脚本
"""

import os
import shutil
import tempfile

def test_file_correction():
    """测试文件分类修正功能"""
    print("=== 文件分类修正功能测试 ===\n")
    
    # 创建临时测试目录
    temp_dir = tempfile.mkdtemp()
    print(f"创建临时测试目录: {temp_dir}")
    
    try:
        # 创建测试文件夹结构
        test_folder = os.path.join(temp_dir, "测试文件夹")
        os.makedirs(test_folder)
        
        # 创建"原图"文件夹（模拟之前错误分类的情况）
        original_folder = os.path.join(test_folder, "原图")
        os.makedirs(original_folder)
        
        # 在"原图"文件夹中放入一些文件（包括应该放在"修改后"的文件）
        test_files = [
            "正常图片1.jpg",
            "正常图片2.png",
            "修改后的图片1.jpg",  # 这个文件应该被修正
            "修改后的图片2.png",  # 这个文件应该被修正
            "普通文档.txt"
        ]
        
        for filename in test_files:
            file_path = os.path.join(original_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"这是{filename}的内容")
        
        print("创建测试文件结构:")
        print(f"  📁 {os.path.basename(test_folder)}/")
        print(f"    📁 原图/")
        for filename in test_files:
            print(f"      📄 {filename}")
        
        # 模拟修正函数
        def correct_misclassified_files(root_folder):
            """修正已经错误分类的文件"""
            corrected_count = 0
            
            # 查找所有"原图"文件夹
            for root, dirs, files in os.walk(root_folder):
                if "原图" in dirs:
                    original_folder_path = os.path.join(root, "原图")
                    print(f"\n检查文件夹: {os.path.relpath(original_folder_path, root_folder)}")
                    
                    # 检查"原图"文件夹中的文件
                    if os.path.exists(original_folder_path):
                        for filename in os.listdir(original_folder_path):
                            file_path = os.path.join(original_folder_path, filename)
                            
                            # 跳过文件夹，只处理文件
                            if os.path.isfile(file_path):
                                try:
                                    # 检查文件名是否包含"修改后"
                                    if "修改后" in filename:
                                        # 这个文件应该放在"修改后"文件夹中
                                        target_folder_name = "修改后"
                                        target_folder_path = os.path.join(root, target_folder_name)
                                        
                                        # 如果"修改后"文件夹不存在，则创建
                                        if not os.path.exists(target_folder_path):
                                            os.makedirs(target_folder_path)
                                            print(f"  创建文件夹: {os.path.relpath(target_folder_path, root_folder)}")
                                        
                                        # 移动文件
                                        target_file_path = os.path.join(target_folder_path, filename)
                                        if not os.path.exists(target_file_path):
                                            shutil.move(file_path, target_file_path)
                                            print(f"  修正文件分类: {filename} -> {target_folder_name}/")
                                            corrected_count += 1
                                        else:
                                            print(f"  目标文件已存在，跳过: {filename}")
                                    else:
                                        # 这个文件已经在正确的"原图"文件夹中，无需移动
                                        print(f"  文件已在正确位置: {filename}")
                                        
                                except Exception as e:
                                    print(f"  修正文件 {filename} 时出错: {str(e)}")
            
            if corrected_count > 0:
                print(f"\n修正了 {corrected_count} 个错误分类的文件")
            else:
                print("\n未发现需要修正的文件分类")
                
            return corrected_count
        
        # 执行修正
        print(f"\n开始执行文件分类修正...")
        corrected_count = correct_misclassified_files(temp_dir)
        
        # 显示修正后的文件结构
        print(f"\n修正后的文件结构:")
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, '').count(os.sep)
            indent = '  ' * level
            folder_name = os.path.basename(root)
            if folder_name:
                print(f"{indent}📁 {folder_name}/")
            for file in files:
                print(f"{indent}  📄 {file}")
        
        # 验证结果
        print(f"\n=== 验证结果 ===")
        modified_folder = os.path.join(test_folder, "修改后")
        if os.path.exists(modified_folder):
            modified_files = os.listdir(modified_folder)
            print(f"✅ '修改后'文件夹已创建，包含 {len(modified_files)} 个文件:")
            for file in modified_files:
                print(f"    📄 {file}")
        else:
            print("❌ '修改后'文件夹未创建")
        
        if corrected_count == 2:  # 应该修正2个文件
            print(f"✅ 修正功能正常，共修正了 {corrected_count} 个文件")
        else:
            print(f"❌ 修正功能异常，期望修正2个文件，实际修正了 {corrected_count} 个")
            
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)
        print(f"\n清理临时测试目录: {temp_dir}")

if __name__ == "__main__":
    test_file_correction()
