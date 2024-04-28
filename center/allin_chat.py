import subprocess
import re
import select
import time
from multiprocessing import Process, Queue

import chat_client
import local_llm
import ChatUI.chat_window as window

use_remote = True

def main(queue):
    # 定义一个函数来处理每一行输出
    pattern = re.compile(r'(\d+:)([^:]+)')
    start_loop = False
    COUNTER = 50
    counter = COUNTER
    tick = 0.5
    question = ''
    # 使用Popen类创建一个进程，用于语音识别程序
    process = subprocess.Popen([
                                'sudo', 
                                './build-aarch64-linux-gnu/install/bin/sherpa-ncnn-alsa', 
                                './sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/tokens.txt',
                                './sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.param',
                                './sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.bin',
                                './sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.param',
                                './sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.bin',
                                './sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.param',
                                './sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.bin',
                                "hw:3,0",
                                '2',
                                'greedy_search'
                                ],
                                cwd='./sherpa-ncnn/', 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)

    # 循环读取进程的输出
    # 定义一个循环，持续监控stdout
    try:
        while True:
            readable, _, _ = select.select([process.stderr], [], [], tick)
            # 如果readable不为空，说明stdout有新的输出
            if process.stderr in readable:
                # 读取新的输出
                if start_loop == False:
                    new_output = process.stderr.readline()
                    if new_output == "Recording started!\n":
                        print(new_output)
                        start_loop = True
                        new_output = process.stderr.readline()
                        print(new_output)
                        new_output = process.stderr.readline()
                        print(new_output)
                    else:
                        print(new_output)
                else :
                    new_output = process.stderr.readline()
                    # 不是空字符串
                    if new_output != "\n":
                        print(new_output)
                        counter = COUNTER
                        question = new_output
                    else:
                        counter -= tick
                        # 时间到，进行输出
                        if counter <= 0 and question != "":
                            # 正则去掉前面的数字
                            match = re.match(r'\d+:', question)
                            if match:
                                question = question.lstrip(match.group(0))
                                if re.match(r"^切换", question):
                                    use_remote = not use_remote
                            print("问: " + question)
                            queue.put("问: " + question)
                            print("答: " + chat(question))
                            queue.put("答: " + chat(question))
                            question = ""
                            counter = COUNTER
            # 如果没有检测到新输出，计时器--
            else:
                print("This should not be printed!")

            # 每隔一段时间检查子程序是否已经结束
            if process.poll() is not None:
                print("子程序已结束")
                break

    except KeyboardInterrupt:
        # 允许用户通过Ctrl+C中断监控
        print("监控已停止")

    finally:
        # 清理资源，关闭子程序
        process.stderr.close()
        if process.poll() is None:
            process.terminate()
        print("子程序已关闭")

def chat(query):
    if use_remote:
        return kimi.remote_chat(query)
    else:
        return local_llm.chat(query)

if __name__ == "__main__":
    queue = Queue()
    kimi = chat_client.Kimi()
    chat_window = Process(target=window.main, args=(queue,))
    chat_window.start()
    main(queue)
    chat_window.join()
    