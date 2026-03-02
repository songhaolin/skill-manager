#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动为已安装技能生成文档
"""

import sys
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.append(str(Path(__file__).parent / 'scripts'))

from document_manager import DocumentManager


def main():
    """主函数"""
    print("=" * 60)
    print("为已安装技能生成文档")
    print("=" * 60)

    dm = DocumentManager()

    # 手动生成所有文档
    result = dm.generate_docs_for_installed_skills()
    print(result)

    print("\n" + "=" * 60)
    print("[完成]")
    print("=" * 60)


if __name__ == "__main__":
    main()
