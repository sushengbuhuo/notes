import streamlit as st
import pandas as pd
import base64
import io
from typing import List, Tuple
import os
import zipfile

# 页面设置
st.set_page_config(
    page_title="Excel文件格式批量转换工具",
    page_icon="📊",
    layout="wide"
)

# 标题和描述
st.title("📊 Excel文件格式批量转换工具")
st.markdown("""
这个工具可以帮助您：
- **批量上传** XLSX 和 XLS 格式的Excel文件
- **互相转换** 文件格式（XLSX ↔ XLS 或 XLS ↔ XLSX）
- **预览数据** 确保转换结果符合预期
- **批量下载** 转换后的文件
""")

def setup_work_directory():
    """设置工作目录，确保文件操作在正确路径下执行"""
    try:
        work_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(work_dir)
        return True
    except Exception as e:
        st.warning(f"工作目录设置注意事项：{e}")
        return True

def read_excel_file(file) -> pd.DataFrame:
    """
    读取Excel文件并返回DataFrame
    
    Parameters:
    file: 上传的文件对象
    
    Returns:
    pd.DataFrame: 读取的Excel数据
    """
    try:
        # 根据文件类型使用适当的读取方法[citation:1]
        if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            df = pd.read_excel(file)
            return df
        else:
            st.error(f"不支持的文件格式: {file.name}")
            return None
    except Exception as e:
        st.error(f"读取文件 {file.name} 时出错: {str(e)}")
        return None

def convert_dataframe_to_excel(df: pd.DataFrame, file_format: str) -> bytes:
    """
    将DataFrame转换为指定格式的Excel字节数据
    
    Parameters:
    df: 要转换的DataFrame
    file_format: 目标格式 ('xlsx' 或 'xls')
    
    Returns:
    bytes: Excel文件的字节数据
    """
    try:
        output = io.BytesIO()
        
        if file_format == 'xlsx':
            # 写入xlsx格式[citation:1]
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
        else:
            # 写入xls格式 xlwt
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
        
        excel_data = output.getvalue()
        return excel_data
    except Exception as e:
        st.error(f"转换数据时出错: {str(e)}")
        return None

def create_download_link(excel_data: bytes, filename: str, link_text: str) -> str:
    """
    创建下载链接[citation:4][citation:6]
    
    Parameters:
    excel_data: Excel文件的字节数据
    filename: 下载的文件名
    link_text: 链接显示文本
    
    Returns:
    str: HTML下载链接
    """
    try:
        # 将字节数据编码为base64字符串[citation:4]
        b64 = base64.b64encode(excel_data).decode()
        href = f'<a href="data:application/vnd.ms-excel;base64,{b64}" download="{filename}" style="display: inline-block; padding: 0.5em 1em; margin: 0.2em; background-color: #f0f2f6; color: #31333f; text-decoration: none; border-radius: 0.3em; border: 1px solid #d0d0d0;">{link_text}</a>'
        return href
    except Exception as e:
        st.error(f"创建下载链接时出错: {str(e)}")
        return ""

def display_data_preview(df: pd.DataFrame, filename: str):
    """
    显示数据预览[citation:3]
    
    Parameters:
    df: 要预览的DataFrame
    filename: 文件名
    """
    # st.subheader(f"📋 数据概览: {filename}")
    with st.expander(f'数据概览：{filename}', expanded=True):
    
        # 显示文件基本信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("行数", df.shape[0])
        with col2:
            st.metric("列数", df.shape[1])
        with col3:
            st.metric("文件大小", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # 显示交互式数据框[citation:3]
    with st.expander(f'数据预览：{filename}'):
        df.index = range(1,len(df)+1)
        st.dataframe(df, width = 'stretch')
    
    # 显示数据类型信息
    with st.expander("查看数据类型信息"):
        st.write(df.dtypes)

def main():
    """主应用函数"""
    
    # 设置工作目录
    # setup_work_directory()

    # 转换设置
    st.sidebar.header("⚙️ 转换设置")
    # st.sidebar.header("📁 文件上传设置")
    
    # 使用提示和优化建议
    with st.sidebar.expander("💡 使用提示和优化建议", expanded=True):
        st.markdown("""
        **性能优化建议：**
        - 单个文件建议不超过10MB以获得最佳性能
        - 对于大型文件，转换可能需要较长时间
        - 确保文件没有被其他程序打开
        
        **功能特点：**
        - ✅ 支持批量上传和转换
        - ✅ 实时数据预览
        - ✅ 保持原始数据格式
        - ✅ 批量下载功能(ZIP)
        
        **注意事项：**
        - XLS格式有行数限制（65,536行）
        - 复杂格式可能会在转换过程中有所变化
        - 建议转换后检查数据完整性
        """)
        for _ in range(8):
            st.write('  ')
    
    # 文件上传区域[citation:2][citation:6]
    uploaded_files = st.file_uploader(
        "选择Excel文件",
        type=["xlsx", "xls"],
        accept_multiple_files=True,
        help="支持批量上传XLSX和XLS格式的Excel文件"
    )
    
    if not uploaded_files:
        st.info("👆 请在上传Excel文件（支持.xlsx和.xls格式）")
        return
    
    st.success(f"已上传 {len(uploaded_files)} 个文件")
    
    target_format = 'xlsx'
    
    # 显示上传的文件列表
    st.header("📄 已上传的文件")
    file_cols = st.columns(3)
    for i, file in enumerate(uploaded_files):
        with file_cols[i % 3]:
            st.text(f"• {file.name} ")
    
    
    # 存储文件信息
    converted_files = []
            
    if st.button("开始批量转换", type="primary", width="stretch"):
        files_to_process = uploaded_files
    
        # 处理选中的文件
        for i,file in enumerate(files_to_process):
            with st.spinner(f"正在处理 {file.name}..."):
                # 读取Excel文件[citation:9]
                df = read_excel_file(file)
                if df is not None:
                    
                    # 转换文件格式
                    original_format = 'xlsx' if file.name.endswith('.xlsx') else 'xls'
                    target_format = 'xls' if file.name.endswith('.xlsx') else 'xlsx'
                    
                    # 显示文件
                    st.write(f'### {i+1}. {file.name} -> 新格式：{target_format} ')
                    with st.expander('转换详情... '):
                        # 显示数据预览
                        display_data_preview(df, file.name)
                    
                    # 生成新文件名
                    new_filename = file.name.replace(f".{original_format}", f"_converted.{target_format}")
                    
                    # 转换数据
                    excel_data = convert_dataframe_to_excel(df, target_format)
                    
                    if excel_data:
                        # 创建下载链接[citation:4][citation:6]
                        # download_link = create_download_link(
                            # excel_data, 
                            # new_filename,
                            # f"📥 下载 {new_filename}"
                        # )
                        
                        # # 显示下载链接
                        # st.markdown(download_link, unsafe_allow_html=True)
                        
                        # 保存转换信息
                        converted_files.append({
                            'original_name': file.name,
                            'new_name': new_filename,
                            'data': excel_data,
                            'dataframe': df,
                            'format': target_format
                        })
                        
                        st.success(f"✅ {file.name} 转换完成！")
    
    # 批量下载区域
    if len(converted_files) > 1:
        st.header("📦 批量下载")
        st.markdown("---")
        
        # 统计信息
        if converted_files:
            st.subheader("📊 转换统计")
            cols = st.columns(2)
            cols[0].metric("目标格式", target_format.upper())
            cols[1].metric("成功转换文件数", len(converted_files))

        
        # 显示单个下载链接
        download_cols = st.columns(2)
        for i, converted_file in enumerate(converted_files):
            with download_cols[i % 2]:
                batch_download_link = create_download_link(
                    converted_file['data'],
                    converted_file['new_name'],
                    f"📥 {converted_file['new_name']}"
                )
                st.markdown(batch_download_link, unsafe_allow_html=True)
        
        # 创建ZIP文件
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_info in converted_files:
                zip_file.writestr(file_info["new_name"], file_info["data"])
        
        zip_data = zip_buffer.getvalue()
        
        # 提供ZIP文件下载
        # st.download_button(
            # label="📦 一键下载所有文件 (ZIP包)",
            # data=zip_data,
            # file_name=f"Excel文件转换为{target_format}.zip",
            # mime="application/zip",
            # type="primary"  # 突出显示主要操作按钮[citation:2]
        # )
        # 对数据进行Base64编码
        b64_data = base64.b64encode(zip_data).decode()
        # 构建下载链接
        file_name = f"Excel文件转换为{target_format}.zip"
        download_href = f'<a href="data:file/csv;base64,{b64_data}" download="{file_name}">📦 一键下载所有文件 (ZIP包)</a>'
        # 使用st.markdown渲染链接
        st.markdown(download_href, unsafe_allow_html=True)

        st.success(f"文件已准备好下载: {file_name}")


if __name__ == "__main__":
    main()