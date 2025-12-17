-- 批量插入历史需求数据
-- 注意：这里使用子查询 (SELECT id FROM users ...) 自动根据人名查找对应的 ID

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '交银理财周度权益基金筛选', '', '基金筛选', '权益', '交银理财', '理财',
    (SELECT id FROM users WHERE display_name = '李迎圣'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-03 00:00:00', '2025-11-03 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '月度债市股市点评', '', '报告|定制', '资产配置', '融通财险', '保险',
    (SELECT id FROM users WHERE display_name = '李迎圣'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-03 00:00:00', '2025-11-03 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '上海银行周报', '', '报告|定制', '资产配置', '上海银行', '银行自营',
    (SELECT id FROM users WHERE display_name = '李迎圣'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-03 00:00:00', '2025-11-03 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '中银理财市场观点周报', '', '报告|定制', '资产配置', '中银理财', '理财',
    (SELECT id FROM users WHERE display_name = '孙宇萌'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-03 00:00:00', '2025-11-03 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '固收+基金客户模拟组合列表底稿修改（DS）', '', '生产化|提效', '固收＋', '东方证券', '券商',
    (SELECT id FROM users WHERE display_name = '刘仟一'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-04 00:00:00', '2025-11-04 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '公募fof、商品型基金、互认基金、QDII基金及含ABS高的不含权基金筛选', '', '基金筛选', '纯债', '英大资本', '保险',
    (SELECT id FROM users WHERE display_name = '孙宇萌'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-04 00:00:00', '2025-11-04 00:00:00', 2.5, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '固收+标签及数据更新', '', '基金筛选', '固收＋', '中海信托', '信托',
    (SELECT id FROM users WHERE display_name = '姚芳'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-05 00:00:00', '2025-11-05 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    'QDII权益型基金筛选', '', '基金筛选', '权益', '中信信托', '信托',
    (SELECT id FROM users WHERE display_name = '吴泽航'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-05 00:00:00', '2025-11-05 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '40只基金入库报告信息整理', '', '报告|定制', '固收＋', '海通资管', '券商',
    (SELECT id FROM users WHERE display_name = '段颖'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-06 00:00:00', '2025-11-06 00:00:00', 2.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '10月基金经理市场观点', '', '报告|定制', '资产配置', '恒丰理财', '理财',
    (SELECT id FROM users WHERE display_name = '刘仟一'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-06 00:00:00', '2025-11-06 00:00:00', 0.5, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '2010年以来每年跑赢基准的纯债、固收+及权益基金筛选及统计', '', '报告|定制', '权益', '泰康资产', '保险',
    (SELECT id FROM users WHERE display_name = '孙宇萌'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-05 00:00:00', '2025-11-06 00:00:00', 5.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '月度大模型市场观点整理', '', '报告|定制', '资产配置', '泰康资产', '保险',
    (SELECT id FROM users WHERE display_name = '孙宇萌'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-06 00:00:00', '2025-11-06 00:00:00', 2.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '10月基金经理市场观点', '', '报告|定制', '资产配置', '中加fof', 'FOF',
    (SELECT id FROM users WHERE display_name = '李典哲'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-06 00:00:00', '2025-11-06 00:00:00', 0.5, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '10月基金经理市场观点', '', '报告|定制', '资产配置', '中信信托', '信托',
    (SELECT id FROM users WHERE display_name = '钱定坤'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-06 00:00:00', '2025-11-06 00:00:00', 0.5, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '基金入库报告信息整理', '', '报告|定制', '纯债', '国泰海通', '券商',
    (SELECT id FROM users WHERE display_name = '段颖'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-07 00:00:00', '2025-11-07 00:00:00', 2.5, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '交银理财周度权益基金筛选', '', '基金筛选', '权益', '交银理财', '理财',
    (SELECT id FROM users WHERE display_name = '李迎圣'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-10 00:00:00', '2025-11-10 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '上海银行周报', '', '报告|定制', '资产配置', '上海银行', '银行自营',
    (SELECT id FROM users WHERE display_name = '李迎圣'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-10 00:00:00', '2025-11-10 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '微盘股策略基金筛选', '', '基金筛选', '权益', '中信信托', '信托',
    (SELECT id FROM users WHERE display_name = '吴泽航'),
    (SELECT id FROM users WHERE display_name = '陈熙雨'),
    '2025-11-10 00:00:00', '2025-11-10 00:00:00', 2.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '量化固收+筛选', '', '基金筛选', '固收＋', '银河证券', '券商',
    (SELECT id FROM users WHERE display_name = '钱一冰'),
    (SELECT id FROM users WHERE display_name = '刘洋'),
    '2025-11-03 00:00:00', '2025-11-03 00:00:00', 2.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '一二级债基筛选', '', '基金筛选', '固收＋', '中信证券', '券商',
    (SELECT id FROM users WHERE display_name = '郭力嘉'),
    (SELECT id FROM users WHERE display_name = '刘洋'),
    '2025-11-03 00:00:00', '2025-11-03 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '可转债基金整理', '', '基金筛选', '固收＋', '五矿固收', '券商',
    (SELECT id FROM users WHERE display_name = '聂慧敏'),
    (SELECT id FROM users WHERE display_name = '刘洋'),
    '2025-11-04 00:00:00', '2025-11-04 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '摊余成本法债基策略及收益测算', '', '知识沉淀', '纯债', '泉州银行', '银行自营',
    (SELECT id FROM users WHERE display_name = '胡奇洋'),
    (SELECT id FROM users WHERE display_name = '刘洋'),
    '2025-11-06 00:00:00', '2025-11-06 00:00:00', 3.5, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '新能源固收+筛选', '', '基金筛选', '固收＋', '中海信托', '信托',
    (SELECT id FROM users WHERE display_name = '姚芳'),
    (SELECT id FROM users WHERE display_name = '刘洋'),
    '2025-11-06 00:00:00', '2025-11-06 00:00:00', 2.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    'Q3行业标签更新及筛选', '', '基金筛选', '固收＋', '中信证券', '券商',
    (SELECT id FROM users WHERE display_name = '郭力嘉'),
    (SELECT id FROM users WHERE display_name = '刘洋'),
    '2025-11-06 00:00:00', '2025-11-06 00:00:00', 8.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '一二级债基筛选', '', '基金筛选', '固收＋', '中信证券', '券商',
    (SELECT id FROM users WHERE display_name = '郭力嘉'),
    (SELECT id FROM users WHERE display_name = '刘洋'),
    '2025-11-10 00:00:00', '2025-11-10 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '二级债基新能源标签及占比', '', '基金筛选', '固收＋', '中海信托', '信托',
    (SELECT id FROM users WHERE display_name = '姚芳'),
    (SELECT id FROM users WHERE display_name = '刘洋'),
    '2025-11-11 00:00:00', '2025-11-11 00:00:00', 1.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    'Q3行业标签更新及筛选', '', '基金筛选', '固收＋', '中信证券', '券商',
    (SELECT id FROM users WHERE display_name = '郭力嘉'),
    (SELECT id FROM users WHERE display_name = '刘洋'),
    '2025-11-07 00:00:00', '2025-11-11 00:00:00', 13.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '贵州银行周报', '', '报告|定制', '资产配置', '贵州银行', '银行资管',
    (SELECT id FROM users WHERE display_name = '金成俊'),
    (SELECT id FROM users WHERE display_name = '朱浩天'),
    '2025-11-03 00:00:00', '2025-11-03 00:00:00', 0.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '每年都跑赢沪深300且每年的回撤都小于沪深300的基金经理筛选', '', '基金筛选', '量化', '人保资产', '保险',
    (SELECT id FROM users WHERE display_name = '胡慧慧'),
    (SELECT id FROM users WHERE display_name = '朱浩天'),
    '2025-11-03 00:00:00', '2025-11-03 00:00:00', 0.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '主动中低频轮动基金筛选', '', '报告|定制', '量化', '客户不详43', '其他',
    (SELECT id FROM users WHERE display_name = '段颖'),
    (SELECT id FROM users WHERE display_name = '朱浩天'),
    '2025-11-03 00:00:00', '2025-11-03 00:00:00', 0.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '机构申赎分位数报表+图片自动化开发', '', '生产化|提效', '量化', '中信银行', '银行资管',
    (SELECT id FROM users WHERE display_name = '钱一冰'),
    (SELECT id FROM users WHERE display_name = '朱浩天'),
    '2025-11-04 00:00:00', '2025-11-04 00:00:00', 0.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '20年以来5年都跑赢沪深300且每年的回撤都小于沪深300的基金筛选', '', '基金筛选', '量化', '人保资产', '保险',
    (SELECT id FROM users WHERE display_name = '胡慧慧'),
    (SELECT id FROM users WHERE display_name = '朱浩天'),
    '2025-11-05 00:00:00', '2025-11-05 00:00:00', 0.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '量化策略基金筛选推荐', '', '基金筛选', '量化', '首创证券', '券商',
    (SELECT id FROM users WHERE display_name = '孙宇萌'),
    (SELECT id FROM users WHERE display_name = '朱浩天'),
    '2025-11-05 00:00:00', '2025-11-05 00:00:00', 0.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '量化策略研究报告整理', '', '知识沉淀', '量化', '首创证券', '券商',
    (SELECT id FROM users WHERE display_name = '孙宇萌'),
    (SELECT id FROM users WHERE display_name = '朱浩天'),
    '2025-11-05 00:00:00', '2025-11-05 00:00:00', 0.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '昨天净值创今年来新高的权益基金', '', '基金筛选', '权益', '兴银理财', '理财',
    (SELECT id FROM users WHERE display_name = '刘仟一'),
    (SELECT id FROM users WHERE display_name = '朱浩天'),
    '2025-11-05 00:00:00', '2025-11-05 00:00:00', 0.0, 'completed', 0
);

INSERT INTO requests (
    title, description, request_type, research_scope, org_name, org_type,
    sales_id, researcher_id, created_at, completed_at, work_hours, status, is_confidential
) VALUES (
    '权益基金产品报告', '', '报告|定制', '量化', '客户不详233', '其他',
    (SELECT id FROM users WHERE display_name = '吴泽航'),
    (SELECT id FROM users WHERE display_name = '朱浩天'),
    '2025-11-06 00:00:00', '2025-11-06 00:00:00', 0.0, 'completed', 0
);