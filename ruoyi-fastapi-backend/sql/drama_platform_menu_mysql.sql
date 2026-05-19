-- 短剧平台管理：菜单 + 普通角色(2)授权（在已初始化 RuoYi 库上执行）
-- 菜单 ID 段 2300–2399
-- PostgreSQL 请使用 drama_platform_menu_pg.sql；全量初始化可用 ruoyi-fastapi-pg.sql（已内联本段菜单）。

INSERT INTO sys_menu VALUES (
  '2300', '短剧平台', '0', '5', 'shortdrama', NULL, '', 'shortdrama', 1, 0, 'M', '0', '0', '',
  'video-camera', 'admin', sysdate(), '', NULL, 'AI 互动短剧'
);
INSERT INTO sys_menu VALUES (
  '2301', '数据看板', '2300', '1', 'dashboard', 'drama/dashboard/index', '', 'DramaDashboard',
  1, 0, 'C', '0', '0', 'sdrama:dashboard:view', 'dashboard', 'admin', sysdate(), '', NULL, ''
);
INSERT INTO sys_menu VALUES (
  '2302', '短剧管理', '2300', '2', 'item', 'drama/drama/index', '', 'DramaItem',
  1, 0, 'C', '0', '0', 'sdrama:drama:list', 'list', 'admin', sysdate(), '', NULL, ''
);
INSERT INTO sys_menu VALUES (
  '2303', '视频节点', '2300', '3', 'video-node', 'drama/videoNode/index', '', 'DramaVideoNode',
  1, 0, 'C', '0', '0', 'sdrama:node:list', 'tree', 'admin', sysdate(), '', NULL, ''
);
INSERT INTO sys_menu VALUES (
  '2304', '评价审核', '2300', '4', 'review', 'drama/review/index', '', 'DramaReview',
  1, 0, 'C', '0', '0', 'sdrama:review:list', 'message', 'admin', sysdate(), '', NULL, ''
);
INSERT INTO sys_menu VALUES (
  '2305', '广告管理', '2300', '5', 'ad', 'drama/ad/index', '', 'DramaAd',
  1, 0, 'C', '0', '0', 'sdrama:ad:list', 'guide', 'admin', sysdate(), '', NULL, ''
);
INSERT INTO sys_menu VALUES (
  '2306', 'C端用户', '2300', '6', 'app-user', 'drama/appUser/index', '', 'DramaAppUser',
  1, 0, 'C', '0', '0', 'sdrama:appuser:list', 'peoples', 'admin', sysdate(), '', NULL, ''
);

-- 按钮权限（常用）
INSERT INTO sys_menu VALUES ('2310', '短剧新增', '2302', '1', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:drama:add', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2311', '短剧修改', '2302', '2', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:drama:edit', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2312', '短剧删除', '2302', '3', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:drama:remove', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2313', '节点新增', '2303', '1', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:node:add', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2314', '节点修改', '2303', '2', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:node:edit', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2315', '节点删除', '2303', '3', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:node:remove', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2316', '选项新增', '2303', '4', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:choice:add', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2317', '审核操作', '2304', '1', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:review:audit', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2318', '上传签名', '2303', '5', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:upload:sign', '#', 'admin', sysdate(), '', NULL, '');
INSERT INTO sys_menu VALUES ('2319', '上传完成', '2303', '6', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:upload:complete', '#', 'admin', sysdate(), '', NULL, '');

-- 授权给「普通角色」role_id=2（与官方初始化一致）；超级管理员走 *:*:*
-- INSERT IGNORE：重复执行或与 v2 脚本重叠时不会因 sys_role_menu 主键报错
INSERT IGNORE INTO sys_role_menu (role_id, menu_id)
SELECT 2, m.menu_id FROM sys_menu m WHERE m.menu_id BETWEEN 2300 AND 2399;
-- 如使用其他角色，请为其重复插入关联
