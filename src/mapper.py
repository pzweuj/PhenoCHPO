import jieba
import pandas as pd
from fuzzywuzzy import fuzz
from typing import Dict, List, Union
import re

class HPOMapper:
    def __init__(self, chpo_path: str = "data/chpo_dict.csv", 
                 similarity_threshold: float = 0.8):
        """
        初始化HPO映射器
        """
        self.similarity_threshold = similarity_threshold
        self.punctuation = "，。！？；：""''（）【】《》、"  # 添加标点符号列表
        
        # 加载CHPO词典
        self.chpo_dict = pd.read_csv(chpo_path)
        
        # 创建映射字典
        self.term_to_hpo = {}
        self.hpo_to_standard_term = {}
        
        for _, row in self.chpo_dict.iterrows():
            hpo_id = row['hpo_id']
            term = row['chinese_term'].strip()
            self.term_to_hpo[term] = hpo_id
            self.hpo_to_standard_term[hpo_id] = term
        
        # 添加常见临床表型词到分词词典
        common_terms = [
            "发育迟缓", "智力障碍", "癫痫发作", "肌肉萎缓", "肌肉萎缩",
            "运动障碍", "发育落后", "智力发育迟缓", "生长迟缓",
            "肌张力", "共济失调", "步态不稳", "发育", "智力", "运动"
        ]
        for term in common_terms:
            jieba.add_word(term)
        
        # 将所有CHPO术语添加到分词词典
        for term in self.term_to_hpo.keys():
            jieba.add_word(term)
    
    def _clean_text(self, text: str) -> str:
        """
        清理文本
        """
        # 移除标点符号
        for punct in self.punctuation:
            text = text.replace(punct, ' ')
            
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def process(self, text: str) -> Dict[str, str]:
        """
        处理单条临床描述文本
        """
        # 首先清理文本
        text = self._clean_text(text)
        
        terms = jieba.lcut(text)
        matches = {}
        
        # 使用滑动窗口组合相邻词
        n = len(terms)
        for i in range(n):
            for j in range(i + 1, min(i + 4, n + 1)):
                term = ''.join(terms[i:j])
                if not term:
                    continue
                
                # 跳过常见的无意义词组
                if self._is_invalid_term(term):
                    continue
                    
                # 直接匹配
                hpo_id = self.term_to_hpo.get(term)
                if hpo_id:
                    matches[hpo_id] = self.hpo_to_standard_term[hpo_id]
                    continue
                
                # 模糊匹配（只对较长的词组进行模糊匹配）
                if len(term) >= 3:  # 增加最小长度限制
                    best_match = self._find_best_match(term)
                    if best_match:
                        matches[best_match] = self.hpo_to_standard_term[best_match]
        
        return matches
    
    def _is_invalid_term(self, term: str) -> bool:
        """
        检查是否为无效术语
        """
        invalid_terms = {
            "患者", "患儿", "表现", "伴有", "出现", "存在", "男", "女",
            "岁", "月", "天", "年", "性", "和", "与", "及", "或",
            "的", "地", "得", "了", "着", "个"
        }
        return (
            term in invalid_terms or
            len(term) < 2 or  # 过短的词
            term.isdigit()    # 纯数字
        )
    
    def _find_best_match(self, term: str) -> Union[str, None]:
        """
        找到最佳匹配的HPO ID
        """
        best_ratio = self.similarity_threshold
        best_hpo = None
        
        for dict_term, dict_hpo in self.term_to_hpo.items():
            # 只比较长度相近的词
            if abs(len(term) - len(dict_term)) > 2:
                continue
                
            # 计算相似度
            ratio = fuzz.ratio(term, dict_term) / 100.0
            
            # 更新最佳匹配
            if ratio > best_ratio:
                # 额外检查，防止错误匹配
                if not self._is_likely_mismatch(term, dict_term):
                    best_ratio = ratio
                    best_hpo = dict_hpo
        
        return best_hpo
    
    def _is_likely_mismatch(self, term1: str, term2: str) -> bool:
        """
        检查是否可能是错误匹配
        """
        # 如果两个词都包含特定关键词，但不完全相同，可能是错误匹配
        keywords = {"萎缩", "发育", "障碍", "异常"}
        term1_keys = {k for k in keywords if k in term1}
        term2_keys = {k for k in keywords if k in term2}
        
        if term1_keys and term2_keys and term1_keys != term2_keys:
            return True
            
        return False

    def batch_process(self, texts: List[str]) -> Dict[str, str]:
        """
        批量处理临床描述文本
        """
        results = {}
        for text in texts:
            matches = self.process(text)
            results.update(matches)
        return dict(sorted(results.items()))
