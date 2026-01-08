import uiautomator2 as u2

d = u2.connect() # 连接手机
# print(d.dump_hierarchy()) # 获取屏幕上所有按钮和文字的 XML
# print(d.device_info)
# print(d.wlan_ip)
# print(d.app_list_running())
# d.open_url("https://www.baidu.com")
# d.screenshot("saved.jpg")
# d.press("home")
# d.screen_on() # 点亮屏幕
# d.screen_off() # 关闭屏幕
# d.info.get('screenOn') # 屏幕是否点亮
# d.unlock() # 解锁：点亮屏幕并解锁，需禁用锁屏密码
# print(d.app_current()
# d.app_stop("com.termux")
# d.app_start("com.termux")

def app_list_running():
    return d.app_list_running()