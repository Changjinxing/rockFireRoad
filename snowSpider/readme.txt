todo list

1. save data to sql
    1. sql table definition
    2. tb_original_source: 住建委 id date source url status content gmt_create gmt_update creator operator
    3. tb_sign_online: 网签数量 id date type[day/week/month/quarter/year] source url status online gmt_create gmt_update creator operator
       1day 5条 + 52week + 12month + 1year + 4q = 434*5source*100year

2. 数据生成图片 done
3. 发送邮件 done
4. 趋势曲线网页 done
5. 发送微信群消息
6. 趋势曲线网页下载生成图片 发送邮件 done
7. 钉钉机器人 or 公众号推送 用a公众号推送给所有人
   7.1 公众号推送方式 公众号开通+管理员权限done
8. 图片html格式优化 done using 冬奥色卡 https://china.huanqiu.com/article/46glrMfOyAb
9. 购买腾讯云 or 阿里云服务 done 腾讯云
10. 部署服务到云端 done  git速度问题 + 图片渲染问题
11. 爬取稳定性 封禁问题

12. data 转换为 request format done
13. deploy java service on cloud
14. apply mysql instance on cloud
15. call service from python side
16. add antf2 service to sharing or other front end service



source
1. 数据： http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=307749
2. 网签趋势参考： http://www.beijingfangshi.com/wx_w1.html