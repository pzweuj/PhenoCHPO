import os
import sys
import PySimpleGUI as sg
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.mapper import HPOMapper



def process_text(input_text, threshold):
    try:
        # 初始化映射器
        mapper = HPOMapper(similarity_threshold=threshold)
        
        # 处理输入文本
        texts = [line.strip() for line in input_text.split('\n') if line.strip()]  # 去除空行和首尾空白
        
        # 处理文本并获取按HPO ID归类的结果
        results = mapper.batch_process(texts)
        
        # 按HPO ID排序
        sorted_results = dict(sorted(results.items()))
        
        # 格式化结果为字符串
        output_text = json.dumps(sorted_results, ensure_ascii=False, indent=2)

        # 空结果
        if len(sorted_results) == 0:
            output_text = "未找到匹配的表型"
        
        # 提取HPO编号并连接为字符串
        hpo_ids = ','.join(sorted_results.keys())
        
        return output_text, hpo_ids

    except Exception as e:
        sg.popup_error(f"处理过程中出现错误: {str(e)}")
        return "", ""

def main():
    notice_string = "注意：程序基于关键词提取，可能存在误判，请人工核对！\n"\
                    "如：\n"\
                    "\t'无头痛'会被识别为\"HP:0002315\": \"头痛\"，\n\n"\
                    "应避免不存在的表型录入。\n\n"\
                    "相似度设置越高，识别准确率越高，但获得的表型会越少。"

    layout = [
        [sg.Text('输入临床信息')], 
        [sg.Multiline(size=(120, 10), key='-INPUT-')],
        [sg.Text('相似度阈值 (0-1之间)'), sg.Slider(range=(0, 1), resolution=0.01, default_value=0.75, orientation='h', key='-THRESHOLD-')],
        [sg.Submit(), sg.Exit()],
        [sg.Text('输出结果')],
        [sg.Multiline(size=(120, 15), key='-OUTPUT-', disabled=True, default_text=notice_string)],
        [sg.Text('HPO编号列表')],
        [sg.InputText(size=(120, 1), key='-HPO_IDS-', disabled=True), sg.Button('复制', key='-COPY-')]
    ]

    window = sg.Window('中文HPO映射工具', layout, finalize=True)

    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Submit':
            input_text = values['-INPUT-']
            threshold = values['-THRESHOLD-']
            
            # 显示等待图形
            window['-OUTPUT-'].update('计算中，请稍候...')
            window.refresh()
            
            output_text, hpo_ids = process_text(input_text, threshold)

            # 更新输出文本和HPO编号
            window['-OUTPUT-'].update(output_text)
            window['-HPO_IDS-'].update(hpo_ids)
        
        if event == '-COPY-':
            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(values['-HPO_IDS-'])

    window.close()

if __name__ == '__main__':
    main() 