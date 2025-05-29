import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, I am Piyush Garg"
tokens = enc.encode(text)

print("Tokens:", tokens)

tokens = []
decoded = enc.decode(tokens)

print("Decoded Text:", decoded)