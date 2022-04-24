from email.policy import default
from operator import index
from sqlalchemy import BIGINT, Column, ForeignKey, Integer, String, VARCHAR

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(VARCHAR, unique=True, index=True)
    hashed_password = Column(VARCHAR)
    username = Column(VARCHAR)
    display_name = Column(VARCHAR)
    user_type = Column(Integer, default=1) # 1 管理员; 2 普通用户
    is_active = Column(Integer, default=1) # 1 active; 2 disabled
    create_time = Column(BIGINT)
    update_time = Column(BIGINT)

class TargetDatasetRecord(Base):
    __tablename__ = "target_dataset_record"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR)
    description = Column(VARCHAR)
    file_path = Column(VARCHAR)
    username = Column(VARCHAR)
    state = Column(Integer, default=2)  # 1 ready, 2 not ready
    create_name = Column(VARCHAR)
    update_name = Column(VARCHAR)
    is_active = Column(Integer, default=1) # 1 active; 2 disabled
    create_time = Column(BIGINT)
    update_time = Column(BIGINT)

class SourceDatasetRecord(Base):
    """
      `id` int NOT NULL AUTO_INCREMENT,
      `title` varchar(120) DEFAULT NULL COMMENT '数据集名称',
      `description` varchar(800) DEFAULT NULL COMMENT '数据集详情描述',
      `file_path` varchar(128) DEFAULT NULL COMMENT '文件在系统中的路径位置',
      `state` tinyint NOT NULL DEFAULT '2' COMMENT '1: 可使用 2: 未准备好',
      `labels` varchar(1000) DEFAULT NULL COMMENT '标签列表的json字符串, 标签在列表中的位置即为标签id',
      `label_num` int NOT NULL DEFAULT '0' COMMENT '标签种类数量',
      `create_name` varchar(100) DEFAULT NULL COMMENT '上传数据集的人',
      `update_name` varchar(100) DEFAULT NULL COMMENT '最近更新数据集信息的人',
      `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
      `create_time` bigint DEFAULT NULL,
      `update_time` bigint DEFAULT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `source_dataset_record_idx_file_path` (`file_path`) USING BTREE,
      KEY `source_dataset_record_idx_update_time` (`update_time`) USING BTREE
    """

    __tablename__ = "source_dataset_record"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR)
    description = Column(VARCHAR)
    file_path = Column(VARCHAR)
    state = Column(Integer, default=2)  # 1 ready, 2 not ready
    labels = Column(VARCHAR)
    label_num = Column(Integer, default=0)
    create_name = Column(VARCHAR)
    update_name = Column(VARCHAR)
    is_active = Column(Integer, default=1) # 1 active; 2 disabled
    create_time = Column(BIGINT)
    update_time = Column(BIGINT, index=True)

class TaskRecord(Base):
    """
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) DEFAULT NULL COMMENT '任务名称',
  `username` varchar(100) NOT NULL COMMENT '本属于属于哪个用户',
  `state` tinyint NOT NULL DEFAULT '2' COMMENT '1: IDLE 2: TRAINING 3: READY',
  `source_id` int DEFAULT NULL COMMENT '源域数据集id',
  `source_name` varchar(120) DEFAULT NULL COMMENT '源域数据集名称, 冗余字段',
  `target_id` int DEFAULT NULL COMMENT '目标域数据集id',
  `target_name` varchar(120) DEFAULT NULL COMMENT '目标域数据集名称, 冗余字段',
  `create_name` varchar(100) DEFAULT NULL COMMENT '上传数据集的人',
  `update_name` varchar(100) DEFAULT NULL COMMENT '更新数据集信息的人',
  `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
    """
    __tablename__ = "task_record"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR)
    username = Column(VARCHAR, index=True)
    state = Column(Integer, default=2)  # 1 ready, 2 not ready
    source_id = Column(Integer)
    source_name = Column(VARCHAR)
    target_id = Column(Integer)
    target_name = Column(VARCHAR)

    create_name = Column(VARCHAR)
    update_name = Column(VARCHAR)
    is_active = Column(Integer, default=1) # 1 active; 2 disabled
    create_time = Column(BIGINT)
    update_time = Column(BIGINT)

class ModelRecord(Base):
    """
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL COMMENT '模型名称，文件名称',
  `task_id` int NOT NULL COMMENT '所属task id',
  `file_path` varchar(128) DEFAULT NULL COMMENT '文件在系统中的路径位置, 包含文件名',
  `model_type` tinyint DEFAULT NULL COMMENT '模型类型, 1 PyTorch 2 Tensorflow 暂时用不到',
  `state` tinyint NOT NULL DEFAULT '2' COMMENT '1: READY 2: TRAINING READY状态下才能被选择用于推理标注',
  `source_id` int DEFAULT NULL COMMENT '源域数据集id',
  `source_name` varchar(120) DEFAULT NULL COMMENT '源域数据集名称, 冗余字段',
  `target_id` int DEFAULT NULL COMMENT '目标域数据集id',
  `target_name` varchar(120) DEFAULT NULL COMMENT '目标域数据集名称, 冗余字段',
  `create_name` varchar(100) DEFAULT NULL COMMENT '上传数据集的人',
  `update_name` varchar(100) DEFAULT NULL COMMENT '更新数据集信息的人',
  `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
  CONSTRAINT `pk_id` PRIMARY KEY (`id`),
  KEY `model_record_idx_task_id` (`task_id`) USING BTREE
    """
    __tablename__ = "model_record"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(VARCHAR)
    task_id = Column(Integer, index=True)
    file_path = Column(VARCHAR)
    model_type = Column(Integer)
    state = Column(Integer, default=2)  # 1 ready, 2 training
    source_id = Column(Integer)
    source_name = Column(VARCHAR)
    target_id = Column(Integer)
    target_name = Column(VARCHAR)
    
    create_name = Column(VARCHAR)
    update_name = Column(VARCHAR)
    is_active = Column(Integer, default=1) # 1 active; 2 disabled
    create_time = Column(BIGINT)
    update_time = Column(BIGINT)