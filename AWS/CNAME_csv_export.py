import os
import csv

# 配置参数
config = {
    "folder_path": "CNAME-csv-export-csvFile",  # 存放 CSV 文件的目录
    "output_txt": "CNAME_csv_export.txt",  # 输出的 TXT 文件名
    "fields": {  # 选择要输出的字段，并映射成 Python 变量
        "域名": "domain",
        "CNAME 名称": "record_name",
        "类型": "record_type",
        "CNAME 值": "cname_value"
    },
    "include_header": False,  # 是否在 TXT 文件中添加表头
    "line_format": "{domain}|{record_name}|{record_type}|{cname_value}|600"  # 自定义格式（已更新）
}


with open(config["output_txt"], "w", encoding="utf-8") as txt_file:
    if config["include_header"]:
        txt_file.write("|".join(config["fields"].values()) + "\n")  # 写入表头（使用映射后的变量名）

    for filename in os.listdir(config["folder_path"]):
        if filename.endswith(".csv"):  # 只处理 CSV 文件
            file_path = os.path.join(config["folder_path"], filename)

            with open(file_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                # 遍历 CSV 数据
                for row in reader:
                    try:
			# 处理字段映射
                        formatted_data = {value: row[key] for key, value in config["fields"].items()}

                        # 处理 domain 名称，去掉 `*`，如果有的话
                        domain_parts = formatted_data["domain"].split(".")
                        formatted_data["domain"] = ".".join(domain_parts[-2:])

                        # 去掉 record_name 中的 domain 部分
                        formatted_data["record_name"] = formatted_data["record_name"].replace(formatted_data["domain"], "").strip(".")

                        # 去掉 cname_value 中的末尾 "."
                        formatted_data["cname_value"] = formatted_data["cname_value"].rstrip(".")

                        # 生成自定义格式的行
                        line = config["line_format"].format(**formatted_data)
                        txt_file.write(line + "\n")
                    except KeyError as e:
                        print(f"⚠️ 字段 {e} 在 {filename} 中不存在，跳过该行！")

print(f"✅ 所有 CSV 数据已转换为 {config['output_txt']}！")
