import os
import re

# 配置文件夹路径
config_folder = 'add/'
# 需要更新的quantumultX配置文件路径
qx_update_file_path = 'quantumultX-update.conf'

# 读取quantumultX-update文件的内容
with open(qx_update_file_path, 'r') as file:
    qx_content = file.read()

# 对每个配置文件进行处理
for section in ['general', 'policy', 'server_remote', 'filter_remote', 'rewrite_remote',
                'server_local', 'filter_local', 'rewrite_local', 'task_local', 'mitm']:
    # 构建对应的.conf文件路径
    conf_file_path = os.path.join(config_folder, section.replace('_', '-') + '.conf')
    # 读取.conf文件中的内容（如果存在）
    if os.path.exists(conf_file_path):
        with open(conf_file_path, 'r') as conf_file:
            conf_content = conf_file.read()
            # 移除可能的section标题
            conf_content = re.sub(r'^\[' + section + r'\]\s*', '', conf_content, flags=re.MULTILINE).strip()

        # 检查quantumultX-update文件中的section内容是否已包含要添加的内容
        section_pattern = re.compile(r'(\[' + re.escape(section) + r'\])\s*([\s\S]*?)(?=\n\[\w+\]|$)', flags=re.MULTILINE)
        match = section_pattern.search(qx_content)
        if match and conf_content in match.group(2):
            print(f"{section} section的内容已存在，跳过添加。")
            continue
        
        # 替换对应section下的内容
        qx_content = section_pattern.sub(r'\1\n' + conf_content + r'\n\2', qx_content)
    else:
        print(f'未找到 {conf_file_path} 文件，跳过此section的更新。')

# 将更新后的内容写回quantumultX-update文件
with open(qx_update_file_path, 'w') as file:
    file.write(qx_content)

print('quantumultX-update 文件的 sections 更新完毕。')