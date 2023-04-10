<div align="center">

# 赛道友你后端

<!-- markdownlint-disable-next-line MD036 -->
_✨ Author: Nagico ✨_
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9|3.10|3.11-blue" alt="python">
  <img src="https://img.shields.io/badge/Django-4.0-blue" alt="django">
  <img src="https://img.shields.io/badge/Docker%20Build-automated-blue" alt="docker">
  <br />
  <a href="https://codecov.io/gh/Nagico/teamup_backend">
    <img src="https://codecov.io/gh/Nagico/teamup_backend/branch/main/graph/badge.svg?token=JNmovF1SJB" alt="codecov">
  </a>
  <a href="http://co-server.nagico.cn:9090/dashboard?id=Nagico_teamup_backend_AYdqv8scqcMnH0jYurou">
    <img src="http://co-server.nagico.cn:9090/api/project_badges/measure?project=Nagico_teamup_backend_AYdqv8scqcMnH0jYurou&metric=alert_status&token=sqb_da520efb5e6dc5f220d57c4daa524f146474733b" alt="sonarqube">
  </a>
  <br />
  <a href="https://github.com/Nagico/teamup_backend/actions/workflows/prod.yml">
    <img src="https://github.com/Nagico/teamup_backend/actions/workflows/prod.yml/badge.svg?branch=production" alt="Production Server CI/CD">
  </a>
  <a href="https://github.com/Nagico/teamup_backend/actions/workflows/test.yml">
    <img src="https://github.com/Nagico/teamup_backend/actions/workflows/test.yml/badge.svg?branch=main" alt="Test Server CI/CD">
  </a>
</p>
<!-- markdownlint-enable MD033 -->

## 项目地址

- ~~生产环境: [api.teamup.ziqiang.net.cn](https://api.teamup.ziqiang.net.cn)~~
- 测试环境: [api.test.teamup.nagico.cn](https://api.test.teamup.nagico.cn)

## 测试

[![codecov](https://codecov.io/gh/Nagico/teamup_backend/branch/main/graphs/sunburst.svg?token=JNmovF1SJB)](https://codecov.io/gh/Nagico/teamup_backend)

## 开发

1. 克隆项目

```bash
git clone https://github.com/Nagico/teamup_backend.git
```

2. 创建 conda 环境（推荐）

```bash
conda create -n teamup python=3.11
conda activate teamup
```

3. 安装依赖

```bash
pip install poetry
poetry install --with dev
pre-commit install
pre-commit install --hook-type commit-msg
```

4. 更新配置文件

将实际配置写入 `config/.env` 文件中

5. 使用 Pycharm 打开项目

在右下角选择 <No Interpreter>, Add New Interpreter, Add Local Interpreter, Conda Environment。在 Use existing environment 中选择 teamup 环境

6. 运行项目

选择 Local Server 作为运行项目，并启动

7. 运行测试

选择 Test All with pytest 作为运行项目，并启动
