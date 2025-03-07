# 定义所有需要监控的日志关键字段
LOGCAT_KEYWORDS = {
    # 新用户相关
    "New_user_active，type=cms": "新用户激活",
    "User_install_new，type=cms": "新用户安装",
    "a，type=cms": "通用技术打点---保活",
    
    # CMP相关
    "CMP_PAGE_LOADING_START，type=cms": "CMP loading开始",
    "CMP_PAGE_LOADING_END，type=cms": "CMP loading结束",
    "CMP_REQUEST_SUCCESS，type=cms": "CMP 请求信息成功",
    "CMP_REQUEST_FAIL，type=cms": "CMP 请求信息失败",
    "CMP_DATA_SUCCESS，type=cms": "CMP 数据表单请求成功",
    "CMP_DATA_FAIL_POP，type=cms": "CMP 数据表单请求失败",
    "CMP_PAGE_LOADING_START_POP，type=cms": "CMP loading开始（从弹窗进入）",
    "CMP_PAGE_LOADING_END_POP，type=cms": "CMP loading结束（从弹窗进入）",
    "CMP_REQUEST_SUCCESS_POP，type=cms": "CMP 请求信息成功（从弹窗进入）",
    "CMP_REQUEST_FAIL_POP，type=cms": "CMP 请求信息失败（从弹窗进入）",
    "CMP_DATA_SUCCESS_POP，type=cms": "CMP 数据表单请求成功（从弹窗进入）",
    "CMP_DATA_FAIL_POP，type=cms": "CMP 数据表单请求失败（从弹窗进入）",
    
    # 开屏页相关
    "Splash_page_show，type=cms": "开屏页展示",
    "com.helperpro.phone.ui.splash.StartSplashActivity，type=cms": "开屏页Activity",
    "Splash_page_START_click，type=cms": "开屏页START按钮点击(取消勾选隐私协议后点击不算)",
    "Splash_loading_start，type=cms": "开屏loading页面开始",
    "Splash_loading_over，type=cms": "开屏loading页面结束",
    
    # 首页和工具页相关
    "Home_show，type=cms": "首页展示",
    "tool_show，type=cms": "工具页展示",
    "Home_JunkClean_click，type=cms": "首页垃圾清理点击",
    "Home_SimilarPhotos_click，type=cms": "首页相似图片清理点击",
    "Home_Large_file_click，type=cms": "首页大文件点击",
    "Home_Virus_click，type=cms": "首页杀毒点击",
    "Home_Process_click，type=cms": "首页app process点击",
    "Home_Batteryinfo_click，type=cms": "首页battery info点击",
    "Home_wifi_click，type=cms": "首页WiFi点击",
    "home_click_other_func，type=cms": "首页其它的随机展示功能点击",
    "tool_click_func，type=cms": "Tool页点击功能",
    "Home_Setting_click，type=cms": "首页右上角设置点击",
    "Home_Grant_click，type=cms": "首页右上角权限点击",
    
    # 后台运行权限相关
    "backstage_show，type=cms": "后台运行权限弹窗展示",
    "backstage_allow，type=cms": "后台运行权限弹窗点击同意",
    "backstage_deny，type=cms": "后台运行权限弹窗点击拒绝",
    "backstage_success，type=cms": "后台运行权限授权成功",
    "backstage_fail，type=cms": "后台运行权限授权失败",
    
    # 通知权限相关
    "home_notification_show，type=cms": "安卓13通知弹窗展示",
    "home_notification_allow，type=cms": "安卓13通知弹窗点击同意",
    "home_notification_deny，type=cms": "安卓13通知弹窗点击拒绝",
    "home_notification_success，type=cms": "安卓13通知弹窗授权成功",
    "home_notification_fail，type=cms": "安卓13通知弹窗授权失败",
    
    # 退出应用相关
    "exit_show，type=cms": "退出应用弹窗展示",
    "exit_click_exit，type=cms": "退出应用弹窗点击exit",
    "exit_click_try，type=cms": "退出应用弹窗点击try it",
    
    # 功能引导相关
    "fuc_guide_show，type=cms": "功能引导弹窗展示",
    "fuc_guide_try，type=cms": "功能引导弹窗点击try it",
    "fuc_guide_close，type=cms": "功能引导弹窗点击关闭",
    
    # 小部件相关
    "home_widget，type=cms": "点击小部件功能",
    "widget_add，type=cms": "小部件功能点击添加图标",
    
    # 垃圾清理相关
    "JunkClean_detail_show，type=cms": "垃圾清理详情页展示",
    "JunkClean_detail_backhome，type=cms": "垃圾清理详情页返回主页",
    "JunkClean_detail_CLEAN_click，type=cms": "垃圾清理详情页CLEAN按钮点击",
    
    # 功能结果页相关
    "Funcs_result_show，type=cms": "各功能完成页展示",
    "Funcs_animation_start，type=cms": "各功能清理动画开始",
    "Funcs_toast_show，type=cms": "各功能动画中返回toast展示",
    "Funcs_result_func_click，type=cms": "各功能结果页功能点击",
    "Funcs_result_backhome，type=cms": "各功能结果页返回主页",
    
    # 杀毒相关
    "trust_look_invoke，type=cms": "trustlook扫毒调用",
    "trust_look_f_invoke，type=cms": "杀毒假扫",
    "trust_look_on_start，type=cms": "杀毒开始扫描回调",
    "trust_look_on_success，type=cms": "杀毒扫描成功回调",
    "trust_look_on_fail，type=cms": "杀毒扫描失败回调",
    "Virus_risk_show，type=cms": "杀毒有风险页展示",
    
    # 设置页面相关
    "About_Setting_click，type=cms": "setting点击",
    "About_Rateus_click，type=cms": "评分点击",
    "About_Feedback_click，type=cms": "反馈点击",
    "About_About_click，type=cms": "关于点击",
    
    # 评分相关
    "Rateus_show，type=cms": "评分弹窗展示",
    "Rateus_result，type=cms": "评分弹窗结果",
    
    # 应用外弹窗相关
    "Outer_guide_all_show，type=cms": "应用外所有弹窗展示（不含通知栏、静默通知）",
    "Outer_guide_all_click，type=cms": "应用外所有弹窗点击（不含通知栏、静默通知）",
    "Outer_guide_time_reach，type=cms": "实际触发应用外功能引导弹窗",
    "Outer_guide_show，type=cms": "应用外功能引导弹窗展示",
    "Outer_guide_click，type=cms": "应用外功能引导弹窗点击使用",
    "Outer_guide_close，type=cms": "应用外功能引导弹窗关闭按钮点击",
    
    # 卸载安装相关
    "Uninstall_monitor，type=cms": "监听到卸载事件",
    "Uninstall_show，type=cms": "卸载弹窗展示",
    "Uninstall_clean_click，type=cms": "卸载弹窗CLEAN按钮点击",
    "Uninstall_close_click，type=cms": "卸载弹窗关闭按钮点击",
    "install_show，type=cms": "安装弹窗展示",
    "install_click，type=cms": "安装弹窗点击",
    
    # 充电状态相关
    "Charging_monitor，type=cms": "监听电源状态",
    "Charging_show，type=cms": "充电弹窗展示",
    "Charging_optimize_click，type=cms": "充电弹窗optimize按钮点击",
    "Charging_close_click，type=cms": "充电弹窗关闭按钮点击",
    
    # 通知栏相关
    "Notification_show，type=cms": "常驻通知栏显示",
    "Notification_click，type=cms": "常驻通知栏点击",
    "Notification_clean_show，type=cms": "通知清理通知栏显示",
    "Notification_clean_click，type=cms": "通知清理通知栏点击",
    
    # 广告相关
    "Splash_ad_request，type=cms": "开屏广告请求",
    "Splash_ad_fill，type=cms": "开屏广告填充",
    "Splash_ad_show，type=cms": "开屏广告展示",
    "Func_ad_request，type=cms": "功能使用插屏广告请求",
    "Func_ad_fill，type=cms": "功能使用插屏广告填充",
    "Func_ad_show，type=cms": "功能使用插屏广告展示",
    "Tool_ad_request，type=cms": "tool原生广告请求",
    "Tool_ad_fill，type=cms": "tool原生广告填充",
    "Tool_ad_show，type=cms": "tool原生广告展示",
    "Result_ad_request，type=cms": "结果页原生广告请求",
    "Result_ad_fill，type=cms": "结果页原生广告填充",
    "Result_ad_show，type=cms": "结果页原生广告展示",
    "Exit_ad_request，type=cms": "退出应用弹窗原生广告请求",
    "Exit_ad_fill，type=cms": "退出应用弹窗原生广告填充",
    "Exit_ad_show，type=cms": "退出应用弹窗原生广告展示",
    
    # 归因相关
    "Attr_Fail，type=cms": "归因失败",
    "Attr_Success，type=cms": "归因成功",

    # 所有上载数据库的关键字（通用匹配规则，最低优先级）
    "，type=cms": "SDK通用技术打点-广告事件"
}