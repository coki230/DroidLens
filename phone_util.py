import uiautomator2 as u2
from io import BytesIO
import base64

d = u2.connect() # 连接手机

def interact_with_element(resource_id, operation, operation_value):
    ele = d(resourceId=resource_id)
    match operation:
        case "click":
            ele.click()
        case "long_click":
            ele.long_click()
        case "clear_text":
            ele.clear_text()
        case "set_text":
            ele.set_text(operation_value)

def click(click_type, x, y):
    if click_type == "click":
        d.click(x=x, y=y)
    elif click_type == "double_click":
        d.double_click(x=x, y=y, duration=0.1)
    elif click_type == "long_click":
        d.long_click(x=x, y=y, duration=0.5)

def get_current_page():
    screenshot = d.screenshot(format='pillow')
    buffer = BytesIO()
    screenshot.convert("RGB").save(buffer, format='JPEG', quality=70)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64


def dump_hierarchy():
    return d.dump_hierarchy()

def app_list():
    return d.app_list()


def app_start(package):
    d.app_start(package)