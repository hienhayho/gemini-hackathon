import os
import argparse
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List

from prompts import PROBLEM_1_3, DETECT_CONTEXT, PROBLEM_4

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Gemini Hackathon")
    parser.add_argument("--img", help="Path to image", type=str, required=True)
    parser.add_argument(
        "--task",
        help="Task number - 1 and 3 are belong to 1, 0: context",
        choices=[0, 1, 2, 4, 5],
        type=int,
        required=True,
    )
    parser.add_argument("--q", help="Additional question", type=str, required=False)
    parser.add_argument(
        "--img2", help="Second picture for task 4", type=str, required=False
    )
    args = parser.parse_args()
    return args


def get_system_prompt(task: int) -> str:
    assert task in [0, 1, 2, 4, 5], "Invalid task."
    if task == 0:
        return DETECT_CONTEXT
    elif task == 1:
        return PROBLEM_1_3
    elif task == 4:
        return PROBLEM_4


def get_imgs(args: argparse.Namespace) -> List[Image.Image]:
    """Get image for specific task

    Args:
        args (argparse.Namespace): Arguments for gemini

    Return:
        List[Image.Image]: List of images
    """
    imgs = []
    img = Image.open(args.img)
    if args.task == 4:
        label_1 = Image.open("images/human_label.png")
        label_2 = Image.open("images/human_label_2.png")
        imgs.extend([img, label_1, label_2])
    else:
        imgs.append(img)
    return imgs


def main() -> None:
    args = parse_args()

    args.img = Path(args.img)

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    imgs = get_imgs(args)

    SYSTEM = get_system_prompt(args.task)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=SYSTEM
    )
    response = model.generate_content([args.q if args.q else "", *imgs])
    print(response.text)


if __name__ == "__main__":
    main()
