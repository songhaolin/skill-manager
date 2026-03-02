#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
意图分析器 - Skill Manager
"""

import re
from typing import Dict, List

class IntentAnalyzer:
    """意图分析器"""

    KEYWORD_MAP = {
        '小说': ['novel', 'story', 'writing'],
        '小红书': ['xiaohongshu', 'content'],
        '任务': ['task', 'plan', 'management'],
        'pdf': ['pdf', 'document'],
        '测试': ['test', 'testing'],
    }

    def analyze(self, user_input: str) -> Dict:
        """分析用户意图"""
        user_input = user_input.strip().lower()

        # 识别意图类型
        if any(word in user_input for word in ['安装', 'install', '添加', 'add']):
            intent = 'install'
        elif any(word in user_input for word in ['创建', 'create', '新建', 'new']):
            intent = 'create'
        else:
            intent = 'search'

        # 提取技能名称
        skill_name = self._extract_skill_name(user_input)

        # 提取关键词
        keywords = self._extract_keywords(user_input)

        # 生成搜索词
        search_terms = self._generate_search_terms(keywords)

        return {
            'intent': intent,
            'skill_name': skill_name,
            'keywords': keywords,
            'search_terms': search_terms,
        }

    def _extract_skill_name(self, text: str) -> str:
        """提取技能名称"""
        patterns = [
            r'(?:安装|install|创建|create)\s+([\w-]+)',
            r'([\w-]+)\s*技能',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return None

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []

        for chinese, english_list in self.KEYWORD_MAP.items():
            if chinese in text:
                keywords.append(chinese)

        words = re.findall(r'[\u4e00-\u9fff]{2,4}|[a-zA-Z]{2,}', text)
        keywords.extend(words)

        return list(set(keywords))

    def _generate_search_terms(self, keywords: List[str]) -> List[str]:
        """生成搜索词"""
        terms = []

        for keyword in keywords:
            if keyword in self.KEYWORD_MAP:
                terms.extend(self.KEYWORD_MAP[keyword])
            elif re.match(r'^[a-zA-Z]+$', keyword):
                terms.append(keyword)

        return list(set(terms))[:5]
