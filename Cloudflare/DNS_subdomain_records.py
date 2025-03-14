import os

# 要生成记录的域名列表
domains_str = """
56cgeryih.com
fghfdfb.com
gu7ffgm.com
gtut5u6cg.com
3wttu8m.com
"""

# string切割
domains = [domain.strip() for domain in domains_str.splitlines()]

# 二级域名
sub_name = "dt"  # 或者您可以根据需要将其赋值为其他内容，如 "sub" 等

# 可配置的 SOA 和 NS 记录
soa_record = {
    'primary_ns': 'rommy.ns.cloudflare.com.',
    'email': 'dns.cloudflare.com.',
    'serial': 2049293924,
    'refresh': 10000,
    'retry': 2400,
    'expire': 604800,
    'minimum_ttl': 3600
}

ns_records = ['rommy.ns.cloudflare.com.', 'sharon.ns.cloudflare.com.']

# CNAME 目标地址，可以自定义
cname_target = "origin_zhanqun_56cg_web.mxxorigin.com."


# 输出文件夹
outdir = 'DNS-subdomain-outdir'

# 如果文件夹不存在，则创建文件夹
if not os.path.exists(outdir):
    os.makedirs(outdir)

# 为每个域名生成文件
for domain in domains:
    records = ""

    # 添加 SOA 记录（从 soa_record 中获取配置信息）
    records += f"{domain}.\t3600\tIN\tSOA\t{soa_record['primary_ns']}\t{soa_record['email']}\t{soa_record['serial']}\t{soa_record['refresh']}\t{soa_record['retry']}\t{soa_record['expire']}\t{soa_record['minimum_ttl']}\n\n"

    # 添加 NS 记录（从 ns_records 中获取配置信息）
    records += f";; NS Records\n"
    for ns in ns_records:
        records += f"{domain}.\t86400\tIN\tNS\t{ns}\n"
    records += "\n"

    # 添加特定的 CNAME 记录
    records += f";; CNAME Records\n"
    records += f"{domain}.\t1\tIN\tCNAME\t{cname_target} ; cf_tags=cf-proxied:true\n"
    records += f"www.{domain}.\t1\tIN\tCNAME\t{cname_target} ; cf_tags=cf-proxied:true\n\n"

    # 生成 CNAME 记录 dt1 到 dt200
    records += f";; CNAME Records\n"
    for i in range(1, 101):
        records += f"{sub_name}{i}.{domain}.\t1\tIN\tCNAME\t{domain}. ; cf_tags=cf-proxied:true\n"

    # 将记录保存到 outdir 文件夹中
    with open(os.path.join(outdir, f"{domain}.txt"), 'w') as file:
        file.write(records)
    print(f"文件 {domain}.txt 已生成到 {outdir}")