import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import hashlib
import binascii
import os
import secrets


def calculate_double_sha1():
    # 获取输入
    key_hex = key_entry.get().strip()
    challenge_hex = challenge_entry.get().strip()

    # 验证输入
    if not key_hex or not challenge_hex:
        messagebox.showerror("输入错误", "密钥和Challenge不能为空")
        status_bar.config(text="错误：密钥和Challenge不能为空")
        return

    # 移除可能存在的空格
    key_hex = key_hex.replace(" ", "")
    challenge_hex = challenge_hex.replace(" ", "")

    try:
        # 验证长度
        if len(key_hex) != 32:
            messagebox.showerror("长度错误", "密钥必须是128位(32个十六进制字符)")
            status_bar.config(text="错误：密钥长度不正确")
            return

        if len(challenge_hex) != 40:
            messagebox.showerror("长度错误", "Challenge必须是20字节(40个十六进制字符)")
            status_bar.config(text="错误：Challenge长度不正确")
            return

        # 将16进制字符串转换为字节
        key_bytes = binascii.unhexlify(key_hex)
        challenge_bytes = binascii.unhexlify(challenge_hex)

        # 第一步计算：SHA1(Key + Challenge)
        step1 = hashlib.sha1()
        step1.update(key_bytes)
        step1.update(challenge_bytes)
        temp_result = step1.digest()
        temp_hex = binascii.hexlify(temp_result).decode('utf-8').upper()

        # 第二步计算：SHA1(Key + temp_result)
        step2 = hashlib.sha1()
        step2.update(key_bytes)
        step2.update(temp_result)
        final_result = step2.digest()
        final_hex = binascii.hexlify(final_result).decode('utf-8').upper()

        # 格式化输出
        formatted_temp = ' '.join([temp_hex[i:i + 2] for i in range(0, len(temp_hex), 2)])
        formatted_final = ' '.join([final_hex[i:i + 2] for i in range(0, len(final_hex), 2)])

        # 更新输出框
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "临时结果 (SHA1(Key + Challenge)):\n")
        result_text.insert(tk.END, formatted_temp + "\n\n")
        result_text.insert(tk.END, "最终结果 (SHA1(Key + 临时结果)):\n")
        result_text.insert(tk.END, formatted_final)
        result_text.config(state=tk.DISABLED)

        # 验证结果（如果使用默认值）
        if key_hex == "0123456789ABCDEFFEDCBA9876543210" and challenge_hex == "E3A9AC282BA5F63EDF904EA561CCA38EBDF26AE3":
            expected = "E6 BE 1E 49 8F C1 9D 60 C6 50 6D 00 7E A9 33 DB FD 61 12 33"
            if formatted_final == expected:
                status_bar.config(text="计算完成（结果验证正确）")
            else:
                status_bar.config(text=f"计算完成（但结果不匹配！预期：{expected}）")
        else:
            status_bar.config(text="计算完成")

    except binascii.Error:
        messagebox.showerror("格式错误", "请输入有效的十六进制数据")
        status_bar.config(text="错误：无效的十六进制数据")
    except Exception as e:
        messagebox.showerror("计算错误", f"发生错误: {str(e)}")
        status_bar.config(text=f"错误：{str(e)}")


def clear_all():
    key_entry.delete(0, tk.END)
    key_entry.insert(0, "0123456789ABCDEFFEDCBA9876543210")
    challenge_entry.delete(0, tk.END)
    challenge_entry.insert(0, "E3A9AC282BA5F63EDF904EA561CCA38EBDF26AE3")
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)
    status_bar.config(text="已重置为默认值")


def generate_random_challenge():
    """生成随机的20字节Challenge并自动计算"""
    # 生成20字节的随机数据
    random_bytes = secrets.token_bytes(20)
    random_hex = binascii.hexlify(random_bytes).decode('utf-8').upper()

    # 更新Challenge输入框
    challenge_entry.delete(0, tk.END)
    challenge_entry.insert(0, random_hex)

    # 自动触发计算
    calculate_double_sha1()

    # 更新状态栏
    status_bar.config(text=f"已生成随机Challenge并计算完成")


def copy_final_to_clipboard():
    result_text.config(state=tk.NORMAL)
    content = result_text.get(1.0, tk.END)
    # 提取最终结果部分
    final_start = content.find("最终结果") + len("最终结果 (SHA1(Key + 临时结果)):\n")
    final_result = content[final_start:].strip()
    result_text.config(state=tk.DISABLED)

    if final_result:
        # 移除空格
        clean_result = final_result.replace(" ", "")
        root.clipboard_clear()
        root.clipboard_append(clean_result)
        status_bar.config(text="最终摘要已复制到剪贴板")
    else:
        status_bar.config(text="无内容可复制")


# 创建主窗口
root = tk.Tk()
root.title("TI电池SHA1认证 - 双重SHA1计算工具---@Enzo Sun 20250712")
root.geometry("550x350")
root.resizable(False, False)

# 设置主题
style = ttk.Style()
style.theme_use('clam')

# 创建输入框架
input_frame = ttk.LabelFrame(root, text="输入参数", padding=(10, 5))
input_frame.pack(padx=10, pady=5, fill=tk.X)

# 密钥输入
ttk.Label(input_frame, text="128-bit Key (Hex):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
key_entry = ttk.Entry(input_frame, width=48)
key_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W, columnspan=2)
key_entry.insert(0, "0123456789ABCDEFFEDCBA9876543210")  # 默认示例密钥

# Challenge输入
ttk.Label(input_frame, text="20-byte Challenge (Hex):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
challenge_entry = ttk.Entry(input_frame, width=48)
challenge_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W, columnspan=2)
challenge_entry.insert(0, "E3A9AC282BA5F63EDF904EA561CCA38EBDF26AE3")  # 默认示例Challenge

# 按钮框架
button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=10, fill=tk.X)

# 计算按钮
calculate_btn = ttk.Button(button_frame, text="计算双重SHA1", command=calculate_double_sha1)
calculate_btn.pack(side=tk.LEFT, padx=5)

# 生成随机Challenge按钮
random_btn = ttk.Button(button_frame, text="生成随机Challenge", command=generate_random_challenge)
random_btn.pack(side=tk.LEFT, padx=5)

# 清空按钮
clear_btn = ttk.Button(button_frame, text="重置默认", command=clear_all)
clear_btn.pack(side=tk.LEFT, padx=5)

# 复制按钮
copy_btn = ttk.Button(button_frame, text="复制最终Digest", command=copy_final_to_clipboard)
copy_btn.pack(side=tk.RIGHT, padx=5)

# 结果框架
result_frame = ttk.LabelFrame(root, text="双重SHA1计算结果", padding=(10, 5))
result_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# 结果文本框 - 使用更大的文本框显示两个步骤的结果
result_text = scrolledtext.ScrolledText(
    result_frame,
    height=1,
    font=("Courier New", 10),
    wrap=tk.WORD
)
result_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
result_text.config(state=tk.DISABLED)  # 初始设置为只读

# 状态栏
status_bar = ttk.Label(root, text="就绪 - 输入参数后点击'计算双重SHA1'", relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# 算法说明
algorithm_frame = ttk.Frame(root)
algorithm_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 5))

algorithm_label = tk.Label(
    algorithm_frame,
    text="算法说明: Digest = SHA1(Key + SHA1(Key + Challenge))",
    foreground="blue",
    font=("Arial", 9, "italic")
)
algorithm_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

# 启动主循环
root.mainloop()