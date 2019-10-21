## IMF_Zabbix_Monitor_Tools
### Log_Analyze主要存放日志分析类型的脚本
- afds_log_analysis用途是分析afds服务航班消息日志最后下发时间


- aftn_analyze用途是分析AFTN报文消息的完整性
> AFTN消息的开头以 `ZZZZ` 为起始，以`NNNN`为结尾。通过判定文件内`ZZZZ`和`NNNN`的差值来判定AFTN消息是否完整。

### Query_Unit主要存放数据库查询相关的脚本
- query为通用型查询脚本，根据`query.conf`，`sys.argv[1]`和`sys.argv[2]`的参数设定来进行相关语句的查询