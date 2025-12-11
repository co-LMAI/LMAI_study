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
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file_path = r"E:\Desktop\data\edit"
text_path = r"E:\Desktop\data\E_text"

for filename in os.listdir(file_path):
    image_path = os.path.join(file_path, filename)
    base64_img = encode_image(image_path)


    completion = client.chat.completions.create(
        model="qwen3-vl-32b-instruct", 
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{'data:image/png;base64,' + base64_img}",
                        },
                    },
                    {"type": "text", "text": "请用一句话描述这个景观设计方案平面图的图像编辑图像，白色是场地外部、紫色是铺装、橘色是广场、灰色是建筑、蓝色是水景、黄色是小品、浅绿色是草地、深绿色是乔木等。"},
                ],
            },
        ],
    )

    output_filename = os.path.splitext(filename)[0] + ".txt"
    if not os.path.exists(text_path):
        os.makedirs(text_path)
    output_path = os.path.join(text_path, output_filename)

    with open(f"{output_path}", "w", encoding="utf-8") as f:
        f.write(completion.choices[0].message.content)

    time.sleep(1)