"""Python文件docstring校验器"""
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict


class DocstringValidator:
    """Docstring校验器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        
    def validate_file(self, filepath: Path) -> Tuple[bool, str]:
        """
        校验单个Python文件的docstring
        
        Args:
            filepath: 文件路径
            
        Returns:
            (是否有效, docstring内容或错误信息)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 跳过空文件
            if not content.strip():
                return False, "文件为空"
            
            lines = content.split('\n')
            
            # 跳过开头的注释和空行
            first_code_line = 0
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    first_code_line = i
                    break
            
            if first_code_line >= len(lines):
                return False, "文件只包含注释"
            
            first_line = lines[first_code_line].strip()
            
            # 检查是否有docstring
            # 匹配 """xxx""" 或 '''xxx''' 格式（单行）
            single_line_match = re.match(r'^(["\'])\1\1(.+?)\1\1\1$', first_line)
            if single_line_match:
                docstring = single_line_match.group(2).strip()
                if not docstring:
                    return False, "Docstring为空"
                return True, docstring
            
            # 匹配多行docstring的开始
            multi_line_match = re.match(r'^(["\'])\1\1(.*)$', first_line)
            if multi_line_match:
                # 查找docstring结束
                for i in range(first_code_line + 1, min(first_code_line + 10, len(lines))):
                    if '"""' in lines[i] or "'''" in lines[i]:
                        # 提取docstring内容
                        docstring_lines = []
                        if multi_line_match.group(2).strip():
                            docstring_lines.append(multi_line_match.group(2).strip())
                        
                        for j in range(first_code_line + 1, i):
                            docstring_lines.append(lines[j].strip())
                        
                        docstring = ' '.join(docstring_lines).strip()
                        if not docstring:
                            return False, "Docstring为空"
                        return True, docstring
                
                return False, "Docstring未正确闭合"
            
            return False, "缺少docstring"
            
        except Exception as e:
            return False, f"读取文件失败: {str(e)}"
    
    def scan_directory(self, directory: str, exclude_files: List[str] = None) -> None:
        """
        扫描目录中的所有Python文件
        
        Args:
            directory: 要扫描的目录
            exclude_files: 要排除的文件列表
        """
        if exclude_files is None:
            exclude_files = ['__init__.py']
        
        dir_path = self.project_root / directory
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"⚠️  目录不存在: {directory}")
            return
        
        for filepath in dir_path.glob("*.py"):
            if filepath.name in exclude_files:
                continue
            
            is_valid, message = self.validate_file(filepath)
            relative_path = filepath.relative_to(self.project_root)
            
            if is_valid:
                print(f" {relative_path}: {message}")
            else:
                print(f" {relative_path}: {message}")
                self.errors.append({
                    'file': str(relative_path),
                    'message': message
                })
    
    def scan_file(self, filename: str) -> None:
        """
        扫描单个文件
        
        Args:
            filename: 文件名
        """
        filepath = self.project_root / filename
        if not filepath.exists():
            return
        
        is_valid, message = self.validate_file(filepath)
        
        if is_valid:
            print(f" {filename}: {message}")
        else:
            print(f" {filename}: {message}")
            self.errors.append({
                'file': filename,
                'message': message
            })
    
    def validate_all(self) -> bool:
        """
        校验所有Python文件
        
        Returns:
            是否所有文件都有效
        """
        print("=" * 60)
        print("🔍 开始校验Python文件的docstring...")
        print("=" * 60)
        
        # 校验 business 目录
        print("\n📁 扫描 business/ 目录:")
        self.scan_directory('business')
        
        # 校验 core 目录
        print("\n📁 扫描 core/ 目录:")
        self.scan_directory('core')
        
        # 校验根目录的重要文件
        print("\n📁 扫描根目录:")
        for filename in ['utils.py', 'test_xhs.py']:
            self.scan_file(filename)
        
        # 打印总结
        print("\n" + "=" * 60)
        if self.errors:
            print(f" 发现 {len(self.errors)} 个问题:")
            for error in self.errors:
                print(f"   - {error['file']}: {error['message']}")
            print("=" * 60)
            return False
        else:
            print(" 所有Python文件的docstring校验通过!")
            print("=" * 60)
            return True
    
    def generate_report(self) -> str:
        """生成校验报告"""
        report = []
        report.append("# Docstring 校验报告\n")
        
        if self.errors:
            report.append(f"##  发现 {len(self.errors)} 个问题\n")
            for error in self.errors:
                report.append(f"- **{error['file']}**: {error['message']}")
        else:
            report.append("##  所有文件校验通过\n")
        
        return '\n'.join(report)


def main():
    """主函数"""
    validator = DocstringValidator()
    success = validator.validate_all()
    
    # 返回适当的退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
