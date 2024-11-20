# PhenoCHPO

这是一个从中文临床信息中，提取出临床表型相关词汇，然后与CHPO的列表进行对照，获取HPO编号的工具。主要使用了分词的功能。

HPO编号与遗传病基因检测分析相关，这个工具可以简化从临床信息中获取HPO编号的人工操作。

## 功能特点
- 中文临床文本分词
- 临床表型术语提取
- CHPO映射匹配
- HPO编号自动获取

## 依赖项
- jieba>=0.42.1
- pandas>=1.3.0
- fuzzywuzzy>=0.18.0
- python-Levenshtein>=0.12.2


## 安装说明

1. 克隆项目

```bash
git clone https://github.com/pzweuj/PhenoCHPO.git
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行使用

```bash
python src/cli.py -i examples/clinical_cases.txt -o examples/output.json -t 0.85
```

参数说明：
- `-i, --input`: 输入文件路径（txt格式）
- `-o, --output`: 输出文件路径（json格式）
- `-t, --threshold`: 相似度阈值（0-1之间，默认0.75）

### 输入格式
输入文件应为txt格式，临床描述，例如：

```
患者，男，5岁，表现为发育迟缓，智力障碍，出现癫痫发作，伴有肌肉萎缩和运动障碍。
```

## 数据说明
- CHPO版本：20220925，可自行构建更新的版本
- 词典格式：CSV文件，包含HPO ID和对应的中文标准术语

## 注意事项
- 确保输入文本为UTF-8编码
- 建议根据具体需求调整相似度阈值
- 处理大量文本时可能需要较长时间

