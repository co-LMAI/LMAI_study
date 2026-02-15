import os, base64
from dotenv import load_dotenv
from openai import OpenAI
import time


def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# 加载 .env 文件中的环境变量
load_dotenv()

client = OpenAI(
    api_key=os.getenv("ZYX_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file_path = r"E:\Desktop\aotoBZ\O_data"
text_path = r"E:\Desktop\aotoBZ\E_text"
text_prosess_path_first = r"E:\Desktop\aotoBZ\P1_text"
text_prosess_path_second = r"E:\Desktop\aotoBZ\P2_text"

for filename in os.listdir(file_path)[95:]:
    image_path = os.path.join(file_path, filename)
    base64_img = encode_image(image_path)

    def get_response(messages):
        completion = client.chat.completions.create(
            model="qwen3-vl-32b-instruct", 
            messages=messages,
        )
        return completion.choices[0].message.content

    output_filename = os.path.splitext(filename)[0] + ".txt"

    # 初始化 messages
    messages = []

    # 第 1 轮
    messages.append({"role": "user", 
                     "content": [
                                {"type": "image_url",
                                 "image_url": {"url": f"{'data:image/png;base64,' + base64_img}",},
                                },
                                {"type": "text", 
                                 "text":"识别该景观平面图种的铺装、广场、建筑、水景、小品、草地、乔木等设计要素,并返回图中包含的要素类别。"
                                 }
                                ]   
                    })
    print("第1轮")
    assistant_output = get_response(messages)
    messages.append({"role": "assistant", "content": assistant_output})
    print(f"模型：{assistant_output}\n")

    if not os.path.exists(text_prosess_path_first):
        os.makedirs(text_prosess_path_first)
    output_path_first = os.path.join(text_prosess_path_first, output_filename)

    with open(f"{output_path_first}", "w", encoding="utf-8") as f:
        f.write(assistant_output)


    # 第 2 轮
    messages.append({"role": "user", "content": "根据以下颜色编码进行标注：{'场地内部': '#000000','外部环境': '#ffffff','铺装': '#ffaaff','广场': '#ffaa00', '建筑': '#b4c4c8','水景': '#00aaff','小品': '#ffff00','植物': '#00aa00','草地': '#aaff00','活动场地': '#aaaaff'}"})
    print("第2轮")
    assistant_output = get_response(messages)
    messages.append({"role": "assistant", "content": assistant_output})
    print(f"模型：{assistant_output}\n")

    if not os.path.exists(text_prosess_path_second):
        os.makedirs(text_prosess_path_second)
    output_path_second = os.path.join(text_prosess_path_second, output_filename)

    with open(f"{output_path_second}", "w", encoding="utf-8") as f:
        f.write(assistant_output)

    # 第 3 轮
    messages.append({"role": "user", "content": "一句话描述，该平面中的要素与对应的颜色隐射关系"})
    print("第3轮")
    assistant_output = get_response(messages)
    messages.append({"role": "assistant", "content": assistant_output})
    print(f"模型：{assistant_output}\n")

    if not os.path.exists(text_path):
        os.makedirs(text_path)
    output_path_final = os.path.join(text_path, output_filename)
    print(output_path_final)
    with open(f"{output_path_final}", "w", encoding="utf-8") as f:
        f.write(assistant_output)

    time.sleep(1)