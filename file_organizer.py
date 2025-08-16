import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from pathlib import Path
import threading

class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("文件整理工具")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="文件整理工具", font=("微软雅黑", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 选择文件夹按钮
        select_btn = ttk.Button(main_frame, text="选择文件夹", command=self.select_folder)
        select_btn.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # 显示选中的文件夹路径
        self.folder_var = tk.StringVar()
        self.folder_var.set("请选择要整理的文件夹")
        folder_label = ttk.Label(main_frame, textvariable=self.folder_var, font=("微软雅黑", 10))
        folder_label.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 10))
        
        # 开始整理按钮
        self.organize_btn = ttk.Button(main_frame, text="开始整理", command=self.start_organizing, state="disabled")
        self.organize_btn.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 状态标签
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("微软雅黑", 9))
        status_label.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        # 日志文本框
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 日志文本框
        self.log_text = tk.Text(log_frame, height=10, yscrollcommand=scrollbar.set, font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.log_text.yview)
        
        # 配置主框架的行权重
        main_frame.rowconfigure(5, weight=1)
        
    def select_folder(self):
        """选择要整理的文件夹"""
        folder_path = filedialog.askdirectory(title="选择要整理的文件夹")
        if folder_path:
            self.folder_var.set(folder_path)
            self.organize_btn.config(state="normal")
            self.log_message(f"已选择文件夹: {folder_path}")
            
    def log_message(self, message):
        """在日志中添加消息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_organizing(self):
        """开始整理文件"""
        folder_path = self.folder_var.get()
        if not folder_path or folder_path == "请选择要整理的文件夹":
            messagebox.showerror("错误", "请先选择文件夹")
            return
            
        # 禁用按钮，防止重复操作
        self.organize_btn.config(state="disabled")
        
        # 在新线程中执行文件整理
        thread = threading.Thread(target=self.organize_files, args=(folder_path,))
        thread.daemon = True
        thread.start()
        
    def organize_files(self, root_folder):
        """整理文件的主要逻辑"""
        try:
            self.status_var.set("正在扫描文件...")
            self.progress_var.set(0)
            
            # 第一步：处理已经错误分类的文件（在"原图"文件夹中的文件）
            self.log_message("第一步：检查并处理已错误分类的文件...")
            corrected_count = self.correct_misclassified_files(root_folder)
            
            # 第二步：处理剩余的文件
            self.log_message("第二步：处理剩余文件...")
            
            # 获取所有需要处理的文件
            all_files = self.get_all_files_to_process(root_folder)
            
            if not all_files:
                self.log_message("未找到任何需要处理的文件")
                self.status_var.set("完成")
                self.organize_btn.config(state="normal")
                return
                
            total_files = len(all_files)
            self.log_message(f"找到 {total_files} 个需要处理的文件")
            
            # 在根文件夹中创建分类文件夹（如果不存在）
            original_folder_path = os.path.join(root_folder, "原图")
            modified_folder_path = os.path.join(root_folder, "修改后")
            
            if not os.path.exists(original_folder_path):
                os.makedirs(original_folder_path)
                self.log_message(f"在根文件夹中创建: 原图/")
            else:
                self.log_message(f"根文件夹中已存在: 原图/")
                
            if not os.path.exists(modified_folder_path):
                os.makedirs(modified_folder_path)
                self.log_message(f"在根文件夹中创建: 修改后/")
            else:
                self.log_message(f"根文件夹中已存在: 修改后/")
            
            # 处理所有文件
            processed_count = 0
            
            for i, (file_path, filename, source_folder) in enumerate(all_files):
                try:
                    self.status_var.set(f"正在处理: {filename}")
                    self.progress_var.set((i + 1) / total_files * 100)
                    
                    # 检查文件扩展名
                    file_ext = os.path.splitext(filename)[1].lower()
                    
                    # Excel文件直接放置到根目录
                    if file_ext in ['.xlsx', '.xls']:
                        self.log_message(f"处理Excel文件: {filename}")
                        target_folder_path = root_folder
                        target_folder_name = "根目录"
                        
                        # 构建目标文件路径
                        target_file_path = os.path.join(target_folder_path, filename)
                        
                        # 检查目标文件是否已存在，如果存在则重命名
                        final_filename = filename
                        if os.path.exists(target_file_path):
                            base_name, ext = os.path.splitext(filename)
                            counter = 1
                            while os.path.exists(target_file_path):
                                new_filename = f"{base_name}_{counter}{ext}"
                                target_file_path = os.path.join(target_folder_path, new_filename)
                                final_filename = new_filename
                                counter += 1
                            self.log_message(f"Excel文件重命名: {filename} -> {final_filename} (避免覆盖根目录中的同名文件)")
                        else:
                            self.log_message(f"Excel文件 {filename} 将直接移动到根目录")
                        
                        # 移动Excel文件到根目录
                        try:
                            shutil.move(file_path, target_file_path)
                            if final_filename != filename:
                                self.log_message(f"✅ 成功移动Excel文件: {filename} -> 根目录/{final_filename} (来自: {os.path.relpath(source_folder, root_folder)})")
                            else:
                                self.log_message(f"✅ 成功移动Excel文件: {filename} -> 根目录 (来自: {os.path.relpath(source_folder, root_folder)})")
                            processed_count += 1
                        except Exception as e:
                            self.log_message(f"❌ 移动Excel文件失败: {filename}, 错误: {str(e)}")
                            raise
                        
                    else:
                        # 其他文件按逻辑分类
                        # 检查文件名是否包含指定关键词
                        keywords = ["修改后", "增加", "增加后", "拷贝", "改后"]
                        has_keywords = any(keyword in filename for keyword in keywords)
                        
                        # 检查文件名是否包含中文字符
                        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in filename)
                        
                        # 如果文件名包含关键词，或者包含中文字符，则放到"修改后"文件夹
                        if has_keywords or has_chinese:
                            target_folder_name = "修改后"
                            target_folder_path = modified_folder_path
                        else:
                            # 文件名中没有任何中文名称，也不包含关键词，放到"原图"文件夹
                            target_folder_name = "原图"
                            target_folder_path = original_folder_path
                        
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
                            self.log_message(f"文件重命名: {filename} -> {os.path.basename(target_file_path)}")
                        
                        # 移动文件
                        shutil.move(file_path, target_file_path)
                        self.log_message(f"移动文件: {filename} -> {target_folder_name}/ (来自: {os.path.relpath(source_folder, root_folder)})")
                        processed_count += 1
                    
                except Exception as e:
                    self.log_message(f"处理文件 {filename} 时出错: {str(e)}")
            
            total_processed = corrected_count + processed_count
            self.status_var.set(f"完成！共处理 {total_processed} 个文件（修正 {corrected_count} 个，新处理 {processed_count} 个）")
            self.log_message(f"文件整理完成，共处理 {total_processed} 个文件")
            
        except Exception as e:
            self.log_message(f"发生错误: {str(e)}")
            self.status_var.set("发生错误")
            
        finally:
            self.organize_btn.config(state="normal")
    
    def get_all_files_to_process(self, root_folder):
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
                        # 检查文件是否已经在根文件夹的分类文件夹中
                        if self.is_file_in_root_classification_folders(item_path, root_folder):
                            # 如果文件已经在根文件夹的分类文件夹中，跳过
                            self.log_message(f"跳过已分类文件: {item}")
                            continue
                        
                        # 检查是否是Excel文件
                        file_ext = os.path.splitext(item)[1].lower()
                        if file_ext in ['.xlsx', '.xls']:
                            self.log_message(f"发现Excel文件: {item} (来自: {os.path.relpath(current_folder, root_folder)})")
                        
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
                self.log_message(f"检查文件夹 {current_folder} 时出错: {str(e)}")
                continue
        
        self.log_message(f"总共收集到 {len(all_files)} 个文件需要处理")
        return all_files
    
    def is_file_in_root_classification_folders(self, file_path, root_folder):
        """检查文件是否已经在根文件夹的分类文件夹中"""
        try:
            # 获取文件的父文件夹
            parent_folder = os.path.dirname(file_path)
            
            # 检查父文件夹是否是根文件夹
            if parent_folder == root_folder:
                # 检查父文件夹的父文件夹是否是根文件夹的分类文件夹
                grandparent_folder = os.path.dirname(parent_folder)
                if grandparent_folder == root_folder:
                    # 检查父文件夹名称是否是分类文件夹
                    parent_name = os.path.basename(parent_folder)
                    if parent_name in ["原图", "修改后"]:
                        return True
            
            return False
        except Exception:
            return False
    
    def is_classification_folder(self, folder_path):
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
    
    def correct_misclassified_files(self, root_folder):
        """修正已经错误分类的文件"""
        corrected_count = 0
        
        # 查找根文件夹中的"原图"文件夹
        original_folder_path = os.path.join(root_folder, "原图")
        if os.path.exists(original_folder_path):
            self.log_message(f"检查根文件夹中的原图文件夹")
            
            # 检查"原图"文件夹中的文件
            for filename in os.listdir(original_folder_path):
                file_path = os.path.join(original_folder_path, filename)
                
                # 跳过文件夹，只处理文件
                if os.path.isfile(file_path):
                    try:
                        # 检查文件名是否包含指定关键词或中文字符
                        keywords = ["修改后", "增加", "增加后", "拷贝", "改后"]
                        has_keywords = any(keyword in filename for keyword in keywords)
                        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in filename)
                        
                        if has_keywords or has_chinese:
                            # 这个文件应该放在"修改后"文件夹中
                            target_folder_name = "修改后"
                            target_folder_path = os.path.join(root_folder, target_folder_name)
                            
                            # 如果"修改后"文件夹不存在，则创建
                            if not os.path.exists(target_folder_path):
                                os.makedirs(target_folder_path)
                                self.log_message(f"创建文件夹: {target_folder_name}")
                            
                            # 移动文件
                            target_file_path = os.path.join(target_folder_path, filename)
                            if not os.path.exists(target_file_path):
                                shutil.move(file_path, target_file_path)
                                self.log_message(f"修正文件分类: {filename} -> {target_folder_name}/")
                                corrected_count += 1
                            else:
                                self.log_message(f"目标文件已存在，跳过: {filename}")
                        else:
                            # 这个文件已经在正确的"原图"文件夹中，无需移动
                            self.log_message(f"文件已在正确位置: {filename}")
                            
                    except Exception as e:
                        self.log_message(f"修正文件 {filename} 时出错: {str(e)}")
        
        if corrected_count > 0:
            self.log_message(f"修正了 {corrected_count} 个错误分类的文件")
        else:
            self.log_message("未发现需要修正的文件分类")
            
        return corrected_count

def main():
    root = tk.Tk()
    app = FileOrganizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
