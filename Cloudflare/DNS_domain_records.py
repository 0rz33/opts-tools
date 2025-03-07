import os
from datetime import datetime

# 要生成记录的域名列表
domains_str = """
aaaa.cc
bbbb.cc
dddd.cc
eeee.cc
"""

# string切割
domains = domains_str.splitlines()

# 配置 SOA 记录
soa_record = {
    "primary_ns": "rommy.ns.cloudflare.com.",
    "email": "dns.cloudflare.com.",
    "serial": 2049300364,
    "refresh": 10000,
    "retry": 2400,
    "expire": 604800,
    "minimum_ttl": 3600
}

# 配置 NS 记录
ns_records = [
    "rommy.ns.cloudflare.com.",
    "sharon.ns.cloudflare.com."
]

# CNAME 记录目标
cname_target = "origin_zhanqun_56cg_web.mxxorigin.com."

# 输出目录
outdir = "DNS-domain-outdir"  # 请替换为您的目标目录

# 创建输出目录（如果不存在的话）
if not os.path.exists(outdir):
    os.makedirs(outdir)

# 当前日期时间
export_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 遍历域名列表，生成对应的 DNS 记录文件
for domain in domains:
    records = ""

    # 添加域名信息头
    records += f";;\n;; Domain:     {domain}\n;; Exported:   {export_time}\n;;\n"
    records += ";; This file is intended for use for informational and archival\n"
    records += ";; purposes ONLY and MUST be edited before use on a production\n"
    records += ";; DNS server.  In particular, you must:\n"
    records += ";;   -- update the SOA record with the correct authoritative name server\n"
    records += ";;   -- update the SOA record with the contact e-mail address information\n"
    records += ";;   -- update the NS record(s) with the authoritative name servers for this domain.\n"
    records += ";;\n"
    records += ";; For further information, please consult the BIND documentation\n"
    records += ";; located on the following website:\n"
    records += ";;\n;; http://www.isc.org/\n;;\n"
    records += ";; And RFC 1035:\n;;\n;; http://www.ietf.org/rfc/rfc1035.txt\n"
    records += ";;\n;; Please note that we do NOT offer technical support for any use\n"
    records += ";; of this zone data, the BIND name server, or any other third-party\n"
    records += ";; DNS software.\n;;\n;; Use at your own risk.\n;;\n"

    # 添加 SOA 记录（从 soa_record 中获取配置信息）
    records += f"{domain}\t3600\tIN\tSOA\t{soa_record['primary_ns']} {soa_record['email']} {soa_record['serial']} {soa_record['refresh']} {soa_record['retry']} {soa_record['expire']} {soa_record['minimum_ttl']}\n\n"

    # 添加 NS 记录（从 ns_records 中获取配置信息）
    records += ";; NS Records\n"
    for ns in ns_records:
        records += f"{domain}\t86400\tIN\tNS\t{ns}\n"
    records += "\n"

    # 添加特定的 CNAME 记录
    records += ";; CNAME Records\n"
    records += f"{domain}\t1\tIN\tCNAME\t{cname_target} ; cf_tags=cf-proxied:true\n"
    records += f"www.{domain}\t1\tIN\tCNAME\t{cname_target} ; cf_tags=cf-proxied:true\n\n"

    # 将记录保存到 outdir 文件夹中
    with open(os.path.join(outdir, f"{domain}.txt"), 'w') as file:
        file.write(records)
    
    print(f"文件 {domain}.txt 已生成到 {outdir}")

print("所有文件已生成！")