#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能安装器 - Skill Manager
"""

import subprocess
from pathlib import Path

class SkillInstallerWrapper:
    """技能安装器"""

    def __init__(self):
        self.skills_dir = Path.home() / ".claude" / "skills"

    def install(self, skill_name: str) -> bool:
        """安装技能"""
        print(f"🚀 安装 {skill_name}...")

        # 方法1: npx skills add
        if self._install_via_npx(skill_name):
            return True

        # 方法2: 从 openai/skills
        if self._install_from_openai(skill_name):
            return True

        print(f"❌ 安装失败")
        return False

    def _install_via_npx(self, skill_name: str) -> bool:
        """通过 npx 安装"""
        try:
            result = subprocess.run(
                ['npx', 'skills', 'add', f'openai/skills@{skill_name}', '-y'],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                return self._verify(skill_name)
            return False
        except:
            return False

    def _install_from_openai(self, skill_name: str) -> bool:
        """从 openai/skills 安装"""
        skill_path = self.skills_dir / skill_name

        try:
            subprocess.run(
                ['git', 'clone', '--depth=1', '--sparse',
                 'https://github.com/openai/skills.git',
                 str(self.skills_dir / f"temp_{skill_name}")],
                check=True,
                capture_output=True,
                timeout=60
            )

            temp_dir = self.skills_dir / f"temp_{skill_name}"
            subprocess.run(
                ['git', 'sparse-checkout', 'set', f'skills/.curated/{skill_name}'],
                cwd=temp_dir,
                check=True,
                capture_output=True
            )

            source = temp_dir / f'skills/.curated/{skill_name}'
            if source.exists():
                subprocess.run(['mv', str(source), str(skill_path)], check=True)
                subprocess.run(['rm', '-rf', str(temp_dir)])
                return self._verify(skill_name)

            return False
        except:
            if temp_dir.exists():
                subprocess.run(['rm', '-rf', str(temp_dir)])
            return False

    def _verify(self, skill_name: str) -> bool:
        """验证安装"""
        skill_path = self.skills_dir / skill_name
        if skill_path.exists() and (skill_path / "SKILL.md").exists():
            print(f"✅ 安装成功！")
            print(f"   使用: /skill {skill_name}")
            return True
        return False
