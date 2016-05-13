# API 文档

## API: 查询单词

URL: /api/v1/search?word={word}  
请求方式：GET  
参数：{word}, 必需，待查询的单词  
返回示例：

```json
{
  "success": true,
  "word": {
    "content": "stir",
    "example": "I'm memorizing word \"stir\"",
    "id": 4437,
    "description": "vt. 动；拨动；激动"
  }
}
```

## API: 获取单词信息

URL: /api/v1/word/{word_id}/  
请求方式：GET  
参数：{word_id}, 必需，待查询的单词 id  
返回示例：

```json
{
  "success": true,
  "word": {
    "content": "stir",
    "example": "I'm memorizing word \"stir\"",
    "id": 4437,
    "description": "vt. 动；拨动；激动"
  }
}
```

## API: 获取单词笔记

URL: /api/v1/word/{word_id}/note/?from={from}&to={to}  
请求方式：GET  
参数：{word_id}, 必需，待查询的单词 id；{from}, 可选，笔记开始条数（从0开始）；{to}, 可选，笔记结束条数  
返回示例：

```json
{
  "notes": [{
    "content": "Note of stir",
    "user": "stdio"
  }, {
    "content": "Another note of stir",
    "user": "User"
  }],
  "success": true
}
```



## API： 添加单词笔记

URL: /api/v1/word/{word_id}/note/  
请求方式：POST  
参数：{word_id}, 必需，待添加的单词 id；{content}, 笔记内容  
返回示例：

```json
{
  "success": true,
  "note": {
    "content": "Note of stir",
    "user": "stdio"
  }
}
```

## API: 获取当前背单词状态

URL: /api/v1/word/memo_status/  
请求方式：GET  
参数：无  
返回示例：

```json
{
  "words": [{
    "status": 3,
    "description": "n.大学肆业生",
    "notes": [{
      "content": "Note of undergraduate",
      "user": "stdio"
    }],
    "id": 4854,
    "content": "undergraduate",
    "learning_id": 47,
    "example": "I'm memorizing word \"undergraduate\"",
    "word_id": 4854
  }, {
    "status": 2,
    "description": "vt.动；拨动；激动",
    "notes": [{
      "content": "Note of stir",
      "user": "stdio"
    }],
    "id": 4437,
    "content": "stir",
    "learning_id": 48,
    "example": "I'm memorizing word \"stir\"",
    "word_id": 4437
  }, 
  ...
 ],
  "success": true
}
```

## 更新背单词状态

URL: /api/v1/word/memo_status/{learning_id}  
请求方式：PUT  
参数：{learning_id}, 当前单词学习 id  
返回示例：

```json
{
  "success": true
}
```

