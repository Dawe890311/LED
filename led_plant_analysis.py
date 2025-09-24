import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    
    # 侧边栏 - 理论基础
    with st.sidebar:
        st.header("📚 理论基础")
        
        with st.expander("🔬 四种光学度量体系", expanded=True):
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
                results, df_clean = calculate_light_analysis(df, total_radiation_flux, total_power, back_panel_temp, power_factor)
                
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

def calculate_light_analysis(df, total_radiation_flux, total_power, back_panel_temp, power_factor):
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

if __name__ == "__main__":
    main()