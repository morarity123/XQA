## xqa

一个支持正则，支持回流，支持随机回答，支持图片等CQ码的你问我答

PS.lan佬不开源，艾琳佬没有回流，所以还是自己动手丰衣足食吧，代码已经尽量简洁了

另外，目前可能会有BUG或注入漏洞，如遇到请反馈

## 注意

请务必先将gocqhttp更新至1.0.0-rc1，旧版可能有点问题

本插件理论上可以和[eqa](https://github.com/pcrbot/erinilis-modules/tree/master/eqa)同时存在，请自测效果

附赠迁移数据功能，请看下方功能介绍

可多行匹配，可匹配图片等，图片只用go-cq的缓存，因此会过期，另外添加问答的时候尽量不转发别人的图片文字组合消息，可能有点问题

回答可以用'#'分割回答，可以随机回复这几个回答,'\#'将不会分割

支持正则表达式，请用英文括号分组，回流用$加数字，回答时优先完全匹配，匹配不到才正则匹配

## 最近四条更新日志

v1.0.1  优化逻辑，精简代码，现在匹配优先完全匹配其次正则匹配，以避免报错，请更新后删除res/img/xqa/data.sqlite文件后重新迁移一下数据

v1.0    首次提交

## 功能

| 功能命令 | 介绍 |
| :---- | :---- |
| 我问A你答B | 设置个人问题 |
| 有人问C你答D | 群管理员设置全群问答 |
| 全群问E你答F | 维护组设置bot所加的所有群都回答的内容 |
| 查问答@某人 | 限群管理单独查某人的全部问答 |
| 查问答@某人G | 限群管理单独搜索某人的问答，G为搜索内容 |
| 不要回答H | 删除某个回答H，优先删除我问其次删除有人问，一次只删一个 |
| @某人不要回答H | 限群管理删除某人的某个回答H |
| 看看有人问 | 看全群设置的问题 |
| 看看有人问X | 搜索全群设置的问题，X为搜索内容 |
| 看看我问 | 看自己设置的问题 |
| 看看我问Y | 搜索自己设置的问题，Y为搜索内容 |

#### 附赠

>   注意：移动数据只能移动每个群的有人问和我问，eqa的能多个群的有人问这里只能复制一个群(创建该有人问的那个群)，本插件里多群问答请使用全群问
    其他正则匹配的内容可能无法复制过来，您可以参照README自己修改data_config.json

    总结:
    第一个命令：eqa的db数据 -> db_config.json -> data_config.json，有需要的请修改data_config.json
    第二个命令：data_config.json -> data.sqlite数据库(本插件使用的数据库)

| 功能命令 | 介绍 |
| :---- | :---- |
| .xqa_extract_data | 如果之前使用过艾琳佬的[eqa](https://github.com/pcrbot/erinilis-modules/tree/master/eqa)，可以通过该功能将数据提取出来，不会删除原文件，但请确保modules下有eqa，且eqa启用不启用均可，注意：点号别漏 |
| .xqa_write_data | 将上一步提取的数据写入数据库，原有xqa的相同问答会被覆盖 |

## 举几个例子

#### 设置问题

- 我问111你答222
    
    发送：111

    bot回复：222

- 我问(.{0,19})我(.{0,19})你答$1优衣酱$2
    
    发送：抱着我可爱的自己

    bot回复：抱着优衣酱可爱的自己

- 有人问333你答444#555#666

    发送：333

    bot回复：444或者555或者666，这里是随机发送

- 有人问(这里是某张图片)你答啊哈哈哈，寄汤来咯

    发送：(刚才某张图片)

    bot回复：啊哈哈哈，寄汤来咯

- 我问(.{1,19})饿了你答不准饿

    发送：我饿了

    bot回复：不准饿

#### 查看我问

- 看看我问

    bot回复：(你的所有问答)

- 看看我问123

    bot回复：(和123有关的你的所有问答)

#### 管理员查问答

- 查问答@某人

    bot回复：(这个人的所有问答)

- 查问答@某人456

    bot回复：(这个人的和456有关的所有问答)

## 使用教程

emmm，就不写了吧，反正别忘了装依赖就行

## 提取的数据结构 `data_config.json`

```
注："all"为有人问
保留全部CQ码，转移过来的图片依旧保持绝对目录，新设置的图片只用缓存
全部不转义，仅有问题由正则，正则就直接写正则匹配表达式
仅有回答里有回流，回流符号$直接写不用转义

{
    "qq群1": {
        "all": {
            "问题1": [
                "回答1",
                "回答2",
                "回答3"
            ],
            "问题2": [
                "回答"
            ]
        },
        "群员qq1": {
            "问题1": [
                "回答"
            ]
        },
        "群员qq2": {
            "问题1": [
                "回答"
            ]
        }
    },
    "qq群2": {
        "all": {
            "问题1": [
                "回答"
            ]
        }
}
```