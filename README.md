# 空参数默认排序IDOR漏洞演示环境
# Blind Guide Vulnerability Demo (Empty Parameter Default Sort IDOR)

---

## 漏洞别名（研究昵称）
盲眼向导漏洞（Blind Guide Vulnerability）

## 研究发现者
余悸（安全研究爱好者） / YuJi (Security Research Enthusiast)

## 研究时间
2026年3月 / March 2026

---

### 项目说明 | Project Description
本项目为安全研究用途，用于复现一类常见的业务逻辑缺陷：当Web应用接口未对资源ID参数做必填校验时，后端会默认返回数据库第一条记录，若缺乏权限校验，则可能导致越权访问。

This project is for security research purposes, demonstrating a common business logic vulnerability: When a web application interface does not enforce required validation on resource ID parameters, the backend will default to returning the first database record. Without proper permission checks, this can lead to unauthorized access.

---

### 运行方式 | How to Run
1.  安装依赖：
    ```bash
    pip install flask flask-sqlalchemy
    ```
2.  启动项目：
    ```bash
    python app.py
    ```
3.  访问地址：`http://127.0.0.1:5000`

1.  Install dependencies:
    ```bash
    pip install flask flask-sqlalchemy
    ```
2.  Start the project:
    ```bash
    python app.py
    ```
3.  Access URL: `http://127.0.0.1:5000`

---

### 复现步骤 | Reproduction Steps
1.  不带参数访问 `/api/project`，观察返回第一条数据（归属其他用户）
2.  带参数访问 `/api/project?project_id=2`，观察返回当前用户数据
3.  对比验证空参数默认行为带来的权限问题

1.  Access `/api/project` without parameters, observe the first record returned (belonging to another user)
2.  Access `/api/project?project_id=2` with parameters, observe the current user's data returned
3.  Compare and verify the permission issues caused by the default behavior of empty parameters

---

### 修复建议 | Mitigation Recommendations
1.  对资源ID参数做必填校验，空参数直接返回错误
2.  禁止空参数下返回默认第一条数据
3.  增加访问者与资源归属的权限校验
4.  接口添加身份认证机制

1.  Enforce required validation on resource ID parameters, return an error for empty parameters
2.  Prohibit returning the default first record when parameters are empty
3.  Add permission checks between the requester and resource ownership
4.  Implement an authentication mechanism for the API

---

### 免责声明 | Disclaimer
本项目仅用于安全学习与技术研究，禁止用于非法测试、攻击真实系统。使用者需自行承担相关行为责任。

This project is for security learning and technical research only. It is strictly prohibited to use it for illegal testing or attacking real systems. The user shall bear full responsibility for any related actions.

