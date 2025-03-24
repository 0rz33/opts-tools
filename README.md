# OPS-tools
# 运维小工具

## 创建用户和用户组 - interactive_acl_multiple_users.sh

交互式

组赋值权限或者个人<code>visudo</code>

## Cloudflare  工具  

### 批量DNS解析

**批量主DNS解析：**
- DNS_domain_records.py  --------  批量主DNS域名解析  导出DNS目录(DNS-domain-outdir) 
    ``` bash
    python DNS_domain_records.py  
    ```
    导出DNS目录(DNS-domain-outdir)

**批量二级DNS解析：**
- DNS_subdomain_records.py  -----  批量二级DNS域名解析  导出DNS目录(DNS-subdomain-outdir)
    ``` bash
    python DNS_subdomain_records.py
    ```
    导出DNS目录(DNS-subdomain-outdir)

## AWS 工具

### 批量解析二级域名

#### (目前只针对Gname)

**手动添加二级域名在AWS里并复制到「CNAME-csv-export-csvFile 」下：**
- CNAME_csv_export.py  --------  此脚本回遍历「CNAME-csv-export-csvFile 」下的所有数据导出CSV数据，生成TXT文件(CNAME_csv_export.txt) 可根据格式
    ``` bash
    python DNS_domain_records.py  
    ```
    导出域名解析TXT(CNAME_csv_export.txt)  
