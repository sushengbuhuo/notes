import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import os
import base64

def merge_excel_files(uploaded_files, skip_rows=0, filter_column=None, keywords=None, exclude_mode=True):
    """
    合并多个Excel文件，支持跳过行数和关键词排除过滤 python -m streamlit run excel_merge.py
    """
    all_dfs = []
    
    for uploaded_file in uploaded_files:
        try:
            # 读取Excel文件，跳过指定行数https://www.52pojie.cn/thread-2072230-1-1.html
            df = pd.read_excel(uploaded_file, skiprows=skip_rows, engine='openpyxl')
            
            # 添加文件名列以便追踪数据来源
            df['_source_file'] = uploaded_file.name
            
            all_dfs.append(df)
            
        except Exception as e:
            st.error(f"读取文件 {uploaded_file.name} 时出错: {str(e)}")
            continue
    
    if not all_dfs:
        st.error("没有成功读取任何Excel文件")
        return None
    
    # 合并所有DataFrame
    try:
        merged_df = pd.concat(all_dfs, ignore_index=True)
    except Exception as e:
        st.error(f"合并数据时出错: {str(e)}")
        return None
    
    # 应用关键词排除过滤
    if filter_column and keywords:
        merged_df = exclude_by_keywords(merged_df, filter_column, keywords, exclude_mode)
    
    return merged_df

def exclude_by_keywords(df, column, keywords_text, exclude_mode=True):
    """
    根据关键词排除数据
    """
    if column not in df.columns:
        st.warning(f"列 '{column}' 在数据中不存在，跳过过滤")
        return df
    
    # 处理关键词输入：支持逗号或空格分隔
    keywords_text = keywords_text.strip()
    if ',' in keywords_text:
        keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
    else:
        keywords = [kw.strip() for kw in keywords_text.split() if kw.strip()]
    
    if not keywords:
        return df
    
    # 构建排除条件
    try:
        # 尝试将关键词转换为数值（用于数字列过滤）
        numeric_keywords = []
        string_keywords = []
        
        for kw in keywords:
            try:
                # 尝试转换为float
                num_val = float(kw)
                numeric_keywords.append(num_val)
            except ValueError:
                string_keywords.append(kw)
        
        # 构建匹配条件（需要排除的数据）
        exclude_conditions = []
        
        # 数值条件
        if numeric_keywords:
            num_condition = df[column].astype(float).isin(numeric_keywords)
            exclude_conditions.append(num_condition)
        
        # 文本条件
        if string_keywords:
            str_conditions = []
            for kw in string_keywords:
                # 使用contains进行部分匹配
                str_conditions.append(df[column].astype(str).str.contains(kw, case=False, na=False))
            
            if str_conditions:
                str_condition = pd.concat(str_conditions, axis=1).any(axis=1)
                exclude_conditions.append(str_condition)
        
        if exclude_conditions:
            # 合并所有排除条件（OR关系）
            final_exclude_condition = pd.concat(exclude_conditions, axis=1).any(axis=1)
            
            # 排除匹配的数据
            filtered_df = df[~final_exclude_condition]
            
            excluded_count = len(df) - len(filtered_df)
            st.success(f"排除过滤完成: 保留 {len(filtered_df)} 行，排除 {excluded_count} 行")
            
            # 显示被排除的数据样本（如果有）
            if excluded_count > 0:
                with st.expander("查看被排除的数据样本"):
                    excluded_data = df[final_exclude_condition].head(10)
                    st.dataframe(excluded_data, width = 'stretch')
                    if len(excluded_data) < excluded_count:
                        st.caption(f"显示前10条被排除数据，共排除{excluded_count}条")
            
            return filtered_df
        else:
            return df
            
    except Exception as e:
        st.error(f"排除数据时出错: {str(e)}")
        return df

def to_excel_bytes(df):
    """将DataFrame转换为Excel字节数据"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Streamlit界面设计
def main():
    st.set_page_config(page_title="Excel多文件合并工具", page_icon="📊", layout="wide")
    
    st.title("📊 Excel多文件合并工具")
    st.markdown("上传多个Excel文件，合并数据并支持**排除过滤**功能")
    
    # 文件上传区域
    st.header("1. 上传Excel文件")
    uploaded_files = st.file_uploader(
        "选择多个Excel文件",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="支持 .xlsx 和 .xls 格式的文件"
    )
    
    if not uploaded_files:
        st.info("请上传一个或多个Excel文件以继续")
        return
    
    st.success(f"已上传 {len(uploaded_files)} 个文件: {[f.name for f in uploaded_files]}")
    
    # 配置选项
    st.header("2. 合并配置")
    
    skip_rows = st.number_input(
        "跳过行数",
        min_value=0,
        value=0,
        help="从每个Excel文件开头跳过的行数"
    )
    
    st.markdown("**数据预览**")
    if st.button("预览第1个文件"):
        if uploaded_files:
            sample_df = pd.read_excel(uploaded_files[0], skiprows=skip_rows, engine='openpyxl')
            with st.expander(f"预览: {uploaded_files[0].name} (共 {len(sample_df)} 行, {len(sample_df.columns)} 列)", expanded=True):
                sample_df.index = range(1, len(sample_df)+1)
                st.dataframe(sample_df.head(10), width = 'stretch')
                # st.caption(f"预览: {uploaded_files[0].name} (共 {len(sample_df)} 行, {len(sample_df.columns)} 列)")
    
    # 过滤选项
    st.header("3. 数据排除过滤")
    
    st.info("🔍 **排除模式**: 输入关键词，匹配这些关键词的数据将被排除")
    
    filter_col1, filter_col2 = st.columns([2, 1])
    
    with filter_col1:
        # 动态获取列名（基于第一个文件）
        if uploaded_files:
            try:
                sample_df = pd.read_excel(uploaded_files[0], skiprows=skip_rows, engine='openpyxl')
                columns = sample_df.columns.tolist()
                
                filter_column = st.selectbox(
                    "选择排除列",
                    options=columns,
                    index=0,
                    help="选择要应用关键词排除的列"
                )
                
            except Exception as e:
                st.error(f"读取文件结构时出错: {str(e)}")
                filter_column = None
        else:
            filter_column = None
    
    with filter_col2:
        keywords_input = st.text_input(
            "排除关键词（多个用逗号或空格分隔）",
            help="用逗号或空格分隔多个关键词，匹配的数据将被排除"
        )
    
    # 执行合并
    if st.button("开始合并", type="primary", width='stretch'):
        if not uploaded_files:
            st.error("请先上传Excel文件")
            return
        
        with st.spinner("正在合并Excel文件..."):
            # 执行合并
            merged_data = merge_excel_files(
                uploaded_files=uploaded_files,
                skip_rows=skip_rows,
                filter_column=filter_column,
                keywords=keywords_input if keywords_input.strip() else None
            )
        
        st.success("✅ 文件合并完成！")
        
        # 显示合并结果
        st.header("合并结果")
        
        # 基本信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总行数", len(merged_data))
        with col2:
            st.metric("总列数", len(merged_data.columns))
        with col3:
            st.metric("源文件数", len(uploaded_files))
        
        # 数据预览
        st.subheader("数据预览")
        merged_data.index = range(1,len(merged_data)+1)
        st.dataframe(merged_data, width = 'stretch')
        
        # 数据统计
        st.subheader("数据统计")
        numeric_cols = merged_data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            st.dataframe(merged_data[numeric_cols].describe(), width = 'stretch')

        if merged_data is not None:
            # 删除所有列都是NaN的行
            merged_data = merged_data[merged_data.notnull().all(axis=1)]
        
            # 数据清理
            merged_data = merged_data.drop('_source_file', axis=1)
            
            # 保存到session state以便下载使用
            st.session_state['merged_data'] = merged_data

    # 下载功能 - 独立显示，不依赖页面刷新
    if 'merged_data' in st.session_state and st.session_state['merged_data'] is not None:
        st.header("下载合并结果")
        
        # 文件名输入
        download_filename = st.text_input("下载文件名", value="Excel数据合并结果.xlsx")
        
        if not download_filename.endswith('.xlsx'):
            download_filename += '.xlsx'
        
        # 转换为Excel字节数据
        excel_data = to_excel_bytes(st.session_state['merged_data'])
        
        # st.download_button(
            # label="📥 下载合并后的Excel文件",
            # data=excel_data,
            # file_name=download_filename,
            # mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            # type="primary"
        # )
        
        # 对数据进行Base64编码
        b64_data = base64.b64encode(excel_data).decode()
        # 构建下载链接
        download_href = f'<a href="data:file/csv;base64,{b64_data}" download="{download_filename}">📥 下载合并后的Excel文件</a>'

        # 使用st.markdown渲染链接
        st.markdown(download_href, unsafe_allow_html=True)
        
        st.success(f"文件已准备好下载: {download_filename}")

# 侧边栏信息
def sidebar_info():
    with st.sidebar:
        st.title("ℹ️ 使用说明")
        
        st.markdown("""
        ### 功能特性
        - **多文件上传**: 支持同时上传多个Excel文件
        - **跳过行数**: 可跳过每个文件开头的指定行数
        - **排除过滤**: 按列排除，支持多关键词
        - **灵活分隔**: 关键词支持逗号或空格分隔
        
        ### 排除过滤说明
        - **排除模式**: 匹配关键词的数据将被**移除**
        - **数字列**: 自动识别数值关键词
        - **文本列**: 支持部分匹配（包含关系）
        - **多关键词**: 满足任一关键词即被排除
        
        ### 使用技巧
        1. 上传前确保文件格式正确
        2. 使用预览功能检查数据结构
        3. 排除关键词不区分大小写
        4. 可查看被排除的数据样本
        5. 下载前可自定义文件名
        """)

if __name__ == "__main__":
    main()
    sidebar_info()