-- 性能优化：补充关键查询的覆盖索引
-- 可重复执行（IF NOT EXISTS 语义）
-- 适用场景：feed流过滤、列表排序

DROP PROCEDURE IF EXISTS proc_drama_perf_idx;

DELIMITER //
CREATE PROCEDURE proc_drama_perf_idx()
BEGIN
  -- drama.status 索引：feed() 和 list_dramas() 按 status='published' 过滤
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'drama'
      AND index_name = 'idx_drama_status'
      AND seq_in_index = 1
      AND column_name = 'status'
  ) THEN
    ALTER TABLE drama ADD INDEX idx_drama_status (status);
  END IF;

  -- drama_ad 复合索引：(status, weight DESC) — feed 广告查询
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'drama_ad'
      AND index_name = 'idx_drama_ad_status_weight'
      AND seq_in_index = 1
      AND column_name = 'status'
  ) THEN
    ALTER TABLE drama_ad ADD INDEX idx_drama_ad_status_weight (status, weight DESC);
  END IF;
END //
DELIMITER ;

CALL proc_drama_perf_idx();
DROP PROCEDURE IF EXISTS proc_drama_perf_idx;