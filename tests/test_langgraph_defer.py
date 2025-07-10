import time
from typing import TypedDict
from langgraph.graph import StateGraph
from functools import wraps
from datetime import datetime
import asyncio



# 增强日志装饰器，支持异步函数
def log_it(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"[start][{datetime.now().strftime('%H:%M:%S.%f')}]{func.__name__}")

        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"[end][{datetime.now().strftime('%H:%M:%S.%f')}]{func.__name__} took {end_time - start_time:.2f} seconds")
        return result

    return async_wrapper

class State(TypedDict):
    data:str
    valid: bool
    
@log_it
async def download_data(x):
    await asyncio.sleep(1)  # 模拟异步IO操作
    print("Download completed")
    return {"data": "sample"}

@log_it
async def validate_data(x):
    await asyncio.sleep(3)  # 比download更慢
    # 添加后台任务
    asyncio.create_task(log_validation_result())
    print("Validation completed")
    return {"valid": True}

async def log_validation_result():
    print("(后台任务: 开始写入验证日志...)")
    await asyncio.sleep(1)
    print("(后台任务: 验证日志写入完成)")

@log_it
async def save_result(x):
    print(f"SAVED RESULT: {x}")
    print(f"SAVE TIMESTAMP: {datetime.now().strftime('%H:%M:%S.%f')}")
    return x


async def test_langgraph_defer_case1():
    print("> run case1:")

    builder = StateGraph(State)
    builder.add_node("download_data", download_data)
    builder.add_node("validate_data", validate_data)
    builder.add_node("save_result", save_result, defer=True)  # 等待完成

    
    builder.set_entry_point("download_data")
    builder.set_entry_point("validate_data")

    # 错误连接方式（独立连接）
    builder.add_edge("download_data", "save_result")
    builder.add_edge("validate_data", "save_result")

    flow = builder.compile()

    print(flow.get_graph().draw_ascii())

    await flow.ainvoke({})


async def test_langgraph_defer_case2():
    print("> run case2:")

    builder = StateGraph(State)
    builder.add_node("download_data", download_data)
    builder.add_node("validate_data", validate_data)
    builder.add_node("save_result", save_result)  # 等待完成

    builder.set_entry_point("download_data")
    builder.set_entry_point("validate_data")

    # 多节点联合连接
    builder.add_edge(("download_data", "validate_data"), "save_result")


    flow = builder.compile()    
    
    print(flow.get_graph().draw_ascii())

    await flow.ainvoke({})
    

async def test_langgraph_defer_case3():
    print("> run case3:")

    builder = StateGraph(State)
    builder.add_node("download_data", download_data)
    builder.add_node("validate_data", validate_data)
    builder.add_node("save_result", save_result,defer=True) # 等待完成

    builder.set_entry_point("download_data")
    builder.set_entry_point("validate_data")

    # 多节点联合连接
    builder.add_edge(("download_data", "validate_data"), "save_result")


    flow = builder.compile()
    print(flow.get_graph().draw_ascii())

    await flow.ainvoke({})


async def run_case():
    # await test_langgraph_defer_case1()
    await test_langgraph_defer_case1()
    # await test_langgraph_defer_case3()




if __name__ == "__main__":
    asyncio.run(run_case())

    