import click

from library.chatgpt import ChatGPT
from library.chatgpt import ONLY_ANSWER
from library.cli import IMPORTANT
from library.utils import train_project

bearer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJmZWRlcmljb3VsZm9AZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImdlb2lwX2NvdW50cnkiOiJVUyJ9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItSlN3dnJrWDhnVnQ4bktOMmhOSEo0TFFKIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwOTUzMjA4MDQ4NTc1Mzc0MDczOSIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NzY2ODU5MTIsImV4cCI6MTY3Nzg5NTUxMiwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvZmZsaW5lX2FjY2VzcyJ9.LB-s3Bk2lQlOl36HeLknZltOVkBamP4OwdvH2rGE-JTNx9Uc1x0wi-4Q6YN3dY_aIkjSAwD1Yv5v1FxVH8sZf-5knC7BWAHHNuLLhCzybcA5pK93oP9OgNCXRYAqnMGNvzYPtFfg6vdcTwfJ2Q4NgOjjLVcRyrhSsavl440j8A2NIj1L0OUdTozfKrV5kPT4uRQEuYEjXbc47k1ClkaTaCSSjG29HZFWH6cl1IhxvL54MzMuRG3_YjMYXotPXAmzvEicphJXU01S1gF3mzSb6U9wiOpnHbQ_pYLObP-4dIvqfbncjiY8XeSPt1l6gDDT5zt_m7RPm54bixdAESJLVQ"  # noqa: E501
cookie = "_ga=GA1.2.1817078780.1675202558; intercom-device-id-dgkjq2bp=4b65b327-5ce5-4328-89b5-e59471d4d2dc; CN_TTGPT=%5B%22en-US-Samantha%22%2C1%2C0.7%2C%22%22%2C%22stop%22%2C%22pause%22%2C1%2C%22send%20message%20now%22%5D; __Host-next-auth.csrf-token=3705741745a8121e230d8e5db0680b39e44205d46f13836be97e00245da584d0%7C7e6da496e8eb417917952a96bf7bc72198457265042b97497e4294a885cfcb51; cf_clearance=TwBXhkMNHE4cbjuq7I6eoUnT10O9pHRbjDPe33mxVkc-1675464700-0-1-5d785e59.eee15729.a7901b9-250; cf_clearance=G2ee12LhonyLbYZjDHVyIvb0a4pEcHxs6ICleGvvwoc-1676338623-0-1-5d785e59.504505c5.a7901b9-160; __Secure-next-auth.callback-url=https%3A%2F%2Fchat.openai.com%2Fchat; intercom-session-dgkjq2bp=SGN3eHNSVGNvTFhrQ0ZHMVg5ZGNRZ2Z0LzB0NWszWDlNRHBZWFlKY0xPanZIUEx1QWlpWDZxTmtCZ2N0YjVHTC0tUWpuY01WcGUxQlpVc2ZzRzY1c3d2UT09--e63044402953b78ed9a3620cb4ff13146b6c8489; _gid=GA1.2.1846323850.1677276784; _cfuvid=94ZSsCbofpftc8zYs_pNPqtKhqsukg.DiUrTB6NGoRY-1677278609160-0-604800000; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..CuIL4M2t2P1V2oiq.6Xb8UjUqLPrfGC9vQX9eq5Cszqs7p78X0K0HokpPlZfRSTzUropQmLdYXPbWxxoP3_mkPAAklQVfVupjpdwBDd0rRvqFTeR0BsHa1TBlerOOAlBJyC-GZLLiOmjB8VNDjOvBNU5IrwELGuAhKdjbUhcFNDgSgzfap1Q_al7TAQc4wD3Uplz-sc4EYkLdQeMqN8WXIb1shty2_yqUsb7cuFgpWbl9rpJgbzbMe1Fvb00NUJaztZmdT4PcFdpgYCfaB5DeTUYaGSntt5zvVhM278MMD0HmVaRyZ7AjBU_DjMxmnlCNuA5rnSv6PxYUe-4dMDKO56dSDwSO7zEIiJKK0uJs9cPIZdirGetKcZFvNsiiifnL0HGejgYs88SgVjKzACFfUYNVDauwzbEJSLtcC_Lbw8OoJxFZO6gBnL0TDOwS4I5rYrprVsWvMUTTvQ7CexqOXfu44ZyrQWGaJ8vYh3vDfvYII6lnA4sSBBnE_no8slW7QIF3K0hkBh9GUjM1qVIADJ29zd7uHmCPM719b22MTx8zCbXQh-xOJeMCdjrNa7i6BcC5rUpTR5dv1GxvEYUSAs4EftZGqfITASMNxa61aCzrOnvOkm5N28OihvZnM9e-_kszsXQY_h4kqPFnKbG77fE2w20xqvzxDPjMr4cDMgqY_s95BA4ub965pv57vivaGlCAeO-8JbY5k-O6CoHRc4-5v-1sltEF-uA4hfIIAgn5keqHD3d5deqBLCUtKW_s7OnWoT6dc5fl_JFL_EQTEz3WFGn8s5Iaw7Bbib85X0luFCfStqC2IJxuHsEu-wXKn203jDj_JBv7CyhmOXgvCudFLJqJ2rqsjy2XpuYpCW8XN-2KJGjdErVbItkJEAy4RlW7n_cnfnF4qxD2C3gN5pHj-YKCYjltAMndlt2Se181vfMksNUwPd5eTJM75Vf4osB2uquAK_SNIX6EhRqv5J0AUVNDXxW1aXF6dra7k6Bi9s1fzD6IRttlY-9LnTBMpO_-EpYHKhu-y8ZlSTBhf8rP4UHmBFkLWRmFJJ1pGBjpvdVYGCG5KBdxWIff8nQAkygSjObkmNd4STxsQCOtuGUp8SM6B1D2r2i6ZwKg7_Q2MvgGNZqZcZFGby8wWc4Zi2mt4kwJ8Yu8eayAwSQmk0yoSbg8XOSX98V1UaRtXybBTqy1S9O0br_lhO8_0nrY6ExCnPHgKDr3rcskws8egU07JNR1VO04-2-TclmXqkIUqyDoV5SOE_0vhlw1SrDppjibREzEuJokXxXAVqTjrsbB3pKVhuIoyVgdvbS8KdMcgC1yVVSI2gZsus25M432cOxi4m95Zh2vdXeRSp2EGMjyjkAuR5EsCjD0cN1YvrsfcJZjKqQWijcJvyuJEyLJaYLUZNrRG-c5Cy2VTC49RoahDSKm4E7oYSOHJI6aIKDgHyP_b7GwYsw_iRi4Flc_ntyPmpcZJf2IEGtddPdH72fR_38Qs0VkBsbrRdUrrbAah5KBWh0Q2SLGHGXCqMLMSkyFOson-641EC6mHnfb7XhFCPejVk_VH6LF4l7qJ_8zHuEbW_XS3f8MgMNIng2PJKKGIW9nQ82gsiATnXMwNws5D8c00SkcMeyAy1OIvQAhku9xN7BBa6-GzdTSqqi6WxyCUYAf5YctI3H9T7C4q8qNqrKDgp8zQirecT_EnrNn0FuKyyDMI1KynrWC6SHk1SaL46aTipBOVeGKEuKEo2EWEXzm2MiNh1P5VMC0PMw9gD_hW5dms4jpEOhjNpOX0fS22GmDsODOpsxmdyBjXUt0SCyrInduDL7H8DKEY7NEfWb-LWvrXxokIASqhZStc9jUWLpSyhNM17rpSckvHwq7SGXWmmaxRrU_vyM1D5TzyOVD1MvvudOjZMRlvyMEDI0eJm-dxiWgaXjYL6NJin6uRMqpAoJSVC0Y2Bb_DmcHz-8dEWAL9nB0VNIZ1zLK5VB4vt5AWAAwtozjbmLIjUvjktzjinXJ5Ku6MwMIbPwnF1KtxCe2VAHEgsT21HiFWknW0U9_QiKjXsgGFzwI7xBptETDZFY4N5ptitzZrCC8k4rNBWfdgsGFh1VUnQWuZzC4PheITj8rpFT0ziYgLaqujZvIjbLMkJPt_D3wYIHOx4uKwg36DA8-WNczx6kdX2rI1NYSW6Np9ihwKqbMYihkQ7mn9ab27VGxZ7_-ecjtppgE7rFvCuUNpi88t1FxcnGIreYHnJhURriklqrky86f7zx1kLd6VMyrZPI568MITQtyKVCafi90ZX65KyrI6cAMVyBAkx5P7PsZIEvIuwXUh6sdd1Rkro64Y289LYFjCkTi8OxDnInT_C4_atOPmjH11EDTeM1QYyLrqKc_KZhewoFkpDSDbbDnAn7MBTFJ8Nn18ATpQHUidv5HjqNkgzobwXY6gfqkEBU7GuBKjpyBdMAecDV8SRa9XAp8WSzK7Vu91tu-q4LWTnXT7B0V43z1OR8f6WnYYMOd0gNHO7Xpyhv1M-pne44AuW87oehh.S-izZsByyMhYp8foB9AEzA; _puid=user-JSwvrkX8gVt8nKN2hNHJ4LQJ:1677278609-iqLaE8O4MxHlS9GxnK8QD2F9bA%2FrdLFHYBHtEI1uC7s%3D; __cf_bm=QDRdegltPflP4EfMm5h67tdhd4oe_v4y3rVFiiGSiGE-1677278609-0-AQzJxMzfT2lAWSsEQMTyUqTt662YxwL7Xrdqyky9VnQr8rI5iYN8XLM+YQvu6wrvHnutZf6OdvcrqzR9lgFdiulPvcA5kcwz5H9B5fW+4dbXIvk5U0kNa9yYoP6Fu1/fy6LKhrh6eMTeWJe/GXujzoLflBH/yC0CVs/P/o8lD6OWOy2ZPPtmSv4ocN4j1y7QeA==; __cf_bm=OndqA.f3aZNCwVW_PppVXL9LjnQ3hJ21fPCmPv6vMjw-1677280812-0-AQzhhxhKOViPuuhFN1UkxZWM6l5YFaHWhBXIrm7Ko8EtrFk9e0523P9JNiZE+tQZMmZzq8Jif0BDGCATH9GMZPk=; _cfuvid=Ftuzq2i0tUeYG6nDBvIGEQbOliucptB2bOiQNkTVNr8-1677280812847-0-604800000"  # noqa: E501


@click.group()
def sai():
    """Sai is a command line tool to use ChatGPT to ask questions about your project"""


# todo: add ignore and parse wildcards option
@sai.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option("--conversation_id", default=None)
def train(path, conversation_id: str = None):
    """Read all the files in a folder and train ChatGPT on them via a prompt"""

    click.secho(
        "This command opens a new chat and train ChatGPT on the proejct you're listing."
    )
    input("Do you want to continue? (Press enter to continue)")

    chatgpt = ChatGPT(bearer, cookie, conversation_id)
    train_project(chatgpt, path)
    click.secho("Training done! Now you can ask questions about your project.")
    click.launch(chatgpt.chat_url.format(chatgpt.conversation_id))


@sai.command()
@click.argument("prompt")
@click.option("--conversation_id", default=None)
def ask(prompt: str, conversation_id: str = None):
    """Ask any question about the project"""
    chatgpt = ChatGPT(bearer, cookie, conversation_id)
    chatgpt.ask(prompt)


@sai.command()
@click.option("--conversation_id", default=None)
def conversation(conversation_id: str = None):
    """Ask any question about the project"""

    chatgpt = ChatGPT(bearer, cookie, conversation_id)
    chatgpt.verbosity = ONLY_ANSWER

    click.secho("You can now start a conversation with ChatGPT.")
    click.secho("Write stop or exit to stop the conversation.", fg=IMPORTANT)
    while True:
        prompt = input("You: ")
        if prompt in ["stop", "exit"]:
            break
        chatgpt.ask(prompt)


@sai.command()
def list():
    """List all the projects you have created"""
    chatgpt = ChatGPT(bearer, cookie)
    chatgpt.list_chats()


@sai.command()
@click.option("--conversation_id", default=None)
def select_conversation(conversation_id: str):
    """Select a conversation to ask questions about"""
    chatgpt = ChatGPT(bearer, cookie)
    chatgpt.select_chat(conversation_id)


if __name__ == "__main__":
    sai()
