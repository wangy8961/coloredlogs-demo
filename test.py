# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime
import time

from aiostomp import AioStomp

from logger import logger


async def run():
    # 测试不同日志级别的颜色
    logger.debug('This is debug message')
    logger.info('This is info message')
    logger.warning('This is warning message')
    logger.error('This is error message')
    logger.critical('This is critical message')

    # 连接 ActiveMQ
    client = AioStomp('127.0.0.1', 61613, error_handler=report_error)
    await client.connect()

    # 定时发送消息到队列
    while True:
        destination = '/queue/channel'
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client.send(destination, body=data, headers={})
        logger.info('Send a message({0}) to queue({1})'.format(data, destination))
        time.sleep(1)


async def report_error(error):
    logger.error('Catch error: ', error)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    # loop.run_forever()
