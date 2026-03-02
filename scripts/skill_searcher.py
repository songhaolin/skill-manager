#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能搜索器 - Skill Manager (修复版)
"""

import subprocess
import re
from typing import List, Dict

class SkillSearcher:
    """技能搜索器"""

    KNOWN_SKILLS = {
        'literary-story': {
            'name': 'literary-story',
            'chinese': '小说写作',
            'description': '基于目录的小说创作工作流',
            'features': ['智能意图路由', '自动进度管理', '防写错保护'],
        },
        'planning-with-files': {
            'name': 'planning-with-files',
            'chinese': '任务规划',
            'description': 'Manus风格的文件规划系统',
            'features': ['任务分解', '会话恢复', '50+工具调用'],
        },
        'xiaohongshu-generator': {
            'name': 'xiaohongshu-generator',
            'chinese': '小红书生成器',
            'description': '生成小红书内容和9宫格图像',
            'features': ['9宫格AI图像', '完整文案', '实时搜索'],
        },
        'pdf': {
            'name': 'pdf',
            'chinese': 'PDF处理',
            'description': 'PDF文件处理工具',
            'features': ['文本提取', '页面旋转', '表单填写'],
        },
        'find-skills': {
            'name': 'find-skills',
            'chinese': '技能查找',
            'description': '搜索和发现技能',
            'features': ['关键词搜索', '分类浏览'],
        },
        'skill-creator': {
            'name': 'skill-creator',
            'chinese': '技能创建',
            'description': '创建新技能的指导',
            'features': ['创建流程', '最佳实践'],
        },
        'skill-installer': {
            'name': 'skill-installer',
            'chinese': '技能安装',
            'description': '安装技能工具',
            'features': ['一键安装', '批量操作'],
        },
    }

    def search(self, search_terms: List[str]) -> List[Dict]:
        """搜索技能"""
        results = []

        for term in search_terms[:3]:
            try:
                output = self._npx_find(term)
                skills = self._parse_output(output)
                results.extend(skills)
            except Exception as e:
                print(f"  ⚠️  搜索 '{term}' 失败: {e}")

        return self._deduplicate(results)

    def _npx_find(self, term: str) -> str:
        """调用 npx skills find"""
        result = subprocess.run(
            ['npx', 'skills', 'find', term],
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8'
        )
        return result.stdout if result.returncode == 0 else ""

    def _parse_output(self, output: str) -> List[Dict]:
        """解析搜索输出 - 更新版"""
        skills = []

        # 新格式：anthropics/skills@pdf 或 owner/repo@skill
        pattern = r'\x1b\[\d+m([^\x1b]+)\x1d\x1b\[\d+'
        matches = re.findall(pattern, output)

        if not matches:
            # 备用格式：直接搜索
            pattern = r'([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)@([a-zA-Z0-9_-]+)'
            matches = re.findall(pattern, output)

        for match in matches:
            if isinstance(match, tuple):
                owner_repo, skill_name = match
                full_name = f"{owner_repo}@{skill_name}"
            else:
                parts = match.split('@')
                if len(parts) >= 2:
                    owner_repo = '@'.join(parts[:-1])
                    skill_name = parts[-1]
                    full_name = match
                else:
                    continue

            skills.append({
                'name': skill_name,
                'full_name': full_name,
                'owner': owner_repo.split('/')[0] if '/' in owner_repo else 'unknown',
            })

        return skills

    def _deduplicate(self, skills: List[Dict]) -> List[Dict]:
        """去重"""
        seen = set()
        unique = []
        for skill in skills:
            if skill['name'] not in seen:
                seen.add(skill['name'])
                unique.append(skill)
        return unique

    def format_results(self, skills: List[Dict]) -> str:
        """格式化结果"""
        if not skills:
            return "❌ 未找到相关技能"

        if len(skills) == 1:
            skill = skills[0]
            info = self.KNOWN_SKILLS.get(skill['name'])

            if info:
                stars = '⭐' * 5
                return f"""✅ 找到完美匹配！

{skill['name']} ({info['chinese']}) {stars}

{info['description']}

核心功能:
{chr(10).join(f"• {f}" for f in info['features'])}

要安装吗？(y/n)"""
            else:
                return f"""✅ 找到技能！

{skill['name']}
{skill.get('full_name', '')}

要安装吗？(y/n)"""

        elif len(skills) <= 5:
            output = f"✅ 找到 {len(skills)} 个相关技能：\n\n"
            for i, skill in enumerate(skills, 1):
                info = self.KNOWN_SKILLS.get(skill['name'])
                chinese = f" ({info['chinese']})" if info else ""
                desc = info['description'][:40] + "..." if info else ""
                output += f"{i}. {skill['name']}{chinese}\n"
                if desc:
                    output += f"   {desc}\n"
                output += "\n"

            output += "选择要安装的技能 (1-{}, 或 all): ".format(len(skills))
            return output
        else:
            return f"✅ 找到 {len(skills)} 个相关技能！\n\n" + \
                   "相关技能太多，请更具体地描述你的需求。\n\n" + \
                   "或者我可以列出前5个：\n\n" + \
                   "\n".join(f"{i}. {s['name']}" for i, s in enumerate(skills[:5], 1))


# 测试
if __name__ == "__main__":
    searcher = SkillSearcher()
    results = searcher.search(['pdf'])
    print(searcher.format_results(results))
