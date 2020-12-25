import aiohttp
import asyncio

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/86.0.4240.75 Safari/537.36 "
}


async def sample_get():
    # 发送一个简单的get请求
    async with aiohttp.ClientSession() as session:
        async with session.get(url="https://www.baidu.com", headers=headers) as response:
            print(response.status)
            print(await response.text())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sample_get())
