import argparse
import json
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 修改导入语句
from src.mapper import HPOMapper

def main():
    # 创建解析器并添加描述
    parser = argparse.ArgumentParser(
        description='中文临床表型HPO映射工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
    python cli.py -i input.txt -o output.json
    python cli.py -i input.txt -o output.json -t 0.85
    
注意:
    - 输入文件必须是txt格式，每行一个临床描述
    - 输出文件为json格式
    - 相似度阈值范围为0-1之间，默认为0.75
        '''
    )

    # 添加参数
    parser.add_argument('--input', '-i', type=str, required=True,
                       help='输入文件路径 (txt格式)')
    parser.add_argument('--output', '-o', type=str, required=True,
                       help='输出文件路径 (json格式)')
    parser.add_argument('--threshold', '-t', type=float, default=0.75,
                       help='相似度阈值 (0-1之间，默认: 0.8)')

    # 如果没有参数，打印帮助信息
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # 验证输入输出文件格式
    if not args.input.endswith('.txt'):
        parser.error("输入文件必须是txt格式")
    if not args.output.endswith('.json'):
        parser.error("输出文件必须是json格式")
    
    # 验证相似度阈值范围
    if not 0 <= args.threshold <= 1:
        parser.error("相似度阈值必须在0到1之间")

    try:
        # 初始化映射器
        mapper = HPOMapper(similarity_threshold=args.threshold)
        
        # 读取输入文件
        with open(args.input, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]  # 去除空行和首尾空白
        
        # 处理文本并获取按HPO ID归类的结果
        results = mapper.batch_process(texts)
        
        # 按HPO ID排序
        sorted_results = dict(sorted(results.items()))
        
        # 保存结果
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(sorted_results, f, ensure_ascii=False, indent=2)
        
        print(f"处理完成！结果已保存至: {args.output}")
        print(f"总计发现 {len(sorted_results)} 个不同的HPO术语")
        
        # 打印一些统计信息
        total_terms = sum(len(terms) for terms in sorted_results.values())
        print(f"共包含 {total_terms} 个中文表型描述")

    except FileNotFoundError as e:
        print(f"错误：找不到文件 - {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 