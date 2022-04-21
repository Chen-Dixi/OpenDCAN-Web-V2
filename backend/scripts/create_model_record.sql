-- opendcan_v2.task_record definition

CREATE TABLE `model_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) DEFAULT NULL COMMENT '模型名称，文件名称',
  `task_id` int NOT NULL COMMENT '所属task id',
  `file_path` varchar(128) DEFAULT NULL COMMENT '文件在系统中的路径位置, 包含文件名',
  `model_type` tinyint DEFAULT NULL COMMENT '模型类型, 1 PyTorch 2 Tensorflow 暂时用不到',
  `state` tinyint NOT NULL DEFAULT '2' COMMENT '1: TRAINING 2: READY READY状态下才能被选择用于推理标注',
  `source_id` int DEFAULT NULL COMMENT '源域数据集id',
  `source_name` varchar(120) DEFAULT NULL COMMENT '源域数据集名称, 冗余字段',
  `target_id` int DEFAULT NULL COMMENT '目标域数据集id',
  `target_name` varchar(120) DEFAULT NULL COMMENT '目标域数据集名称, 冗余字段',
  `create_name` varchar(100) DEFAULT NULL COMMENT '启动模型训练的人',
  `update_name` varchar(100) DEFAULT NULL COMMENT '更新模型信息的人',
  `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
  CONSTRAINT `pk_id` PRIMARY KEY (`id`),
  KEY `model_record_idx_task_id` (`task_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;