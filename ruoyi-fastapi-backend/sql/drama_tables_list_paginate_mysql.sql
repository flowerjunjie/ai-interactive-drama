-- 性能优化：分页支持 + 冗余字段压缩
-- 可重复执行

DROP PROCEDURE IF EXISTS proc_drama_list_paginate;

DELIMITER //
CREATE PROCEDURE proc_drama_list_paginate()
BEGIN
  -- drama 复合索引：(status, sort) — list_dramas 默认排序
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'drama'
      AND index_name = 'idx_drama_status_sort'
      AND seq_in_index = 1
      AND column_name = 'status'
  ) THEN
    ALTER TABLE drama ADD INDEX idx_drama_status_sort (status, sort DESC);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'drama'
      AND index_name = 'idx_drama_status_heat'
      AND seq_in_index = 1
      AND column_name = 'status'
  ) THEN
    ALTER TABLE drama ADD INDEX idx_drama_status_heat (status, heat DESC);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'drama'
      AND index_name = 'idx_drama_status_create'
      AND seq_in_index = 1
      AND column_name = 'status'
  ) THEN
    ALTER TABLE drama ADD INDEX idx_drama_status_create (status, create_time DESC);
  END IF;
END //
DELIMITER ;

CALL proc_drama_list_paginate();
DROP PROCEDURE IF EXISTS proc_drama_list_paginate;