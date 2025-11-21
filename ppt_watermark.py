import os
import cv2
import numpy as np
from PIL import Image, ImageStat
from typing import List, Dict, Tuple
from utils.logger import Logger
from config import WATERMARK_SIZE_THRESHOLD, WATERMARK_OPACITY_THRESHOLD, WATERMARK_POSITION_WEIGHTS, WATERMARK_DETECTION_THRESHOLD
 
 
class WatermarkDetector:
    """水印检测器"""
 
    def __init__(self):
        self.logger = Logger.get_logger()
 
    def detect_watermarks(self, images: List[Dict]) -> List[Dict]:
        """
        检测图片中的水印
         
        Args:
            images: 图片信息列表
             
        Returns:
            标记了水印的图片信息列表
             
        Note:
            使用配置文件中的 WATERMARK_DETECTION_THRESHOLD 作为判定阈值
        """
        self.logger.info(f"开始检测 {len(images)} 张图片中的水印")
         
        for image in images:
            try:
                # 计算水印概率
                watermark_score = self._calculate_watermark_score(image)
                 
                # 根据分数判断是否为水印（使用配置文件中的阈值）
                image['watermark_score'] = watermark_score
                image['is_watermark'] = watermark_score >= WATERMARK_DETECTION_THRESHOLD
                 
                if image['is_watermark']:
                    self.logger.debug(f"图片 {image['id']} 被识别为水印，分数: {watermark_score:.2f} (阈值: {WATERMARK_DETECTION_THRESHOLD})")
                else:
                    self.logger.debug(f"图片 {image['id']} 不被识别为水印，分数: {watermark_score:.2f} (阈值: {WATERMARK_DETECTION_THRESHOLD})")
                     
            except Exception as e:
                self.logger.error(f"检测图片 {image.get('id', 'unknown')} 水印时出错: {str(e)}")
                image['watermark_score'] = 0.0
                image['is_watermark'] = False
         
        watermark_count = sum(1 for img in images if img['is_watermark'])
        self.logger.info(f"水印检测完成，发现 {watermark_count} 张疑似水印图片")
         
        return images
 
    def _calculate_watermark_score(self, image: Dict) -> float:
        """计算图片是水印的概率分数"""
        score = 0.0
         
        # 1. 基于大小的评分 (0-0.3)
        size_score = self._calculate_size_score(image)
        score += size_score * 0.3
         
        # 2. 基于位置的评分 (0-0.3)
        position_score = self._calculate_position_score(image)
        score += position_score * 0.3
         
        # 3. 基于透明度的评分 (0-0.2)
        transparency_score = self._calculate_transparency_score(image)
        score += transparency_score * 0.2
         
        # 4. 基于颜色复杂度的评分 (0-0.2)
        color_score = self._calculate_color_score(image)
        score += color_score * 0.2
         
        return min(score, 1.0)  # 确保分数不超过1.0
 
    def _calculate_size_score(self, image: Dict) -> float:
        """
        基于大小计算水印分数，结合相对大小和绝对大小
         
        Args:
            image: 图片信息字典，包含size_percent（相对大小百分比）和width、height（绝对像素尺寸）
             
        Returns:
            float: 水印分数，范围0-1
        """
        size_percent = image.get('size_percent', 0)
        width = image.get('width', 0)
        height = image.get('height', 0)
         
        # 1. 基于相对大小的评分 (权重60%)
        if size_percent < WATERMARK_SIZE_THRESHOLD * 100:
            relative_score = 1.0
        else:
            # 随着尺寸增大，水印概率降低
            relative_score = max(0, 1.0 - (size_percent - WATERMARK_SIZE_THRESHOLD * 100) / 20)
         
        # 2. 基于绝对大小的评分 (权重40%)
        # 水印通常绝对尺寸也较小
        # 计算图片的绝对面积（像素）
        absolute_area = width * height
         
        # 设置绝对大小的阈值（可根据实际情况调整）
        # 小于500x500的图片更可能是水印
        absolute_threshold = 500 * 500  # 250000像素
         
        if absolute_area <= absolute_threshold:
            absolute_score = 1.0
        else:
            # 随着绝对面积增大，水印概率降低
            # 使用对数缩放，避免大尺寸图片得分过低
            import math
            excess_ratio = math.log(absolute_area / absolute_threshold) / math.log(10)  # 以10为底的对数
            absolute_score = max(0, 1.0 - excess_ratio * 0.2)  # 每增加10倍面积，分数降低0.2
         
        # 综合评分：相对大小权重60%，绝对大小权重40%
        final_score = relative_score * 0.6 + absolute_score * 0.4
         
        return min(final_score, 1.0)  # 确保分数不超过1.0
 
    def _calculate_position_score(self, image: Dict) -> float:
        """基于位置计算水印分数"""
        position_type = image.get('position_type', 'other')
         
        # 根据位置类型返回相应的权重
        return WATERMARK_POSITION_WEIGHTS.get(position_type, 0.1)
 
    def _calculate_transparency_score(self, image: Dict) -> float:
        """基于透明度计算水印分数，并添加透明度信息到图片数据"""
        try:
            # 读取图片
            img_path = image.get('temp_path')
            if not img_path or not os.path.exists(img_path):
                image['opacity'] = 1.0  # 默认完全不透明
                return 0.0
                 
            # 使用PIL读取图片
            img = Image.open(img_path)
             
            # 如果是RGBA模式，检查alpha通道
            if img.mode == 'RGBA':
                alpha = img.split()[-1]  # 获取alpha通道
                alpha_mean = ImageStat.Stat(alpha).mean[0] / 255  # 归一化到0-1
                 
                # 保存透明度信息到图片数据
                image['opacity'] = alpha_mean
                 
                # 透明度越低（alpha_mean越小），越可能是水印
                return max(0, 1.0 - alpha_mean)
            else:
                # 如果不是RGBA模式，设置透明度为1.0（完全不透明）
                image['opacity'] = 1.0
                 
            # 如果没有透明度信息，返回中等分数
            return 0.5
             
        except Exception as e:
            self.logger.warning(f"计算图片透明度分数时出错: {str(e)}")
            image['opacity'] = 1.0  # 出错时默认完全不透明
            return 0.5
 
    def _calculate_color_score(self, image: Dict) -> float:
        """基于颜色复杂度计算水印分数"""
        try:
            # 读取图片
            img_path = image.get('temp_path')
            if not img_path or not os.path.exists(img_path):
                return 0.0
                 
            # 使用OpenCV读取图片
            img = cv2.imread(img_path)
            if img is None:
                return 0.0
                 
            # 转换为HSV颜色空间
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
             
            # 计算颜色直方图
            hist_h = cv2.calcHist([hsv], [0], None, [180], [0, 180])
            hist_s = cv2.calcHist([hsv], [1], None, [256], [0, 256])
            hist_v = cv2.calcHist([hsv], [2], None, [256], [0, 256])
             
            # 归一化直方图
            cv2.normalize(hist_h, hist_h, 0, 1, cv2.NORM_MINMAX)
            cv2.normalize(hist_s, hist_s, 0, 1, cv2.NORM_MINMAX)
            cv2.normalize(hist_v, hist_v, 0, 1, cv2.NORM_MINMAX)
             
            # 计算颜色复杂度（熵）
            def calculate_entropy(hist):
                entropy = 0
                for i in range(len(hist)):
                    if hist[i] > 0:
                        # 确保 hist[i] 是标量值
                        value = float(hist[i])
                        entropy -= value * np.log2(value)
                return entropy
             
            entropy_h = calculate_entropy(hist_h)
            entropy_s = calculate_entropy(hist_s)
            entropy_v = calculate_entropy(hist_v)
             
            # 平均熵
            avg_entropy = (entropy_h + entropy_s + entropy_v) / 3
             
            # 水印通常颜色简单，熵较低
            # 将熵值转换为0-1的分数，熵越低分数越高
            max_entropy = 8.0  # 理论最大熵值
            color_score = max(0, 1.0 - avg_entropy / max_entropy)
             
            return color_score
             
        except Exception as e:
            self.logger.warning(f"计算图片颜色分数时出错: {str(e)}")
            return 0.5
 
    def set_watermark_manually(self, images: List[Dict], image_ids: List[str], is_watermark: bool):
        """手动设置图片的水印状态"""
        for image in images:
            if image['id'] in image_ids:
                image['is_watermark'] = is_watermark
                self.logger.info(f"手动设置图片 {image['id']} 为 {'水印' if is_watermark else '非水印'}")
 
    def get_watermark_images(self, images: List[Dict]) -> List[Dict]:
        """获取所有被标记为水印的图片"""
        return [img for img in images if img['is_watermark']]