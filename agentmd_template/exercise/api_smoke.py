import os
from anthropic import Anthropic
c = Anthropic(api_key=os.environ["ANTHROPIC_AUTH_TOKEN"], base_url=os.environ["ANTHROPIC_BASE_URL"])
r = c.messages.create(model="glm-4.6", max_tokens=512, messages=[{"role":"user","content":"只回复两个字：成功"}])
print([b.type for b in r.content])
print(next(b.text for b in r.content if b.type=="text"))
