# Data Architecture

PostgreSQL 保存权威业务数据；LangGraph Checkpoint 只保存执行状态；Redis 用于缓存、分布式锁和短期状态；对象存储保存大文件；pgvector 或向量数据库用于检索。

