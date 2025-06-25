## install direnv

## install uv

###  使用统一venv

#### 配置.env

#### 运行

```
# 项目根目录
source .venv/bin/activate

uv pip install -r requirements-dev.txt
uv pip install --group libs/langgraph/pyproject.toml:dev


#uv sync --active --inexact 

```
