import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import io
import sys
import os
import platform
from datetime import datetime

# 尝试导入PDF相关库，如果失败则使用简化版本
try:
    import plotly.io as pio
    from matplotlib import pyplot as plt
    import seaborn as sns
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    # 尝试导入PIL用于图像处理
    try:
        from PIL import Image as PILImage
        PIL_AVAILABLE = True
    except ImportError:
        PIL_AVAILABLE = False
    PDF_AVAILABLE = True
    
    # 在Streamlit Cloud上显示成功信息
    print("✅ PDF生成依赖库加载成功")
    
except ImportError as e:
    PDF_AVAILABLE = False
    PIL_AVAILABLE = False
    
    # 改进的错误提示，特别针对Streamlit Cloud
    print(f"⚠️ PDF依赖库加载失败: {str(e)}")
    print("📝 如果您在本地运行，请执行: pip install matplotlib seaborn reportlab Pillow")
    print("🌐 如果您在Streamlit Cloud部署，请确保 requirements.txt 包含所有必需依赖库")
    
    # 创建一个虚拟的streamlit模块用于错误显示
    import sys
    if 'streamlit' in sys.modules:
        try:
            import streamlit as st_temp
            st_temp.warning("⚠️ PDF生成功能不可用，将使用简化版HTML报告")
        except:
            pass

def generate_simplified_report(results, df_clean):
    """生成简化版本的HTML报告（当PDF库不可用时）"""
    
    # 获取基本信息
    basic_info = results.get('basic_info', {})
    input_params = results.get('input_params', {})
    calculations = results.get('calculations', {})
    percentages = results.get('percentages', {})
    
    # 当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 构建简化的HTML报告
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>LED植物照明光学度量体系分析报告</title>
        <style>
            /* 优先使用支持中文的字体 */
            body {{ 
                font-family: 'Noto Sans SC', 'Microsoft YaHei', '微软雅黑', 'Arial Unicode MS', Arial, sans-serif; 
                margin: 20px; 
                line-height: 1.6; 
            }}
            h1 {{ color: #2c3e50; text-align: center; }}
            h2 {{ color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #3498db; color: white; }}
            .highlight {{ background-color: #f1f2f6; padding: 15px; border-left: 4px solid #3498db; }}
        </style>
        <!-- 添加Google字体支持 -->
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap" rel="stylesheet">
    </head>
    <body>
        <h1>🌱 LED植物照明光学度量体系分析报告</h1>
        <p><strong>报告生成时间：</strong>{current_time}</p>
        
        <h2>📋 测试基本信息</h2>
        <table>
            <tr><th>项目</th><th>数值</th></tr>
            <tr><td>灯具型号</td><td>{basic_info.get('lamp_model', '未填写')}</td></tr>
            <tr><td>制造商/单位</td><td>{basic_info.get('manufacturer', '未填写')}</td></tr>
            <tr><td>测试日期</td><td>{basic_info.get('test_date', '未填写')}</td></tr>
            <tr><td>总辐射通量</td><td>{input_params.get('total_radiation_flux', 0):.1f} W</td></tr>
            <tr><td>总功率</td><td>{input_params.get('total_power', 0):.1f} W</td></tr>
            <tr><td>后面板温度</td><td>{input_params.get('back_panel_temp', 0):.1f} ℃</td></tr>
            <tr><td>功率因数</td><td>{input_params.get('power_factor', 0):.3f}</td></tr>
        </table>
        
        <h2>🏆 综合评价</h2>
        <div class="highlight">
            <p><strong>总体评级：</strong>{calculations.get('quality_rating', '未知')} {calculations.get('quality_icon', '')}</p>
            <ul>
                <li><strong>PPE (光合光子效率)：</strong>{calculations.get('ppe', 0):.3f} μmol/J</li>
                <li><strong>PAR占比：</strong>{calculations.get('par_ratio', 0)*100:.1f}%</li>
                <li><strong>R/B比：</strong>{calculations.get('r_b_ratio', 0):.2f}</li>
                <li><strong>光能比：</strong>{calculations.get('light_energy_ratio', 0):.3f}</li>
            </ul>
        </div>
        
        <h2>🌈 光谱分布数据</h2>
        <table>
            <tr><th>光谱波段</th><th>波长范围</th><th>积分值</th><th>占比</th></tr>
            <tr><td>蓝光</td><td>400-500 nm</td><td>{calculations.get('blue_integration', 0):.2f}</td><td>{percentages.get('blue_percentage', 0):.1f}%</td></tr>
            <tr><td>绿光</td><td>500-600 nm</td><td>{calculations.get('green_integration', 0):.2f}</td><td>{percentages.get('green_percentage', 0):.1f}%</td></tr>
            <tr><td>红光</td><td>600-700 nm</td><td>{calculations.get('red_integration', 0):.2f}</td><td>{percentages.get('red_percentage', 0):.1f}%</td></tr>
            <tr><td>远红光</td><td>700-800 nm</td><td>{calculations.get('far_red_integration', 0):.2f}</td><td>{percentages.get('far_red_percentage', 0):.1f}%</td></tr>
        </table>
        
        <h2>💡 光谱优化建议</h2>
        <ul>
    """
    
    suggestions = calculations.get('optimization_suggestions', [])
    for suggestion in suggestions:
        html_content += f"<li>{suggestion}</li>"
    
    html_content += """
        </ul>
        
        <h2>📖 分析方法说明</h2>
        <p><strong>核心计算公式：</strong></p>
        <ul>
            <li>光能比 = 光合有效积分 ÷ 总积分</li>
            <li>总光子通量 = 总辐射通量 × 光能比 (μmol/s)</li>
            <li>PPE = 总光子通量 ÷ 总功率 (μmol/J)</li>
        </ul>
        
        <footer style="text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid #ddd;">
            <p>LED植物照明光学度量体系分析系统 | 基于四种光学度量体系</p>
        </footer>
    </body>
    </html>
    """
    
    return html_content.encode('utf-8')

def generate_chart_images(results, df_clean):
    """生成图表图片用于PDF报告"""
    chart_images = {}
    
    # 验证输入数据
    if not results or not isinstance(results, dict):
        raise ValueError("分析结果数据不完整，无法生成图表")
    
    if df_clean is None or df_clean.empty:
        raise ValueError("光谱数据为空，无法生成图表")
    
    # 获取必要的数据
    calculations = results.get('calculations', {})
    percentages = results.get('percentages', {})
    
    print(f"图表生成数据验证：")
    print(f"- 光谱数据点数: {len(df_clean)}")
    print(f"- 计算结果数量: {len(calculations)}")
    print(f"- 百分比数据数量: {len(percentages)}")
    
    try:
        # 首先强制设置matplotlib后端为Agg，确保在任何环境下都能正常工作
        import matplotlib
        print(f"🔧 当前后端: {matplotlib.get_backend()}")
        matplotlib.use('Agg', force=True)  # 强制切换后端
        print(f"✅ 切换后端为: Agg")
        
        # 然后导入其他库
        from matplotlib import pyplot as plt
        import matplotlib.font_manager as fm
        import platform
        import os
        
        # 字体加载调试信息
        print("======= Matplotlib字体加载开始 =======")
        
        # 设置matplotlib中文字体 - 增强版本，优先使用本地字体
        # 首先尝试加载项目中的中文字体
        base_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(base_dir, 'fonts')
        local_fonts = [
            os.path.join(fonts_dir, 'NotoSansSC-Regular.ttf'),
            os.path.join(fonts_dir, 'NotoSansSC-Regular.otf'),
            os.path.join(fonts_dir, 'NotoSansSC-Regular.ttc'),
            # 添加更多可能的中文字体文件名
            os.path.join(fonts_dir, 'simhei.ttf'),
            os.path.join(fonts_dir, 'simsun.ttc'),
            os.path.join(fonts_dir, 'msyh.ttc'),
        ]
        
        font_set = False
        chinese_fonts = []
        current_font = None
        
        # 尝试加载本地可用的中文字体
        for font_path in local_fonts:
            if os.path.exists(font_path):
                try:
                    # 尝试添加字体到matplotlib
                    fm.fontManager.addfont(font_path)
                    font_name = os.path.splitext(os.path.basename(font_path))[0]
                    chinese_fonts.append(font_name)
                    font_set = True
                    print(f"✅ 成功加载本地中文字体: {font_path}")
                    # 不再break，尝试加载所有可用字体
                except Exception as e:
                    print(f"⚠️ 加载本地字体 {font_path} 失败: {str(e)}")
        
        # 获取系统信息
        system = platform.system()
        print(f"检测到系统: {system}")
        
        # 如果本地字体加载失败，尝试系统字体
        if not font_set:
            print("本地字体加载失败，尝试加载系统字体")
            
            # 初始化字体列表
            potential_fonts = []
            font_names = []
            
            # 根据系统选择可能的字体路径
            if system == "Windows":
                # Windows常见中文字体路径
                potential_fonts = [
                    'C:/Windows/Fonts/simhei.ttf',     # 黑体
                    'C:/Windows/Fonts/simsun.ttc',     # 宋体
                    'C:/Windows/Fonts/msyh.ttc',       # 微软雅黑
                    'C:/Windows/Fonts/simkai.ttf',     # 楷体
                    'C:/Windows/Fonts/simfang.ttf'     # 仿宋
                ]
                font_names = ['SimHei', 'SimSun', 'Microsoft YaHei', 'KaiTi', 'FangSong']
            elif system == "Darwin":  # macOS
                potential_fonts = [
                    '/System/Library/Fonts/PingFang.ttc',
                    '/System/Library/Fonts/STSong.ttc',
                    '/System/Library/Fonts/STHeiti Light.ttc',
                    '/System/Library/Fonts/STKaiti.ttc',
                    '/System/Library/Fonts/STFangsong.ttc',
                    '/Library/Fonts/PingFang.ttc',  # 备选路径
                    '/Library/Fonts/NotoSansSC-Regular.ttf'  # 用户安装的字体
                ]
                font_names = ['PingFang SC', 'STSong', 'STHeiti', 'STKaiti', 'STFangsong', 'PingFang SC', 'Noto Sans SC']
            else:  # Linux/其他系统，特别是Streamlit Cloud环境
                # 扩展Linux字体路径，覆盖更多可能的位置
                potential_fonts = [
                    # Streamlit Cloud环境中可能存在的字体路径
                    '/usr/share/fonts/truetype/noto/NotoSansSC-Regular.ttf',
                    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                    # 其他常见Linux字体路径
                    '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
                    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
                    '/var/lib/defoma/fontconfig.d/fonts/truetype/wqy/wqy-microhei.ttc',
                    # Docker环境中可能的字体路径
                    '/usr/local/share/fonts/noto/NotoSansSC-Regular.ttf',
                    # 尝试查找所有已安装的Noto Sans SC字体
                    '/usr/share/fonts/truetype/noto/NotoSansSC*.ttf'
                ]
                font_names = ['Noto Sans SC', 'Noto Sans CJK', 'Droid Sans Fallback', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'Noto Sans SC', 'Noto Sans SC']
            
            # 检查字体文件是否存在并添加到matplotlib
            for font_path, font_name in zip(potential_fonts, font_names):
                if os.path.exists(font_path):
                    try:
                        # 添加字体到matplotlib
                        fm.fontManager.addfont(font_path)
                        chinese_fonts.append(font_name)
                        font_set = True
                        print(f"✅ 成功加载系统字体: {font_path} ({font_name})")
                        # 不再break，尝试加载所有可用字体
                    except Exception as e:
                        print(f"⚠️ 无法添加字体 {font_name}: {e}")
            
            # 尝试直接通过字体名称加载（不依赖文件路径）- 增强版本
            if not font_set:
                print("尝试直接通过字体名称加载系统中文字体...")
                # 扩展通用中文字体名称列表，覆盖更多可能支持中文的字体
                common_chinese_fonts = [
                    # 首选字体，通常在大多数系统上可用
                    'Noto Sans SC', 'Noto Sans CJK',
                    # Windows字体
                    'SimHei', 'Microsoft YaHei', 'SimSun',
                    # macOS字体
                    'PingFang SC', 'STHeiti', 'STSong',
                    # Linux字体
                    'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback',
                    # 其他可能支持中文的通用字体
                    'Arial Unicode MS', 'DejaVu Sans', 'Arial',
                    # 作为最后手段的兜底字体
                    'sans-serif'
                ]
                
                # 尝试所有字体名称，直到找到可用的
                for font_name in common_chinese_fonts:
                    try:
                        # 尝试创建字体属性，验证字体是否可用
                        font_prop = fm.FontProperties(family=font_name)
                        # 更准确的字体验证
                        try:
                            # 尝试获取字体文件路径
                            font_files = [f for f in fm.findSystemFonts(fontpaths=None) if font_name.lower() in f.lower()]
                            if font_files:
                                chinese_fonts.append(font_name)
                                font_set = True
                                print(f"✅ 成功通过字体名称加载: {font_name} (找到字体文件: {font_files[0]})")
                                # 尝试加载找到的字体文件
                                try:
                                    for font_file in font_files[:3]:  # 加载前3个找到的字体文件
                                        fm.fontManager.addfont(font_file)
                                        print(f"  - 已添加字体文件: {font_file}")
                                except Exception as inner_e:
                                    print(f"  - 添加字体文件时出错: {inner_e}")
                                break
                        except:
                            # 如果获取字体文件路径失败，使用基本验证
                            if font_prop.get_family()[0] != 'sans-serif':
                                chinese_fonts.append(font_name)
                                font_set = True
                                print(f"✅ 成功通过字体名称加载: {font_name}")
                                break
                    except Exception as e:
                        print(f"⚠️ 字体名称 {font_name} 不可用: {e}")
        
        # 设置matplotlib字体 - 增强版本
        try:
            # 构建字体列表 - 更全面的字体回退机制
            font_list = []
            
            # 添加已加载的中文字体（如果有）
            if chinese_fonts:
                font_list.extend(chinese_fonts)
                print(f"已加载的中文字体: {chinese_fonts}")
            else:
                # 默认字体列表，包含更多可能支持中文的字体，排序以确保最佳兼容性
                font_list = [
                    'Noto Sans SC', 'Noto Sans CJK',  # 首选开源字体
                    'SimHei', 'Microsoft YaHei', 'SimSun',  # Windows字体
                    'PingFang SC', 'STHeiti', 'STSong',  # macOS字体
                    'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback',  # Linux字体
                    'Arial Unicode MS',  # 通用Unicode字体
                    'DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif'  # 兜底字体
                ]
                print("使用默认中文字体列表")
            
            # 去重但保持顺序
            unique_font_list = []
            seen = set()
            for font in font_list:
                if font not in seen:
                    seen.add(font)
                    unique_font_list.append(font)
            font_list = unique_font_list
            
            # 针对不同平台优化字体列表
            if platform.system() == 'Darwin':  # macOS
                # 强制将STHeiti和Arial Unicode MS放在最前面
                font_list = ['STHeiti', 'Arial Unicode MS', 'PingFang SC'] + [f for f in font_list if f not in ['STHeiti', 'Arial Unicode MS', 'PingFang SC']]
                print(f"✅ 为macOS优化字体列表，优先使用STHeiti和Arial Unicode MS")
            elif platform.system() == 'Windows':
                font_list = ['SimHei', 'Microsoft YaHei'] + [f for f in font_list if f not in ['SimHei', 'Microsoft YaHei']]
                print(f"✅ 为Windows优化字体列表，优先使用SimHei和Microsoft YaHei")
            else:  # Linux / Streamlit Cloud
                # 增强Streamlit Cloud环境的字体支持
                # 检测是否在Streamlit Cloud环境 - 增强版
                is_streamlit_cloud = False
                
                # 多维度检测Streamlit Cloud环境
                if 'streamlit' in sys.modules:
                    is_streamlit_cloud = True
                    print("🌐 检测到Streamlit模块")
                if os.environ.get('STREAMLIT_RUNTIME') == 'true':
                    is_streamlit_cloud = True
                    print("🌐 检测到STREAMLIT_RUNTIME环境变量")
                if os.environ.get('PWD', '').endswith('app'):
                    is_streamlit_cloud = True
                    print("🌐 检测到PWD路径特征")
                if os.environ.get('DOCKER_CONTAINER') == 'true':
                    is_streamlit_cloud = True
                    print("🌐 检测到Docker容器环境")
                if os.environ.get('HOME') == '/home/appuser':
                    is_streamlit_cloud = True
                    print("🌐 检测到Streamlit Cloud默认用户")
                
                if is_streamlit_cloud:
                    # Streamlit Cloud优先使用的字体列表 - 增强版
                    streamlit_cloud_priority = ['Noto Sans SC', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback', 'Roboto', 'DejaVu Sans', 'Arial Unicode MS']
                    font_list = streamlit_cloud_priority + [f for f in font_list if f not in streamlit_cloud_priority]
                    print(f"✅ 为Streamlit Cloud环境优化字体列表: {streamlit_cloud_priority[:3]}...")
                    
                    # 确保使用Agg后端（无头环境必需）
                    import matplotlib
                    matplotlib.use('Agg', force=True)
                    
                    # 为Streamlit Cloud设置额外的字体渲染参数
                    plt.rcParams['pdf.fonttype'] = 42  # 确保文本不被渲染为路径
                    plt.rcParams['ps.fonttype'] = 42
                    print("✅ Streamlit环境强制使用Agg后端")
                else:
                    # 一般Linux环境
                    font_list = ['WenQuanYi Micro Hei', 'DejaVu Sans', 'SimHei', 'Arial Unicode MS'] + \
                               [f for f in font_list if f not in ['WenQuanYi Micro Hei', 'DejaVu Sans', 'SimHei', 'Arial Unicode MS']]
                    print(f"✅ 为Linux环境优化字体列表")
            
            # 不再移除Noto Sans SC，保留更多可能的中文字体选项
            # 但避免重复字体
            font_list = list(dict.fromkeys(font_list))
            
            # 验证font_list是否为空
            if not font_list:
                font_list = ['STHeiti', 'Arial Unicode MS', 'SimHei', 'sans-serif']
                print("⚠️ 初始font_list为空，已重置为默认值")
            
            # 显式设置字体列表和其他关键参数
            plt.rcParams['font.family'] = ['sans-serif']
            plt.rcParams['font.sans-serif'] = font_list
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            
            # 重要：设置PDF字体类型为42，避免文本被渲染为路径
            plt.rcParams['pdf.fonttype'] = 42
            plt.rcParams['ps.fonttype'] = 42
            
            # 设置图像渲染质量
            plt.rcParams['figure.dpi'] = 300
            plt.rcParams['savefig.dpi'] = 300
            
            # 尝试重建字体缓存
            try:
                if hasattr(fm, '_rebuild'):
                    fm._rebuild()
                elif hasattr(fm.fontManager, '_rebuild'):
                    fm.fontManager._rebuild()
                print("✅ 字体缓存已重建")
            except Exception as e:
                print(f"⚠️ 重建字体缓存失败: {e}")
            
            # 更详细的字体信息
            print(f"当前设置的字体列表: {font_list}")
            
            # 创建一个临时图形进行更严格的字体验证
            fig = plt.figure(figsize=(2, 2))
            ax = fig.add_subplot(111)
            # 测试更多中文字符，包括生僻字
            test_text = ax.text(0.5, 0.5, '测试中文字体 植物生长 光质分析', ha='center', va='center', fontsize=12)
            
            # 获取实际使用的字体信息
            renderer = fig.canvas.get_renderer()
            text_font = test_text.get_fontproperties()
            actual_font = text_font.get_name()
            actual_size = text_font.get_size_in_points()
            
            # 检查是否有中文字符丢失（通过测量文本宽度）
            bbox = test_text.get_window_extent(renderer=renderer)
            text_width = bbox.width
            
            print(f"实际使用的字体: {actual_font}")
            print(f"字体大小: {actual_size}pt")
            print(f"测试文本宽度: {text_width}px")
            
            # 字体有效性判断
            if actual_font.lower() in ['sans-serif', 'dejavu sans', 'arial', 'roboto']:
                print(f"⚠️ 可能使用了回退字体({actual_font})，中文字符可能显示不正常")
                
                # 检测是否在Streamlit Cloud环境 - 增强版
                is_streamlit_cloud = False
                if 'streamlit' in sys.modules:
                    is_streamlit_cloud = True
                if os.environ.get('STREAMLIT_RUNTIME') == 'true':
                    is_streamlit_cloud = True
                if os.environ.get('PWD', '').endswith('app'):
                    is_streamlit_cloud = True
                if os.environ.get('HOME') == '/home/appuser':
                    is_streamlit_cloud = True
                
                if is_streamlit_cloud:
                    # Streamlit Cloud特殊字体回退策略 - 增强版
                    aggressive_fonts = ['Noto Sans SC', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback', 'Roboto', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
                    print(f"🔧 Streamlit Cloud环境应用特殊字体回退策略: {aggressive_fonts[:3]}...")
                    
                    # 为Streamlit Cloud设置额外的PDF渲染参数
                    plt.rcParams['pdf.fonttype'] = 42  # 确保文本不被渲染为路径
                    plt.rcParams['ps.fonttype'] = 42
                    plt.rcParams['text.antialiased'] = True  # 启用文本抗锯齿
                else:
                    # 通用激进字体策略
                    aggressive_fonts = ['SimHei', 'WenQuanYi Micro Hei', 'Arial Unicode MS', 'DejaVu Sans', 'sans-serif']
                    print(f"🔧 应用通用字体回退策略: {aggressive_fonts[:3]}...")
                
                # 显式设置字体参数
                plt.rcParams['font.family'] = ['sans-serif']
                plt.rcParams['font.sans-serif'] = aggressive_fonts
                plt.rcParams['axes.unicode_minus'] = False  # 确保负号正常显示
                
                # 对于Streamlit环境，添加额外保障
                if is_streamlit_cloud:
                    print("✅ 在Streamlit Cloud环境中应用增强的文本渲染设置")
                    # 尝试直接使用字体名称而不是列表索引
                    try:
                        # 逐个尝试字体，直到找到可用的
                        for font in aggressive_fonts:
                            try:
                                # 创建临时文本对象测试字体
                                test_font = plt.font_manager.FontProperties(family=font)
                                if test_font.get_name().lower() != 'sans-serif':
                                    plt.rcParams['font.sans-serif'] = [font] + aggressive_fonts[1:]
                                    print(f"✅ 成功验证并应用字体: {font}")
                                    break
                            except:
                                continue
                    except:
                        print("⚠️ 字体验证失败，继续使用字体列表")
            else:
                print("✅ 字体验证成功，应能正确显示中文")
            
            plt.close(fig)
            
        except Exception as e:
            print(f"字体设置失败，使用默认设置: {e}")
            # 应急字体设置，更加激进的回退机制
            plt.rcParams['font.family'] = ['sans-serif']
            plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'DejaVu Sans', 'Arial', 'sans-serif']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 强制设置matplotlib使用Agg后端，这在无头环境（如Streamlit Cloud）中更可靠
            try:
                import matplotlib
                matplotlib.use('Agg', force=True)
                print("✅ 强制使用Agg后端，适用于无头环境")
                import matplotlib
                matplotlib.use('Agg')
                print("已切换到Agg后端以提高兼容性")
            except:
                pass
        
        print("======= Matplotlib字体加载完成 =======")
        
        # 1. 光谱分布图（彩虹图谱）
        # 重要：为每个图表创建前重置matplotlib字体设置，避免之前的设置影响
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = font_list
        plt.rcParams['axes.unicode_minus'] = False
        
        # 增强Streamlit Cloud环境的字体支持
        if 'streamlit' in sys.modules:
            print("🔧 再次确认Streamlit环境下的字体设置")
            # 强制使用Noto Sans SC作为首选字体
            plt.rcParams['font.sans-serif'] = ['Noto Sans SC'] + [f for f in font_list if f != 'Noto Sans SC']
            # 确保使用Agg后端
            import matplotlib
            matplotlib.use('Agg', force=True)
            # 设置渲染参数
            plt.rcParams['pdf.fonttype'] = 42
            plt.rcParams['ps.fonttype'] = 42
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 确保font_list存在且不为空，增强Streamlit Cloud支持
        print("🔧 为光谱图进行字体环境检查")
        if 'font_list' not in locals() or not font_list:
            # 检测是否在Streamlit Cloud环境 - 增强版
            is_streamlit_cloud = False
            if 'streamlit' in sys.modules:
                is_streamlit_cloud = True
            if os.environ.get('STREAMLIT_RUNTIME') == 'true':
                is_streamlit_cloud = True
            if os.environ.get('PWD', '').endswith('app'):
                is_streamlit_cloud = True
            if os.environ.get('HOME') == '/home/appuser':
                is_streamlit_cloud = True
            
            if is_streamlit_cloud:
                # Streamlit Cloud优先字体列表 - 增强版
                font_list = ['Noto Sans SC', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback', 'Roboto', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
                print("⚠️ 在Streamlit Cloud环境中重新初始化font_list，优先使用Noto Sans SC")
            else:
                # 标准环境字体列表
                if platform.system() == 'Darwin':
                    font_list = ['STHeiti', 'Arial Unicode MS', 'PingFang SC', 'sans-serif']
                elif platform.system() == 'Windows':
                    font_list = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
                else:
                    font_list = ['WenQuanYi Micro Hei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
                print(f"⚠️ 重新初始化font_list: {font_list[:2]}...")
        
        # 显式设置字体并验证，增强多平台兼容性
        plt.rcParams['font.sans-serif'] = font_list
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 智能选择字体 - 逐个验证
        font_family = None
        for font in font_list:
            try:
                test_font = plt.font_manager.FontProperties(family=font)
                if test_font.get_name().lower() != 'sans-serif':
                    font_family = font
                    break
            except:
                continue
        
        # 如果找不到合适的字体，使用第一个
        if font_family is None:
            font_family = font_list[0]
        
        print(f"光谱图使用字体: {font_family}")
        
        # 显式设置字体参数，确保在无头环境中也能正常工作
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = [font_family] + font_list[1:]
        print(f"✅ 光谱图最终字体设置: {plt.rcParams['font.sans-serif'][:3]}...")
        
        # 为Streamlit Cloud环境添加额外的字体安全保障
        if 'streamlit' in sys.modules:
            print("✅ 为Streamlit环境应用增强的字体设置")
            # 添加PDF渲染参数
            plt.rcParams['pdf.fonttype'] = 42
            plt.rcParams['ps.fonttype'] = 42
        
        wavelengths = df_clean['wavelength'].values
        radiations = df_clean['radiation'].values
        
        # 验证光谱数据
        if len(wavelengths) == 0 or len(radiations) == 0:
            raise ValueError("光谱数据为空")
        
        print(f"光谱图数据：波长范围 {wavelengths.min():.1f}-{wavelengths.max():.1f} nm，{len(wavelengths)} 个数据点")
        
        # 创建彩虹色谱效果
        def wavelength_to_rgb(wavelength):
            """将波长转换为RGB颜色值 (基于可见光谱)"""
            if wavelength < 380:
                return (0.5, 0.0, 1.0)  # 紫外线区域显示为紫色
            elif wavelength < 440:
                # 紫到蓝
                t = (wavelength - 380) / (440 - 380)
                return (0.5 - 0.5*t, 0.0, 1.0)
            elif wavelength < 490:
                # 蓝到青
                t = (wavelength - 440) / (490 - 440)
                return (0.0, t, 1.0)
            elif wavelength < 510:
                # 青到绿
                t = (wavelength - 490) / (510 - 490)
                return (0.0, 1.0, 1.0 - t)
            elif wavelength < 580:
                # 绿到黄
                t = (wavelength - 510) / (580 - 510)
                return (t, 1.0, 0.0)
            elif wavelength < 645:
                # 黄到橙
                t = (wavelength - 580) / (645 - 580)
                return (1.0, 1.0 - 0.5*t, 0.0)
            elif wavelength < 750:
                # 橙到红
                t = (wavelength - 645) / (750 - 645)
                return (1.0, 0.5 - 0.5*t, 0.0)
            else:
                # 红外线区域显示为深红
                return (0.5, 0.0, 0.0)
        
        # 创建连续的彩虹填充效果
        step = 5  # 每5nm一个颜色段
        min_wave = int(wavelengths.min())
        max_wave = int(wavelengths.max())
        
        # 按小段创建填充，每段使用对应的光谱颜色
        for wave_start in range(min_wave, max_wave, step):
            wave_end = min(wave_start + step, max_wave)
            
            # 筛选该波长范围内的数据
            mask = (wavelengths >= wave_start) & (wavelengths < wave_end)
            if np.any(mask):
                range_waves = wavelengths[mask]
                range_rads = radiations[mask]
                
                if len(range_waves) > 0:
                    # 计算该范围的中心波长用于颜色映射
                    center_wave = (wave_start + wave_end) / 2
                    r, g, b = wavelength_to_rgb(center_wave)
                    color = f'rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, 0.8)'
                    
                    # 创建填充区域
                    ax.fill_between(range_waves, range_rads, alpha=0.8, color=(r, g, b))
        
        # 添加整体光谱线条作为轮廓
        ax.plot(wavelengths, radiations, color='black', linewidth=1.5, alpha=0.7)
        
        # 设置坐标轴和标题 - 显式设置字体
        font_family = plt.rcParams['font.sans-serif'][0] if plt.rcParams['font.sans-serif'] else 'sans-serif'
        
        # 为图表添加网格和边界设置
        ax.grid(True, linestyle='--', alpha=0.7)
        # 强制使用已知在Streamlit Cloud环境中可用的字体组合
        title_font_dict = {'fontsize': 14, 'fontweight': 'bold', 'family': font_family}
        label_font_dict = {'fontsize': 12, 'fontweight': 'bold', 'family': font_family}
        
        ax.set_title('LED Spectral Distribution (Rainbow)', **title_font_dict)
        ax.set_xlabel('Wavelength (nm)', **label_font_dict)
        ax.set_ylabel('Radiation Intensity', **label_font_dict)
        print(f"✅ 光谱图标题和标签字体已设置为: {font_family}")
        
        # 显式设置刻度标签的字体
        for label in ax.get_xticklabels():
            label.set_fontfamily(font_family)
            label.set_fontsize(10)
        for label in ax.get_yticklabels():
            label.set_fontfamily(font_family)
            label.set_fontsize(10)
        print("✅ 光谱图刻度标签字体已设置")
        
        # 添加波段标记
        bands = [(400, 500, 'Blue'), (500, 600, 'Green'), (600, 700, 'Red'), (700, 800, 'Far Red')]
        band_colors = ['blue', 'green', 'red', 'maroon']
        
        for i, (start, end, label) in enumerate(bands):
            mask = (wavelengths >= start) & (wavelengths < end)
            if np.any(mask):
                center = (start + end) / 2
                max_y = radiations[mask].max() if len(radiations[mask]) > 0 else radiations.max() * 0.8
                # 添加半透明的波段标记
                ax.axvspan(start, end, alpha=0.1, color=band_colors[i])
                ax.text(center, max_y * 1.1, label, ha='center', va='bottom', 
                       fontsize=11, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor=band_colors[i]))
        
        plt.tight_layout()
        
        # 保存前再次确认字体设置
        print(f"保存光谱图前的字体设置: {plt.rcParams['font.sans-serif']}")
        
        # 保存为字节流 - 添加更多参数确保正确渲染
        img_buffer = io.BytesIO()
        # 为Streamlit Cloud环境添加额外的保存参数
        save_params = {
            'format': 'png',
            'dpi': 200,  # 适当降低dpi以减小文件大小
            'bbox_inches': 'tight',
            'facecolor': 'white',
            'edgecolor': 'none',
            'pad_inches': 0.1,
            'metadata': {'Title': 'LED Spectral Distribution', 
                        'Author': 'LED Plant Light Analysis System',
                        'Creator': 'matplotlib'}
        }
        
        # 在Streamlit环境中添加额外的字体渲染保障
        if 'streamlit' in sys.modules:
            print("🔧 在Streamlit环境中应用增强的保存设置")
            # 尝试使用不同的渲染后端选项
            try:
                import matplotlib.backends.backend_agg as agg
                canvas = agg.FigureCanvasAgg(fig)
                canvas.draw()
                # 保存时强制使用文本模式而非路径模式
                save_params['bbox_inches'] = 'tight'
                save_params['pad_inches'] = 0.2  # 增加边距确保文字完整
            except Exception as e:
                print(f"⚠️ Canvas操作异常: {e}")
        
        plt.savefig(img_buffer, **save_params)
        img_buffer.seek(0)
        chart_images['spectrum'] = img_buffer
        plt.close()
        print("✅ 彩虹光谱分布图生成完成")
        
        # 2. 光质分布饼图
        # 重置matplotlib设置，确保每个图表都有独立的字体环境
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = font_list
        plt.rcParams['axes.unicode_minus'] = False
        
        # 为饼图专门设置字体
        if 'streamlit' in sys.modules:
            print("🔧 为饼图应用Streamlit环境字体设置")
            plt.rcParams['font.sans-serif'] = ['Noto Sans SC'] + [f for f in font_list if f != 'Noto Sans SC']
        
        fig, ax = plt.subplots(figsize=(10, 8))
        percentages = results.get('percentages', {})
        
        # 验证百分比数据
        required_percentages = ['blue_percentage', 'green_percentage', 'red_percentage', 'far_red_percentage']
        missing_data = [key for key in required_percentages if key not in percentages]
        if missing_data:
            print(f"警告：缺少百分比数据 {missing_data}")
        
        labels = ['Blue\n(400-500nm)', 'Green\n(500-600nm)', 'Red\n(600-700nm)', 'Far Red\n(700-800nm)']
        sizes = [
            percentages.get('blue_percentage', 0),
            percentages.get('green_percentage', 0),
            percentages.get('red_percentage', 0),
            percentages.get('far_red_percentage', 0)
        ]
        
        print(f"饼图数据：蓝光{sizes[0]:.1f}%, 绿光{sizes[1]:.1f}%, 红光{sizes[2]:.1f}%, 远红光{sizes[3]:.1f}%")
        
        colors_pie = ['#4285F4', '#34A853', '#EA4335', '#FB04DA']
        
        # 确保font_list存在且不为空，增强Streamlit Cloud支持
        print("🔧 为饼图进行字体环境检查")
        if 'font_list' not in locals() or not font_list:
            # 增强版Streamlit Cloud环境检测
            is_streamlit_cloud = (
                'streamlit' in sys.modules or 
                os.environ.get('STREAMLIT_RUNTIME') == 'true' or 
                os.environ.get('PWD', '').endswith('app') or
                os.environ.get('HOME', '') == '/home/appuser' or
                os.path.exists('/.dockerenv')
            )
            print(f"检测环境: Streamlit Cloud={is_streamlit_cloud}")
            
            if is_streamlit_cloud:
                # Streamlit Cloud优先字体列表 - 增强版
                font_list = ['Noto Sans SC', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback', 'Roboto', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
                print("⚠️ 在Streamlit Cloud环境中重新初始化font_list，优先使用Noto Sans SC")
            else:
                # 标准环境字体列表
                if platform.system() == 'Darwin':
                    font_list = ['STHeiti', 'Arial Unicode MS', 'PingFang SC', 'sans-serif']
                elif platform.system() == 'Windows':
                    font_list = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
                else:
                    font_list = ['WenQuanYi Micro Hei', 'Droid Sans Fallback', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
                print(f"⚠️ 重新初始化font_list: {font_list[:2]}...")
        
        # 智能字体选择：逐个验证字体是否可用
        available_font = font_list[0]
        # 增强版字体验证
        for font_candidate in font_list:
            try:
                print(f"🔍 测试字体: {font_candidate}")
                # 创建一个字体属性对象进行测试
                test_font_prop = plt.font_manager.FontProperties(family=font_candidate)
                # 检查字体是否真的被识别
                if test_font_prop.get_name().lower() != 'sans-serif':
                    available_font = font_candidate
                    print(f"✓ 确认字体 {available_font} 可用")
                    break
            except Exception as e:
                print(f"⚠️ 字体 {font_candidate} 测试失败: {e}")
                continue
        
        # 设置字体
        plt.rcParams['font.sans-serif'] = [available_font] + font_list[1:]
        plt.rcParams['font.family'] = ['sans-serif']
        print(f"✅ 饼图最终字体设置: {plt.rcParams['font.sans-serif'][:3]}...")
        
        # 显式设置字体参数
        plt.rcParams['font.sans-serif'] = [available_font] + font_list[1:]
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['pdf.fonttype'] = 42
        plt.rcParams['ps.fonttype'] = 42
        
        # 为Streamlit Cloud环境添加PDF/PS渲染参数
        if is_streamlit_cloud:
            plt.rcParams['pdf.fonttype'] = 42
            plt.rcParams['ps.fonttype'] = 42
            plt.rcParams['text.antialiased'] = True
            print("✅ 为Streamlit Cloud环境应用增强的字体和渲染设置")
        
        # 显式设置字体，增强多平台兼容性
        font_family = available_font
        print(f"饼图相关设置使用字体: {font_family}")
        
        # 强制设置字体参数，确保在无头环境中也能正常工作
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = [font_family] + font_list[1:]
        print(f"饼图使用字体: {font_family}")
        
        # 为饼图标签创建字体字典
        label_font_dict = {'fontsize': 11, 'fontweight': 'bold', 'family': font_family}
        title_font_dict = {'fontsize': 16, 'fontweight': 'bold', 'family': font_family}
        
        # 使用字体字典
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                                         startangle=90, textprops=label_font_dict)
        
        # 确保饼图标签使用正确字体
        for text in texts:
            text.set_fontweight('bold')
            text.set_fontfamily(font_family)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
            autotext.set_fontfamily(font_family)
            
        # 使用字体字典
        ax.set_title('Light Quality Distribution', pad=20, **title_font_dict)
        print("✅ 饼图标题字体已设置")
        
        plt.tight_layout()
        
        # 保存前再次确认字体设置
        print(f"保存饼图前的字体设置: {plt.rcParams['font.sans-serif']}")
        
        # 保存为字节流
        img_buffer = io.BytesIO()
        
        # 为Streamlit Cloud环境添加额外的保存参数
        save_params = {
            'format': 'png',
            'dpi': 200,
            'bbox_inches': 'tight',
            'facecolor': 'white',
            'edgecolor': 'none',
            'pad_inches': 0.1,
            'metadata': {'Title': 'Light Quality Distribution', 
                        'Author': 'LED Plant Light Analysis System',
                        'Creator': 'matplotlib'}
        }
        
        # 在Streamlit环境中添加额外的字体渲染保障
        if 'streamlit' in sys.modules:
            print("🔧 在Streamlit环境中应用增强的饼图保存设置")
            # 尝试使用不同的渲染后端选项
            try:
                import matplotlib.backends.backend_agg as agg
                canvas = agg.FigureCanvasAgg(fig)
                canvas.draw()
                # 保存时强制使用文本模式而非路径模式
                save_params['bbox_inches'] = 'tight'
                save_params['pad_inches'] = 0.2  # 增加边距确保文字完整
            except Exception as e:
                print(f"⚠️ 饼图Canvas操作异常: {e}")
        
        plt.savefig(img_buffer, **save_params)
        img_buffer.seek(0)
        chart_images['pie'] = img_buffer
        plt.close()
        print("✅ 光质分布饼图生成完成")
        
        # 3. 作物适应性雷达图
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
        
        crop_suitability = results.get('calculations', {}).get('crop_suitability', {})
        categories = list(crop_suitability.keys())
        values = list(crop_suitability.values())
        
        print(f"雷达图数据：{len(categories)} 个作物类型")
        for cat, val in zip(categories, values):
            print(f"  {cat}: {val}分")
        
        # 确保font_list存在且不为空，增强Streamlit Cloud支持
        if 'font_list' not in locals() or not font_list:
            # 增强版Streamlit Cloud环境检测
            is_streamlit_cloud = (
                'streamlit' in sys.modules or 
                os.environ.get('STREAMLIT_RUNTIME') == 'true' or 
                os.environ.get('PWD', '').endswith('app') or
                os.environ.get('HOME', '') == '/home/appuser' or
                os.path.exists('/.dockerenv')
            )
            print(f"检测环境: Streamlit Cloud={is_streamlit_cloud}")
            
            if is_streamlit_cloud:
                # Streamlit Cloud优先字体列表 - 增强版
                font_list = ['Noto Sans SC', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback', 'Roboto', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
                print("⚠️ 在Streamlit Cloud环境中重新初始化font_list，优先使用Noto Sans SC")
            else:
                # 标准环境字体列表
                if platform.system() == 'Darwin':
                    font_list = ['STHeiti', 'Arial Unicode MS', 'PingFang SC', 'sans-serif']
                elif platform.system() == 'Windows':
                    font_list = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
                else:
                    font_list = ['WenQuanYi Micro Hei', 'Droid Sans Fallback', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
                print(f"⚠️ 重新初始化font_list: {font_list[:2]}...")
        
        # 智能字体选择：逐个验证字体是否可用
        available_font = font_list[0]
        try:
            test_font = available_font
            plt.rcParams['font.sans-serif'] = [test_font]
            plt.rcParams['font.family'] = ['sans-serif']
            # 测试字体是否真的生效
            test_fig, test_ax = plt.subplots(figsize=(1, 1))
            test_ax.text(0.5, 0.5, '测试字体', fontsize=10)
            plt.close(test_fig)
            print(f"✓ 确认字体 {test_font} 可用")
        except Exception as e:
            print(f"⚠️ 字体 {available_font} 不可用: {e}")
            # 尝试下一个字体
            if len(font_list) > 1:
                available_font = font_list[1]
                print(f"尝试使用备用字体: {available_font}")
        
        # 显式设置字体参数
        plt.rcParams['font.sans-serif'] = font_list
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 为Streamlit Cloud环境添加PDF/PS渲染参数
        if is_streamlit_cloud:
            plt.rcParams['pdf.fonttype'] = 42
            plt.rcParams['ps.fonttype'] = 42
            plt.rcParams['text.antialiased'] = True
            print("✅ 为Streamlit Cloud环境应用增强的字体和渲染设置")
        
        # 显式设置雷达图字体，增强多平台兼容性
        font_family = available_font
        print(f"雷达图使用字体: {font_family}")
        
        # 强制设置字体参数，确保在无头环境中也能正常工作
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = [font_family] + font_list[1:]
        
        if categories and values:
            # 闭合雷达图
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            values += values[:1]  # 闭合
            angles += angles[:1]  # 闭合
            
            ax.plot(angles, values, 'o-', linewidth=3, color='#4285F4', markersize=8)
            ax.fill(angles, values, alpha=0.25, color='#4285F4')
            ax.set_xticks(angles[:-1])
            # 明确设置字体，增加额外的字体回退机制
            try:
                ax.set_xticklabels(categories, fontsize=12, fontweight='bold', fontfamily=font_family)
            except:
                # 如果第一个字体失败，尝试使用回退字体
                for fallback_font in font_list[1:]:
                    try:
                        ax.set_xticklabels(categories, fontsize=12, fontweight='bold', fontfamily=fallback_font)
                        print(f"⚠️ 切换到回退字体: {fallback_font}")
                        break
                    except:
                        continue
            ax.set_ylim(0, 100)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10, fontweight='bold', fontfamily=font_family)
            ax.set_title('Crop Adaptability Evaluation', fontsize=16, fontweight='bold', pad=30, fontfamily=font_family)
            ax.grid(True, alpha=0.6)
            
            # 设置网格线样式
            ax.grid(True, linestyle='--', alpha=0.7)
        else:
            ax.text(0.5, 0.5, 'No Crop Adaptability Data', transform=ax.transAxes, 
                   ha='center', va='center', fontsize=14, fontfamily=font_family)
        
        plt.tight_layout()
        
        # 保存前再次确认字体设置
        print(f"保存雷达图前的字体设置: {plt.rcParams['font.sans-serif']}")
        
        # 保存为字节流
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, 
                   format='png', 
                   dpi=200,  # 适当降低dpi以减小文件大小
                   bbox_inches='tight',
                   facecolor='white', 
                   edgecolor='none',
                   pad_inches=0.1,
                   metadata={'Title': '作物适应性评价', 
                            'Author': 'LED植物灯光效分析系统',
                            'Creator': 'matplotlib'})
        img_buffer.seek(0)
        chart_images['radar'] = img_buffer
        plt.close()
        print("✅ 作物适应性雷达图生成完成")
        
        print(f"\n🎯 所有图表生成完成，共生成 {len(chart_images)} 个图表文件")
        
    except Exception as e:
        st.error(f"生成图表时出错: {str(e)}")
        # 如果生成图表失败，返回空字典
        chart_images = {}
        
        # 尝试清理可能存在的图形对象
        try:
            import matplotlib.pyplot as plt
            plt.close('all')  # 关闭所有可能打开的图形
        except:
            pass
    
    return chart_images

def generate_pdf_report(results, df_clean):
    """生成PDF格式的分析报告"""
    
    # 验证输入数据的完整性
    if not results or not isinstance(results, dict):
        raise ValueError("分析结果数据不完整，无法生成PDF报告")
    
    if df_clean is None or df_clean.empty:
        raise ValueError("光谱数据不完整，无法生成PDF报告")
    
    # 验证核心数据是否存在
    calculations = results.get('calculations', {})
    percentages = results.get('percentages', {})
    basic_info = results.get('basic_info', {})
    input_params = results.get('input_params', {})
    
    if not calculations:
        raise ValueError("计算结果为空，无法生成PDF报告")
    
    print(f"PDF报告数据验证通过：")
    print(f"- 计算结果项目数: {len(calculations)}")
    print(f"- 百分比数据项目数: {len(percentages)}")
    print(f"- 光谱数据行数: {len(df_clean)}")
    
    # 创建字节流
    buffer = io.BytesIO()
    
    # 创建PDF文档
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # 获取样式
    styles = getSampleStyleSheet()
    
    # 设置适合英文显示的字体
    pdf_font = 'Helvetica'  # 默认字体，适合英文
    try:
        import platform
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import reportlab.lib.fonts
        import os
        import sys
        
        # 检测是否在Streamlit Cloud环境
        is_streamlit_cloud = False
        if 'streamlit' in sys.modules:
            is_streamlit_cloud = True
            print("🌐 检测到Streamlit模块")
        if os.environ.get('STREAMLIT_RUNTIME') == 'true':
            is_streamlit_cloud = True
            print("🌐 检测到STREAMLIT_RUNTIME环境变量")
        
        print(f"📊 英文报告字体设置中...")
        
        # 优先使用标准英文字体或通用字体
        # 尝试加载NotoSans字体（通用且支持多种语言）
        font_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
        noto_font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')
        
        if os.path.exists(noto_font_path):
            try:
                # 注册NotoSans字体
                pdfmetrics.registerFont(TTFont('NotoSans', noto_font_path))
                pdf_font = 'NotoSans'
                print(f"✅ 成功注册本地NotoSans字体: {noto_font_path}")
            except Exception as e:
                print(f"⚠️ 注册NotoSans字体失败: {str(e)}")
        else:
            # 尝试系统中的标准英文字体
            system = platform.system()
            print(f"🔍 系统: {system}，尝试加载系统英文字体")
            
            # 根据系统设置可能的英文字体路径
            font_paths = []
            
            if is_streamlit_cloud:
                print(f"🔍 Streamlit Cloud环境: 尝试加载DejaVu Sans")
                font_paths = [
                    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVuSans'),
                    ('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 'NotoSans')
                ]
            elif system == "Windows":
                font_paths = [
                    ('C:/Windows/Fonts/arial.ttf', 'Arial'),
                    ('C:/Windows/Fonts/segoeui.ttf', 'SegoeUI')
                ]
            elif system == "Darwin":
                font_paths = [
                    ('/System/Library/Fonts/Helvetica.ttc', 'Helvetica'),
                    ('/System/Library/Fonts/SFPro.ttf', 'SFPro')
                ]
            else:  # Linux
                font_paths = [
                    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVuSans'),
                    ('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 'NotoSans')
                ]
            
            # 尝试加载系统字体
            for font_path, font_alias in font_paths:
                if os.path.exists(font_path):
                    try:
                        if font_path.endswith('.ttf'):
                            pdfmetrics.registerFont(TTFont(font_alias, font_path))
                        else:  # .ttc files
                            pdfmetrics.registerFont(TTFont(font_alias, font_path, subfontIndex=0))
                        
                        pdf_font = font_alias
                        print(f"✅ 成功注册系统字体: {font_alias}")
                        break
                    except Exception as e:
                        print(f"⚠️ 注册字体 {font_alias} 失败: {str(e)}")
                        continue
            
    except Exception as e:
        print(f"⚠️ 字体注册过程中发生异常: {str(e)}")
        print("📋 将使用默认字体Helvetica")
    
    print(f"📋 最终使用字体: {pdf_font}")
    
    # 为Streamlit Cloud环境添加额外的字体安全保障
    if is_streamlit_cloud:
        print("✅ 在Streamlit Cloud环境中应用增强的PDF渲染设置")
        # 确保使用可靠的字体
        print(f"📋 使用字体: {pdf_font}")
    
    # 使用pdf_font变量而不是chinese_font
    chinese_font = pdf_font  # 保持与后续代码的兼容性
    print(f"📋 PDF报告字体已设置为: {chinese_font}")
    
    # 创建自定义样式（英文优先）
    # 确保使用标准英文字体
    # 对于英文文本，移除CJK换行参数
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # 居中
        textColor=colors.darkblue,
        fontName=chinese_font
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue,
        fontName=chinese_font
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.darkgreen,
        fontName=chinese_font
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName=chinese_font,
        encoding='UTF-8'
    )
    
    # 添加表格文本专用样式
    table_style = ParagraphStyle(
        'CustomTable',
        parent=styles['Normal'],
        fontSize=9,
        fontName=chinese_font,
        encoding='UTF-8'
    )
    
    print("📝 PDF样式创建完成，所有样式已应用中文字体设置")
    
    # 内容列表
    story = []
    
    # 标题
    title = Paragraph("LED植物照明光学度量体系分析报告", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # 报告生成时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_para = Paragraph(f"报告生成时间：{current_time}", normal_style)
    story.append(time_para)
    story.append(Spacer(1, 20))
    
    # 基本信息
    story.append(Paragraph("测试基本信息", heading_style))
    
    basic_info = results.get('basic_info', {})
    input_params = results.get('input_params', {})
    
    basic_data = [
        ['项目', '数值'],
        ['灯具型号', basic_info.get('lamp_model', '未填写')],
        ['制造商/单位', basic_info.get('manufacturer', '未填写')],
        ['测试日期', basic_info.get('test_date', '未填写')],
        ['总辐射通量', f"{input_params.get('total_radiation_flux', 0):.1f} W"],
        ['总功率', f"{input_params.get('total_power', 0):.1f} W"],
        ['后面板温度', f"{input_params.get('back_panel_temp', 0):.1f} ℃"],
        ['功率因数', f"{input_params.get('power_factor', 0):.3f}"]
    ]
    
    basic_table = Table(basic_data, colWidths=[2*inch, 3*inch])
    basic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),  # 使用中文字体
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(basic_table)
    story.append(Spacer(1, 20))
    
    # 综合评价
    story.append(Paragraph("综合评价", heading_style))
    
    calculations = results.get('calculations', {})
    
    # 综合评价表格
    eval_data = [
        ['评价项目', '数值', '等级'],
        ['总体评级', f"{calculations.get('quality_rating', '未知')}", ''],
        ['PPE (光合光子效率)', f"{calculations.get('ppe', 0):.3f} μmol/J", 
         "优秀" if calculations.get('ppe', 0) > 2.5 else "良好" if calculations.get('ppe', 0) > 2.0 else "一般"],
        ['PAR占比', f"{calculations.get('par_ratio', 0)*100:.1f}%", 
         "优秀" if calculations.get('par_ratio', 0) > 0.8 else "良好" if calculations.get('par_ratio', 0) > 0.6 else "一般"],
        ['R/B比', f"{calculations.get('r_b_ratio', 0):.2f}", 
         "适宜" if 0.5 <= calculations.get('r_b_ratio', 0) <= 3.0 else "偏离"],
        ['光能比', f"{calculations.get('light_energy_ratio', 0):.3f}", 
         "高效" if calculations.get('light_energy_ratio', 0) > 0.5 else "中等" if calculations.get('light_energy_ratio', 0) > 0.3 else "低效"]
    ]
    
    eval_table = Table(eval_data, colWidths=[2*inch, 2*inch, 1.5*inch])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(eval_table)
    story.append(Spacer(1, 20))
    
    # 核心性能指标
    story.append(Paragraph("核心性能指标", heading_style))
    
    performance_data = [
        ['指标', '数值', '单位', '说明'],
        ['总光子通量', f"{calculations.get('total_photon_flux', 0):.2f}", 'μmol/s', '总辐射通量×光能比'],
        ['PAR功率', f"{calculations.get('par_power', 0):.2f}", 'W', 'PAR波段(400-700nm)功率'],
        ['光效', f"{calculations.get('luminous_efficacy', 0):.3f}", 'W/W', '辐射光效'],
        ['估算PPFD', f"{calculations.get('ppfd_estimated', 0):.0f}", 'μmol/m²/s', '假设1m²面积的光强'],
        ['光能利用效率', f"{calculations.get('light_energy_efficiency', 0)*100:.1f}", '%', 'PAR功率占总功率比例'],
        ['热损失率', f"{calculations.get('heat_loss_rate', 0)*100:.1f}", '%', '转化为热量的功率比例'],
        ['年度电费', f"{calculations.get('annual_electricity_cost', 0):.0f}", '元', '按12小时/天运行估算']
    ]
    
    performance_table = Table(performance_data, colWidths=[1.5*inch, 1.2*inch, 0.8*inch, 2*inch])
    performance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(performance_table)
    story.append(PageBreak())
    
    # 生成图表
    chart_images = generate_chart_images(results, df_clean)
    
    # 添加光谱分布图（修复长宽比）
    if 'spectrum' in chart_images:
        story.append(Paragraph("光谱分布分析", heading_style))
        chart_images['spectrum'].seek(0)
        
        # 获取图片实际尺寸并保持长宽比
        try:
            from PIL import Image as PILImage
            pil_img = PILImage.open(chart_images['spectrum'])
            original_width, original_height = pil_img.size
            
            # 设置最大宽度为6英寸，按比例计算高度
            max_width = 6 * inch
            aspect_ratio = original_height / original_width
            img_height = max_width * aspect_ratio
            
            # 如果高度过大，限制高度并重新计算宽度
            max_height = 4 * inch
            if img_height > max_height:
                img_height = max_height
                img_width = img_height / aspect_ratio
            else:
                img_width = max_width
            
            # 重置流位置
            chart_images['spectrum'].seek(0)
            img = Image(chart_images['spectrum'], width=img_width, height=img_height)
            story.append(img)
            story.append(Spacer(1, 20))
            
        except ImportError:
            # 如果PIL不可用，使用默认尺寸
            chart_images['spectrum'].seek(0)
            img = Image(chart_images['spectrum'], width=6*inch, height=3*inch)
            story.append(img)
            story.append(Spacer(1, 20))
        except Exception as e:
            story.append(Paragraph(f"Spectrum chart loading failed: {str(e)}", normal_style))
            story.append(Spacer(1, 20))
    
    # Spectrum distribution data table
    story.append(Paragraph("Spectral Distribution Data", subheading_style))
    
    percentages = results.get('percentages', {})
    spectrum_data = [
        ['Spectral Band', 'Wavelength Range', 'Integration Value', 'Percentage', 'Characteristics'],
        ['Blue Light', '400-500 nm', f"{calculations.get('blue_integration', 0):.2f}", 
         f"{percentages.get('blue_percentage', 0):.1f}%", 'Promotes chlorophyll synthesis'],
        ['Green Light', '500-600 nm', f"{calculations.get('green_integration', 0):.2f}", 
         f"{percentages.get('green_percentage', 0):.1f}%", 'Lower photosynthetic efficiency'],
        ['Red Light', '600-700 nm', f"{calculations.get('red_integration', 0):.2f}", 
         f"{percentages.get('red_percentage', 0):.1f}%", 'Promotes flowering and fruiting'],
        ['Far Red Light', '700-800 nm', f"{calculations.get('far_red_integration', 0):.2f}", 
         f"{percentages.get('far_red_percentage', 0):.1f}%", 'Regulates stem elongation']
    ]
    
    spectrum_table = Table(spectrum_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1*inch, 1.4*inch])
    spectrum_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(spectrum_table)
    story.append(Spacer(1, 20))
    
    # 添加光质分布饼图（修复长宽比）
    if 'pie' in chart_images:
        story.append(Paragraph("Light Quality Distribution", subheading_style))
        chart_images['pie'].seek(0)
        
        # 获取饼图实际尺寸并保持长宽比
        try:
            from PIL import Image as PILImage
            pil_img = PILImage.open(chart_images['pie'])
            original_width, original_height = pil_img.size
            
            # 饼图通常是正方形，设置合适的尺寸
            img_size = 4 * inch
            aspect_ratio = original_height / original_width
            
            if aspect_ratio > 1:  # 高度大于宽度
                img_height = img_size
                img_width = img_size / aspect_ratio
            else:  # 宽度大于等于高度
                img_width = img_size
                img_height = img_size * aspect_ratio
            
            # 重置流位置
            chart_images['pie'].seek(0)
            img = Image(chart_images['pie'], width=img_width, height=img_height)
            story.append(img)
            story.append(Spacer(1, 20))
            
        except ImportError:
            # 如果PIL不可用，使用默认尺寸
            chart_images['pie'].seek(0)
            img = Image(chart_images['pie'], width=4*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 20))
        except Exception as e:
            story.append(Paragraph(f"Pie chart loading failed: {str(e)}", normal_style))
            story.append(Spacer(1, 20))
    
    # Plant physiological response indicators
    story.append(Paragraph("Plant Physiological Response Indicators", heading_style))
    
    physio_data = [
        ['Indicator', 'Value', 'Mechanism', 'Effect'],
        ['Cryptochrome Activity', f"{calculations.get('crypto_activity', 0):.3f}", 'Senses blue light and UV-A', 'Regulates phototropism and circadian clock'],
        ['Phytochrome Activity', f"{calculations.get('phyto_activity', 0):.3f}", 'Senses red/far-red light', 'Regulates photoperiodic responses'],
        ['Anthocyanin Synthesis Index', f"{calculations.get('anthocyanin_index', 0):.3f}", 'Induced by purple and blue light', 'Enhances stress resistance and coloring'],
        ['Chlorophyll Synthesis Index', f"{calculations.get('chlorophyll_synthesis', 0):.3f}", 'Synergistic effect of red and blue light', 'Promotes photosynthetic pigment formation']
    ]
    
    physio_table = Table(physio_data, colWidths=[1.5*inch, 1*inch, 1.8*inch, 1.7*inch])
    physio_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(physio_table)
    story.append(PageBreak())
    
    # 添加作物适应性雷达图（修复长宽比）
    if 'radar' in chart_images:
        story.append(Paragraph("Crop Adaptability Evaluation", heading_style))
        chart_images['radar'].seek(0)
        
        # 雷达图通常也接近正方形
        try:
            from PIL import Image as PILImage
            pil_img = PILImage.open(chart_images['radar'])
            original_width, original_height = pil_img.size
            
            img_size = 4.5 * inch
            aspect_ratio = original_height / original_width
            
            if aspect_ratio > 1:
                img_height = img_size
                img_width = img_size / aspect_ratio
            else:
                img_width = img_size
                img_height = img_size * aspect_ratio
            
            # 重置流位置
            chart_images['radar'].seek(0)
            img = Image(chart_images['radar'], width=img_width, height=img_height)
            story.append(img)
            story.append(Spacer(1, 20))
            
        except ImportError:
            # 如果PIL不可用，使用默认尺寸
            chart_images['radar'].seek(0)
            img = Image(chart_images['radar'], width=4.5*inch, height=4.5*inch)
            story.append(img)
            story.append(Spacer(1, 20))
        except Exception as e:
            story.append(Paragraph(f"Radar chart loading failed: {str(e)}", normal_style))
            story.append(Spacer(1, 20))
    
    # Crop adaptability data table
    crop_suitability = calculations.get('crop_suitability', {})
    crop_data = [['Crop Type', 'Adaptability Score', 'Evaluation Level', 'Recommended Applications']]
    
    crop_recommendations = {
        'Leafy Vegetables': 'Lettuce, Spinach, Bok choy, Celery',
        'Fruiting Vegetables': 'Tomato, Cucumber, Pepper, Eggplant',
        'Seedling Growth': 'Various vegetable seedlings, Flower seedlings'
    }
    
    for crop_type, score in crop_suitability.items():
        # Convert Chinese crop types to English for consistency
        en_crop_type = {'叶菜类': 'Leafy Vegetables', '果菜类': 'Fruiting Vegetables', '育苗专用': 'Seedling Growth'}.get(crop_type, crop_type)
        
        if score >= 80:
            level = "Excellent"
        elif score >= 60:
            level = "Good"
        else:
            level = "Fair"
        recommendation = crop_recommendations.get(en_crop_type, 'General')
        crop_data.append([en_crop_type, f"{score}", level, recommendation])
    
    crop_table = Table(crop_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 2.3*inch])
    crop_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(crop_table)
    story.append(Spacer(1, 20))
    
    # Growth stage adaptability
    story.append(Paragraph("Growth Stage Adaptability Analysis", heading_style))
    
    growth_stages = calculations.get('growth_stage_suitability', {})
    if growth_stages:
        growth_data = [['Growth Stage', 'Adaptability Score', 'Spectral Requirements']]
        
        stage_requirements = {
            'Germination': 'Moderate blue and red light, promotes germination',
            'Seedling': 'High blue light ratio, controls excessive growth',
            'Vegetative Growth': 'Balanced red and blue light, promotes leaf development',
            'Flowering': 'High red light ratio, promotes flower bud differentiation',
            'Fruiting': 'Balanced spectrum, high light intensity requirement'
        }
        
        for stage, score in growth_stages.items():
            # Convert Chinese growth stages to English
            en_stage = {'发芽期': 'Germination', '苗期': 'Seedling', '营养生长期': 'Vegetative Growth', 
                       '开花期': 'Flowering', '结果期': 'Fruiting'}.get(stage, stage)
            requirement = stage_requirements.get(en_stage, 'Balanced spectrum')
            growth_data.append([en_stage, f"{score}", requirement])
        
        growth_table = Table(growth_data, colWidths=[1.5*inch, 1.5*inch, 3*inch])
        growth_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), chinese_font),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(growth_table)
        story.append(Spacer(1, 20))
    
    # Optimization suggestions
    story.append(Paragraph("Spectral Optimization Suggestions", heading_style))
    
    suggestions = calculations.get('optimization_suggestions', [])
    # Convert Chinese suggestions to English or use directly if already in English
    en_suggestions = []
    for suggestion in suggestions:
        if "较为合理" in suggestion:
            en_suggestions.append("The spectrum is relatively reasonable")
        else:
            # Keep the original suggestion for now - in a real scenario we would translate all suggestions
            en_suggestions.append(suggestion)
    
    if len(en_suggestions) == 1 and "relatively reasonable" in en_suggestions[0]:
        suggestion_text = f"✓ {en_suggestions[0]}"
    else:
        suggestion_text = "The following optimization items were detected:<br/>"
        for i, suggestion in enumerate(en_suggestions, 1):
            suggestion_text += f"{i}. {suggestion}<br/>"
    
    story.append(Paragraph(suggestion_text, normal_style))
    story.append(Spacer(1, 20))
    
    # Detailed calculation data
    story.append(Paragraph("Detailed Calculation Data", heading_style))
    
    calculation_data = [
        ['Calculation Item', 'Value', 'Formula/Explanation'],
        ['Photosynthetic Active Integration', f"{calculations.get('photosynthetic_active', 0):.2f}", 'Σ(λ×radiation)/119.8'],
        ['Total Integration', f"{calculations.get('total_integration', 0):.2f}", 'Σradiation values'],
        ['PAR Integration', f"{calculations.get('par_integration', 0):.2f}", 'Sum of radiation values 400-700nm'],
        ['R/Fr Ratio', f"{calculations.get('r_fr_ratio', 0):.2f}", 'Red light integration/Far red light integration'],
        ['UV-A/B Ratio', f"{calculations.get('uva_b_ratio', 0):.3f}", 'UV-A integration/Blue light integration'],
        ['DLI', f"{calculations.get('dli', 0):.2f}", 'Total photon flux×12×3600/1000000 mol/m²/d']
    ]
    
    calc_table = Table(calculation_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
    calc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(calc_table)
    story.append(Spacer(1, 20))
    
    # Analysis method description
    story.append(Paragraph("Analysis Method Description", heading_style))
    
    method_text = """
    Core Calculation Formulas:<br/>
    • Light Energy Ratio = Photosynthetic Active Integration ÷ Total Integration<br/>
    • Total Photon Flux = Total Radiation Flux × Light Energy Ratio (μmol/s)<br/>
    • PPE = Total Photon Flux ÷ Total Power (μmol/J)<br/>
    • Integration Value = (λ × Radiation) ÷ 119.8 (Photon energy conversion constant)<br/>
    <br/>
    Evaluation Standards:<br/>
    • PPE Grade: Excellent(>2.5), Good(2.0-2.5), Fair(<2.0) μmol/J<br/>
    • PAR Percentage Grade: Excellent(>80%), Good(60-80%), Fair(<60%)<br/>
    • R/B Ratio Range: Leafy vegetables(0.5-1.5), Fruiting vegetables(1.0-3.0)<br/>
    • Light Energy Ratio: High efficiency(>0.5), Medium(0.3-0.5), Low efficiency(<0.3)<br/>
    <br/>
    Technical Features:<br/>
    This analysis is based on four optical measurement systems: Radiometry, Photometry, Photonmetry, and Plant Photonmetry.<br/>
    Combined with McCree (1972) plant photosynthetic sensitivity curve, it provides scientifically accurate LED plant lighting evaluation.
    """
    
    story.append(Paragraph(method_text, normal_style))
    story.append(Spacer(1, 30))
    
    # Report signature
    footer_text = f"""
    ————————————————————————————————————————————————————————————<br/>
    LED Plant Lighting Optical Measurement System Analysis<br/>
    Report Generated Time: {current_time}<br/>
    Technical Support: Professional analysis tool based on scientific photometry theory<br/>
    ————————————————————————————————————————————————————————————
    """
    
    story.append(Paragraph(footer_text, normal_style))
    
    # 生成PDF
    doc.build(story)
    
    # 获取PDF数据
    buffer.seek(0)
    pdf_data = buffer.read()
    buffer.close()
    
    return pdf_data

def create_downloadable_report(results, df_clean, filename="LED_Plant_Analysis_Report"):
    """创建可下载的报告文件"""
    if PDF_AVAILABLE:
        # 生成PDF报告
        return generate_pdf_report(results, df_clean), "application/pdf", filename + ".pdf"
    else:
        # 生成简化的HTML报告
        return generate_simplified_report(results, df_clean), "text/html", filename + ".html"

def main():
    # 设置页面配置
    st.set_page_config(
        page_title="LED植物照明光学度量体系分析",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 添加自定义CSS样式
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .theory-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 主标题
    st.markdown('<h1 class="main-header">🌱 LED植物照明光学度量体系分析系统</h1>', unsafe_allow_html=True)
    
    # 侧边栏 - 使用说明（移到最上面）
    with st.sidebar:
        st.header("📖 使用说明")
        
        with st.expander("💡 快速开始", expanded=True):
            st.markdown("""
            **第一步：准备数据**
            - 准备LED光谱测试数据文件（CSV/Excel格式）
            - 确保文件包含波长(nm)和辐射强度两列数据
            - 推荐波长范围：380-800nm
            
            **第二步：输入参数**
            - 输入测试灯具的总辐射通量(W)
            - 输入测试灯具的总功率(W)
            - 输入后面板温度(℃)和功率因数
            
            **第三步：上传文件**
            - 点击文件上传按钮选择光谱数据文件
            - 系统会自动检查和清洗数据
            - 查看数据预览确认格式正确
            
            **第四步：查看结果**
            - 系统自动计算各项光学指标
            - 查看综合评价和性能指标
            - 参考优化建议改进光谱配置
            """)
        
        with st.expander("📊 核心指标说明", expanded=False):
            st.markdown("""
            **PPE (光合光子效率)**
            - 单位：μmol/J
            - 计算：总光子通量 ÷ 总功率
            - 评价标准：>2.5优秀，2.0-2.5良好，<2.0一般
            
            **PAR占比**
            - 光合有效辐射(400-700nm)占总辐射的比例
            - 评价标准：>80%优秀，60-80%良好，<60%一般
            
            **R/B比 (红蓝比)**
            - 红光(600-700nm)与蓝光(400-500nm)的比值
            - 叶菜类适宜范围：0.5-1.5
            - 果菜类适宜范围：1.0-3.0
            
            **光能比**
            - 光合有效积分与总积分的比值
            - 反映光谱的光合有效性
            """)
        
        with st.expander("🎯 应用场景", expanded=False):
            st.markdown("""
            **🥬 叶菜类栽培**
            - 重点关注：高蓝光比例、适中红蓝比
            - 推荐配置：蓝光>20%，R/B=0.5-1.5
            
            **🍅 果菜类栽培**
            - 重点关注：高红光比例、适量远红光
            - 推荐配置：红光>35%，R/B=1.0-3.0
            
            **🌱 育苗专用**
            - 重点关注：高蓝光、适量UV-A
            - 推荐配置：蓝光>25%，R/B=0.3-1.0
            """)
        
        with st.expander("⚠️ 常见问题", expanded=False):
            st.markdown("""
            **数据格式错误**
            - 检查文件是否为CSV或Excel格式
            - 确保第1列为波长，第2列为辐射强度
            - 删除表头和空行，确保数据从第1行开始
            
            **计算结果异常**
            - 检查辐射通量和功率输入是否合理
            - 确认光谱数据波长范围包含400-700nm
            - 验证辐射强度数值为正数
            
            **光谱优化建议**
            - PPE过低：增加光合有效光子输出比例
            - PAR占比低：提高400-700nm波段比例
            - 红蓝比不当：调整LED芯片配比
            """)
        
        st.header("📚 理论基础")
        
        with st.expander("🔬 四种光学度量体系", expanded=False):
            st.markdown("""
            **1. 辐射度学 (Radiometry)**
            - 辐射通量 Φₑ (W)
            - 辐照度 Eₑ (W/m²)
            
            **2. 光度学 (Photometry)**  
            - 光通量 Φ (lm)
            - 照度 E (lx)
            - 基于人眼视见函数 V(λ)
            
            **3. 光子度量学 (Photon Metrics)**
            - 光子通量 Φₚ (μmol/s)
            - 光子通量密度 Eₚ (μmol/m²/s)
            - PPF/PPFD (400-700nm)
            
            **4. 植物光子度量学 (Plant Photon Metrics)**
            - 植物光子通量 Φₚₚ (μmol/s)
            - 基于植物光合敏感曲线 P(λ)
            """)
        
        with st.expander("📐 核心公式"):
            st.markdown("""
            **光子能量转换常数**
            ```
            γ = NAhc = 119.8 W·s·nm·μmol⁻¹
            ```
            
            **新的核心计算公式**
            ```
            光能比 = 光合有效积分 ÷ 总积分
            总光子通量 = 总辐射通量 × 光能比 (μmol/s)
            PPE = 总光子通量 ÷ 总功率 (μmol/J)
            ```
            
            **积分计算公式**
            ```
            积分值 = (λ × 辐射) ÷ 119.8
            光合有效积分 = Σ积分值
            总积分 = Σ辐射值
            ```
            """)
        
        with st.expander("🎯 评价标准"):
            st.markdown("""
            **PPE等级 (新标准)**
            - 优秀: > 2.5 μmol/J
            - 良好: 2.0-2.5 μmol/J  
            - 一般: < 2.0 μmol/J
            
            **PAR占比等级**
            - 优秀: > 80%
            - 良好: 60-80%
            - 一般: < 60%
            
            **R/B比值范围**
            - 叶菜类: 0.5-1.5
            - 果菜类: 1.0-3.0
            
            **光能比**
            - 高效: > 0.5
            - 中等: 0.3-0.5
            - 低效: < 0.3
            """)
    
    st.markdown("---")
    
    # 输入参数部分
    st.header("1. 输入测试参数")
    
    # 灯具基本信息
    st.subheader("📋 灯具基本信息")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        lamp_model = st.text_input(
            "灯具型号", 
            value="",
            placeholder="例如：LED-PL-600W-V2.0",
            help="输入待分析灯具的型号名称"
        )
    
    with col2:
        manufacturer = st.text_input(
            "制造商/单位", 
            value="",
            placeholder="例如：某某科技有限公司",
            help="输入灯具制造商或测试单位名称"
        )
    
    with col3:
        test_date = st.date_input(
            "测试日期",
            help="选择测试日期"
        )
    
    st.subheader("⚡ 电气参数")
    col1, col2 = st.columns(2)
    
    with col1:
        total_radiation_flux = st.number_input(
            "测试灯具的总辐射通量 (W)", 
            min_value=0.0, 
            value=100.0,
            step=1.0,
            help="输入LED灯具的总辐射通量，单位为瓦特(W)"
        )
        
        back_panel_temp = st.number_input(
            "测试灯具后面板的温度 (℃)", 
            min_value=-50.0, 
            max_value=200.0,
            value=25.0,
            step=0.1,
            help="输入LED灯具后面板的温度，单位为摄氏度(℃)"
        )
    
    with col2:
        total_power = st.number_input(
            "测试灯具的总功率 (W)", 
            min_value=0.0, 
            value=150.0,
            step=1.0,
            help="输入LED灯具的总功率，单位为瓦特(W)"
        )
        
        power_factor = st.number_input(
            "功率因数", 
            min_value=0.0, 
            max_value=1.0,
            value=0.9,
            step=0.01,
            help="输入功率因数，数值范围为0-1"
        )
    
    st.markdown("---")
    
    # 文件上传部分
    st.header("2. 上传光谱数据文件")
    
    # 添加数据格式说明
    with st.expander("📝 数据格式要求和示例", expanded=False):
        st.markdown("""
        **📋 文件格式要求：**
        - 支持文件类型：CSV、TXT、Excel (.xlsx, .xls)
        - 至少包含两列数据：第1列为波长，第2列为辐射值
        - 数据必须为数值型，不能包含文字或空值
        - 波长单位：纳米 (nm)
        - 建议波长范围：200-1000nm，重点关注400-700nm PAR波段
        
        **✅ 正确格式示例：**
        """)
        
        example_data = pd.DataFrame({
            '波长(nm)': [400, 410, 420, 430, 440, 450],
            '辐射强度': [0.12, 0.18, 0.25, 0.31, 0.28, 0.22]
        })
        st.dataframe(example_data, use_container_width=True)
        
        # 提供示例文件下载
        st.markdown("**📥 下载示例文件：**")
        
        # 创建更完整的示例数据
        sample_wavelengths = np.arange(380, 781, 5)  # 380-780nm，每5nm一个点
        sample_radiations = []
        
        for wl in sample_wavelengths:
            # 模拟一个典型的LED光谱（蓝红双峰）
            blue_peak = np.exp(-0.5 * ((wl - 450) / 25) ** 2) * 0.8
            red_peak = np.exp(-0.5 * ((wl - 660) / 30) ** 2) * 1.0
            green_component = np.exp(-0.5 * ((wl - 520) / 40) ** 2) * 0.2
            radiation = blue_peak + red_peak + green_component + np.random.normal(0, 0.02)
            sample_radiations.append(max(0, radiation))  # 确保非负值
        
        sample_df = pd.DataFrame({
            '波长(nm)': sample_wavelengths,
            '辐射强度': sample_radiations
        })
        
        # 转换为CSV格式供下载
        csv_data = sample_df.to_csv(index=False)
        
        st.download_button(
            label="📥 下载CSV示例文件",
            data=csv_data,
            file_name="LED光谱数据示例.csv",
            mime="text/csv",
            help="下载这个示例文件，了解正确的数据格式"
        )
        
        st.markdown("""
        **❌ 常见错误：**
        - 包含表头但数据格式不正确
        - 第1行为文字说明而非数据
        - 数据中包含空白行
        - 波长或辐射值包含非数值字符
        - 使用逗号作为小数分隔符（应使用点号）
        
        **💡 数据准备建议：**
        - 确保数据从第1行开始，无额外表头
        - 删除所有空行和无效数据行
        - 波长数据按升序排列
        - 辐射值应大于等于0
        """)
    
    uploaded_file = st.file_uploader(
        "选择光谱数据文件 (CSV/TXT/Excel)", 
        type=['csv', 'txt', 'xlsx', 'xls'],
        help="请确保文件格式符合上述要求"
    )
    
    if uploaded_file is not None:
        # 读取数据
        try:
            if uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            
            # 确保数据有正确的列名
            if df.shape[1] >= 2:
                df.columns = ['wavelength', 'radiation'] + list(df.columns[2:])
                
                st.success(f"成功读取数据文件，共 {len(df)} 行数据")
                st.subheader("数据预览")
                st.dataframe(df.head(10))
                
                # 进行计算
                results, df_clean = calculate_light_analysis(
                    df, total_radiation_flux, total_power, back_panel_temp, power_factor,
                    lamp_model, manufacturer, test_date
                )
                
                # 检查计算结果是否有效
                if results is not None and df_clean is not None:
                    # 显示结果
                    display_results(results, df_clean)
                else:
                    st.warning("无法完成分析，请检查数据文件格式和内容")
                
            else:
                st.error("数据文件格式不正确，请确保文件至少包含两列数据")
                
        except Exception as e:
            st.error(f"读取文件时发生错误: {str(e)}")
    else:
        st.info("请上传包含波长和辐射数据的文件")

def calculate_light_analysis(df, total_radiation_flux, total_power, back_panel_temp, power_factor, lamp_model, manufacturer, test_date):
    """计算光效分析结果"""
    
    # 显示原始数据信息
    st.info(f"📊 原始数据信息：共 {len(df)} 行，{df.shape[1]} 列")
    
    # 检查列名
    if df.shape[1] < 2:
        st.error("❌ 数据文件至少需要包含两列数据（波长和辐射值）")
        return None, None
    
    # 显示列名信息
    st.write(f"📋 检测到的列名：{list(df.columns)}")
    
    # 检查数据类型和内容
    st.write("🔍 数据质量检查：")
    
    # 检查第一列（波长）
    wavelength_col = df.iloc[:, 0]
    radiation_col = df.iloc[:, 1]
    
    wavelength_issues = []
    radiation_issues = []
    
    # 波长数据检查
    wavelength_null_count = wavelength_col.isnull().sum()
    wavelength_non_numeric = 0
    try:
        wavelength_numeric = pd.to_numeric(wavelength_col, errors='coerce')
        wavelength_non_numeric = wavelength_numeric.isnull().sum() - wavelength_null_count
    except:
        wavelength_non_numeric = len(wavelength_col)
    
    if wavelength_null_count > 0:
        wavelength_issues.append(f"包含 {wavelength_null_count} 个空值")
    if wavelength_non_numeric > 0:
        wavelength_issues.append(f"包含 {wavelength_non_numeric} 个非数值")
    
    # 辐射数据检查
    radiation_null_count = radiation_col.isnull().sum()
    radiation_non_numeric = 0
    try:
        radiation_numeric = pd.to_numeric(radiation_col, errors='coerce')
        radiation_non_numeric = radiation_numeric.isnull().sum() - radiation_null_count
    except:
        radiation_non_numeric = len(radiation_col)
    
    if radiation_null_count > 0:
        radiation_issues.append(f"包含 {radiation_null_count} 个空值")
    if radiation_non_numeric > 0:
        radiation_issues.append(f"包含 {radiation_non_numeric} 个非数值")
    
    # 显示数据问题
    if wavelength_issues:
        st.warning(f"⚠️ 波长列（第1列）问题：{', '.join(wavelength_issues)}")
    else:
        st.success("✅ 波长列数据格式正确")
        
    if radiation_issues:
        st.warning(f"⚠️ 辐射列（第2列）问题：{', '.join(radiation_issues)}")
    else:
        st.success("✅ 辐射列数据格式正确")
    
    # 显示数据样例
    st.write("📋 数据前5行预览：")
    st.dataframe(df.head(), use_container_width=True)
    
    # 尝试数据转换和清洗
    try:
        # 强制转换为数值类型，无效值变为NaN
        df_converted = df.copy()
        df_converted.iloc[:, 0] = pd.to_numeric(df_converted.iloc[:, 0], errors='coerce')
        df_converted.iloc[:, 1] = pd.to_numeric(df_converted.iloc[:, 1], errors='coerce')
        
        # 重新设置列名
        df_converted.columns = ['wavelength', 'radiation'] + list(df_converted.columns[2:])
        
        # 删除包含NaN的行
        df_clean = df_converted.dropna(subset=['wavelength', 'radiation'])
        
        st.write(f"🧹 数据清洗结果：从 {len(df)} 行清洗到 {len(df_clean)} 行")
        
        # 检查清洗后的数据是否为空
        if df_clean.empty or len(df_clean) == 0:
            st.error("❌ 数据清洗后为空！")
            st.write("💡 **可能的原因和解决方案：**")
            
            issues_found = []
            solutions = []
            
            if wavelength_null_count == len(df) or wavelength_non_numeric == len(df):
                issues_found.append("第1列（波长）全部为无效数据")
                solutions.append("确保第1列包含数值型的波长数据（如 400, 450, 500...）")
                
            if radiation_null_count == len(df) or radiation_non_numeric == len(df):
                issues_found.append("第2列（辐射）全部为无效数据")
                solutions.append("确保第2列包含数值型的辐射强度数据")
            
            if not issues_found:
                issues_found.append("数据格式可能不符合要求")
                solutions.append("检查文件是否为CSV/Excel格式，且数据从第1行开始")
            
            for i, (issue, solution) in enumerate(zip(issues_found, solutions), 1):
                st.write(f"{i}. **问题**: {issue}")
                st.write(f"   **解决**: {solution}")
            
            st.write("\n📝 **正确的数据格式示例：**")
            example_data = pd.DataFrame({
                '波长(nm)': [400, 410, 420, 430, 440],
                '辐射强度': [0.1, 0.2, 0.3, 0.25, 0.15]
            })
            st.dataframe(example_data, use_container_width=True)
            
            return None, None
        
        # 显示清洗后的数据范围
        wavelength_range = f"{df_clean['wavelength'].min():.0f} - {df_clean['wavelength'].max():.0f} nm"
        radiation_range = f"{df_clean['radiation'].min():.3f} - {df_clean['radiation'].max():.3f}"
        
        st.success(f"✅ 数据清洗成功！波长范围：{wavelength_range}，辐射范围：{radiation_range}")
        
        wavelength = df_clean['wavelength'].astype(float).values
        radiation = df_clean['radiation'].astype(float).values
        
        # 检查数组长度是否一致
        if len(wavelength) != len(radiation):
            min_len = min(len(wavelength), len(radiation))
            wavelength = wavelength[:min_len]
            radiation = radiation[:min_len]
            st.warning(f"⚠️ 数组长度不一致，已截取到 {min_len} 个数据点")
        
        # 检查数据是否为空
        if len(wavelength) == 0 or len(radiation) == 0:
            st.error("❌ 有效数据为空，请检查文件格式")
            return None, None
        
        # 1. 计算每个波长的积分值 (λ × 辐射 ÷ 119.8)
        integration_values = (wavelength * radiation) / 119.8
        
        # 检查是否有无效值，同时保持数组长度一致
        valid_mask = ~(np.isnan(integration_values) | np.isinf(integration_values))
        
        if not np.any(valid_mask):
            st.error("所有计算结果都包含无效值，请检查数据质量")
            return None, None
            
        # 应用掩码保持所有数组长度一致
        wavelength = wavelength[valid_mask]
        radiation = radiation[valid_mask]
        integration_values = integration_values[valid_mask]
        
        # 最终检查数据是否还有剩余
        if len(wavelength) == 0:
            st.error("过滤无效值后没有剩余数据")
            return None, None
            
    except Exception as e:
        st.error(f"数据预处理出错: {str(e)}")
        return None, None
    
    # 2. 光合有效积分 (积分值的求和)
    photosynthetic_active = np.sum(integration_values)
    
    # 3. 总积分 (所有辐射值求和)
    total_integration = np.sum(radiation)
    
    # 4. 不同波长范围的积分计算
    def calculate_wavelength_range_integration(df_data, integration_vals, min_wave, max_wave, include_upper=False):
        """计算波长范围内的积分值求和（用于光合有效积分的各波段）"""
        if include_upper:
            mask = (df_data['wavelength'] >= min_wave) & (df_data['wavelength'] <= max_wave)
        else:
            mask = (df_data['wavelength'] >= min_wave) & (df_data['wavelength'] < max_wave)
        return integration_vals[mask].sum()
    
    def calculate_wavelength_range_radiation(df_data, radiation_vals, min_wave, max_wave, include_upper=False):
        """计算波长范围内的辐射值求和（用于PAR积分等）"""
        if include_upper:
            mask = (df_data['wavelength'] >= min_wave) & (df_data['wavelength'] <= max_wave)
        else:
            mask = (df_data['wavelength'] >= min_wave) & (df_data['wavelength'] < max_wave)
        return radiation_vals[mask].sum()
    
    # PAR积分 (400-700nm辐射值总和，不包括700)
    par_integration = calculate_wavelength_range_radiation(df_clean, radiation, 400, 700)
    
    # 蓝光积分 (400-500nm，不包括500) - 使用积分值
    blue_integration = calculate_wavelength_range_integration(df_clean, integration_values, 400, 500)
    
    # 绿光积分 (500-600nm，不包括600) - 使用积分值
    green_integration = calculate_wavelength_range_integration(df_clean, integration_values, 500, 600)
    
    # 红光积分 (600-700nm，不包括700) - 使用积分值
    red_integration = calculate_wavelength_range_integration(df_clean, integration_values, 600, 700)
    
    # 远红光积分 (700-800nm，不包括800) - 使用积分值
    far_red_integration = calculate_wavelength_range_integration(df_clean, integration_values, 700, 800)
    
    # 新增光形态建成相关参数
    # UV-A积分 (315-400nm) - 使用积分值
    uva_integration = calculate_wavelength_range_integration(df_clean, integration_values, 315, 400)
    
    # UV-B积分 (280-315nm) - 使用积分值  
    uvb_integration = calculate_wavelength_range_integration(df_clean, integration_values, 280, 315)
    
    # 紫光积分 (380-420nm) - 使用积分值
    violet_integration = calculate_wavelength_range_integration(df_clean, integration_values, 380, 420)
    
    # 近红外积分 (700-850nm) - 使用积分值
    nir_integration = calculate_wavelength_range_integration(df_clean, integration_values, 700, 850)
    
    # 5. 灯具光质总和积分（扩展版本）
    light_quality_total = blue_integration + green_integration + red_integration + far_red_integration
    extended_light_quality = uva_integration + violet_integration + blue_integration + green_integration + red_integration + far_red_integration + nir_integration
    
    # 6. 各颜色光占比计算（基于扩展光质总和）
    blue_percentage = (blue_integration / extended_light_quality * 100) if extended_light_quality > 0 else 0
    green_percentage = (green_integration / extended_light_quality * 100) if extended_light_quality > 0 else 0
    red_percentage = (red_integration / extended_light_quality * 100) if extended_light_quality > 0 else 0
    far_red_percentage = (far_red_integration / extended_light_quality * 100) if extended_light_quality > 0 else 0
    
    # 新增光形态建成占比
    uva_percentage = (uva_integration / extended_light_quality * 100) if extended_light_quality > 0 else 0
    uvb_percentage = (uvb_integration / extended_light_quality * 100) if extended_light_quality > 0 else 0
    violet_percentage = (violet_integration / extended_light_quality * 100) if extended_light_quality > 0 else 0
    nir_percentage = (nir_integration / extended_light_quality * 100) if extended_light_quality > 0 else 0
    
    # 7. 光效计算
    luminous_efficacy = total_radiation_flux / total_power if total_power > 0 else 0
    
    # 8. 重新设计的计算指标
    # 光能比 (光合有效积分/总积分)
    light_energy_ratio = photosynthetic_active / total_integration if total_integration > 0 else 0
    
    # 总光子通量 (总辐射通量 × 光能比，单位: μmol/s)
    total_photon_flux = total_radiation_flux * light_energy_ratio
    
    # PPE (总光子通量/总功率，单位: μmol/J)
    ppe = total_photon_flux / total_power if total_power > 0 else 0
    
    # 保留原有的PAR占比计算
    par_ratio = par_integration / total_integration if total_integration > 0 else 0
    
    # 保留原有的光质比例计算
    # R/B (红光积分/蓝光积分)
    r_b_ratio = red_integration / blue_integration if blue_integration > 0 else 0
    
    # R/Fr (红光积分/远红光积分)
    r_fr_ratio = red_integration / far_red_integration if far_red_integration > 0 else 0
    
    # UV-A/B (UV-A积分/蓝光积分) - 移到光质比例指标
    uva_b_ratio = uva_integration / blue_integration if blue_integration > 0 else 0
    
    # 删除的比例参数
    # b_g_ratio = blue_integration / green_integration if green_integration > 0 else 0
    # g_r_ratio = green_integration / red_integration if red_integration > 0 else 0
    
    # 保留的其他比例参数
    v_b_ratio = violet_integration / blue_integration if blue_integration > 0 else 0
    nir_r_ratio = nir_integration / red_integration if red_integration > 0 else 0
    
    # PAR功率 (总辐射通量 × PAR占比，单位: W)
    par_power = total_radiation_flux * par_ratio
    
    # 9. 植物光合敏感曲线P(λ)相关计算 (McCree 1972)
    def plant_photosynthetic_response(wavelength):
        """McCree (1972) 植物光合敏感曲线P(λ)"""
        if wavelength < 400 or wavelength > 700:
            return 0.0
        elif wavelength <= 550:
            # 蓝光区域峰值在430nm附近
            return np.exp(-0.5 * ((wavelength - 430) / 40) ** 2) * 0.8 + \
                   np.exp(-0.5 * ((wavelength - 470) / 30) ** 2) * 0.6
        else:
            # 红光区域峰值在630-680nm附近
            return np.exp(-0.5 * ((wavelength - 630) / 35) ** 2) * 0.9 + \
                   np.exp(-0.5 * ((wavelength - 670) / 25) ** 2) * 0.7
    
    # 计算植物光子度量学参数
    plant_response_values = np.array([plant_photosynthetic_response(w) for w in wavelength])
    plant_weighted_integration = np.sum(integration_values * plant_response_values)
    plant_photon_efficacy = plant_weighted_integration / total_integration if total_integration > 0 else 0
    
    # 10. 光谱质量评价参数
    # 数据有效性检查
    if len(radiation) == 0 or len(wavelength) == 0:
        # 如果数据为空，设置默认值
        peak_wavelength = 550  # 默认峰值波长
        spectral_width = 0
        spectral_uniformity = 0
        color_saturation = 0
    else:
        # 峰值波长位置
        try:
            max_radiation_idx = np.argmax(radiation)
            peak_wavelength = wavelength[max_radiation_idx]
            
            # 光谱宽度计算 (半峰宽 FWHM)
            max_radiation_value = radiation[max_radiation_idx]
            half_max = max_radiation_value / 2
            indices = np.where(radiation >= half_max)[0]
            spectral_width = wavelength[indices[-1]] - wavelength[indices[0]] if len(indices) > 1 else 0
            
            # 光谱均匀性指数 (标准差/平均值)
            spectral_uniformity = np.std(radiation) / np.mean(radiation) if np.mean(radiation) > 0 else 0
            
            # 色彩饱和度指数 (主峰值/平均值)  
            color_saturation = max_radiation_value / np.mean(radiation) if np.mean(radiation) > 0 else 0
        except (ValueError, IndexError) as e:
            # 出现异常时使用默认值
            peak_wavelength = 550
            spectral_width = 0
            spectral_uniformity = 0
            color_saturation = 0
    
    # 11. 植物生理响应参数
    # DLI计算 (假设12小时光照) - 使用新的总光子通量
    photoperiod_hours = 12  # 可以作为参数输入
    dli = total_photon_flux * 3600 * photoperiod_hours / 1000000  # mol/m²/d
    
    # 光饱和点达成率 (基于不同作物的典型光饱和点)
    crop_light_saturation = {
        '叶菜类': 300,    # μmol/m²/s
        '果菜类': 800,    # μmol/m²/s  
        '花卉类': 400,    # μmol/m²/s
        '草本类': 200     # μmol/m²/s
    }
    
    # 假设PPFD为总光子通量值（简化计算）
    ppfd_estimated = total_photon_flux  
    saturation_rates = {}
    for crop_type, saturation_point in crop_light_saturation.items():
        saturation_rate = min(ppfd_estimated / saturation_point, 1.0) if saturation_point > 0 else 0
        saturation_rates[crop_type] = saturation_rate
    
    # 光补偿点评估 (一般植物光补偿点在5-20 μmol/m²/s)
    light_compensation_point = 15  # μmol/m²/s (平均值)
    compensation_multiple = ppfd_estimated / light_compensation_point if light_compensation_point > 0 else 0
    
    # 光形态指数 (基于R/Fr比值)
    if r_fr_ratio > 1.2:
        morphology_index = "紧凑型"
    elif r_fr_ratio > 0.8:
        morphology_index = "正常型"
    else:
        morphology_index = "徒长型"
    
    # 12. 扩展的植物生理响应评价指标
    
    # 光形态建成相关指标
    # Cryptochrome活性指数 (基于蓝光和UV-A)
    crypto_activity = (blue_integration + uva_integration) / extended_light_quality if extended_light_quality > 0 else 0
    
    # Phytochrome活性指数 (基于红光和远红光)
    phyto_activity = red_integration / (red_integration + far_red_integration) if (red_integration + far_red_integration) > 0 else 0
    
    # 花青素合成指数 (基于紫光和蓝光)
    anthocyanin_index = (violet_integration + blue_integration) / extended_light_quality if extended_light_quality > 0 else 0
    
    # 叶绿素合成效率指数 (基于红蓝光比例)
    chlorophyll_synthesis = (red_integration + blue_integration) / extended_light_quality if extended_light_quality > 0 else 0
    
    # 13. 不同作物类型的专业评价
    crop_suitability = {}
    
    # 叶菜类作物评价 (适宜R/B: 0.5-1.5, 高蓝光需求)
    leafy_score = 0
    if 0.5 <= r_b_ratio <= 1.5:
        leafy_score += 30
    elif 0.3 <= r_b_ratio <= 2.0:
        leafy_score += 20
    else:
        leafy_score += 10
    
    if blue_percentage > 20:
        leafy_score += 25
    elif blue_percentage > 15:
        leafy_score += 15
    else:
        leafy_score += 5
    
    if green_percentage < 15:  # 绿光不宜过多
        leafy_score += 20
    else:
        leafy_score += 10
    
    if par_ratio > 0.8:
        leafy_score += 25
    elif par_ratio > 0.6:
        leafy_score += 15
    else:
        leafy_score += 5
    
    crop_suitability['叶菜类'] = min(leafy_score, 100)
    
    # 果菜类作物评价 (适宜R/B: 1.0-3.0, 高红光需求)
    fruit_score = 0
    if 1.0 <= r_b_ratio <= 3.0:
        fruit_score += 30
    elif 0.7 <= r_b_ratio <= 4.0:
        fruit_score += 20
    else:
        fruit_score += 10
    
    if red_percentage > 35:
        fruit_score += 25
    elif red_percentage > 25:
        fruit_score += 15
    else:
        fruit_score += 5
    
    if far_red_percentage > 5:  # 适量远红光促进开花
        fruit_score += 20
    else:
        fruit_score += 10
    
    if par_ratio > 0.8:
        fruit_score += 25
    elif par_ratio > 0.6:
        fruit_score += 15
    else:
        fruit_score += 5
    
    crop_suitability['果菜类'] = min(fruit_score, 100)
    
    # 育苗专用评价 (高蓝光，适中红光)
    seedling_score = 0
    if 0.3 <= r_b_ratio <= 1.0:
        seedling_score += 30
    elif 0.2 <= r_b_ratio <= 1.5:
        seedling_score += 20
    else:
        seedling_score += 10
    
    if blue_percentage > 25:
        seedling_score += 30
    elif blue_percentage > 20:
        seedling_score += 20
    else:
        seedling_score += 10
    
    if uva_b_ratio > 0.1:  # UV-A促进育苗
        seedling_score += 20
    else:
        seedling_score += 10
    
    if ppe > 2.0:
        seedling_score += 20
    else:
        seedling_score += 10
    
    crop_suitability['育苗专用'] = min(seedling_score, 100)
    
    # 14. 光谱质量综合评价
    # 光谱完整性指数 (各波段均匀度)
    band_completeness = 0
    total_bands = 8  # UV-B, UV-A, 紫, 蓝, 绿, 红, 远红, 近红外
    
    band_percentages = [
        uvb_percentage, uva_percentage, violet_percentage, blue_percentage,
        green_percentage, red_percentage, far_red_percentage, nir_percentage
    ]
    
    non_zero_bands = sum(1 for p in band_percentages if p > 1)  # 超过1%才算有效
    spectral_completeness = non_zero_bands / total_bands
    
    # 光谱平衡指数 (避免某一波段过度突出)
    max_band_percentage = max(band_percentages)
    spectral_balance = 1 - (max_band_percentage - 40) / 60 if max_band_percentage > 40 else 1
    spectral_balance = max(spectral_balance, 0)
    
    # 15. 能效与经济性扩展分析
    # 光能利用效率 (PAR输出功率/总功率)
    light_energy_efficiency = par_power / total_power if total_power > 0 else 0
    
    # 热损失率
    heat_loss_rate = (total_power - total_radiation_flux) / total_power if total_power > 0 else 0
    
    # 单位面积成本效益 (假设照射面积1m²)
    illumination_area = 1.0  # m²
    ppfd_per_area = total_photon_flux / illumination_area  # μmol/m²/s
    
    # 投资回报评估 (基于PPE和电费)
    electricity_cost_per_kwh = 0.6  # 元/kWh
    daily_electricity_cost = (total_power / 1000) * 12 * electricity_cost_per_kwh  # 元/天
    annual_electricity_cost = daily_electricity_cost * 365  # 元/年
    
    # 光效成本比 (PPE/每年电费，越高越好)
    efficiency_cost_ratio = ppe / (annual_electricity_cost / 100) if annual_electricity_cost > 0 else 0
    
    # 16. 光谱优化建议
    optimization_suggestions = []
    
    if ppe < 2.0:
        optimization_suggestions.append("建议提高PPE：增加光合有效光子输出比例")
    
    if par_ratio < 0.6:
        optimization_suggestions.append("建议优化光谱分布：提高PAR波段(400-700nm)比例")
    
    if r_b_ratio < 0.3:
        optimization_suggestions.append("建议增加红光比例：当前红蓝比过低，可能影响植物伸长和开花")
    elif r_b_ratio > 4.0:
        optimization_suggestions.append("建议增加蓝光比例：当前红蓝比过高，可能导致徒长")
    
    if blue_percentage < 10:
        optimization_suggestions.append("建议增加蓝光(400-500nm)：促进叶绿素合成和植物紧凑生长")
    elif blue_percentage > 40:
        optimization_suggestions.append("建议适当减少蓝光：过多蓝光可能抑制植物伸长")
    
    if green_percentage > 20:
        optimization_suggestions.append("建议减少绿光(500-600nm)：绿光利用效率较低")
    
    if far_red_percentage < 2:
        optimization_suggestions.append("建议添加少量远红光(700-800nm)：促进茎伸长和叶片展开")
    elif far_red_percentage > 15:
        optimization_suggestions.append("建议减少远红光：过多远红光可能导致徒长")
    
    if uva_percentage < 1:
        optimization_suggestions.append("建议添加UV-A(315-400nm)：提高植物抗逆性和次生代谢物含量")
    
    if heat_loss_rate > 0.4:
        optimization_suggestions.append("建议改善散热设计：当前热损失率较高，影响能效")
    
    if not optimization_suggestions:
        optimization_suggestions.append("当前光谱配置较为合理，各项指标均在适宜范围内")
    
    # 17. 植物生长阶段适配性评价
    growth_stage_suitability = {}
    
    # 发芽期适配性 (需要适量蓝光和红光)
    germination_score = 50  # 基础分
    if 15 <= blue_percentage <= 30:
        germination_score += 20
    if 25 <= red_percentage <= 45:
        germination_score += 20
    if ppe > 1.8:
        germination_score += 10
    growth_stage_suitability['发芽期'] = min(germination_score, 100)
    
    # 苗期适配性 (高蓝光，适中红光)
    seedling_stage_score = 50
    if blue_percentage > 25:
        seedling_stage_score += 25
    if 0.5 <= r_b_ratio <= 1.2:
        seedling_stage_score += 20
    if uva_percentage > 2:
        seedling_stage_score += 5
    growth_stage_suitability['苗期'] = min(seedling_stage_score, 100)
    
    # 营养生长期适配性 (平衡红蓝光)
    vegetative_score = 50
    if 1.0 <= r_b_ratio <= 2.0:
        vegetative_score += 20
    if par_ratio > 0.7:
        vegetative_score += 15
    if 10 <= green_percentage <= 15:
        vegetative_score += 10
    if far_red_percentage > 3:
        vegetative_score += 5
    growth_stage_suitability['营养生长期'] = min(vegetative_score, 100)
    
    # 开花期适配性 (高红光，少量远红光)
    flowering_score = 50
    if red_percentage > 35:
        flowering_score += 20
    if r_b_ratio > 2.0:
        flowering_score += 15
    if 5 <= far_red_percentage <= 12:
        flowering_score += 10
    if r_fr_ratio > 2.0:
        flowering_score += 5
    growth_stage_suitability['开花期'] = min(flowering_score, 100)
    
    # 结果期适配性 (均衡光谱，高光强)
    fruiting_score = 50
    if ppe > 2.2:
        fruiting_score += 15
    if par_ratio > 0.8:
        fruiting_score += 15
    if 1.5 <= r_b_ratio <= 3.0:
        fruiting_score += 15
    if spectral_completeness > 0.6:
        fruiting_score += 5
    growth_stage_suitability['结果期'] = min(fruiting_score, 100)
    ppfd_per_watt = ppfd_estimated / total_power if total_power > 0 else 0
    
    # 不同波段的光子效率
    blue_photon_efficiency = blue_integration / total_integration if total_integration > 0 else 0
    green_photon_efficiency = green_integration / total_integration if total_integration > 0 else 0  
    red_photon_efficiency = red_integration / total_integration if total_integration > 0 else 0
    
    # 热辐射损失评估 (基于总功率和辐射通量差异)
    thermal_loss_ratio = (total_power - total_radiation_flux) / total_power if total_power > 0 else 0
    thermal_loss_percentage = thermal_loss_ratio * 100
    
    # 运行成本估算 (假设电费0.6元/kWh，每日12小时)
    daily_energy_consumption = total_power * photoperiod_hours / 1000  # kWh/day
    electricity_rate = 0.6  # 元/kWh
    daily_operating_cost = daily_energy_consumption * electricity_rate  # 元/day
    monthly_operating_cost = daily_operating_cost * 30  # 元/month
    annual_operating_cost = daily_operating_cost * 365  # 元/year
    
    # 光质评价 - 基于新的计算标准
    def evaluate_light_quality(ppe_val, par_ratio_val, rb_ratio):
        """基于新PPE标准的光质评价"""
        # PPE评价标准 (μmol/J)
        ppe_score = 3 if ppe_val > 2.5 else 2 if ppe_val > 2.0 else 1
        par_score = 3 if par_ratio_val > 0.8 else 2 if par_ratio_val > 0.6 else 1
        rb_score = 3 if 0.5 <= rb_ratio <= 3.0 else 2 if 0.3 <= rb_ratio <= 4.0 else 1
        
        total_score = ppe_score + par_score + rb_score
        if total_score >= 8:
            return "优秀", "🏆"
        elif total_score >= 6:
            return "良好", "👍"
        else:
            return "一般", "📈"
    
    quality_rating, quality_icon = evaluate_light_quality(ppe, par_ratio, r_b_ratio)
    
    results = {
        'basic_info': {
            'lamp_model': lamp_model,
            'manufacturer': manufacturer,
            'test_date': str(test_date)
        },
        'input_params': {
            'total_radiation_flux': total_radiation_flux,
            'total_power': total_power,
            'back_panel_temp': back_panel_temp,
            'power_factor': power_factor
        },
        'calculations': {
            'photosynthetic_active': photosynthetic_active,
            'total_integration': total_integration,
            'par_integration': par_integration,
            'blue_integration': blue_integration,
            'green_integration': green_integration,
            'red_integration': red_integration,
            'far_red_integration': far_red_integration,
            'uva_integration': uva_integration,
            'uvb_integration': uvb_integration,
            'violet_integration': violet_integration,
            'nir_integration': nir_integration,
            'light_quality_total': light_quality_total,
            'extended_light_quality': extended_light_quality,
            'luminous_efficacy': luminous_efficacy,
            
            # 新的核心计算指标
            'light_energy_ratio': light_energy_ratio,
            'total_photon_flux': total_photon_flux,
            'ppe': ppe,
            
            # 保留的指标
            'par_ratio': par_ratio,
            'r_b_ratio': r_b_ratio,
            'r_fr_ratio': r_fr_ratio,
            'uva_b_ratio': uva_b_ratio,
            'v_b_ratio': v_b_ratio,
            'nir_r_ratio': nir_r_ratio,
            'par_power': par_power,
            
            # 扩展的植物生理响应指标
            'crypto_activity': crypto_activity,
            'phyto_activity': phyto_activity,
            'anthocyanin_index': anthocyanin_index,
            'chlorophyll_synthesis': chlorophyll_synthesis,
            
            # 作物适应性评价
            'crop_suitability': crop_suitability,
            
            # 光谱质量评价
            'spectral_completeness': spectral_completeness,
            'spectral_balance': spectral_balance,
            
            # 能效经济性分析
            'light_energy_efficiency': light_energy_efficiency,
            'heat_loss_rate': heat_loss_rate,
            'ppfd_per_area': ppfd_per_area,
            'annual_electricity_cost': annual_electricity_cost,
            'efficiency_cost_ratio': efficiency_cost_ratio,
            
            # 优化建议
            'optimization_suggestions': optimization_suggestions,
            
            # 生长阶段适配性
            'growth_stage_suitability': growth_stage_suitability,
            
            'plant_weighted_integration': plant_weighted_integration,
            'plant_photon_efficacy': plant_photon_efficacy,
            'peak_wavelength': peak_wavelength,
            'spectral_width': spectral_width,
            'spectral_uniformity': spectral_uniformity,
            'color_saturation': color_saturation,
            'dli': dli,
            'saturation_rates': saturation_rates,
            'compensation_multiple': compensation_multiple,
            'morphology_index': morphology_index,
            'ppfd_estimated': ppfd_estimated,
            'ppfd_per_watt': ppfd_per_watt,
            'blue_photon_efficiency': blue_photon_efficiency,
            'green_photon_efficiency': green_photon_efficiency,
            'red_photon_efficiency': red_photon_efficiency,
            'thermal_loss_percentage': thermal_loss_percentage,
            'daily_operating_cost': daily_operating_cost,
            'monthly_operating_cost': monthly_operating_cost,
            'annual_operating_cost': annual_operating_cost,
            'quality_rating': quality_rating,
            'quality_icon': quality_icon
        },
        'percentages': {
            'blue_percentage': blue_percentage,
            'green_percentage': green_percentage,
            'red_percentage': red_percentage,
            'far_red_percentage': far_red_percentage,
            'uva_percentage': uva_percentage,
            'uvb_percentage': uvb_percentage,
            'violet_percentage': violet_percentage,
            'nir_percentage': nir_percentage
        }
    }
    
    return results, df_clean

def display_results(results, df):
    """显示分析结果"""
    
    st.markdown("---")
    st.header("🔬 分析结果")
    
    # 输入参数展示区域
    st.subheader("📊 测试参数")
    
    # 显示基本信息
    basic_info = results.get('basic_info', {})
    if any(basic_info.values()):
        st.markdown("##### 📋 基本信息")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lamp_model = basic_info.get('lamp_model', '未填写')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
                <h4>🏷️ 灯具型号</h4>
                <h3>{lamp_model}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            manufacturer = basic_info.get('manufacturer', '未填写')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
                <h4>🏢 制造商/单位</h4>
                <h3>{manufacturer}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            test_date = basic_info.get('test_date', '未填写')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
                <h4>📅 测试日期</h4>
                <h3>{test_date}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("##### ⚡ 电气参数")
    # 使用卡片式布局
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h3>🔆 总辐射通量</h3>
            <h2>{results['input_params']['total_radiation_flux']:.1f} W</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h3>⚡ 总功率</h3>
            <h2>{results['input_params']['total_power']:.1f} W</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h3>🌡️ 后面板温度</h3>
            <h2>{results['input_params']['back_panel_temp']:.1f} ℃</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h3>🔋 功率因数</h3>
            <h2>{results['input_params']['power_factor']:.3f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 综合评价卡片 - 移到顶部
    st.subheader(f"🏆 综合评价: {results['calculations']['quality_rating']} {results['calculations']['quality_icon']}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ppe_rating = "优秀" if results['calculations']['ppe'] > 2.5 else "良好" if results['calculations']['ppe'] > 2.0 else "一般"
        color = "#28a745" if ppe_rating == "优秀" else "#ffc107" if ppe_rating == "良好" else "#dc3545"
        st.markdown(f"""
        <div style='background: {color}; padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h4>⚡ PPE评价: {ppe_rating}</h4>
            <p>数值: {results['calculations']['ppe']:.3f} μmol/J</p>
            <p>标准: >2.5优秀, 2.0-2.5良好, <2.0一般</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        par_rating = "优秀" if results['calculations']['par_ratio'] > 0.8 else "良好" if results['calculations']['par_ratio'] > 0.6 else "一般"
        color = "#28a745" if par_rating == "优秀" else "#ffc107" if par_rating == "良好" else "#dc3545"
        st.markdown(f"""
        <div style='background: {color}; padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h4>🌿 PAR占比评价: {par_rating}</h4>
            <p>数值: {results['calculations']['par_ratio']:.1%}</p>
            <p>标准: >80%优秀, 60-80%良好, <60%一般</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        rb_rating = "适宜" if 0.5 <= results['calculations']['r_b_ratio'] <= 3.0 else "偏离"
        color = "#28a745" if rb_rating == "适宜" else "#dc3545"
        st.markdown(f"""
        <div style='background: {color}; padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h4>🔴🔵 R/B比评价: {rb_rating}</h4>
            <p>数值: {results['calculations']['r_b_ratio']:.2f}</p>
            <p>叶菜: 0.5-1.5, 果菜: 1.0-3.0</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 核心性能指标
    st.subheader("🎯 核心性能指标")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "⚡ PPE μmol/J", 
            f"{results['calculations']['ppe']:.3f}",
            help="总光子通量/总功率，最新的光合光子效率指标"
        )
    with col2:
        st.metric(
            "🌱 总光子通量 μmol/s", 
            f"{results['calculations']['total_photon_flux']:.2f}",
            help="总辐射通量×光能比"
        )
    with col3:
        st.metric(
            "🌿 PAR占比", 
            f"{results['calculations']['par_ratio']:.1%}",
            help="PAR积分/总积分，光合有效辐射比例"
        )
    with col4:
        st.metric(
            "🔄 光能比", 
            f"{results['calculations']['light_energy_ratio']:.3f}",
            help="光合有效积分/总积分，光合有效光能转化效率"
        )
    
    # 光质比例指标
    st.subheader("🎨 光质比例指标")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🔴/🔵 R/B", 
            f"{results['calculations']['r_b_ratio']:.2f}",
            help="红光积分/蓝光积分，影响植物形态建成"
        )
    with col2:
        st.metric(
            "🔴/🟤 R/Fr", 
            f"{results['calculations']['r_fr_ratio']:.2f}",
            help="红光积分/远红光积分，影响植物光周期响应"
        )
    with col3:
        st.metric(
            "🟣/🔵 UV-A/B", 
            f"{results['calculations']['uva_b_ratio']:.3f}",
            help="UV-A积分/蓝光积分，影响植物抗逆性"
        )
    with col4:
        st.metric(
            "🔴🔢 NIR/R", 
            f"{results['calculations']['nir_r_ratio']:.2f}",
            help="近红外积分/红光积分"
        )
    
    st.markdown("---")
    
    # 扩展功能1：植物生理响应指标
    st.subheader("🧬 植物生理响应指标")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🔵 隐花色素活性", 
            f"{results['calculations']['crypto_activity']:.3f}",
            help="基于蓝光和UV-A，影响植物向光性和生物钟调节"
        )
    with col2:
        st.metric(
            "🔴 光敏色素活性", 
            f"{results['calculations']['phyto_activity']:.3f}",
            help="基于红光/远红光比例，调节植物光周期响应"
        )
    with col3:
        st.metric(
            "💜 花青素合成指数", 
            f"{results['calculations']['anthocyanin_index']:.3f}",
            help="基于紫光和蓝光，影响抗逆性和着色"
        )
    with col4:
        st.metric(
            "🌿 叶绿素合成指数", 
            f"{results['calculations']['chlorophyll_synthesis']:.3f}",
            help="基于红蓝光组合，影响光合色素合成"
        )
    
    st.markdown("---")
    
    # 扩展功能2：作物适应性评价
    st.subheader("🌾 作物适应性评价")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        leafy_score = results['calculations']['crop_suitability']['叶菜类']
        leafy_color = "#28a745" if leafy_score >= 80 else "#ffc107" if leafy_score >= 60 else "#dc3545"
        st.markdown(f"""
        <div style='background: {leafy_color}; padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h4>🥬 叶菜类适应性</h4>
            <h2>{leafy_score}分</h2>
            <p>生菜、菠菜、小白菜等</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        fruit_score = results['calculations']['crop_suitability']['果菜类']
        fruit_color = "#28a745" if fruit_score >= 80 else "#ffc107" if fruit_score >= 60 else "#dc3545"
        st.markdown(f"""
        <div style='background: {fruit_color}; padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h4>🍅 果菜类适应性</h4>
            <h2>{fruit_score}分</h2>
            <p>番茄、黄瓜、辣椒等</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        seedling_score = results['calculations']['crop_suitability']['育苗专用']
        seedling_color = "#28a745" if seedling_score >= 80 else "#ffc107" if seedling_score >= 60 else "#dc3545"
        st.markdown(f"""
        <div style='background: {seedling_color}; padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
            <h4>🌱 育苗专用适应性</h4>
            <h2>{seedling_score}分</h2>
            <p>种子萌发、幼苗培育</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 扩展功能3：生长阶段适配性
    st.subheader("📈 生长阶段适配性分析")
    
    stage_names = list(results['calculations']['growth_stage_suitability'].keys())
    stage_scores = list(results['calculations']['growth_stage_suitability'].values())
    
    # 创建生长阶段适配性柱状图
    fig_stages = go.Figure(data=[
        go.Bar(
            x=stage_names, 
            y=stage_scores,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            text=[f'{score}分' for score in stage_scores],
            textposition='auto'
        )
    ])
    
    fig_stages.update_layout(
        title="不同生长阶段适配性评分",
        xaxis_title="生长阶段",
        yaxis_title="适配性评分",
        height=400,
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig_stages, use_container_width=True)
    
    st.markdown("---")
    
    # 扩展功能4：光谱质量分析
    st.subheader("🌈 光谱质量综合分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "📊 光谱完整性", 
            f"{results['calculations']['spectral_completeness']:.1%}",
            help="评估光谱覆盖的波段完整程度"
        )
        st.metric(
            "⚖️ 光谱平衡性", 
            f"{results['calculations']['spectral_balance']:.3f}",
            help="评估各波段分布的均衡程度"
        )
    
    with col2:
        # 光谱质量雷达图
        categories = ['完整性', '平衡性', 'PAR占比', 'PPE性能', '红蓝比适宜度']
        
        # 计算各维度得分（0-1标准化）
        completeness_score = results['calculations']['spectral_completeness']
        balance_score = results['calculations']['spectral_balance']
        par_score = min(results['calculations']['par_ratio'] / 0.9, 1.0)  # 以0.9为满分
        ppe_score = min(results['calculations']['ppe'] / 3.0, 1.0)  # 以3.0为满分
        rb_score = 1.0 if 0.5 <= results['calculations']['r_b_ratio'] <= 3.0 else 0.5
        
        scores = [completeness_score, balance_score, par_score, ppe_score, rb_score]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='当前光谱',
            fillcolor='rgba(0, 123, 255, 0.3)',
            line_color='rgba(0, 123, 255, 1)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="光谱质量雷达图",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    st.markdown("---")
    
    # 扩展功能5：能效与经济性分析
    st.subheader("💰 能效与经济性分析")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "⚡ 光能利用效率", 
            f"{results['calculations']['light_energy_efficiency']:.1%}",
            help="PAR输出功率占总功率的比例"
        )
    with col2:
        st.metric(
            "🔥 热损失率", 
            f"{results['calculations']['heat_loss_rate']:.1%}",
            help="总功率中转化为热量的比例"
        )
    with col3:
        st.metric(
            "💡 单位面积光强", 
            f"{results['calculations']['ppfd_per_area']:.0f} μmol/m²/s",
            help="假设1m²照射面积下的PPFD值"
        )
    with col4:
        st.metric(
            "💲 年度电费", 
            f"{results['calculations']['annual_electricity_cost']:.0f} 元",
            help="按每日12小时运行计算的年度电费"
        )
    
    st.markdown("---")
    
    # 扩展功能6：光谱优化建议
    st.subheader("💡 光谱优化建议")
    
    suggestions = results['calculations']['optimization_suggestions']
    
    if len(suggestions) == 1 and "较为合理" in suggestions[0]:
        st.success("🎉 " + suggestions[0])
    else:
        st.warning("📋 检测到以下可优化项目：")
        for i, suggestion in enumerate(suggestions, 1):
            st.write(f"{i}. {suggestion}")
    
    # 优化建议的优先级分析
    priority_suggestions = {
        "高优先级": [],
        "中优先级": [],
        "低优先级": []
    }
    
    for suggestion in suggestions:
        if "PPE" in suggestion or "PAR" in suggestion:
            priority_suggestions["高优先级"].append(suggestion)
        elif "红蓝比" in suggestion or "热损失" in suggestion:
            priority_suggestions["中优先级"].append(suggestion)
        else:
            priority_suggestions["低优先级"].append(suggestion)
    
    if any(priority_suggestions.values()):
        st.markdown("#### 🎯 优化建议优先级")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if priority_suggestions["高优先级"]:
                st.error("🔴 高优先级")
                for suggestion in priority_suggestions["高优先级"]:
                    st.write(f"• {suggestion}")
        
        with col2:
            if priority_suggestions["中优先级"]:
                st.warning("🟡 中优先级")
                for suggestion in priority_suggestions["中优先级"]:
                    st.write(f"• {suggestion}")
        
        with col3:
            if priority_suggestions["低优先级"]:
                st.info("🟢 低优先级")
                for suggestion in priority_suggestions["低优先级"]:
                    st.write(f"• {suggestion}")
    
    st.markdown("---")
    
    # 光谱积分详情
    st.subheader("🌈 光谱积分详情")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 基础积分值")
        st.metric("✨ 光合有效积分", f"{results['calculations']['photosynthetic_active']:.2f}")
        st.metric("📊 总积分", f"{results['calculations']['total_integration']:.2f}")
        st.metric("🌿 PAR积分 (400-700nm)", f"{results['calculations']['par_integration']:.2f}")
        st.metric("🎨 光质总和积分", f"{results['calculations']['light_quality_total']:.2f}")
    
    with col2:
        st.markdown("#### 各波段积分")
        st.metric("🔵 蓝光积分 (400-500nm)", f"{results['calculations']['blue_integration']:.2f}")
        st.metric("🟢 绿光积分 (500-600nm)", f"{results['calculations']['green_integration']:.2f}")
        st.metric("🔴 红光积分 (600-700nm)", f"{results['calculations']['red_integration']:.2f}")
        st.metric("🟤 远红光积分 (700-800nm)", f"{results['calculations']['far_red_integration']:.2f}")
    
    st.subheader("光质分布占比")
    
    # 光质占比饼图
    colors = ['#4285F4', '#34A853', '#EA4335', "#FB04DA"]  # 蓝、绿、红、远红
    labels = ['蓝光 (400-500nm)', '绿光 (500-600nm)', '红光 (600-700nm)', '远红光 (700-800nm)']
    values = [
        results['percentages']['blue_percentage'],
        results['percentages']['green_percentage'],
        results['percentages']['red_percentage'],
        results['percentages']['far_red_percentage']
    ]
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        marker_colors=colors,
        textinfo='label+percent',
        textfont_size=12
    )])
    
    fig_pie.update_layout(
        title="光质分布占比",
        font=dict(size=14),
        height=500
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 光谱分布图
    st.subheader("光谱分布图")
    
    fig_spectrum = go.Figure()
    
    # 使用Rainbow颜色映射创建连续的光谱颜色填充
    def wavelength_to_rgb(wavelength):
        """将波长转换为RGB颜色值 (基于可见光谱)"""
        if wavelength < 380:
            return (0.5, 0.0, 1.0)  # 紫外线区域显示为紫色
        elif wavelength < 440:
            # 紫到蓝
            t = (wavelength - 380) / (440 - 380)
            return (0.5 - 0.5*t, 0.0, 1.0)
        elif wavelength < 490:
            # 蓝到青
            t = (wavelength - 440) / (490 - 440)
            return (0.0, t, 1.0)
        elif wavelength < 510:
            # 青到绿
            t = (wavelength - 490) / (510 - 490)
            return (0.0, 1.0, 1.0 - t)
        elif wavelength < 580:
            # 绿到黄
            t = (wavelength - 510) / (580 - 510)
            return (t, 1.0, 0.0)
        elif wavelength < 645:
            # 黄到橙
            t = (wavelength - 580) / (645 - 580)
            return (1.0, 1.0 - 0.5*t, 0.0)
        elif wavelength < 750:
            # 橙到红
            t = (wavelength - 645) / (750 - 645)
            return (1.0, 0.5 - 0.5*t, 0.0)
        else:
            # 红外线区域显示为深红
            return (0.5, 0.0, 0.0)
    
    # 创建连续的彩虹填充效果
    wavelengths = df['wavelength'].values
    radiations = df['radiation'].values
    
    # 数据检查
    if len(wavelengths) == 0 or len(radiations) == 0:
        st.warning("光谱数据为空，无法显示光谱分布图")
        return
    
    try:
        # 按小段创建填充，每段使用对应的光谱颜色
        step = 5  # 每5nm一个颜色段
        min_wave = int(wavelengths.min())
        max_wave = int(wavelengths.max())
        
        # 检查波长范围是否合理
        if min_wave >= max_wave or max_wave - min_wave < 10:
            st.warning("波长数据范围异常，使用简化显示")
            # 使用简化的图表
            fig_spectrum = go.Figure()
            fig_spectrum.add_trace(go.Scatter(
                x=wavelengths,
                y=radiations,
                mode='lines+markers',
                name='光谱强度',
                line=dict(color='blue', width=2)
            ))
        else:
            fig_spectrum = go.Figure()
            
            for wave_start in range(min_wave, max_wave, step):
                wave_end = min(wave_start + step, max_wave)
                
                # 筛选该波长范围内的数据
                mask = (wavelengths >= wave_start) & (wavelengths < wave_end)
                if np.any(mask):
                    range_waves = wavelengths[mask]
                    range_rads = radiations[mask]
                    
                    if len(range_waves) > 0:
                        # 计算该范围的中心波长用于颜色映射
                        center_wave = (wave_start + wave_end) / 2
                        r, g, b = wavelength_to_rgb(center_wave)
                        color = f'rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, 0.7)'
                        
                        # 创建填充区域
                        x_fill = [wave_start] + list(range_waves) + [wave_end]
                        y_fill = [0] + list(range_rads) + [0]
                        
                        fig_spectrum.add_trace(go.Scatter(
                            x=x_fill,
                            y=y_fill,
                            fill='tozeroy',
                            fillcolor=color,
                            line=dict(color=color, width=0),
                            mode='lines',
                            showlegend=False,
                            hoverinfo='skip'
                        ))
            
            # 添加整体光谱线条作为轮廓
            fig_spectrum.add_trace(go.Scatter(
                x=df['wavelength'],
                y=df['radiation'],
                mode='lines',
                name='光谱强度',
                line=dict(color='black', width=2),
                opacity=0.8
            ))
    
    except Exception as e:
        st.error(f"生成光谱分布图时出错: {str(e)}")
        # 使用简化的图表作为后备
        fig_spectrum = go.Figure()
        fig_spectrum.add_trace(go.Scatter(
            x=wavelengths,
            y=radiations,
            mode='lines+markers',
            name='光谱强度',
            line=dict(color='blue', width=2)
        ))
    
    # 添加波长范围标注
    wavelength_ranges = [
        (400, 500, '蓝光'),
        (500, 600, '绿光'),  
        (600, 700, '红光'),
        (700, 800, '远红光')
    ]
    
    for min_wave, max_wave, label in wavelength_ranges:
        # 在对应区域添加文字标注
        center_wave = (min_wave + max_wave) / 2
        mask = (df['wavelength'] >= min_wave) & (df['wavelength'] < max_wave)
        if np.any(mask):
            max_y = df[mask]['radiation'].max()
            fig_spectrum.add_annotation(
                x=center_wave,
                y=max_y * 1.1,
                text=label,
                showarrow=False,
                font=dict(size=12, color='black'),
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='black',
                borderwidth=1
            )
    
    fig_spectrum.update_layout(
        title="LED光谱分布 (彩虹色谱)",
        xaxis_title="波长 (nm)",
        yaxis_title="辐射强度",
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", 
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig_spectrum, use_container_width=True)
    
    # 植物光合敏感曲线对比图
    st.subheader("🌱 植物光合敏感曲线分析 (McCree 1972)")
    
    # 生成植物光合敏感曲线数据
    wavelength_range = np.arange(380, 780, 1)
    
    def plant_photosynthetic_response_viz(wavelength):
        """用于可视化的植物光合敏感曲线"""
        if wavelength < 400 or wavelength > 700:
            return 0.0
        elif wavelength <= 550:
            return np.exp(-0.5 * ((wavelength - 430) / 40) ** 2) * 0.8 + \
                   np.exp(-0.5 * ((wavelength - 470) / 30) ** 2) * 0.6
        else:
            return np.exp(-0.5 * ((wavelength - 630) / 35) ** 2) * 0.9 + \
                   np.exp(-0.5 * ((wavelength - 670) / 25) ** 2) * 0.7
    
    def human_eye_response(wavelength):
        """人眼视见函数V(λ)近似"""
        if wavelength < 380 or wavelength > 780:
            return 0.0
        else:
            return np.exp(-0.5 * ((wavelength - 555) / 100) ** 2)
    
    plant_response_curve = [plant_photosynthetic_response_viz(w) for w in wavelength_range]
    human_response_curve = [human_eye_response(w) for w in wavelength_range]
    
    fig_comparison = go.Figure()
    
    # 植物光合敏感曲线
    fig_comparison.add_trace(go.Scatter(
        x=wavelength_range,
        y=plant_response_curve,
        mode='lines',
        name='植物光合敏感曲线 P(λ)',
        line=dict(color='#2E8B57', width=3),
        fill='tozeroy',
        fillcolor='rgba(46, 139, 87, 0.3)'
    ))
    
    # 人眼视见函数
    fig_comparison.add_trace(go.Scatter(
        x=wavelength_range,
        y=human_response_curve,
        mode='lines',
        name='人眼视见函数 V(λ)',
        line=dict(color='#FF6347', width=3, dash='dash'),
        fill='tozeroy',
        fillcolor='rgba(255, 99, 71, 0.2)'
    ))
    
    # 添加实际光谱数据（归一化）
    if len(df) > 0:
        normalized_spectrum = df['radiation'] / df['radiation'].max()
        fig_comparison.add_trace(go.Scatter(
            x=df['wavelength'],
            y=normalized_spectrum,
            mode='lines',
            name='测试光谱 (归一化)',
            line=dict(color='#4169E1', width=2),
            opacity=0.8
        ))
    
    fig_comparison.update_layout(
        title="光学度量体系对比分析",
        xaxis_title="波长 (nm)",
        yaxis_title="相对响应",
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white'
    )
    
    # 添加重要波长标注
    important_wavelengths = [
        (430, "蓝光峰值", "#0000FF"),
        (555, "人眼峰值", "#00FF00"), 
        (630, "红光峰值1", "#FF0000"),
        (670, "红光峰值2", "#8B0000")
    ]
    
    for wl, label, color in important_wavelengths:
        fig_comparison.add_vline(
            x=wl, line_dash="dot", line_color=color,
            annotation_text=f"{label}\n{wl}nm",
            annotation_position="top"
        )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # 植物光子度量学分析
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔬 植物光子度量学指标")
        st.metric("植物加权积分", f"{results['calculations']['plant_weighted_integration']:.2f}")
        st.metric("植物光子效能", f"{results['calculations']['plant_photon_efficacy']:.3f}")
        
        st.markdown("""
        **说明**: 基于McCree (1972)的22种植物光合响应光谱均值，
        更准确地评估光源对植物光合作用的有效性。
        """)
    
    with col2:
        st.markdown("#### 📊 四种度量体系对比")
        comparison_data = {
            "度量体系": [
                "辐射度学", "光度学", "光子度量学", "植物光子度量学"
            ],
            "核心参数": [
                f"{results['calculations']['total_integration']:.2f}",
                "基于人眼V(λ)",
                f"{results['calculations']['ppe']:.3f} μmol/J",
                f"{results['calculations']['plant_photon_efficacy']:.3f}"
            ],
            "适用场景": [
                "能量评价", "人因照明", "植物照明标准", "精准植物照明"
            ]
        }
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # 详细数据表格
    st.subheader("📋 详细计算结果")
    
    # 创建三个分类的表格
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 性能指标")
        performance_data = {
            "指标": [
                "PPE (新标准)", "总光子通量", "PAR占比", "光能比", 
                "R/B比", "R/Fr比", "PAR功率", "光效"
            ],
            "数值": [
                f"{results['calculations']['ppe']:.3f} μmol/J",
                f"{results['calculations']['total_photon_flux']:.2f} μmol/s",
                f"{results['calculations']['par_ratio']:.3f}",
                f"{results['calculations']['light_energy_ratio']:.3f}",
                f"{results['calculations']['r_b_ratio']:.2f}",
                f"{results['calculations']['r_fr_ratio']:.2f}",
                f"{results['calculations']['par_power']:.2f} W",
                f"{results['calculations']['luminous_efficacy']:.3f} W/W"
            ],
            "说明": [
                "总光子通量/总功率",
                "总辐射通量×光能比",
                "光合有效辐射比例",
                "光合有效积分/总积分",
                "红蓝光比例",
                "红远红光比例",
                "PAR波段功率",
                "辐射光效"
            ]
        }
        performance_df = pd.DataFrame(performance_data)
        st.dataframe(performance_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 🌈 光谱积分")
        spectrum_data = {
            "波段": [
                "光合有效积分", "总积分", "PAR积分 (400-700nm)",
                "蓝光积分 (400-500nm)", "绿光积分 (500-600nm)",
                "红光积分 (600-700nm)", "远红光积分 (700-800nm)",
                "光质总和积分"
            ],
            "数值": [
                f"{results['calculations']['photosynthetic_active']:.2f}",
                f"{results['calculations']['total_integration']:.2f}",
                f"{results['calculations']['par_integration']:.2f}",
                f"{results['calculations']['blue_integration']:.2f}",
                f"{results['calculations']['green_integration']:.2f}",
                f"{results['calculations']['red_integration']:.2f}",
                f"{results['calculations']['far_red_integration']:.2f}",
                f"{results['calculations']['light_quality_total']:.2f}"
            ],
            "占比 (%)": [
                "-", "-", f"{results['calculations']['par_ratio']*100:.1f}%",
                f"{results['percentages']['blue_percentage']:.1f}%",
                f"{results['percentages']['green_percentage']:.1f}%",
                f"{results['percentages']['red_percentage']:.1f}%",
                f"{results['percentages']['far_red_percentage']:.1f}%",
                "100.0%"
            ]
        }
        spectrum_df = pd.DataFrame(spectrum_data)
        st.dataframe(spectrum_df, use_container_width=True, hide_index=True)
    
    # 添加一个综合评价卡片
    st.markdown("---")
    st.subheader("📈 综合评价")
    
    # 计算一些评价指标
    ppe_rating = "优秀" if results['calculations']['ppe'] > 2.5 else "良好" if results['calculations']['ppe'] > 2.0 else "一般"
    par_rating = "优秀" if results['calculations']['par_ratio'] > 0.8 else "良好" if results['calculations']['par_ratio'] > 0.6 else "一般"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **⚡ PPE评价**: {ppe_rating}
        
        PPE (新): {results['calculations']['ppe']:.3f} μmol/J
        
        光能比: {results['calculations']['light_energy_ratio']:.3f}
        """)
    
    with col2:
        st.success(f"""
        **🌿 光质评价**: {par_rating}
        
        PAR占比: {results['calculations']['par_ratio']:.1%}
        
        R/B比: {results['calculations']['r_b_ratio']:.2f}
        """)
    
    with col3:
        st.warning(f"""
        **⚡ 能效总结**
        
        总功率: {results['input_params']['total_power']:.1f} W
        
        总光子通量: {results['calculations']['total_photon_flux']:.2f} μmol/s
        """)
    
    # 在最后添加报告下载功能
    st.markdown("---")
    st.header("📄 分析报告下载")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **📋 完整分析报告内容包括：**
        - 🏷️ 灯具基本信息（型号、制造商、测试日期）
        - ⚡ 电气参数（辐射通量、功率、温度、功率因数）
        - 🏆 综合评价和等级评定
        - 🎯 核心性能指标（PPE、PAR占比、R/B比、光能比）
        - 🌈 光谱分布图表和数据分析
        - 🧬 植物生理响应指标
        - 🌾 作物适应性评价（叶菜类、果菜类、育苗专用）
        - 📈 生长阶段适配性分析
        - 💰 能效与经济性分析
        - 💡 专业光谱优化建议
        - 📊 详细计算数据和方法说明
        """)
    
    with col2:
        # 生成报告内容
        if PDF_AVAILABLE:
            try:
                report_data = generate_pdf_report(results, df)
                mime_type = "application/pdf"
                file_ext = ".pdf"
                format_name = "PDF"
                
                # 生成文件名（包含灯具型号和日期）
                lamp_model = results.get('basic_info', {}).get('lamp_model', 'Unknown')
                test_date = results.get('basic_info', {}).get('test_date', 'Unknown')
                
                if lamp_model and lamp_model != '未填写' and lamp_model.strip():
                    # 清理文件名中的特殊字符
                    clean_model = "".join(c for c in lamp_model if c.isalnum() or c in (' ', '-', '_')).strip()
                    filename = f"LED光谱分析报告_{clean_model}_{test_date}{file_ext}"
                else:
                    filename = f"LED光谱分析报告_{test_date}{file_ext}"
                
                st.download_button(
                    label="📥 下载完整分析报告 (PDF)",
                    data=report_data,
                    file_name=filename,
                    mime=mime_type,
                    help="点击下载包含所有图表和分析数据的PDF报告",
                    use_container_width=True
                )
                
                st.success("✅ PDF报告生成成功！")
                st.info("📊 报告包含完整图表和专业分析数据")
                
            except Exception as e:
                st.error(f"❌ PDF报告生成失败：{str(e)}")
                st.info("💡 请确保分析数据完整后重试")
                # 显示详细错误信息用于调试
                if st.checkbox("显示详细错误信息"):
                    st.exception(e)
        else:
            # PDF库不可用时的处理
            st.error("❌ PDF生成功能不可用")
            
            # 检查运行环境并给出相应建议
            st.markdown("**💡 解决方案：**")
            
            with st.expander("🔧 在Streamlit Cloud上部署", expanded=True):
                st.markdown("""
                如果您在Streamlit Cloud上运行此应用，请确保您的GitHub仓库包含正确的 `requirements.txt` 文件：
                
                ```
                streamlit>=1.28.0
                pandas>=1.5.0
                numpy>=1.21.0
                plotly>=5.15.0
                matplotlib>=3.7.0
                seaborn>=0.12.0
                reportlab>=4.0.0
                Pillow>=10.0.0
                openpyxl>=3.0.0
                ```
                
                **部署步骤：**
                1. 在您的GitHub仓库根目录创建/更新 `requirements.txt` 文件
                2. 将上述内容添加到文件中
                3. 提交并推送更改到GitHub
                4. 在Streamlit Cloud中重新部署应用
                5. 等待依赖库安装完成（通常需要几分钟）
                """)
            
            with st.expander("💻 本地运行"):
                st.markdown("""
                如果您在本地运行此应用，请在终端中执行：
                ```bash
                pip install matplotlib seaborn reportlab Pillow
                ```
                然后重启应用。
                """)
            
            st.markdown("**📄 临时解决方案：**")
            st.info("当前将为您生成简化版HTML报告，包含主要分析数据但不含图表。")
            
            try:
                report_data = generate_simplified_report(results, df)
                mime_type = "text/html"
                file_ext = ".html"
                
                # 生成文件名
                lamp_model = results.get('basic_info', {}).get('lamp_model', 'Unknown')
                test_date = results.get('basic_info', {}).get('test_date', 'Unknown')
                
                if lamp_model and lamp_model != '未填写' and lamp_model.strip():
                    clean_model = "".join(c for c in lamp_model if c.isalnum() or c in (' ', '-', '_')).strip()
                    filename = f"LED光谱分析报告_{clean_model}_{test_date}{file_ext}"
                else:
                    filename = f"LED光谱分析报告_{test_date}{file_ext}"
                
                st.download_button(
                    label="📥 下载简化分析报告 (HTML)",
                    data=report_data,
                    file_name=filename,
                    mime=mime_type,
                    help="下载包含主要分析数据的HTML报告（不含图表）",
                    use_container_width=True
                )
                
                st.warning("⚠️ 当前为简化版HTML报告（不含图表）")
                
            except Exception as e:
                st.error(f"❌ 报告生成失败：{str(e)}")
                if st.checkbox("显示详细错误信息"):
                    st.exception(e)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; margin-top: 20px;'>
        <p>🌱 LED植物照明光学度量体系分析系统</p>
        <p>基于四种光学度量体系：辐射度学 | 光度学 | 光子度量学 | 植物光子度量学</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()