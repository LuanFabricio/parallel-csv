import asyncio

async def hw(id: int) -> None:
    print(f"[{id}] Hello World!")

bg_tasks = []
for idx in range(20):
    task = asyncio.create_task(hw(id=idx), name=f"bg_task_{idx}", loop=_event_loop)
    bg_tasks.append(bg_tasks)
    task.add_done_callback(lambda _: print("idk"))

for task in bg_tasks:
    task.result()
