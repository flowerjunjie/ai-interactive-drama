-- 短剧平台管理：菜单 + 普通角色(role_id=2) 授权（PostgreSQL，在已初始化 RuoYi 库上执行一次）
-- 与 drama_platform_menu_mysql.sql + drama_platform_menu_v2_mysql.sql 内容一致。
-- 若已用新版 ruoyi-fastapi-pg.sql 全量初始化，可跳过本脚本。

insert into sys_menu values(2300, '短剧平台', 0, '5', 'shortdrama', null, '', 'shortdrama', 1, 0, 'M', '0', '0', '', 'video-camera', 'admin', current_timestamp, '', null, 'AI 互动短剧') on conflict (menu_id) do nothing;
insert into sys_menu values(2301, '数据看板', 2300, '1', 'dashboard', 'drama/dashboard/index', '', 'DramaDashboard', 1, 0, 'C', '0', '0', 'sdrama:dashboard:view', 'dashboard', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2302, '短剧管理', 2300, '2', 'item', 'drama/drama/index', '', 'DramaItem', 1, 0, 'C', '0', '0', 'sdrama:drama:list', 'list', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2303, '视频节点', 2300, '3', 'video-node', 'drama/videoNode/index', '', 'DramaVideoNode', 1, 0, 'C', '0', '0', 'sdrama:node:list', 'tree', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2304, '用户评价审核', 2300, '4', 'review', 'drama/review/index', '', 'DramaReview', 1, 0, 'C', '0', '0', 'sdrama:review:list', 'message', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2305, '广告管理', 2300, '5', 'ad', 'drama/ad/index', '', 'DramaAd', 1, 0, 'C', '0', '0', 'sdrama:ad:list', 'guide', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2306, 'C端用户', 2300, '6', 'app-user', 'drama/appUser/index', '', 'DramaAppUser', 1, 0, 'C', '0', '0', 'sdrama:appuser:list', 'peoples', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2310, '短剧新增', 2302, '1', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:drama:add', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2311, '短剧修改', 2302, '2', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:drama:edit', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2312, '短剧删除', 2302, '3', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:drama:remove', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2313, '节点新增', 2303, '1', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:node:add', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2314, '节点修改', 2303, '2', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:node:edit', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2315, '节点删除', 2303, '3', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:node:remove', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2316, '选项新增', 2303, '4', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:choice:add', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2317, '审核操作', 2304, '1', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:review:audit', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2318, '上传签名', 2303, '5', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:upload:sign', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2319, '上传完成', 2303, '6', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:upload:complete', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2320, '评论管理', 2300, '7', 'comment', 'drama/comment/index', '', 'DramaComment', 1, 0, 'C', '0', '0', 'sdrama:comment:list', 'chat-dot-square', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2321, '上传文件', 2300, '8', 'upload-file', 'drama/uploadFile/index', '', 'DramaUploadFile', 1, 0, 'C', '0', '0', 'sdrama:upload:list', 'upload', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2322, '视频审核', 2300, '9', 'video-audit', 'drama/videoAudit/index', '', 'DramaVideoAudit', 1, 0, 'C', '0', '0', 'sdrama:video_audit:list', 'video-camera', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2325, '评论删除', 2320, '1', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:comment:remove', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;
insert into sys_menu values(2326, '评论屏蔽', 2320, '2', '', '', '', '', 1, 0, 'F', '0', '0', 'sdrama:comment:hide', '#', 'admin', current_timestamp, '', null, '') on conflict (menu_id) do nothing;

insert into sys_role_menu (role_id, menu_id) values (2, 2300) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2301) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2302) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2303) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2304) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2305) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2306) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2310) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2311) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2312) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2313) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2314) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2315) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2316) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2317) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2318) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2319) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2320) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2321) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2322) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2325) on conflict do nothing;
insert into sys_role_menu (role_id, menu_id) values (2, 2326) on conflict do nothing;

select setval(pg_get_serial_sequence('sys_menu', 'menu_id'), coalesce((select max(menu_id) from sys_menu), 1));
