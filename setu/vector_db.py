import json
import chromadb
import random

class ImageVectorSearchSystem:
    def __init__(self):
        pass

    def init(self, db_path, collection_name="image_collection"):
        # 初始化 Chroma 客户端，设置数据持久化路径
        self.client = chromadb.PersistentClient(path=db_path)
        # 创建或获取集合
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        # 确保集合已经创建
        self.collection = self.client.get_collection(name=collection_name)

    def insert_data(self, image_id, image_description, feature_vector):
        """插入图片描述及其特征向量到数据库"""
        self.collection.add(
            documents=[image_description],
            embeddings=[feature_vector],
            ids=[image_id]
        )

    def search_by_vector(self, query_vector, n_results = 1):
        """根据特征向量检索数据"""
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=n_results,
            include=['embeddings', 'documents', 'metadatas', 'distances']
        )
        return results
    
    def random_choose(self):
        all_results = self.collection.get(
            include=['documents']
        )

        # 随机选择一个文档 ID
        random_result = random.choice(all_results['ids'])
        return random_result
    
    def get_data_by_id(self, id):
        results = self.collection.get(
            ids = [id],
            include=['embeddings', 'documents']
        )
        return results

    def load_data(self):
        """加载数据，由于使用 PersistentClient，此步骤通常是自动的"""
        self.collection = self.client.get_collection(name=self.collection.name)

    def save_data(self):
        """保存数据，PersistentClient 会自动处理数据持久化，此方法可能不是必须的"""
        self.collection.save()

    def close(self):
        """关闭数据库连接"""
        pass

# db
ivss = ImageVectorSearchSystem()
ivss_group = ImageVectorSearchSystem()

# 使用示例
if __name__ == "__main__":
    SETU_ROOT = '../setu'
    ivss.init(db_path=SETU_ROOT + '/CLIP/data/setudb_purify_240606', collection_name='setu')
    ivss_group.init(db_path=SETU_ROOT + '/CLIP/data/setudb_group_240708', collection_name='setu')
    print(len(ivss.collection.get()['ids']))
    print(ivss_group.collection.get())
    # # 初始化系统
    # db_system = ImageVectorSearchSystem()
    # db_system.init(db_path="./test.db")

    # # 清空数据
    # all_ids = db_system.collection.get()['ids']
    # # db_system.collection.delete(ids=all_ids)
    # print(db_system.collection.get(include=['embeddings', 'documents', 'metadatas']))

    # # 插入图片数据
    # db_system.insert_data(image_id='id', image_description="{'url':'test.url'}", feature_vector=[1,1,1,1])
    # print(db_system.collection.get(include=['embeddings', 'documents', 'metadatas']))
    
    # # 检索相似图片
    # query_vector = [1,1,1,-1]
    # similar_images = db_system.search_by_vector(query_vector, n_results=5)
    # print(similar_images)
    
    # # 数据库关闭前确保保存数据
    # db_system.close()