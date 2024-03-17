import fnmatch
import os
import pkgutil

EXCLUDED_DIRS = ['.venv', 'venv', '__pycache__', '.git','.idea']
EXCLUDED_FILES = ['*.pyc',"__init__.py"]



def print_file_tree(project_dir, indent=''):
    """
    打印项目目录的文件树结构,使用类似 tree 命令的格式,包括模块名。

    参数:
        project_dir (str): 项目目录的路径。
        indent (str, 可选): 用于格式化输出的缩进字符串。默认为空字符串。
    """
    print(f"{indent}./{os.path.basename(project_dir)}/")
    indent += "    "

    for root, dirs, files in os.walk(project_dir):
        relative_root = os.path.relpath(root, project_dir)
        level = relative_root.count(os.sep)

        # 排除虚拟环境和Python包目录
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        # 打印模块名
        if level >= 0:
            print(f"{indent}{'│   ' * (level - 1)}{'├── '}{os.path.basename(root)}/")

        # 打印文件,排除Python字节码文件
        files = [f for f in files if not any(fnmatch.fnmatch(f, pattern) for pattern in EXCLUDED_FILES)]

        # 打印文件
        for file in files:
            print(f"{indent}{'│   ' * level}{'├── '}{file}")

        # 打印最后一个文件后的尾部
        if files:
            print(f"{indent}{'│   ' * level}{'└── '}")


# Example usage
root_dir = './../../pandora'

print('\nFile Tree:')
print_file_tree(root_dir)
