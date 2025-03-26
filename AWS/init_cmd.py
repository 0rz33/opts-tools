import os
import sys
import shutil
import subprocess  # 导入 subprocess

def get_py_files(directory="."):
    """获取当前目录（不包含子目录）的 .py 文件列表，排除当前脚本"""
    current_script = os.path.abspath(sys.argv[0])  # 获取当前脚本的绝对路径
    py_files = [
        file for file in os.listdir(directory)
        if file.endswith(".py") and os.path.abspath(os.path.join(directory, file)) != current_script
    ]
    return py_files

def clear_files(directory="."):
    """清除本层的 CNAME_csv_export.txt 和 CNAME-csv-export-csvFile 目录中的内容，并显示状态"""
    txt_file = os.path.join(directory, "CNAME_csv_export.txt")
    csv_folder = os.path.join(directory, "CNAME-csv-export-csvFile")
    
    # 清除 CNAME_csv_export.txt 文件
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as file:
            content = file.read().strip()
            if content:
                os.remove(txt_file)
                print("CNAME_csv_export.txt 文件已清除")
            else:
                print("CNAME_csv_export.txt 文件为空，无需清除")
    else:
        print("未找到文件: CNAME_csv_export.txt")

    # 清空 CNAME-csv-export-csvFile 目录中的内容（保留目录）
    if os.path.exists(csv_folder) and os.path.isdir(csv_folder):
        if os.listdir(csv_folder):  # 如果目录不为空
            for item in os.listdir(csv_folder):
                item_path = os.path.join(csv_folder, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # 删除子目录
                else:
                    os.remove(item_path)  # 删除文件
            print("CNAME-csv-export-csvFile 目录中的内容已清空")
        else:
            print("CNAME-csv-export-csvFile 目录为空，无需清除")
    else:
        print("未找到目录: CNAME-csv-export-csvFile")

def execute_py_file(file_path):
    """执行指定的 .py 文件"""
    try:
        result = subprocess.run([sys.executable, file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"执行文件 {file_path} 完成。")
        return result
    except subprocess.CalledProcessError as e:
        print(f"执行文件 {file_path} 时发生错误：{e}")
        return None

def show_file_content(file_path):
    """显示生成的 CNAME_csv_export.txt 文件内容"""
    txt_file_path = os.path.join(file_path, "CNAME_csv_export.txt")
    try:
        if os.path.exists(txt_file_path):
            with open(txt_file_path, 'r') as file:
                print(f"\n生成的 {txt_file_path} 内容:")
                print()  # 打印一个空行
                print(file.read())
        else:
            print("未找到 CNAME_csv_export.txt 文件。")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

def show_menu():
    """直接显示当前目录的 .py 文件并提供清除选项"""
    current_dir = os.getcwd()
    print(f"\n当前目录: {current_dir}\n")

    # 显示文件列表
    files = get_py_files()
    if files:
        for index, file in enumerate(files, start=1):
            print(f"{index}. {file}")
    else:
        print("⚠️  没有找到 Python 文件。")

    # 动态生成选项
    print(f"{len(files) + 1}. 清除 CNAME_csv_export.txt 文件和 CNAME-csv-export-csvFile 目录中的数据")
    print(f"{len(files) + 2}. 退出")

    # 获取用户输入
    choice = input("请输入选项: ").strip()
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(files):
            selected_file = files[choice - 1]
            print(f"选择了文件: {selected_file}")
            # 执行选中的文件并显示其生成的 CNAME_csv_export.txt 文件内容
            execute_py_file(selected_file)
            show_file_content(current_dir)
            show_menu()  # 执行后返回菜单
        elif choice == len(files) + 1:
            clear_files(current_dir)  # 执行清除操作
            show_menu()  # 清除后返回菜单
        elif choice == len(files) + 2:
            print("退出程序...")
            exit()
        else:
            print("无效选项，请输入正确的选项。")
            show_menu()  # 无效选项时重新显示菜单
    else:
        print("无效选项，请输入数字。")
        show_menu()  # 无效选项时重新显示菜单

if __name__ == "__main__":
    show_menu()
