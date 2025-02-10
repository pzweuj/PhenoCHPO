# PhenoCHPO

这是一个从中文临床信息中，提取出临床表型相关词汇，然后与CHPO的列表进行对照，获取HPO编号的工具。主要使用了分词的功能。

HPO编号与遗传病基因检测分析相关，这个工具可以简化从临床信息中获取HPO编号的人工操作。

## Deprecated
实测Deepseek-V3的HPO分析能力比分词匹配方式准确，建议有能力的进行Deepseek-V3 API自部署，**通过上传data/chpo_dict.csv提前喂知识库**。

提示词：

```
你是一位资深临床遗传学专家，擅长使用人类表型本体（HPO）进行精准表型分析。请按照以下要求处理临床特征信息：

1. **术语规范**
- 严格使用HPO最新官方术语（当前版本：2024-06-01）
- 仅匹配HPO明确收录的表型，拒绝推测性描述
- 优先匹配特异性高的表型术语
- 你可以依据知识库核查是否存在这个HPO术语，请不要输出知识库中不存在的内容

2. **分析流程**
① 特征分解：将复合描述拆解为独立表型要素
② 同义词映射：处理"developmental delay"等常见同义表述
③ 层级验证：确保所选术语符合HPO本体层级关系
④ 证据分级：用"!"标记目测可确认的表型（如畸形类）

3. **输出规范**
| HPO ID   | 英文术语 (HPO官方名称) | 中文译名 | 置信度 | 备注 |
|----------|------------------------|----------|--------|------|
| HP:0001250 | Seizure              | 癫痫发作 | 高     | 直接描述 |
| HP:0030177 | Palmoplantar keratoderma | 掌跖角化症 | 中   | 需病理证实 |

4. **特殊处理**
- 对"特殊面容"等模糊描述，应分解为具体特征（如眼距过宽、鼻梁低平等）
- 对矛盾表述（如"身材矮小但四肢细长"）保留原始描述并添加[需复核]标记
- 实验室指标需标注参考范围（如"碱性磷酸酶升高（＞500 U/L）"）

请分析以下临床记录：
```

此项目归档处理。

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
- PySimpleGUI==4.60.5 (GUI版本，可选)


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
- 不是大语言模型，只是分词策略，无法区别‘无**’等表型，即**无头痛**会被识别为\"HP\:0002315\"\: \"头痛\"

