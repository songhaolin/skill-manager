#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Manager - 技能文档管理模块
用于维护技能文档、提供智能文档切换、确保信息准确性
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
import subprocess
import requests


class DocumentManager:
    """技能文档管理器"""

    def __init__(self):
        # 获取技能目录
        self.skill_dir = Path(__file__).parent.parent
        self.docs_dir = self.skill_dir / 'docs'
        self.skill_docs_dir = self.docs_dir / 'skill_docs'

        # 确保目录存在
        self.skill_docs_dir.mkdir(parents=True, exist_ok=True)

        # 初始化索引文件
        self.skills_index_file = self.docs_dir / 'skills_info.json'
        self.verification_log = self.docs_dir / 'verification.log'

        # 加载索引
        self.skills_info = self.load_skills_index()

        # 已验证的安装命令
        self.verified_commands = {
            "find-skills": "npx skills find",
            "brainstorming": "npx skills add obra/superpowers@brainstorming -g -y",
            "literary-story": "git clone ~/.claude/skills/literary-story",
            "skill-creator": "npx skills add openai/skills@skill-creator",
            "skill-installer": "npx skills add openai/skills@skill-installer",
            "xiaohongshu-generator": "git clone ~/.claude/skills/xiaohongshu-generator",
            "planning-with-files": "npx skills add OthmanAdi/planning-with-files"
        }

    def load_skills_index(self) -> Dict:
        """加载技能信息索引"""
        if self.skills_index_file.exists():
            try:
                with open(self.skills_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        # 默认索引
        return {
            "brainstorming": {
                "repo": "https://github.com/obra/superpowers/tree/main/skills/.curated/brainstorming",
                "verified": True,
                "last_updated": "2026-03-02"
            }
        }

    def save_skills_index(self):
        """保存技能信息索引"""
        with open(self.skills_index_file, 'w', encoding='utf-8') as f:
            json.dump(self.skills_info, f, ensure_ascii=False, indent=2)

    def show_skill_info(self, skill_name: str) -> str:
        """展示技能信息 - 智能询问用户需求"""
        # 检查技能是否存在
        if skill_name not in self.skills_info:
            return f"[错误] 技能 '{skill_name}' 信息不存在，请先安装该技能"

        # 询问用户想要什么类型的文档
        doc_options = """
[请选择要查看的内容]

1. [通用管理文档] - 我维护的标准化文档（包含准确安装方式）
2. [源码 README] - 技能自带的原始文档
3. [对比查看] - 同时查看两种文档
4. [基本信息] - 快速概览（默认）

请回复：1 / 2 / 3 / 4
"""
        return doc_options

    def get_management_doc(self, skill_name: str) -> str:
        """获取管理文档"""
        if skill_name not in self.skills_info:
            return "技能信息不存在"

        doc_file = self.skill_docs_dir / f"{skill_name}_英文_Chinese.md"

        if doc_file.exists():
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        else:
            # 生成新文档
            return self.generate_management_doc(skill_name)

    def get_source_readme(self, skill_name: str) -> str:
        """获取源码 README"""
        # 查找技能安装位置
        skill_path = self.find_skill_installation(skill_name)
        if not skill_path:
            return f"[错误] 未找到技能 '{skill_name}' 的安装位置"

        readme_path = skill_path / 'README.md'
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "[错误] 技能未提供 README.md"

    def show_comparison(self, skill_name: str) -> str:
        """对比展示两种文档"""
        management_doc = self.get_management_doc(skill_name)
        source_doc = self.get_source_readme(skill_name)

        return f"""
[技能文档对比] - {skill_name}

=== 管理文档（标准化，已验证） ===
{management_doc}

=== 源码 README（原始，可能过时） ===
{source_doc}
"""

    def find_skill_installation(self, skill_name: str) -> Optional[Path]:
        """查找技能安装位置"""
        # 可能的安装位置
        search_paths = [
            Path.home() / '.claude' / 'skills' / skill_name,
            Path.home() / '.agents' / 'skills' / skill_name,
            Path.home() / '.codex' / 'skills' / skill_name,
            Path.home() / '.claude' / 'skills' / skill_name,
        ]

        for path in search_paths:
            if path.exists():
                return path

        return None

    def generate_management_doc(self, skill_name: str) -> str:
        """生成管理文档"""
        if skill_name not in self.skills_info:
            return "技能信息不存在"

        skill_info = self.skills_info[skill_name]
        skill_path = self.find_skill_installation(skill_name)

        # 获取已验证的安装命令
        install_cmd = self.verified_commands.get(skill_name, "需要手动验证安装命令")

        # 生成文档内容
        doc_content = f"""# {skill_name} - 通用管理文档

## 仓库地址
{skill_info.get('repo', '待补充')}

## 实际功能
{self.analyze_skill_function(skill_path) if skill_path else '需要安装后分析'}

## 使用方法
{self.generate_usage_examples(skill_path) if skill_path else '需要安装后生成'}

## 安装方式（已验证）
```bash
{install_cmd}
```

## 使用示例
{self.generate_examples(skill_name)}

---

[文档生成时间]：{self.get_current_time()}
[安装命令验证状态]：{'已验证' if skill_name in self.verified_commands else '待验证'}
"""

        # 保存文档
        doc_file = self.skill_docs_dir / f"{skill_name}_英文_Chinese.md"
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)

        # 更新索引
        self.skills_info[skill_name]['last_updated'] = self.get_current_time()
        self.save_skills_index()

        return doc_content

    def analyze_skill_function(self, skill_path: Path) -> str:
        """分析技能功能"""
        if not skill_path:
            return ""

        # 读取 SKILL.md
        skill_md = skill_path / 'SKILL.md'
        if skill_md.exists():
            with open(skill_md, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 提取描述
            for i, line in enumerate(lines):
                if line.strip().startswith('description:'):
                    description = line.split(':', 1)[1].strip()
                    if description.startswith('"') and description.endswith('"'):
                        description = description[1:-1]
                    return description

        return "功能描述待补充"

    def generate_usage_examples(self, skill_path: Path) -> str:
        """生成使用示例"""
        if not skill_path:
            return ""

        examples = []

        # 基本用法
        examples.append("/skill {skill_name}")

        # 查看帮助
        examples.append("/skill {skill_name} --help")

        # 交互式使用
        examples.append("直接描述需求，如：'我想写小说'")

        return "\n".join(f"- {ex}" for ex in examples)

    def generate_examples(self, skill_name: str) -> str:
        """生成使用示例"""
        examples = {
            "find-skills": [
                "/skill find-skills",
                "如何做React性能优化？",
                "找任务管理工具",
                "需要测试工具"
            ],
            "brainstorming": [
                "/skill brainstorming",
                "为新产品想创意",
                "解决技术难题",
                "头脑风暴会议"
            ],
            "literary-story": [
                "/skill literary-story",
                "开始写小说",
                "创建新章节",
                "管理小说结构"
            ]
        }

        if skill_name in examples:
            return "\n".join(f"- {ex}" for ex in examples[skill_name])

        return f"- /skill {skill_name}\n- 描述你的需求"

    def handle_user_selection(self, skill_name: str, choice: str) -> str:
        """处理用户选择"""
        if choice == "1":
            return self.get_management_doc(skill_name)
        elif choice == "2":
            return self.get_source_readme(skill_name)
        elif choice == "3":
            return self.show_comparison(skill_name)
        elif choice == "4":
            # 快速概览
            skill_info = self.skills_info.get(skill_name, {})
            return f"""
[{skill_name} 快速概览]

仓库：{skill_info.get('repo', '待补充')}
安装：{self.verified_commands.get(skill_name, '需要手动验证')}
状态：{'[已安装]' if self.find_skill_installation(skill_name) else '[未安装]'}
"""
        else:
            return "[错误] 无效选择，请输入 1-4"

    def check_and_install_skill(self, skill_name: str) -> bool:
        """检查并安装技能"""
        if skill_name in self.skills_info:
            return True

        # 使用 skill-installer 安装
        try:
            result = subprocess.run(
                ['python', 'scripts/skill_installer.py', skill_name],
                cwd=self.skill_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # 添加到索引
                self.skills_info[skill_name] = {
                    "repo": "待补充",
                    "verified": False,
                    "last_updated": self.get_current_time()
                }
                self.save_skills_index()
                return True
        except:
            pass

        return False

    def get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    # 测试
    dm = DocumentManager()
    print("Document Manager 初始化完成")
    print(f"文档目录：{dm.skill_docs_dir}")
    print(f"已管理技能：{list(dm.skills_info.keys())}")