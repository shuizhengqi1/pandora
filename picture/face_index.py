import torch
import numpy as np
import faiss
import glob

feature_files = glob.glob('./test/*.pt')
features = [torch.load(f) for f in feature_files]
features = torch.vstack(features).numpy()

# 创建Faiss索引
d = features.shape[1]  # 特征维度
index = faiss.IndexFlatL2(d)
index.add(features)


# 查询重合的特征
def search_similar_faces(query_feature, threshold=0.8):
    # 计算L2距离
    distances, indices = index.search(query_feature, k=1)
    # 转换为余弦相似度
    cosine_similarities = 1 - distances / 2
    # 找到相似度高于阈值的索引
    similar_indices = indices[cosine_similarities.flatten() > threshold]
    # 返回相似的特征文件
    return [feature_files[i] for i in similar_indices]


# 假设query_feature是要查询的人脸特征
query_feature = features[0:1]  # 拿第一张图片的特征作为示例
similar_faces = search_similar_faces(query_feature)
print(similar_faces)
